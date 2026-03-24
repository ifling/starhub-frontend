<template>
  <view class="page">
    <view class="tabs">
      <view
        v-for="t in tabs"
        :key="t.key"
        class="tab"
        :class="{ 'tab--active': activeTab === t.key }"
        @click="activeTab = t.key"
      >
        <text class="tab-text">{{ t.label }}</text>
        <view v-if="activeTab === t.key" class="tab-underline"></view>
      </view>
    </view>

    <view v-if="activeTab === 'created'" class="panel">
      <view class="toolbar">
        <view class="sort" @click="onClickSort">
          <text class="sort-text">时间</text>
          <text class="sort-arrow">▲</text>
        </view>

        <view class="toggle-pill" @click="onToggleExpired">
          <view class="pill-icon"></view>
          <text class="pill-text">已隐藏过期</text>
        </view>

        <view class="btn-create" @click="onCreate">创建</view>
      </view>

      <view class="search-row">
        <view class="search-box">
          <view class="search-icon"></view>
          <input
            class="search-input"
            v-model="keyword"
            placeholder="请输入关键字搜索活动"
            placeholder-class="search-placeholder"
            confirm-type="search"
            @confirm="onSearch"
          />
          <view v-if="keyword" class="search-clear" @click="keyword = ''">×</view>
        </view>
        <view class="search-btn" @click="onSearch">搜索</view>
      </view>

      <view v-if="createdLoading" class="loading-text">加载中...</view>

      <view v-else-if="createdListFiltered.length" class="created-list">
        <view
          v-for="act in createdListFiltered"
          :key="act.id"
          class="created-item"
          @click="onOpenSignup(act)"
        >
          <!-- 第一行：标题（过期时显示状态图标） -->
          <view class="created-item__row created-item__row--title">
            <text class="created-title">{{ act.title }}</text>
            <view v-if="isExpired(act.deadline_at)" class="created-status-icon" />
          </view>

          <!-- 第二行：截止（时间图标 + 编辑/删除同一行） -->
          <view class="created-item__row created-item__row--deadline">
            <view class="deadline-left">
              <text class="created-meta created-meta--label">截止</text>
              <view class="deadline-time-icon" />
              <text class="created-meta created-meta--time">{{ formatDeadline(act.deadline_at) }}</text>
            </view>
            <view class="deadline-actions">
              <text class="created-action" @click.stop="onEdit(act)">编辑</text>
              <text class="created-action created-action--danger" @click.stop="onDelete(act)">删除</text>
            </view>
          </view>

          <!-- 第三行：活动类型 + 人数图标 + 已报名人数 -->
          <view class="created-item__row created-item__row--type">
            <text class="created-type">{{ act.type }}</text>
            <view class="signup-pair">
              <view class="signup-icon" />
              <text class="created-signup-count">{{ act.signup_count || 0 }}</text>
            </view>
          </view>
        </view>
      </view>

      <text v-else class="empty-text empty-text--created">
        您尚未创建任何活动（未过期的），可以点击上方的按钮查看全部。
      </text>

      <view class="note">
        <text class="note-line">- 创建活动后，点击进入详情页，分享至微信群会团员进行报名，团员报名后可以在本页面中选择【我参与的】查看本人报名的所有活动。</text>
        <text class="note-line">- 默认会隐藏已过期的活动。</text>
        <text class="note-line">- 请规范填写活动相关内容，确保内容有意义，否则系统会判定为无效条目并自动清除。</text>
        <text class="note-line">- 如果当前时间已超过活动开始时间，则显示“已过期”，无法继续报名。</text>
      </view>

      <view class="feedback" @click="onFeedback">
        <view class="feedback-icon"></view>
        <text class="feedback-text">反馈</text>
      </view>
    </view>

    <view v-else-if="activeTab === 'template'" class="panel panel--center">
      <view class="center-action" @click="onCreateTemplate">
        <text class="center-plus">＋</text>
        <text class="center-text">创建模板</text>
      </view>
      <text class="center-tip">- 在此创建模板后，在创建活动时可以直接导入，以节约时间和精力。</text>

      <view class="feedback" @click="onFeedback">
        <view class="feedback-icon"></view>
        <text class="feedback-text">反馈</text>
      </view>
    </view>

    <view v-else-if="activeTab === 'joined'" class="panel">
      <view class="big-pill" @click="onToggleExpired">
        <view class="pill-icon"></view>
        <text class="pill-text">已隐藏过期活动</text>
      </view>
      <text class="empty-text">您尚未报名任何活动（未过期的），可以点击上方的按钮查看更多。</text>
    </view>

    <view v-else class="panel">
      <view class="direct-card">
        <input
          class="direct-input"
          v-model="code"
          placeholder="请输入活动码"
          placeholder-class="direct-placeholder"
          confirm-type="done"
        />
      </view>

      <view class="btn-join" @click="onJoin">
        <view class="btn-join-icon"></view>
        <text class="btn-join-text">进入活动报名</text>
      </view>

      <text class="direct-tip">
        提示：在活动报名页可以获取“活动码”，在此输入可以直达对应活动。此功能主要服务于不使用微信群的公会/团队，无需分享，直接凭码进入报名。
      </text>
    </view>

    <view v-if="showEditor" class="editor-mask" @click.self="onCloseEditor">
      <view class="editor-sheet">
        <view class="editor-tabs">
          <view
            v-for="t in editorTabs"
            :key="t.key"
            class="editor-tab"
            :class="{ 'editor-tab--active': activeEditorTab === t.key }"
            @click="activeEditorTab = t.key"
          >
            <text class="editor-tab-text">{{ t.label }}</text>
            <view
              v-if="activeEditorTab === t.key"
              class="editor-tab-underline"
            ></view>
          </view>
        </view>

        <scroll-view scroll-y class="editor-body">
          <view v-if="activeEditorTab === 'basic'">
            <view class="field field--inline">
              <text class="field-label field-label--inline">标题</text>
              <input
                class="field-input field-input--inline"
                v-model="form.title"
                placeholder="请输入标题"
                placeholder-class="field-placeholder"
              />
            </view>

            <view class="field field--inline">
              <text class="field-label field-label--inline">类型</text>
              <view class="field-row field-row--inline" @click="onPickType">
                <text class="field-value">{{ form.type }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>

            <view class="field field--inline">
              <text class="field-label field-label--inline">报名截止日期</text>
              <view class="field-row field-row--inline" @click="onPickDate">
                <text class="field-value">{{ form.deadlineDate }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>

            <view class="field field--inline">
              <text class="field-label field-label--inline">报名截止时间</text>
              <view class="field-row field-row--inline" @click="onPickTime">
                <text class="field-value">{{ form.deadlineTime }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>

            <view class="field field--inline">
              <text class="field-label field-label--inline">
                限制转发（非发起者不能转发）
              </text>
              <view class="field-row field-row--inline" @click="onPickForwardLimit">
                <text class="field-value">{{ form.forwardLimit }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>

            <view class="field field--inline">
              <text class="field-label field-label--inline">限制一人多报</text>
              <view class="field-row field-row--inline" @click="onPickMultiLimit">
                <text class="field-value">{{ form.multiLimit }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>

            <view class="field field--textarea">
              <textarea
                class="field-textarea"
                v-model="form.desc"
                placeholder="选填，请输入活动的简介或描述，限 2000 字（注意：请不要输入表情字符）"
                placeholder-class="field-placeholder"
              />
            </view>

            <text class="editor-tip">
              报名截止时间前如未改为活动开始时间，则显示“已过期”，无法报名。
            </text>
          </view>

          <view v-else-if="activeEditorTab === 'limit'" class="limit-panel">
            <view class="limit-row" @click="openLimitPicker('total')">
              <text class="limit-label">总人数</text>
              <view class="limit-row-right">
                <text class="limit-value">{{ limitLabel(limitForm.total) }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>
            <view class="limit-row" @click="openLimitPicker('tank')">
              <text class="limit-label">坦克总数</text>
              <view class="limit-icon limit-icon--tank"></view>
              <view class="limit-row-right">
                <text class="limit-value">{{ limitLabel(limitForm.tank) }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>
            <view class="limit-row" @click="openLimitPicker('healer')">
              <text class="limit-label">治疗总数</text>
              <view class="limit-icon limit-icon--healer"></view>
              <view class="limit-row-right">
                <text class="limit-value">{{ limitLabel(limitForm.healer) }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>
            <view class="limit-row" @click="openLimitPicker('dps')">
              <text class="limit-label">输出总数</text>
              <view class="limit-icon limit-icon--dps"></view>
              <view class="limit-row-right">
                <text class="limit-value">{{ limitLabel(limitForm.dps) }}</text>
                <text class="field-arrow">›</text>
              </view>
            </view>

            <view class="limit-divider">
              <text class="limit-divider-text">—————职业人数限制————</text>
            </view>

            <view class="limit-class-grid">
              <view
                v-for="cls in limitClassList"
                :key="cls.id"
                class="limit-class-block"
              >
                <view class="limit-class-row1" @click="openClassLimitPicker(cls.id)">
                  <text class="limit-class-name" :style="{ color: cls.color || '#111827' }">{{ cls.name }}</text>
                  <view class="limit-class-right">
                    <text class="limit-infinity">{{ cls.limit === -1 ? '禁止' : (cls.limit == null ? '∞' : cls.limit) }}</text>
                    <text class="field-arrow">›</text>
                  </view>
                </view>
                <view class="limit-class-specs">
                  <view class="limit-spec-col">
                    <text class="limit-spec-name">{{ cls.specs[0].name }}</text>
                    <text
                      class="limit-spec-val"
                      @click.stop="openSpecLimitPicker(cls.id, 0)"
                    >{{ cls.specs[0].limit === -1 ? '禁止' : (cls.specs[0].limit == null ? '∞' : cls.specs[0].limit) }}</text>
                  </view>
                  <view class="limit-spec-col">
                    <text class="limit-spec-name">{{ cls.specs[1].name }}</text>
                    <text
                      class="limit-spec-val"
                      @click.stop="openSpecLimitPicker(cls.id, 1)"
                    >{{ cls.specs[1].limit === -1 ? '禁止' : (cls.specs[1].limit == null ? '∞' : cls.specs[1].limit) }}</text>
                  </view>
                </view>
              </view>
            </view>
          </view>

          <view v-else class="seat-panel">
            <view class="seat-add" @click="onAddSeat">
              <text class="seat-add-plus">＋</text>
              <text class="seat-add-text">新增</text>
            </view>
            <text class="seat-tip">
              创建一些比如“老板”等特殊席位，可进行报名，最多5类。
              <text class="seat-tip--danger">活动创建后“特殊席位”将无法新增和删除。</text>
            </text>
          </view>
        </scroll-view>

        <view class="editor-footer">
          <button class="btn-ghost" @click="onImportTemplate">导入模板</button>
          <button class="btn-secondary" @click="onCloseEditor">取消</button>
          <button class="btn-primary" @click="onSubmit">确定</button>
        </view>
      </view>

      <view
        v-if="showTypePicker"
        class="picker-pop"
        @click.self="onCloseTypePicker"
      >
        <view class="picker-card">
          <view
            v-for="opt in typeOptions"
            :key="opt"
            class="picker-item"
            @click.stop="onSelectType(opt)"
          >
            <text class="picker-text">{{ opt }}</text>
          </view>
        </view>
      </view>

      <view
        v-if="showDatePicker"
        class="picker-pop"
        @click.self="onCloseDatePicker"
      >
        <view class="date-card" @click.stop>
          <view class="date-header">
            <text class="date-title">选择器</text>
          </view>
          <picker-view
            class="date-picker-view"
            :value="datePickerIndex"
            indicator-style="height: 80rpx"
            @change="onDateChange"
          >
            <picker-view-column>
              <view
                v-for="(y, yi) in datePickerYears"
                :key="yi"
                class="date-item"
              >
                <text class="date-item-text">{{ y }}</text>
              </view>
            </picker-view-column>
            <picker-view-column>
              <view
                v-for="(m, mi) in datePickerMonths"
                :key="mi"
                class="date-item"
              >
                <text class="date-item-text">{{ m }}</text>
              </view>
            </picker-view-column>
            <picker-view-column>
              <view
                v-for="(d, di) in datePickerDays"
                :key="di"
                class="date-item"
              >
                <text class="date-item-text">{{ d }}</text>
              </view>
            </picker-view-column>
          </picker-view>
          <view class="date-footer">
            <button class="btn-date-cancel" @click.stop="onCloseDatePicker">
              取消
            </button>
            <button class="btn-date-ok" @click.stop="onConfirmDate">
              确认
            </button>
          </view>
        </view>
      </view>

      <view
        v-if="showTimePicker"
        class="picker-pop"
        @click.self="onCloseTimePicker"
      >
        <view class="date-card" @click.stop>
          <view class="date-header">
            <text class="date-title">选择器</text>
          </view>
          <picker-view
            class="date-picker-view"
            :value="timePickerIndex"
            indicator-style="height: 80rpx"
            @change="onTimeChange"
          >
            <picker-view-column>
              <view
                v-for="(h, hi) in timePickerHours"
                :key="hi"
                class="date-item"
              >
                <text class="date-item-text">{{ h }}</text>
              </view>
            </picker-view-column>
            <picker-view-column>
              <view
                v-for="(m, mi) in timePickerMinutes"
                :key="mi"
                class="date-item"
              >
                <text class="date-item-text">{{ m }}</text>
              </view>
            </picker-view-column>
          </picker-view>
          <view class="date-footer">
            <button class="btn-date-cancel" @click.stop="onCloseTimePicker">
              取消
            </button>
            <button class="btn-date-ok" @click.stop="onConfirmTime">
              确认
            </button>
          </view>
        </view>
      </view>

      <view v-if="showLimitPicker" class="picker-pop">
        <view class="picker-mask" @click="closeLimitPicker"></view>
        <view class="date-card limit-picker-card" @click.stop>
          <scroll-view
            scroll-y
            class="limit-picker-scroll"
            :scroll-into-view="limitScrollIntoView"
          >
            <view
              v-for="(opt, idx) in limitOptions"
              :key="idx"
              :id="'limit-opt-' + idx"
              class="limit-opt-row"
              @click.stop="selectLimitAndClose(opt)"
            >
              <text class="limit-opt-text">{{ opt }}</text>
            </view>
          </scroll-view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'
import { isLoggedIn } from '../../utils/auth'

export default {
  name: 'StonePage',
  data() {
    return {
      tabs: [
        { key: 'created', label: '我创建的' },
        { key: 'template', label: '模板' },
        { key: 'joined', label: '我参与的' },
        { key: 'direct', label: '直达' },
      ],
      activeTab: 'created',
      keyword: '',
      code: '',
      hideExpired: true,
      sortAsc: true,
      createdLoading: false,
      createdList: [],
      editingId: null,
      showEditor: false,
      editorTabs: [
        { key: 'basic', label: '基本信息' },
        { key: 'limit', label: '人数限定' },
        { key: 'seat', label: '特殊席位' },
      ],
      activeEditorTab: 'basic',
      form: {
        title: '',
        type: '副本',
        deadlineDate: '2026-03-16',
        deadlineTime: '19:30',
        forwardLimit: '不限制',
        multiLimit: '不限制',
        desc: '',
      },
      showTypePicker: false,
      typeOptions: ['副本', 'PVP', '其他'],
      showDatePicker: false,
      datePickerYears: [],
      datePickerMonths: [],
      datePickerDays: [],
      datePickerIndex: [2, 2, 15],
      showTimePicker: false,
      timePickerHours: [],
      timePickerMinutes: [],
      timePickerIndex: [19, 30],
      limitForm: {
        total: null,
        tank: null,
        healer: null,
        dps: null,
      },
      limitClassList: [
        { id: 'senyuzhe', name: '森语者', color: '#32BF0F', limit: null, specs: [{ name: '惩击', limit: null }, { name: '愈合', limit: null }] },
        { id: 'bingmo', name: '冰魔导师', color: '#5C82E1', limit: null, specs: [{ name: '冰矛', limit: null }, { name: '射线', limit: null }] },
        { id: 'leiying', name: '雷影剑士', color: '#6B39DE', limit: null, specs: [{ name: '居合', limit: null }, { name: '月刃', limit: null }] },
        { id: 'qinglan', name: '青岚骑士', color: '#11B5B2', limit: null, specs: [{ name: '重装', limit: null }, { name: '空战', limit: null }] },
        { id: 'juren', name: '巨人守护者', color: '#08A0DC', limit: null, specs: [{ name: '岩盾', limit: null }, { name: '格挡', limit: null }] },
        { id: 'shensheshou', name: '神射手', color: '#D4D116', limit: null, specs: [{ name: '驭兽', limit: null }, { name: '驯鹰', limit: null }] },
        { id: 'shendun', name: '神盾骑士', color: '#0F68B3', limit: null, specs: [{ name: '防护', limit: null }, { name: '光盾', limit: null }] },
        { id: 'linghun', name: '灵魂乐手', color: '#1F9F0E', limit: null, specs: [{ name: '狂音', limit: null }, { name: '协奏', limit: null }] },
      ],
      showLimitPicker: false,
      limitPickerTarget: null,
      limitPickerIndex: 1,
      limitScrollIntoView: '',
      limitOptions: (() => {
        const arr = ['禁止', '不限']
        for (let i = 1; i <= 99; i++) arr.push(String(i))
        return arr
      })(),
    }
  },
  computed: {
    createdListFiltered() {
      const kw = (this.keyword || '').trim()
      let list = Array.isArray(this.createdList) ? this.createdList.slice() : []
      if (kw) {
        list = list.filter((a) => (a.title || '').includes(kw))
      }
      if (this.hideExpired) {
        const now = Date.now()
        list = list.filter((a) => {
          if (!a.deadline_at) return true
          const t = Date.parse(a.deadline_at)
          if (Number.isNaN(t)) return true
          return t >= now
        })
      }
      list.sort((a, b) => {
        const ta = Date.parse(a.created_at || '') || 0
        const tb = Date.parse(b.created_at || '') || 0
        return this.sortAsc ? ta - tb : tb - ta
      })
      return list
    },
  },
  watch: {
    activeTab(val) {
      if (val === 'created') {
        // #ifdef H5
        if (!isLoggedIn()) {
          uni.navigateTo({ url: '/pages/login/index' })
          return
        }
        // #endif
        this.fetchCreated()
      }
    },
  },
  onLoad() {
    // 进入“组队/集合石”页面时就预加载我创建的活动，避免仅在创建成功后才刷新
    if (this.activeTab === 'created') {
      // #ifdef H5
      if (!isLoggedIn()) {
        uni.navigateTo({ url: '/pages/login/index' })
        return
      }
      // #endif
      this.fetchCreated()
    }
  },
  onShow() {
    if (this.activeTab === 'created') {
      // #ifdef H5
      if (!isLoggedIn()) {
        return
      }
      // #endif
      this.fetchCreated()
    }
  },
  methods: {
    toast(title) {
      uni.showToast({ title, icon: 'none' })
    },
    onClickSort() {
      this.sortAsc = !this.sortAsc
      this.toast('排序（占位）')
    },
    onToggleExpired() {
      this.hideExpired = !this.hideExpired
      this.toast(this.hideExpired ? '已隐藏过期' : '已显示过期（占位）')
    },
    onCreate() {
      // #ifdef H5
      if (!isLoggedIn()) {
        uni.navigateTo({ url: '/pages/login/index' })
        return
      }
      // #endif
      this.editingId = null
      this.form.title = ''
      this.form.type = '副本'
      this.form.desc = ''
      const now = new Date()
      const future = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 7,
      )
      const y = future.getFullYear()
      const m = (future.getMonth() + 1).toString().padStart(2, '0')
      const d = future.getDate().toString().padStart(2, '0')
      this.form.deadlineDate = `${y}-${m}-${d}`
      this.showEditor = true
    },
    onSearch() {
      // computed will filter
    },
    onEdit(act) {
      this.editingId = act.id
      this.form.title = act.title || ''
      this.form.type = act.type || '副本'
      this.form.desc = act.desc || ''
      const dt = act.deadline_at ? new Date(act.deadline_at) : null
      if (dt && !Number.isNaN(dt.getTime())) {
        const y = dt.getFullYear()
        const m = String(dt.getMonth() + 1).padStart(2, '0')
        const d = String(dt.getDate()).padStart(2, '0')
        const hh = String(dt.getHours()).padStart(2, '0')
        const mm = String(dt.getMinutes()).padStart(2, '0')
        this.form.deadlineDate = `${y}-${m}-${d}`
        this.form.deadlineTime = `${hh}:${mm}`
      }
      this.activeEditorTab = 'basic'
      this.showEditor = true
    },
    async onDelete(act) {
      const ok = await new Promise((resolve) => {
        uni.showModal({
          title: '确认删除',
          content: `删除活动「${act.title || ''}」？`,
          success: (res) => resolve(!!res.confirm),
          fail: () => resolve(false),
        })
      })
      if (!ok) return
      try {
        await request(`/activities/${act.id}`, { method: 'DELETE' })
        this.createdList = this.createdList.filter((a) => a.id !== act.id)
        this.toast('已删除')
      } catch (e) {
        this.toast('删除失败')
      }
    },
    onFeedback() {
      this.toast('反馈（占位）')
    },
    onCreateTemplate() {
      this.toast('创建模板（占位）')
    },
    onJoin() {
      this.toast('进入活动报名（占位）')
    },
    onOpenSignup(act) {
      if (!act || !act.id) {
        this.toast('活动数据无效')
        return
      }
      uni.navigateTo({
        url: `/pages/signup/index?activityId=${encodeURIComponent(act.id)}`,
      })
    },
    onCloseEditor() {
      this.showEditor = false
    },
    onImportTemplate() {
      this.toast('导入模板（占位）')
    },
    onSubmit() {
      this.submitActivity()
    },
    async fetchCreated() {
      if (this.createdLoading) return
      this.createdLoading = true
      try {
        const rows = await request('/activities/mine')
        this.createdList = Array.isArray(rows) ? rows : []
      } catch (e) {
        this.toast('加载失败')
      } finally {
        this.createdLoading = false
      }
    },
    buildDeadlineISO() {
      const d = (this.form.deadlineDate || '').trim()
      const t = (this.form.deadlineTime || '').trim()
      if (!d || !t) return null
      const iso = `${d}T${t}:00`
      const dt = new Date(iso)
      if (Number.isNaN(dt.getTime())) return null
      return dt.toISOString()
    },
    async submitActivity() {
      const title = (this.form.title || '').trim()
      if (!title) {
        this.toast('请输入标题')
        this.activeEditorTab = 'basic'
        return
      }
      const payload = {
        title,
        type: this.form.type || '副本',
        deadline_at: this.buildDeadlineISO(),
        desc: (this.form.desc || '').trim() || null,
      }
      uni.showLoading({ title: '保存中' })
      try {
        let act = null
        if (this.editingId) {
          act = await request(`/activities/${this.editingId}`, { method: 'PUT', data: payload })
        } else {
          act = await request('/activities', { method: 'POST', data: payload })
        }
        this.showEditor = false
        this.editingId = null
        await this.fetchCreated()
        this.toast('已保存')
        return act
      } catch (e) {
        this.toast('保存失败')
      } finally {
        uni.hideLoading()
      }
    },
    formatDeadline(deadlineAt) {
      if (!deadlineAt) return '-'
      const dt = new Date(deadlineAt)
      if (Number.isNaN(dt.getTime())) return '-'
      const y = dt.getFullYear()
      const m = String(dt.getMonth() + 1).padStart(2, '0')
      const d = String(dt.getDate()).padStart(2, '0')
      const hh = String(dt.getHours()).padStart(2, '0')
      const mm = String(dt.getMinutes()).padStart(2, '0')
      const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
      const weekday = weekdays[dt.getDay()]
      return `${y}-${m}-${d} ${hh}:${mm} ${weekday}`
    },
    isExpired(deadlineAt) {
      if (!deadlineAt) return false
      const t = Date.parse(deadlineAt)
      if (Number.isNaN(t)) return false
      return t < Date.now()
    },
    onPickType() {
      this.showTypePicker = true
    },
    onPickDate() {
      if (!this.datePickerYears.length) {
        const years = []
        for (let y = 2024; y <= 2028; y++) {
          years.push(`${y}年`)
        }
        const months = []
        for (let m = 1; m <= 12; m++) {
          const mm = m < 10 ? `0${m}` : `${m}`
          months.push(`${mm}月`)
        }
        const days = []
        for (let d = 1; d <= 31; d++) {
          const dd = d < 10 ? `0${d}` : `${d}`
          days.push(`${dd}日`)
        }
        this.datePickerYears = years
        this.datePickerMonths = months
        this.datePickerDays = days
      }
      const parts = this.form.deadlineDate.split('-')
      const year = parseInt(parts[0] || '2026')
      const month = parseInt(parts[1] || '3')
      const day = parseInt(parts[2] || '16')
      const yIndex = Math.min(
        Math.max(year - 2024, 0),
        this.datePickerYears.length - 1,
      )
      const mIndex = Math.min(
        Math.max(month - 1, 0),
        this.datePickerMonths.length - 1,
      )
      const dIndex = Math.min(
        Math.max(day - 1, 0),
        this.datePickerDays.length - 1,
      )
      this.datePickerIndex = [yIndex, mIndex, dIndex]
      this.showDatePicker = true
    },
    onPickTime() {
      if (!this.timePickerHours.length) {
        const hours = []
        for (let h = 0; h <= 23; h++) {
          const hh = h.toString().padStart(2, '0')
          hours.push(hh)
        }
        const minutes = []
        for (let m = 0; m <= 59; m++) {
          const mm = m.toString().padStart(2, '0')
          minutes.push(mm)
        }
        this.timePickerHours = hours
        this.timePickerMinutes = minutes
      }

      const [hStr, mStr] = this.form.deadlineTime.split(':')
      const h = parseInt(hStr || '19')
      const m = parseInt(mStr || '30')
      const hIndex = Math.min(
        Math.max(h, 0),
        this.timePickerHours.length - 1,
      )
      const mIndex = Math.min(
        Math.max(m, 0),
        this.timePickerMinutes.length - 1,
      )
      this.timePickerIndex = [hIndex, mIndex]
      this.showTimePicker = true
    },
    onPickForwardLimit() {
      this.toast('选择限制转发（占位）')
    },
    onPickMultiLimit() {
      this.toast('选择一人多报限制（占位）')
    },
    onCloseTypePicker() {
      this.showTypePicker = false
    },
    onSelectType(opt) {
      this.form.type = opt
      this.showTypePicker = false
    },
    onCloseDatePicker() {
      this.showDatePicker = false
    },
    onDateChange(e) {
      this.datePickerIndex = e.detail.value
    },
    onConfirmDate() {
      const [yi, mi, di] = this.datePickerIndex
      const year = 2024 + yi
      const month = (mi + 1).toString().padStart(2, '0')
      const day = (di + 1).toString().padStart(2, '0')
      const picked = new Date(`${year}-${month}-${day}T00:00:00`)
      const today = new Date()
      const todayOnly = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate(),
      )
      if (picked < todayOnly) {
        this.toast('不能选择当前日期之前的时间')
        return
      }
      this.form.deadlineDate = `${year}-${month}-${day}`
      this.showDatePicker = false
    },
    onCloseTimePicker() {
      this.showTimePicker = false
    },
    onTimeChange(e) {
      this.timePickerIndex = e.detail.value
    },
    onConfirmTime() {
      const [hi, mi] = this.timePickerIndex
      const hour = this.timePickerHours[hi] || '19'
      const minute = this.timePickerMinutes[mi] || '30'
      this.form.deadlineTime = `${hour}:${minute}`
      this.showTimePicker = false
    },
    onAddSeat() {
      this.toast('新增特殊席位（占位）')
    },
    limitLabel(val) {
      if (val === -1) return '禁止'
      if (val === null || val === undefined) return '不限'
      return String(val)
    },
    getLimitValueIndex(val) {
      if (val === -1) return 0
      if (val === null || val === undefined) return 1
      const n = parseInt(val, 10)
      if (n >= 1 && n <= 99) return 1 + n
      return 1
    },
    openLimitPicker(target) {
      this.limitPickerTarget = target
      let cur = null
      if (target === 'total') cur = this.limitForm.total
      else if (target === 'tank') cur = this.limitForm.tank
      else if (target === 'healer') cur = this.limitForm.healer
      else if (target === 'dps') cur = this.limitForm.dps
      this.limitPickerIndex = this.getLimitValueIndex(cur)
      this.limitScrollIntoView = ''
      this.showLimitPicker = true
      const index = this.limitPickerIndex
      this.$nextTick(() => {
        this.limitScrollIntoView = 'limit-opt-' + index
        setTimeout(() => {
          this.limitScrollIntoView = ''
          this.$nextTick(() => {
            this.limitScrollIntoView = 'limit-opt-' + index
          })
        }, 80)
      })
    },
    openClassLimitPicker(classId) {
      this.limitPickerTarget = 'class_' + classId
      const cls = this.limitClassList.find((c) => c.id === classId)
      this.limitPickerIndex = this.getLimitValueIndex(cls ? cls.limit : null)
      this.limitScrollIntoView = ''
      this.showLimitPicker = true
      const index = this.limitPickerIndex
      this.$nextTick(() => {
        this.limitScrollIntoView = 'limit-opt-' + index
        setTimeout(() => {
          this.limitScrollIntoView = ''
          this.$nextTick(() => {
            this.limitScrollIntoView = 'limit-opt-' + index
          })
        }, 80)
      })
    },
    openSpecLimitPicker(classId, specIndex) {
      this.limitPickerTarget = 'spec_' + classId + '_' + specIndex
      const cls = this.limitClassList.find((c) => c.id === classId)
      const spec = cls && cls.specs && cls.specs[specIndex] ? cls.specs[specIndex] : null
      this.limitPickerIndex = this.getLimitValueIndex(spec ? spec.limit : null)
      this.limitScrollIntoView = ''
      this.showLimitPicker = true
      const index = this.limitPickerIndex
      this.$nextTick(() => {
        this.limitScrollIntoView = 'limit-opt-' + index
        setTimeout(() => {
          this.limitScrollIntoView = ''
          this.$nextTick(() => {
            this.limitScrollIntoView = 'limit-opt-' + index
          })
        }, 80)
      })
    },
    closeLimitPicker() {
      this.showLimitPicker = false
      this.limitPickerTarget = null
      this.limitScrollIntoView = ''
    },
    selectLimitAndClose(opt) {
      let val = null
      if (opt === '禁止') val = -1
      else if (opt === '不限') val = null
      else val = parseInt(opt, 10)
      if (this.limitPickerTarget === 'total') {
        this.limitForm.total = val
      } else if (this.limitPickerTarget === 'tank') {
        this.limitForm.tank = val
      } else if (this.limitPickerTarget === 'healer') {
        this.limitForm.healer = val
      } else if (this.limitPickerTarget === 'dps') {
        this.limitForm.dps = val
      } else if (this.limitPickerTarget && this.limitPickerTarget.startsWith('class_')) {
        const id = this.limitPickerTarget.replace('class_', '')
        const cls = this.limitClassList.find((c) => c.id === id)
        if (cls) cls.limit = val
      } else if (this.limitPickerTarget && this.limitPickerTarget.startsWith('spec_')) {
        const parts = this.limitPickerTarget.replace('spec_', '').split('_')
        const classId = parts[0]
        const specIndex = parseInt(parts[1], 10)
        const cls = this.limitClassList.find((c) => c.id === classId)
        if (cls && cls.specs && cls.specs[specIndex] !== undefined) {
          cls.specs[specIndex].limit = val
        }
      }
      this.closeLimitPicker()
    },
  },
}
</script>

<style>
.page {
  min-height: 100vh;
  background: #f6f7fb;
}

.tabs {
  display: flex;
  flex-direction: row;
  background: #ffffff;
  padding: 18rpx 24rpx 0;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding-bottom: 14rpx;
  color: rgba(0, 0, 0, 0.5);
}

.tab--active {
  color: rgba(0, 0, 0, 0.9);
}

.tab-text {
  font-size: 28rpx;
}

.tab-underline {
  width: 120rpx;
  height: 6rpx;
  border-radius: 6rpx;
  margin-top: 16rpx;
  background: #10b981;
}

.panel {
  padding: 22rpx 24rpx 48rpx;
}

.toolbar {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18rpx;
}

.sort {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.sort-text {
  font-size: 28rpx;
  color: #111827;
  font-weight: 600;
}

.sort-arrow {
  font-size: 18rpx;
  color: rgba(17, 24, 39, 0.7);
  transform: translateY(-1rpx);
}

.toggle-pill {
  flex: 1;
  margin: 0 18rpx;
  height: 76rpx;
  border-radius: 14rpx;
  background: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 8rpx 18rpx rgba(0, 0, 0, 0.12);
}

.big-pill {
  height: 88rpx;
  border-radius: 14rpx;
  background: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  box-shadow: 0 8rpx 18rpx rgba(0, 0, 0, 0.12);
  margin-bottom: 36rpx;
}

.pill-icon {
  width: 26rpx;
  height: 18rpx;
  border-radius: 18rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.9);
  position: relative;
}
.pill-icon::after {
  content: '';
  width: 6rpx;
  height: 6rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.9);
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.pill-text {
  color: rgba(255, 255, 255, 0.95);
  font-size: 28rpx;
  font-weight: 600;
}

.btn-create {
  width: 120rpx;
  height: 72rpx;
  border-radius: 12rpx;
  background: #10b981;
  color: #fff;
  font-size: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 18rpx;
}

.search-box {
  flex: 1;
  height: 76rpx;
  border-radius: 999rpx;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  padding: 0 18rpx;
  gap: 12rpx;
}

.search-icon {
  width: 26rpx;
  height: 26rpx;
  border-radius: 999rpx;
  border: 2rpx solid rgba(0, 0, 0, 0.35);
  position: relative;
}
.search-icon::after {
  content: '';
  width: 14rpx;
  height: 2rpx;
  background: rgba(0, 0, 0, 0.35);
  position: absolute;
  right: -10rpx;
  bottom: -6rpx;
  transform: rotate(45deg);
  border-radius: 2rpx;
}

.search-input {
  flex: 1;
  height: 76rpx;
  font-size: 26rpx;
  color: #111827;
}

.search-placeholder {
  color: rgba(17, 24, 39, 0.45);
}

.search-clear {
  width: 36rpx;
  height: 36rpx;
  border-radius: 999rpx;
  background: rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 26rpx;
}

.search-btn {
  font-size: 28rpx;
  color: rgba(17, 24, 39, 0.85);
}

.card {
  padding: 20rpx 0;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10rpx;
}

.card-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #111827;
}

.card-actions {
  display: flex;
  gap: 26rpx;
}

.card-action {
  font-size: 26rpx;
  color: #10b981;
}

.card-meta {
  margin-bottom: 8rpx;
}

.meta-left {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10rpx;
}

.meta-icon {
  width: 22rpx;
  height: 22rpx;
  border-radius: 6rpx;
  background: rgba(0, 0, 0, 0.15);
}
.meta-icon--clock {
  border-radius: 999rpx;
}
.meta-icon--group {
  border-radius: 8rpx;
}

.meta-text {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.7);
}

.card-sub {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.sub-text {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.7);
}

.note {
  padding: 18rpx 0 0;
}

.note-line {
  display: block;
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.75);
  line-height: 40rpx;
  margin-top: 10rpx;
}

.feedback {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  margin-top: 26rpx;
  padding: 18rpx 0;
  color: #111827;
}

.feedback-icon {
  width: 26rpx;
  height: 26rpx;
  border-radius: 999rpx;
  border: 2rpx solid rgba(16, 185, 129, 0.8);
  position: relative;
}
.feedback-icon::after {
  content: '?';
  font-size: 18rpx;
  color: rgba(16, 185, 129, 0.9);
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -52%);
}

.feedback-text {
  font-size: 26rpx;
  color: rgba(16, 185, 129, 0.9);
}

.panel--center {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.center-action {
  margin-top: 36rpx;
  color: #10b981;
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.center-plus {
  font-size: 32rpx;
  color: #10b981;
}

.center-text {
  font-size: 28rpx;
  color: #10b981;
}

.center-tip {
  margin-top: 18rpx;
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.45);
}

.empty-text {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.45);
  margin-top: 26rpx;
}

.empty-text--created {
  margin-bottom: 8rpx;
}

.loading-text {
  margin-top: 18rpx;
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.5);
}

.created-list {
  margin-top: 18rpx;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.created-item {
  background: #ffffff;
  border-radius: 16rpx;
  padding: 18rpx 18rpx 14rpx;
  border: 2rpx solid rgba(0, 0, 0, 0.06);
}

.created-item__row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.created-item__row--meta {
  margin-top: 10rpx;
  color: rgba(17, 24, 39, 0.6);
  font-size: 24rpx;
}

.created-item__row--title {
  margin-bottom: 8rpx;
}

.created-item__row--deadline {
  margin-bottom: 6rpx;
}

.created-item__row--type {
  justify-content: flex-start;
  gap: 12rpx;
}

.created-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #111827;
}

.created-meta {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.55);
}

.created-item__row--actions {
  margin-top: 12rpx;
  justify-content: flex-end;
  gap: 28rpx;
}

.created-status-icon {
  width: 26rpx;
  height: 26rpx;
  background-image: url('/static/icons/deadline-time.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  border-radius: 8rpx;
}

.deadline-left {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.deadline-actions {
  display: flex;
  align-items: center;
  gap: 28rpx;
}

.deadline-time-icon {
  width: 22rpx;
  height: 22rpx;
  background-image: url('/static/icons/deadline-time.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.created-type {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.65);
}

.signup-pair {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0;
}

.signup-icon {
  width: 26rpx;
  height: 26rpx;
  background-image: url('/static/icons/signup-count.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  margin-right: 0;
}

.created-signup-count {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.65);
  margin-left: 0;
}

.created-action {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.65);
}

.created-action--danger {
  color: #ef4444;
}

.direct-card {
  background: #ffffff;
  border-radius: 16rpx;
  padding: 18rpx;
  border: 2rpx solid rgba(0, 0, 0, 0.06);
}

.direct-input {
  height: 160rpx;
  font-size: 28rpx;
  color: #111827;
}

.direct-placeholder {
  color: rgba(17, 24, 39, 0.35);
}

.btn-join {
  margin-top: 22rpx;
  height: 92rpx;
  border-radius: 10rpx;
  background: #22c55e;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
}

.btn-join-icon {
  width: 28rpx;
  height: 28rpx;
  border-radius: 8rpx;
  background: rgba(255, 255, 255, 0.9);
}

.btn-join-text {
  color: #fff;
  font-size: 30rpx;
  font-weight: 700;
}

.direct-tip {
  display: block;
  margin-top: 18rpx;
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.45);
  line-height: 38rpx;
}

.editor-mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  z-index: 99;
}

.editor-sheet {
  width: 100%;
  max-height: 90vh;
  background: #ffffff;
  border-top-left-radius: 22rpx;
  border-top-right-radius: 22rpx;
  padding-bottom: env(safe-area-inset-bottom);
}

.editor-tabs {
  display: flex;
  flex-direction: row;
  padding: 20rpx 28rpx 0;
}

.editor-tab {
  flex: 1;
  align-items: center;
  justify-content: flex-end;
  display: flex;
  flex-direction: column;
  padding-bottom: 16rpx;
  color: rgba(0, 0, 0, 0.45);
}

.editor-tab--active {
  color: rgba(0, 0, 0, 0.9);
}

.editor-tab-text {
  font-size: 28rpx;
}

.editor-tab-underline {
  width: 120rpx;
  height: 6rpx;
  border-radius: 6rpx;
  margin-top: 14rpx;
  background: #10b981;
}

.editor-body {
  max-height: 70vh;
  padding: 0 28rpx 12rpx;
}

.field {
  padding: 18rpx 0;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.field--inline {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.field--textarea {
  border-bottom-width: 0;
}

.field-label {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.9);
  margin-bottom: 12rpx;
}

.field-label--inline {
  width: 220rpx;
  margin-bottom: 0;
}

.field-input {
  height: 64rpx;
  font-size: 26rpx;
  border-radius: 10rpx;
  padding: 0 18rpx;
  background: #f3f4f6;
}

.field-input--inline {
  flex: 1;
}

.field-placeholder {
  color: rgba(17, 24, 39, 0.4);
}

.field-row {
  height: 64rpx;
  border-radius: 10rpx;
  background: #f9fafb;
  padding: 0 18rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.field-row--inline {
  flex: 1;
}

.field-value {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.9);
}

.field-arrow {
  font-size: 30rpx;
  color: rgba(17, 24, 39, 0.35);
}

.field-plus {
  font-size: 32rpx;
  color: #10b981;
}

.field-textarea {
  margin-top: 0;
  min-height: 160rpx;
  width: 100%;
  box-sizing: border-box;
  padding: 12rpx 18rpx;
  border-radius: 10rpx;
  background: #f3f4f6;
  font-size: 26rpx;
  color: #111827;
}

.editor-tip {
  display: block;
  margin-top: 8rpx;
  margin-bottom: 4rpx;
  font-size: 22rpx;
  color: rgba(17, 24, 39, 0.5);
}

.editor-footer {
  padding: 10rpx 20rpx 20rpx;
  display: flex;
  flex-direction: row;
  gap: 16rpx;
}

.btn-ghost,
.btn-secondary,
.btn-primary {
  flex: 1;
  height: 72rpx;
  font-size: 26rpx;
  border-radius: 12rpx;
}

.btn-ghost {
  background: #16a34a;
  color: #ffffff;
}

.btn-secondary {
  background: #ffffff;
  color: #111827;
  border: 2rpx solid rgba(156, 163, 175, 0.9);
}

.btn-primary {
  background: #10b981;
  color: #ffffff;
}

.picker-pop {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.picker-mask {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 0;
}

.picker-card {
  width: 360rpx;
  background: #ffffff;
  border-radius: 16rpx;
  box-shadow: 0 18rpx 40rpx rgba(0, 0, 0, 0.18);
  overflow: hidden;
}

.picker-item {
  padding: 22rpx 28rpx;
  border-bottom: 2rpx solid rgba(229, 231, 235, 1);
}

.picker-item:last-child {
  border-bottom-width: 0;
}

.picker-text {
  font-size: 28rpx;
  color: #111827;
  text-align: center;
}

.date-card {
  width: 600rpx;
  background: #ffffff;
  border-radius: 16rpx;
  box-shadow: 0 18rpx 40rpx rgba(0, 0, 0, 0.18);
  overflow: hidden;
}

.date-header {
  padding: 22rpx 28rpx 0;
}

.date-title {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.85);
}

.date-picker-view {
  height: 360rpx;
  margin-top: 12rpx;
}

.date-item {
  height: 80rpx;
  align-items: center;
  justify-content: center;
  display: flex;
}

.date-item-text {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.9);
}

.date-footer {
  display: flex;
  flex-direction: row;
  padding: 16rpx 24rpx 24rpx;
  gap: 24rpx;
}

.btn-date-cancel,
.btn-date-ok {
  flex: 1;
  height: 72rpx;
  font-size: 26rpx;
  border-radius: 12rpx;
}

.btn-date-cancel {
  background: #e5e7eb;
  color: #111827;
}

.btn-date-ok {
  background: #22c55e;
  color: #ffffff;
}

.limit-panel {
  padding-bottom: 24rpx;
}

.limit-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 20rpx 16rpx 20rpx 0;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.limit-label {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.9);
  margin-right: 16rpx;
}

.limit-icon {
  width: 32rpx;
  height: 32rpx;
  border-radius: 8rpx;
  margin-right: 12rpx;
}

.limit-icon--tank {
  background-image: url('/static/icons/tank.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.limit-icon--healer {
  background-image: url('/static/icons/healer.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.limit-icon--dps {
  background-image: url('/static/icons/dps.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.seat-panel {
  padding-top: 14rpx;
  padding-bottom: 10rpx;
}

.seat-add {
  padding: 34rpx 0 18rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  color: #10b981;
}

.seat-add-plus {
  font-size: 34rpx;
  line-height: 1;
}

.seat-add-text {
  font-size: 30rpx;
  line-height: 1;
}

.seat-tip {
  display: block;
  padding: 0 8rpx;
  margin-top: 22rpx;
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.45);
  line-height: 40rpx;
  text-align: center;
}

.seat-tip--danger {
  color: #ef4444;
}

.limit-row-right {
  margin-left: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8rpx;
  flex-shrink: 0;
}

.limit-value {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.7);
}

.limit-divider {
  padding: 24rpx 0 16rpx;
  text-align: center;
}

.limit-divider-text {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.5);
}

.limit-class-grid {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.limit-class-block {
  width: 33.33%;
  box-sizing: border-box;
  padding: 12rpx 8rpx 16rpx;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8rpx;
}

.limit-class-row1 {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8rpx;
}

.limit-class-name {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.9);
}

.limit-class-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4rpx;
}

.limit-infinity {
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.6);
}

.limit-class-specs {
  display: flex;
  flex-direction: row;
  gap: 24rpx;
  padding: 0 8rpx;
}

.limit-spec-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
}

.limit-spec-name {
  font-size: 22rpx;
  color: rgba(17, 24, 39, 0.7);
}

.limit-spec-val {
  font-size: 22rpx;
  color: rgba(17, 24, 39, 0.6);
}

.limit-picker-card {
  position: relative;
  z-index: 1;
  width: 400rpx;
  padding-top: 12rpx;
}

.limit-picker-scroll {
  height: 400rpx;
}

.limit-opt-row {
  padding: 24rpx 28rpx;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.limit-opt-row:active {
  background: rgba(0, 0, 0, 0.04);
}

.limit-opt-text {
  font-size: 28rpx;
  color: #111827;
  text-align: center;
}
</style>

