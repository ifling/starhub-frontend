<template>
  <view class="page">
    <view class="hero-card">
      <view class="hero-main">
        <text class="hero-title">{{ activity.title || '标题' }}</text>
        <view class="meta-row">
          <text class="meta-label">截止:</text>
          <text class="meta-value">{{ formatDeadline(activity.deadline_at) }}</text>
        </view>
        <view class="meta-row meta-row--type">
          <text class="created-type">{{ activity.type || '-' }}</text>
          <view class="meta-row-type-right">
            <view class="signup-pair">
              <view class="signup-icon"></view>
              <text class="signup-count">{{ signupCount }}</text>
            </view>
            <view v-if="activityCreatorName" class="activity-creator">
              <view class="activity-creator-avatar" :style="activityCreatorAvatarStyle">
                <text class="activity-creator-avatar-text">{{ activityCreatorInitial }}</text>
              </view>
              <text class="activity-creator-name">{{ activityCreatorName }}</text>
            </view>
          </view>
        </view>
        <view class="quick-block">
          <view class="quick-row">
            <view class="quick-item" @click="openRoleStatModal('tank')">
              <view class="quick-icon quick-icon--tank"></view>
              <text class="quick-num">{{ quickRoleCounts.tank }}</text>
              <text class="quick-chevron">›</text>
            </view>
            <view class="quick-item" @click="openRoleStatModal('healer')">
              <view class="quick-icon quick-icon--healer"></view>
              <text class="quick-num">{{ quickRoleCounts.healer }}</text>
              <text class="quick-chevron">›</text>
            </view>
            <view class="quick-item" @click="openRoleStatModal('dps')">
              <view class="quick-icon quick-icon--dps"></view>
              <text class="quick-num">{{ quickRoleCounts.dps }}</text>
              <text class="quick-chevron">›</text>
            </view>
          </view>
        </view>
      </view>
      <view class="hero-side">
        <button class="side-btn side-btn--share" size="mini">分享</button>
        <button class="side-btn" size="mini" @click="reload">刷新</button>
        <button class="side-btn" size="mini">举报</button>
      </view>
    </view>

    <view class="action-buttons">
      <button
        v-for="btn in headerButtons"
        :key="btn.key"
        class="action-btn"
        @click="onHeaderButtonClick(btn.key)"
      >
        {{ btn.label }}
      </button>
    </view>

    <view class="content">
      <view v-if="loading" class="placeholder">加载中...</view>
      <view v-else class="signup-list-wrap">
        <scroll-view scroll-y class="signup-left-summary" :show-scrollbar="false">
          <view
            class="signup-left-item"
            :class="{ 'signup-left-item--active': activeLeftKey === 'my' }"
            @click="scrollToGroup('my')"
            :style="{ color: '#16a34a' }"
          >
            我的报名（{{ mySignups.length }}）
          </view>

          <view
            v-for="g in signupClassGroups"
            :key="g.classLabel"
            class="signup-left-item"
            :class="{ 'signup-left-item--active': activeLeftKey === g.classLabel }"
            @click="scrollToGroup(g.classLabel)"
            :style="{ color: getClassColorByLabel(g.classLabel) }"
          >
            {{ g.classLabel }}（{{ g.signups.length }}）
          </view>

          <view v-if="!signupClassGroups.length" class="signup-left-empty">
            暂无其他报名
          </view>
        </scroll-view>

        <scroll-view
          scroll-y
          class="signup-groups"
          :scroll-top="scrollTop"
          @scroll="onSignupScroll"
          ref="signupScroll"
          :show-scrollbar="false"
        >
          <view
            class="signup-group-section"
          >
            <view class="signup-group-box">
              <view
                class="signup-group-title"
                :id="getGroupSectionId('my')"
              >
                <text class="signup-group-title-text">
                  我的报名（{{ mySignups.length }}）
                </text>
              </view>
              <view v-if="mySignups.length" class="signup-card-list">
                <view
                  v-for="s in mySignups"
                  :key="s.id"
                  class="signup-person-card"
                >
                <view
                  class="signup-avatar"
                  :style="{ background: getClassColorByLabel(getSignupClassLabel(s)) }"
                >
                  <text class="signup-avatar-text">
                    {{ (s.nickname || '').slice(0, 1) || '•' }}
                  </text>
                </view>
                <view class="signup-person-main">
                  <view class="signup-person-name-row">
                    <text class="signup-person-name">{{ s.nickname || '-' }}</text>
                  </view>
                  <view class="signup-person-meta-row">
                    <view class="signup-meta-badge">
                      {{ getSignupRoleText(s) }}
                    </view>
                    <text class="signup-person-time">{{ formatSignupTime(s.created_at) }}</text>
                  </view>
                </view>
                <button
                  v-if="isMySignup(s)"
                  class="signup-person-more"
                  @click="onSignupMore(s)"
                >
                  ...
                </button>
                <view
                  v-if="getSignupSpecBarVisible(s)"
                  class="signup-spec-bar"
                  :style="getSignupSpecBarStyle(s)"
                ></view>
              </view>
              </view>
              <view v-else class="signup-group-empty">暂无报名</view>
            </view>
          </view>

          <view
            v-for="g in signupClassGroups"
            :key="g.classLabel"
            class="signup-group-section"
          >
            <view class="signup-group-box">
              <view
                class="signup-group-title signup-group-title--colored"
                :id="getGroupSectionId(g.classLabel)"
                :style="{ background: getClassColorByLabel(g.classLabel) }"
              >
                <view
                  class="signup-group-icon role-icon"
                  :class="`role-icon--${getClassKeyByLabel(g.classLabel)}`"
                  :style="{ backgroundColor: '#ffffff' }"
                ></view>
                <text class="signup-group-title-text">
                  {{ g.classLabel }}（{{ g.signups.length }}）
                </text>
              </view>
              <view v-if="g.signups.length" class="signup-card-list">
                <view
                  v-for="s in g.signups"
                  :key="s.id"
                  class="signup-person-card"
                >
                <view
                  class="signup-avatar"
                  :style="{ background: getClassColorByLabel(g.classLabel) }"
                >
                  <text class="signup-avatar-text">
                    {{ (s.nickname || '').slice(0, 1) || '•' }}
                  </text>
                </view>
                <view class="signup-person-main">
                  <view class="signup-person-name-row">
                    <text class="signup-person-name">{{ s.nickname || '-' }}</text>
                  </view>
                  <view class="signup-person-meta-row">
                    <view class="signup-meta-badge">{{ getSignupRoleText(s) }}</view>
                    <text class="signup-person-time">{{ formatSignupTime(s.created_at) }}</text>
                  </view>
                </view>
                <button
                  v-if="isMySignup(s)"
                  class="signup-person-more"
                  @click="onSignupMore(s)"
                >
                  ...
                </button>
                <view
                  v-if="getSignupSpecBarVisible(s)"
                  class="signup-spec-bar"
                  :style="getSignupSpecBarStyle(s)"
                ></view>
              </view>
              </view>
              <view v-else class="signup-group-empty">暂无报名</view>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>

    <view v-if="showInfoModal" class="modal-mask" @click="closeInfoModal">
      <view class="info-modal" @click.stop>
        <view class="signup-modal-header">
          <view class="signup-modal-title">{{ infoModalTitle }}</view>
          <view class="signup-modal-close" @click="closeInfoModal">×</view>
        </view>
        <view class="info-body">
          <view v-if="infoModalKey === 'intro'">{{ activity.desc || '暂无简介。' }}</view>
          <view v-else-if="infoModalKey === 'limit'" class="limit-view">
            <view v-if="!hasActivityLimits" class="limit-missing">
              当前活动未保存“人数限定”数据（可能是活动创建于旧版本，或后端未更新/未迁移）。
              请在“组队-我创建的”活动里编辑并重新保存一次人数限定后再查看。
            </view>

            <view class="limit-grid">
              <view class="limit-row">
                <view class="limit-cell limit-cell--label">总人数</view>
                <view class="limit-cell limit-cell--value">{{ limitDisplay(limitPayload.total) }}</view>
              </view>
              <view class="limit-row">
                <view class="limit-cell limit-cell--label">
                  <view class="quick-icon quick-icon--tank limit-role-icon"></view>
                  <text>坦克</text>
                </view>
                <view class="limit-cell limit-cell--value">{{ limitDisplay(limitPayload.tank) }}</view>
              </view>
              <view class="limit-row">
                <view class="limit-cell limit-cell--label">
                  <view class="quick-icon quick-icon--healer limit-role-icon"></view>
                  <text>治疗</text>
                </view>
                <view class="limit-cell limit-cell--value">{{ limitDisplay(limitPayload.healer) }}</view>
              </view>
              <view class="limit-row">
                <view class="limit-cell limit-cell--label">
                  <view class="quick-icon quick-icon--dps limit-role-icon"></view>
                  <text>输出</text>
                </view>
                <view class="limit-cell limit-cell--value">{{ limitDisplay(limitPayload.dps) }}</view>
              </view>
            </view>

            <view class="limit-classes">
              <view
                v-for="c in limitClasses"
                :key="c.id"
                class="limit-class-row"
              >
                <view
                  class="limit-class-name"
                  :style="{ color: getClassColorByLabel(c.name) }"
                >
                  {{ c.name }}
                </view>
                <view class="limit-class-limit">{{ limitDisplay(c.limit) }}</view>
                <view class="limit-spec-pair limit-spec-pair--first">
                  <view class="limit-spec-name-col">
                    {{ (c.specs && c.specs[0] && c.specs[0].name) || '-' }}
                  </view>
                  <view class="limit-spec-limit-col">
                    {{ limitDisplay((c.specs && c.specs[0] && c.specs[0].limit)) }}
                  </view>
                </view>
                <view class="limit-spec-pair limit-spec-pair--second">
                  <view class="limit-spec-name-col">
                    {{ (c.specs && c.specs[1] && c.specs[1].name) || '-' }}
                  </view>
                  <view class="limit-spec-limit-col">
                    {{ limitDisplay((c.specs && c.specs[1] && c.specs[1].limit)) }}
                  </view>
                </view>
              </view>
            </view>

            <view class="limit-tip">
              <text class="limit-tip-line">提示：∞ 表示人数不限，× 表示禁止</text>
            </view>
          </view>
          <view v-else-if="infoModalKey === 'log'">日志暂未接入。</view>
        </view>
        <view class="signup-modal-footer">
          <button class="footer-btn footer-btn--ghost" @click="closeInfoModal">关闭</button>
        </view>
      </view>
    </view>

    <!-- 坦克/治疗/输出 人数统计详情 -->
    <view v-if="showRoleStatModal" class="modal-mask" @click="closeRoleStatModal">
      <view class="info-modal role-stat-modal" @click.stop>
        <view class="signup-modal-header">
          <view class="signup-modal-title">{{ roleStatTitle }}</view>
          <view class="signup-modal-close" @click="closeRoleStatModal">×</view>
        </view>
        <scroll-view scroll-y class="role-stat-scroll" :show-scrollbar="false">
          <view class="role-stat-inner">
            <view v-if="!roleStatList.length" class="role-stat-empty">该分类暂无报名</view>
            <view v-else class="role-stat-tags">
              <view
                v-for="s in roleStatList"
                :key="s.id"
                class="role-stat-tag"
                :style="roleStatTagStyle(s)"
              >
                <text class="role-stat-tag-text">{{ getRoleStatLine(s) }}</text>
              </view>
            </view>
          </view>
        </scroll-view>
        <view class="signup-modal-footer">
          <button class="footer-btn footer-btn--ghost" @click="closeRoleStatModal">关闭</button>
        </view>
      </view>
    </view>

    <view v-if="showSignupModal" class="modal-mask" @click="closeSignupModal">
      <view class="signup-modal" @click.stop>
        <view class="signup-modal-header">
          <view class="signup-modal-title">报名</view>
          <view class="signup-modal-close" @click="closeSignupModal">×</view>
        </view>

        <view class="signup-form">
          <view class="form-row form-row--inline">
            <view class="form-label form-label--inline">游戏ID*</view>
            <input
              class="form-input"
              v-model.trim="signupForm.gameId"
              placeholder="必填，请输入游戏ID"
            />
          </view>

          <view
            class="form-row form-row--inline form-row--clickable"
            @click="openMainRolePicker"
          >
            <view class="form-label form-label--inline">职业-专精</view>
            <view class="form-right">
              <text class="form-value">{{ signupForm.mainRole || '请选择' }}</text>
              <text class="form-arrow">›</text>
            </view>
          </view>

          <view class="form-row form-row--textarea-inline">
            <view class="form-label form-label--textarea-inline">备注</view>
            <input
              class="form-input form-input--note"
              v-model.trim="signupForm.note"
              maxlength="100"
              placeholder="选填，限100字"
            />
          </view>
        </view>

        <view class="signup-modal-footer">
          <button class="footer-btn footer-btn--ghost" @click="closeSignupModal">
            取消
          </button>
          <button class="footer-btn footer-btn--ghost" @click="openHistoryRoles">
            历史角色
          </button>
          <button class="footer-btn footer-btn--primary" type="primary" @click="submitSignup">
            确定
          </button>
        </view>
      </view>
    </view>

    <!-- 历史角色（全屏） -->
    <view v-if="showHistoryRoles" class="modal-mask" @click="closeHistoryRoles">
      <view class="history-roles" @click.stop>
        <view class="signup-modal-header">
          <view class="signup-modal-title">历史角色</view>
          <view class="signup-modal-close" @click="closeHistoryRoles">×</view>
        </view>
        <scroll-view scroll-y class="history-roles-list" :show-scrollbar="false">
          <view v-if="!historyRoles.length" class="history-roles-empty">暂无历史角色</view>
          <view
            v-for="(r, idx) in historyRoles"
            :key="`${r.gameId}_${r.mainRole}_${idx}`"
            class="history-roles-item"
            @click="useHistoryRole(r)"
          >
            <view class="history-roles-gameid">{{ r.gameId }}</view>
            <view class="history-roles-role">{{ r.mainRole }}</view>
          </view>
        </scroll-view>
      </view>
    </view>

    <view v-if="showRolePicker" class="picker-pop" @click.self="closeRolePicker">
      <view class="picker-card">
        <view class="picker-header">
          <view class="picker-title">职业-专精</view>
          <view class="picker-close" @click="closeRolePicker">×</view>
        </view>
        <scroll-view scroll-y class="picker-list">
          <view class="role-grid">
            <view
              v-for="cls in roleClassOptions"
              :key="cls"
              class="picker-item"
              @click="selectRoleClass(cls)"
            >
              <view
                class="role-option"
                :style="{
                  borderColor: roleClassColorMap[cls] || 'rgba(148, 163, 184, 1)',
                }"
              >
                <view
                  class="role-icon"
                  :class="`role-icon--${cls}`"
                  :style="{ backgroundColor: roleClassColorMap[cls] || '#0b3a67' }"
                ></view>
                <text
                  class="role-label"
                  :style="{ color: roleClassColorMap[cls] || '#0b3a67' }"
                >
                  {{ roleClassLabels[cls] }}
                </text>
              </view>
            </view>
          </view>

          <view class="role-grid role-grid--spec">
            <view
              v-for="spec in roleSpecsByClass[selectedRoleClass] || []"
              :key="spec"
              class="picker-item"
              @click="selectRoleSpec(spec)"
            >
              <view
                class="role-option"
                :style="{
                  borderColor: roleClassColorMap[selectedRoleClass] || 'rgba(148, 163, 184, 1)',
                }"
              >
                <view
                  class="role-icon"
                  :class="`role-icon--${selectedRoleClass}`"
                  :style="{ backgroundColor: roleClassColorMap[selectedRoleClass] || '#0b3a67' }"
                ></view>
                <text
                  class="role-label"
                  :style="{ color: roleClassColorMap[selectedRoleClass] || '#0b3a67' }"
                >
                  {{ spec }}
                </text>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>

    <!-- 三点按钮功能菜单 -->
    <view
      v-if="showSignupActionsMenu"
      class="modal-mask actions-menu-mask"
      @click="closeSignupActionsMenu"
    >
      <view class="actions-menu" @click.stop>
        <view class="actions-menu-item" @click="onSignupEditNote">
          修改备注
        </view>
        <view class="actions-menu-item" @click="onSignupLeave">
          请假
        </view>
        <view class="actions-menu-item actions-menu-item--danger" @click="onSignupCancel">
          取消报名
        </view>
        <view class="actions-menu-item actions-menu-item--close" @click="closeSignupActionsMenu">
          关闭
        </view>
      </view>
    </view>

    <!-- 修改备注弹窗 -->
    <view
      v-if="showEditNoteModal"
      class="modal-mask actions-menu-mask"
      @click="closeEditNoteModal"
    >
      <view class="edit-note-modal" @click.stop>
        <view class="signup-modal-header">
          <view class="signup-modal-title">修改备注</view>
          <view class="signup-modal-close" @click="closeEditNoteModal">×</view>
        </view>
        <view class="edit-note-body">
          <view class="edit-note-label">备注</view>
          <input
            class="form-input"
            v-model.trim="editNoteDraft"
            maxlength="100"
            placeholder="选填，限100字"
          />
        </view>
        <view class="signup-modal-footer">
          <button class="footer-btn footer-btn--ghost" @click="closeEditNoteModal">
            取消
          </button>
          <button
            class="footer-btn footer-btn--primary"
            type="primary"
            @click="onConfirmEditNote"
          >
            保存
          </button>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

/** 人数限定展示、报名列表分组、职业选择器：统一职业顺序 */
const CLASS_DISPLAY_ORDER_IDS = [
  'juren',
  'shendun',
  'senyuzhe',
  'linghun',
  'bingmo',
  'leiying',
  'qinglan',
  'shensheshou',
]

export default {
  name: 'SignupPage',
  data() {
    return {
      activityId: '',
      loading: false,
      headerButtons: [
        { key: 'intro', label: '简介' },
        { key: 'limit', label: '限制' },
        { key: 'log', label: '日志' },
        { key: 'signup', label: '报名' },
      ],
      activity: {
        title: '',
        type: '',
        deadline_at: '',
        desc: '',
        owner_username: '',
      },
      signupCount: 0,
      signups: [],
      myGameId: '',
      mySignupIds: [],
      activeLeftKey: 'my',
      groupIdToLabel: {},
      scrollUpdateTimer: null,
      scrollTop: 0,
      showSignupActionsMenu: false,
      currentSignupForMenu: null,
      showEditNoteModal: false,
      editNoteDraft: '',
      showInfoModal: false,
      infoModalKey: 'intro',
      showSignupModal: false,
      showHistoryRoles: false,
      historyRoles: [],
      showRoleStatModal: false,
      roleStatSlot: 'tank',
      showRolePicker: false,
      roleClassOptions: [...CLASS_DISPLAY_ORDER_IDS],
      roleClassLabels: {
        shendun: '神盾骑士',
        juren: '巨人守护者',
        leiying: '雷影剑士',
        qinglan: '青岚骑士',
        bingmo: '冰魔导师',
        shensheshou: '神射手',
        senyuzhe: '森语者',
        linghun: '灵魂乐手',
      },
      roleClassColorMap: {
        senyuzhe: '#32BF0F',
        bingmo: '#5C82E1',
        leiying: '#6B39DE',
        qinglan: '#11B5B2',
        juren: '#08A0DC',
        shensheshou: '#D4D116',
        shendun: '#0F68B3',
        linghun: '#1F9F0E',
      },
      selectedRoleClass: 'juren',
      roleSpecsByClass: {
        senyuzhe: ['惩击', '愈合'],
        bingmo: ['冰矛', '射线'],
        leiying: ['居合', '月刃'],
        qinglan: ['重装', '空战'],
        juren: ['岩盾', '格挡'],
        shensheshou: ['驭兽', '驯鹰'],
        shendun: ['防护', '光盾'],
        linghun: ['狂音', '协奏'],
      },
      signupForm: {
        gameId: '',
        mainRole: '',
        note: '',
      },
    }
  },
  onLoad(query) {
    this.activityId = query && query.activityId ? String(query.activityId) : ''
    try {
      this.myGameId = uni.getStorageSync('starhub_my_game_id') || ''
      const rawIds = uni.getStorageSync('starhub_my_signup_ids')
      this.mySignupIds = rawIds ? JSON.parse(rawIds) : []
    } catch {
      this.myGameId = ''
      this.mySignupIds = []
    }
    this.reload()
  },
  methods: {
    rebuildGroupIdMap() {
      const map = {}
      map[this.getGroupSectionId('my')] = 'my'
      for (const g of this.signupClassGroups || []) {
        map[this.getGroupSectionId(g.classLabel)] = g.classLabel
      }
      this.groupIdToLabel = map
    },
    updateActiveFromScroll() {
      // 根据右侧滚动位置，找最靠近顶部的分组标题
      const query = uni.createSelectorQuery().in(this)
      let containerRect = null
      let titles = []
      query.select('.signup-groups').boundingClientRect((r) => {
        containerRect = r
      })
      query.selectAll('.signup-group-title').boundingClientRect((arr) => {
        titles = Array.isArray(arr) ? arr : []
      })
      query.exec(() => {
        if (!containerRect || !titles.length) return
        const cTop = containerRect.top || 0
        const threshold = cTop + 8

        // 选出“顶部最近且不在阈值之上太多”的那个；如果都在阈值之上，用最后一个
        let best = null
        for (const t of titles) {
          if (!t) continue
          const top = t.top || 0
          if (top <= threshold) {
            best = t
          } else {
            // 第一个进入视口下方的标题：若还没 best，则用它；否则保持 best（上一个标题）
            if (!best) best = t
            break
          }
        }
        if (!best || !best.id) return
        const label = this.groupIdToLabel[best.id]
        if (!label) return
        this.activeLeftKey = label
      })
    },
    getSignupClassLabel(s) {
      const note = s && s.note ? String(s.note) : ''
      const m =
        note.match(/专精[:：]\s*([^；;]+)/) ||
        note.match(/主专精[:：]\s*([^；;]+)/) ||
        note.match(/职业[:：]\s*([^；;]+)/)
      const v = m && m[1] ? String(m[1]) : ''
      if (!v) {
        if (s && s.role) return this.roleToApiRoleText(s.role)
        return '未分类'
      }
      const parts = v.split('-')
      return parts[0] || v
    },
    /** 报名页第四行：坦克/治疗/输出人数。职业归类：巨人守护者、神盾骑士=坦克；森语者、灵魂乐手=治疗；其余=输出 */
    getQuickRoleSlotByLabel(label) {
      const x = String(label || '').trim()
      if (x === '坦克' || x === '巨人守护者' || x === '神盾骑士') return 'tank'
      if (x === '治疗' || x === '森语者' || x === '灵魂乐手') return 'healer'
      if (x === '输出') return 'dps'
      return 'dps'
    },
    /** 坦克/治疗/输出统计弹窗：一行「游戏ID-专精」 */
    getRoleStatLine(s) {
      const id = (s && s.nickname != null ? String(s.nickname) : '').trim() || '-'
      const spec = String(this.getSignupRoleText(s) || '').trim() || '-'
      return `${id}-${spec}`
    },
    hexToRgba(hex, a) {
      const h = String(hex || '').trim()
      if (!h.startsWith('#')) return `rgba(148, 163, 184, ${a})`
      let x = h.slice(1)
      if (x.length === 3) x = x.split('').map((ch) => ch + ch).join('')
      if (x.length !== 6) return `rgba(148, 163, 184, ${a})`
      const n = parseInt(x, 16)
      if (Number.isNaN(n)) return `rgba(148, 163, 184, ${a})`
      const r = (n >> 16) & 255
      const g = (n >> 8) & 255
      const b = n & 255
      return `rgba(${r},${g},${b},${a})`
    },
    roleStatTagStyle(s) {
      const c = this.getClassColorByLabel(this.getSignupClassLabel(s))
      return {
        color: c,
        borderColor: c,
        backgroundColor: this.hexToRgba(c, 0.14),
      }
    },
    roleToApiRoleText(role) {
      if (!role) return '未分类'
      if (role === 'tank') return '坦克'
      if (role === 'healer') return '治疗'
      if (role === 'dps') return '输出'
      return String(role)
    },
    getSignupRoleText(s) {
      const label = this.getSignupClassLabel(s)
      // 展示“专精”末尾（岩盾/格挡/狂暴...），如果能解析到专精就取第二段
      const note = s && s.note ? String(s.note) : ''
      const m = note.match(/专精[:：]\s*([^；;]+)/) || note.match(/主专精[:：]\s*([^；;]+)/)
      if (m && m[1]) {
        const parts = String(m[1]).split('-')
        if (parts.length >= 2) return parts[1]
      }
      return label
    },
    getSignupSpecName(s) {
      const note = s && s.note ? String(s.note) : ''
      const m = note.match(/专精[:：]\s*([^；;]+)/) || note.match(/主专精[:：]\s*([^；;]+)/)
      if (!m || !m[1]) return ''
      const parts = String(m[1]).split('-')
      return parts.length >= 2 ? String(parts[1] || '') : ''
    },
    getSignupSpecIndex(s) {
      const classLabel = this.getSignupClassLabel(s)
      const classKey = this.getClassKeyByLabel(classLabel)
      if (!classKey) return null
      const specs = (this.roleSpecsByClass && this.roleSpecsByClass[classKey]) || []
      if (!Array.isArray(specs) || specs.length < 2) return null
      const specName = this.getSignupSpecName(s)
      if (!specName) return null
      if (specName === specs[1]) return 1
      if (specName === specs[0]) return 0
      return null
    },
    getSignupSpecBarVisible(s) {
      return this.getSignupSpecIndex(s) !== null
    },
    getSignupSpecBarStyle(s) {
      const idx = this.getSignupSpecIndex(s)
      const classLabel = this.getSignupClassLabel(s)
      const color = this.getClassColorByLabel(classLabel)
      if (idx === 1) {
        return {
          backgroundImage: `linear-gradient(90deg, #ffffff 0%, #ffffff 50%, ${color} 50%, ${color} 100%)`,
        }
      }
      return {
        backgroundImage: `linear-gradient(90deg, ${color} 0%, ${color} 50%, #ffffff 50%, #ffffff 100%)`,
      }
    },
    limitDisplay(val) {
      if (val === -1) return '×'
      if (val === null || val === undefined) return '∞'
      return String(val)
    },
    formatSignupTime(iso) {
      if (!iso) return '--'
      const dt = new Date(iso)
      if (Number.isNaN(dt.getTime())) return '--'
      const mm = String(dt.getMonth() + 1).padStart(2, '0')
      const dd = String(dt.getDate()).padStart(2, '0')
      const hh = String(dt.getHours()).padStart(2, '0')
      const mi = String(dt.getMinutes()).padStart(2, '0')
      return `${mm}-${dd} ${hh}:${mi}`
    },
    getClassColorByLabel(label) {
      // roleClassColorMap 是 key->color；这里把 classLabel 映射到 key 再取颜色
      const inv = {
        森语者: this.roleClassColorMap && this.roleClassColorMap.senyuzhe,
        冰魔导师: this.roleClassColorMap && this.roleClassColorMap.bingmo,
        雷影剑士: this.roleClassColorMap && this.roleClassColorMap.leiying,
        青岚骑士: this.roleClassColorMap && this.roleClassColorMap.qinglan,
        巨人守护者: this.roleClassColorMap && this.roleClassColorMap.juren,
        神射手: this.roleClassColorMap && this.roleClassColorMap.shensheshou,
        神盾骑士: this.roleClassColorMap && this.roleClassColorMap.shendun,
        灵魂乐手: this.roleClassColorMap && this.roleClassColorMap.linghun,
      }
      return (inv && inv[label]) || '#94a3b8'
    },
    getClassKeyByLabel(label) {
      const map = {
        森语者: 'senyuzhe',
        冰魔导师: 'bingmo',
        雷影剑士: 'leiying',
        青岚骑士: 'qinglan',
        巨人守护者: 'juren',
        神射手: 'shensheshou',
        神盾骑士: 'shendun',
        灵魂乐手: 'linghun',
      }
      return map[label] || ''
    },
    sanitizeGroupId(label) {
      const s = String(label || '')
      // scroll-into-view 的匹配在不同运行时对 id 兼容性不一致，
      // 这里把 label 做成纯 ASCII，避免中文/特殊字符导致匹配失败。
      return encodeURIComponent(s).replace(/%/g, '_')
    },
    getGroupSectionId(label) {
      if (label === 'my') return 'group_my'
      return `group_${this.sanitizeGroupId(label)}`
    },
    scrollToGroup(label) {
      const id = this.getGroupSectionId(label)
      // H5: use native scrollIntoView for stable behavior inside scroll containers.
      // #ifdef H5
      setTimeout(() => {
        try {
          const el = document.getElementById(id)
          const container = this.$refs.signupScroll
          if (el && container) {
            // Try direct scrollTop update inside the scroll container.
            const containerEl = container.getBoundingClientRect ? container : null
            if (containerEl && el.getBoundingClientRect) {
              const cRect = containerEl.getBoundingClientRect()
              const tRect = el.getBoundingClientRect()
              const delta = (tRect.top || 0) - (cRect.top || 0)
              const next = (containerEl.scrollTop || 0) + delta
              containerEl.scrollTop = next
              this.scrollTop = next
              return
            }
          }
          if (el && el.scrollIntoView) {
            el.scrollIntoView({ behavior: 'auto', block: 'start' })
          }
        } catch {}
      }, 30)
      return
      // #endif

      // Fallback (非 H5): keep the old scrollTop calculation.
      setTimeout(() => {
        const targetSelector = `#${id}`
        let targetRect = null
        let containerRect = null
        const query = uni.createSelectorQuery()
        query.select(targetSelector).boundingClientRect((r) => {
          targetRect = r
        })
        query.select('.signup-groups').boundingClientRect((r) => {
          containerRect = r
        })
        query.exec(() => {
          if (!targetRect || !containerRect) return
          const old = Number(this.scrollTop) || 0
          const delta = (targetRect.top || 0) - (containerRect.top || 0)
          this.scrollTop = old + delta
        })
      }, 30)
    },
    onSignupScroll(e) {
      const v = e && e.detail ? e.detail.scrollTop : 0
      if (typeof v === 'number') this.scrollTop = v
      // throttle: avoid heavy selectorQuery on every tick
      if (this.scrollUpdateTimer) return
      this.scrollUpdateTimer = setTimeout(() => {
        this.scrollUpdateTimer = null
        this.updateActiveFromScroll()
      }, 120)
    },
    isMySignup(s) {
      if (!s) return false
      const id = s && s.id != null ? String(s.id) : ''
      if (id && Array.isArray(this.mySignupIds) && this.mySignupIds.includes(id)) return true
      // fallback: nickname match
      if (!this.myGameId) return false
      const n = s && s.nickname != null ? String(s.nickname) : ''
      return String(n) === String(this.myGameId)
    },
    onSignupMore(signup) {
      this.currentSignupForMenu = signup || null
      this.showEditNoteModal = false
      this.showSignupActionsMenu = true
    },
    closeSignupActionsMenu() {
      this.showSignupActionsMenu = false
      this.currentSignupForMenu = null
    },
    closeEditNoteModal() {
      this.showEditNoteModal = false
    },
    extractRemarkFromNote(note) {
      const raw = note == null ? '' : String(note)
      const m = raw.match(/备注[:：]\s*([^；;]*)/)
      if (m && m[1] != null) return String(m[1]).trim()
      return ''
    },
    updateNoteRemark(note, remark) {
      const raw = note == null ? '' : String(note)
      const rem = (remark == null ? '' : String(remark)).trim()
      const parts = raw.split('；').map((p) => p.trim()).filter(Boolean)
      const next = []
      for (const p of parts) {
        if (/^备注[:：]/.test(p)) continue
        next.push(p)
      }
      if (rem) next.push(`备注: ${rem}`)
      return next.join('；')
    },
    async recreateSignupWithNote(signup, updatedNote) {
      if (!signup || !signup.id) return
      const oldId = String(signup.id)
      await request(`/activities/${this.activityId}/signups/${signup.id}`, { method: 'DELETE' })
      const created = await request(`/activities/${this.activityId}/signups`, {
        method: 'POST',
        data: {
          nickname: signup.nickname,
          role: signup.role,
          note: updatedNote,
        },
      })
      // update local "mine" ids
      try {
        const next = Array.isArray(this.mySignupIds) ? this.mySignupIds.slice() : []
        const createdId = created && created.id != null ? String(created.id) : ''
        const filtered = next.filter((x) => String(x) !== oldId)
        if (createdId && !filtered.includes(createdId)) filtered.push(createdId)
        this.mySignupIds = filtered
        uni.setStorageSync('starhub_my_signup_ids', JSON.stringify(this.mySignupIds))
      } catch {}
      return created
    },
    async onSignupEditNote() {
      if (!this.currentSignupForMenu) return
      this.showSignupActionsMenu = false
      this.editNoteDraft = this.extractRemarkFromNote(this.currentSignupForMenu.note)
      this.showEditNoteModal = true
    },
    async onSignupLeave() {
      if (!this.currentSignupForMenu) return
      const signup = this.currentSignupForMenu
      const currentRemark = this.extractRemarkFromNote(signup.note)
      const nextRemark = currentRemark ? `${currentRemark}；请假` : '请假'
      const updatedNote = this.updateNoteRemark(signup.note, nextRemark)
      uni.showLoading({ title: '更新中' })
      try {
        await this.recreateSignupWithNote(signup, updatedNote)
        uni.showToast({ title: '已设置请假', icon: 'none' })
        this.closeSignupActionsMenu()
        await this.reload()
      } catch (e) {
        uni.showToast({ title: '更新失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
    async onSignupCancel() {
      if (!this.currentSignupForMenu) return
      const signup = this.currentSignupForMenu
      uni.showLoading({ title: '取消报名中' })
      try {
        const oldId = signup && signup.id != null ? String(signup.id) : ''
        await request(`/activities/${this.activityId}/signups/${signup.id}`, { method: 'DELETE' })
        if (oldId && Array.isArray(this.mySignupIds)) {
          this.mySignupIds = this.mySignupIds.filter((x) => String(x) !== oldId)
          uni.setStorageSync('starhub_my_signup_ids', JSON.stringify(this.mySignupIds))
        }
        uni.showToast({ title: '已取消报名', icon: 'none' })
        this.closeSignupActionsMenu()
        await this.reload()
      } catch (e) {
        uni.showToast({ title: '取消失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
    async onConfirmEditNote() {
      if (!this.currentSignupForMenu) return
      const signup = this.currentSignupForMenu
      const updatedNote = this.updateNoteRemark(signup.note, this.editNoteDraft)
      uni.showLoading({ title: '保存中' })
      try {
        await this.recreateSignupWithNote(signup, updatedNote)
        uni.showToast({ title: '备注已更新', icon: 'none' })
        this.showEditNoteModal = false
        await this.reload()
      } catch (e) {
        uni.showToast({ title: '保存失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
    async reload() {
      if (!this.activityId) {
        uni.showToast({ title: '缺少活动ID', icon: 'none' })
        return
      }
      this.loading = true
      try {
        const data = await request(`/activities/${this.activityId}`)
        this.activity = data || {}
        const signups = await request(`/activities/${this.activityId}/signups`)
        this.signups = Array.isArray(signups) ? signups : []
        this.signupCount = this.signups.length
      } catch (e) {
        uni.showToast({ title: '加载失败', icon: 'none' })
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.rebuildGroupIdMap()
          this.updateActiveFromScroll()
        })
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
      return `${y}-${m}-${d} ${hh}:${mm} ${weekdays[dt.getDay()]}`
    },
    onHeaderButtonClick(key) {
      if (key === 'signup') {
        this.openSignupModal()
        return
      }
      this.openInfoModal(key)
    },
    openInfoModal(key) {
      this.infoModalKey = key
      this.showInfoModal = true
      this.showSignupModal = false
      this.showRolePicker = false
      this.showRoleStatModal = false
    },
    closeInfoModal() {
      this.showInfoModal = false
    },
    openSignupModal() {
      // reset every open
      this.signupForm = {
        gameId: '',
        mainRole: '',
        note: '',
      }
      this.showRolePicker = false
      this.showRoleStatModal = false
      this.showSignupModal = true
    },
    closeSignupModal() {
      this.showSignupModal = false
      this.showRolePicker = false
    },
    openRoleStatModal(slot) {
      this.roleStatSlot = slot === 'healer' || slot === 'dps' ? slot : 'tank'
      this.showRoleStatModal = true
      this.showInfoModal = false
      this.showSignupModal = false
      this.showRolePicker = false
      this.showHistoryRoles = false
    },
    closeRoleStatModal() {
      this.showRoleStatModal = false
    },
    openMainRolePicker() {
      this.selectedRoleClass = this.roleClassOptions[0]
      this.showRolePicker = true
    },
    closeRolePicker() {
      this.showRolePicker = false
    },
    getHistoryStorageKey() {
      // 用本机“当前账号”维度隔离；这里用最近一次报名的 gameId 作为账号标识（无更可靠账号信息时）。
      let k = ''
      try {
        k = uni.getStorageSync('starhub_my_game_id') || ''
      } catch {}
      const key = (k || this.myGameId || 'default').trim()
      return `starhub_history_roles_${encodeURIComponent(key)}`
    },
    loadHistoryRoles() {
      try {
        const raw = uni.getStorageSync(this.getHistoryStorageKey())
        const arr = raw ? JSON.parse(raw) : []
        this.historyRoles = Array.isArray(arr) ? arr.slice(0, 20) : []
      } catch {
        this.historyRoles = []
      }
    },
    saveHistoryRole(gameId, mainRole) {
      const gid = String(gameId || '').trim()
      const role = String(mainRole || '').trim()
      if (!gid || !role) return
      this.loadHistoryRoles()
      const next = []
      // newest first, de-dupe by (gameId + mainRole)
      next.push({ gameId: gid, mainRole: role })
      for (const r of this.historyRoles || []) {
        if (!r) continue
        const rg = String(r.gameId || '').trim()
        const rr = String(r.mainRole || '').trim()
        if (!rg || !rr) continue
        if (rg === gid && rr === role) continue
        next.push({ gameId: rg, mainRole: rr })
        if (next.length >= 20) break
      }
      this.historyRoles = next
      try {
        uni.setStorageSync(this.getHistoryStorageKey(), JSON.stringify(next))
      } catch {}
    },
    openHistoryRoles() {
      this.loadHistoryRoles()
      this.showRoleStatModal = false
      this.showHistoryRoles = true
    },
    closeHistoryRoles() {
      this.showHistoryRoles = false
    },
    useHistoryRole(r) {
      if (!r) return
      const gid = String(r.gameId || '').trim()
      const role = String(r.mainRole || '').trim()
      if (gid) this.signupForm.gameId = gid
      if (role) this.signupForm.mainRole = role
      // 尝试同步当前职业到选择器（不影响正常使用）
      try {
        const clsLabel = role.split('-')[0]
        const key = this.getClassKeyByLabel(clsLabel)
        if (key) this.selectedRoleClass = key
      } catch {}
      this.showHistoryRoles = false
    },
    selectRoleClass(cls) {
      this.selectedRoleClass = cls
    },

    selectRoleSpec(spec) {
      if (!this.selectedRoleClass) return
      this.signupForm.mainRole = `${this.roleClassLabels[this.selectedRoleClass] || this.selectedRoleClass}-${spec}`
      this.showRolePicker = false
    },
    roleToApiRole(mainRole) {
      if (!mainRole) return 'dps'
      const s = String(mainRole)
      if (s.includes('愈合') || s.includes('光盾') || s.includes('协奏') || s.includes('恢复')) return 'healer'
      if (s.includes('防护') || s.includes('岩盾') || s.includes('格挡') || s.includes('重装')) return 'tank'
      return 'dps'
    },
    buildNote() {
      const parts = []
      if (this.signupForm.mainRole) parts.push(`专精: ${this.signupForm.mainRole}`)
      if (this.signupForm.note) parts.push(`备注: ${this.signupForm.note}`)
      const note = parts.join('；')
      if (!note) return null
      return note.length > 200 ? note.slice(0, 200) : note
    },
    async submitSignup() {
      const gameId = (this.signupForm.gameId || '').trim()
      if (!gameId) {
        uni.showToast({ title: '请输入游戏ID', icon: 'none' })
        return
      }
      if (!this.signupForm.mainRole) {
        uni.showToast({ title: '请选择职业-专精', icon: 'none' })
        return
      }
      if (!this.activityId) return

      const payload = {
        nickname: gameId,
        role: this.roleToApiRole(this.signupForm.mainRole),
        note: this.buildNote(),
      }

      uni.showLoading({ title: '提交中' })
      try {
        const created = await request(`/activities/${this.activityId}/signups`, { method: 'POST', data: payload })
        uni.showToast({ title: '报名成功', icon: 'none' })
        try {
          uni.setStorageSync('starhub_my_game_id', gameId)
        } catch {}
        this.myGameId = gameId
        // record "mine" by signup id (supports multi-role signup)
        try {
          const createdId =
            created && created.id != null ? String(created.id) : ''
          if (createdId) {
            if (!Array.isArray(this.mySignupIds)) this.mySignupIds = []
            if (!this.mySignupIds.includes(createdId)) this.mySignupIds.push(createdId)
            uni.setStorageSync('starhub_my_signup_ids', JSON.stringify(this.mySignupIds))
          }
        } catch {}
        this.showSignupModal = false
        // 保存历史角色（最多20条，去重：gameId + 职业-专精）
        try {
          this.saveHistoryRole(gameId, this.signupForm.mainRole)
        } catch {}
        // refresh list
        await this.reload()
      } catch (e) {
        uni.showToast({ title: '报名失败', icon: 'none' })
      } finally {
        uni.hideLoading()
      }
    },
  },
  computed: {
    hasActivityLimits() {
      return !!(this.activity && this.activity.limits)
    },
    limitPayload() {
      const l = this.activity && this.activity.limits ? this.activity.limits : null
      return {
        total: l && l.total !== undefined ? l.total : null,
        tank: l && l.tank !== undefined ? l.tank : null,
        healer: l && l.healer !== undefined ? l.healer : null,
        dps: l && l.dps !== undefined ? l.dps : null,
        classes: l && Array.isArray(l.classes) ? l.classes : [],
      }
    },
    limitClasses() {
      const arr = (this.limitPayload && this.limitPayload.classes) || []
      if (arr && arr.length) {
        const list = arr
          .filter((c) => c && c.id && c.name)
          .slice(0, 30)
        list.sort((a, b) => {
          const ia = CLASS_DISPLAY_ORDER_IDS.indexOf(a.id)
          const ib = CLASS_DISPLAY_ORDER_IDS.indexOf(b.id)
          return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib)
        })
        return list
      }
      // fallback: show empty template (still matches职业/专精结构)
      return CLASS_DISPLAY_ORDER_IDS.map((id) => ({
        id,
        name: this.roleClassLabels[id] || id,
        limit: null,
        specs: (this.roleSpecsByClass[id] || []).map((name) => ({ name, limit: null })),
      }))
    },
    mySignups() {
      if (Array.isArray(this.mySignupIds) && this.mySignupIds.length) {
        return (this.signups || []).filter((s) => {
          const id = s && s.id != null ? String(s.id) : ''
          return id && this.mySignupIds.includes(id)
        })
      }
      if (!this.myGameId) return []
      return (this.signups || []).filter(
        (s) => String(s.nickname || '') === String(this.myGameId),
      )
    },
    signupClassGroups() {
      const list = this.signups || []
      const map = {}
      for (const s of list) {
        const cls = this.getSignupClassLabel(s)
        if (!map[cls]) map[cls] = []
        map[cls].push(s)
      }
      const groups = Object.keys(map).map((k) => ({ classLabel: k, signups: map[k] }))
      groups.sort((a, b) => {
        const ka = this.getClassKeyByLabel(a.classLabel)
        const kb = this.getClassKeyByLabel(b.classLabel)
        const ia = ka ? CLASS_DISPLAY_ORDER_IDS.indexOf(ka) : -1
        const ib = kb ? CLASS_DISPLAY_ORDER_IDS.indexOf(kb) : -1
        const sa = ia === -1 ? 1000 : ia
        const sb = ib === -1 ? 1000 : ib
        if (sa !== sb) return sa - sb
        return String(a.classLabel).localeCompare(String(b.classLabel), 'zh-CN')
      })
      return groups
    },
    infoModalTitle() {
      if (this.infoModalKey === 'intro') return '简介'
      if (this.infoModalKey === 'limit') return '人数限制'
      if (this.infoModalKey === 'log') return '日志'
      return '信息'
    },
    activityCreatorName() {
      const u = this.activity && this.activity.owner_username
      return u != null && String(u).trim() ? String(u).trim() : ''
    },
    activityCreatorInitial() {
      const n = this.activityCreatorName
      if (!n) return '?'
      return n.slice(0, 1)
    },
    activityCreatorAvatarStyle() {
      const palette = ['#0f68b3', '#32bf0f', '#6b39de', '#5c82e1', '#11b5b2', '#d4d116']
      const name = this.activityCreatorName || ''
      let h = 0
      for (let i = 0; i < name.length; i++) h += name.charCodeAt(i)
      return { backgroundColor: palette[h % palette.length] }
    },
    quickRoleCounts() {
      let tank = 0
      let healer = 0
      let dps = 0
      const list = Array.isArray(this.signups) ? this.signups : []
      for (const s of list) {
        const label = this.getSignupClassLabel(s)
        const slot = this.getQuickRoleSlotByLabel(label)
        if (slot === 'tank') tank += 1
        else if (slot === 'healer') healer += 1
        else dps += 1
      }
      return { tank, healer, dps }
    },
    roleStatList() {
      const slot = this.roleStatSlot
      if (!slot || !['tank', 'healer', 'dps'].includes(slot)) return []
      return (this.signups || []).filter(
        (s) => this.getQuickRoleSlotByLabel(this.getSignupClassLabel(s)) === slot,
      )
    },
    roleStatTitle() {
      const n = Array.isArray(this.roleStatList) ? this.roleStatList.length : 0
      if (this.roleStatSlot === 'tank') return `坦克（${n}）`
      if (this.roleStatSlot === 'healer') return `治疗（${n}）`
      if (this.roleStatSlot === 'dps') return `输出（${n}）`
      return `报名统计（${n}）`
    },
  },
}
</script>

<style>
.page {
  min-height: 100vh;
  background: #e5e7eb;
}

.hero-card {
  background: #ffffff;
  margin: 0;
  padding: 14rpx 14rpx 10rpx;
  display: flex;
  gap: 14rpx;
  border-bottom: 2rpx solid #d1d5db;
}

.hero-main {
  flex: 1;
}

.hero-side {
  width: 104rpx;
  display: flex;
  flex-direction: column;
  gap: 10rpx;
}

.hero {
  background: #ffffff;
  padding: 20rpx 24rpx 16rpx;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.08);
}

.hero-title {
  display: block;
  font-size: 38rpx;
  font-weight: 700;
  color: #111827;
  margin-bottom: 10rpx;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-top: 8rpx;
}

.meta-label {
  font-size: 28rpx;
  color: #111827;
  font-weight: 600;
}

.meta-value {
  font-size: 28rpx;
  color: #111827;
}

.meta-row--type {
  margin-top: 14rpx;
  justify-content: space-between;
  width: 100%;
  flex-wrap: nowrap;
  gap: 12rpx;
}

.created-type {
  font-size: 30rpx;
  color: #111827;
  flex-shrink: 0;
}

.meta-row-type-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16rpx;
  margin-left: auto;
  flex-shrink: 0;
  min-width: 0;
}

.signup-pair {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-left: 0;
  flex-shrink: 0;
}

.activity-creator {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8rpx;
  max-width: 220rpx;
}

.activity-creator-avatar {
  width: 44rpx;
  height: 44rpx;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-creator-avatar-text {
  color: #ffffff;
  font-size: 22rpx;
  font-weight: 800;
}

.activity-creator-name {
  font-size: 22rpx;
  color: #334155;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.signup-icon {
  width: 26rpx;
  height: 26rpx;
  background-image: url('/static/icons/signup-count.svg');
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.signup-count {
  font-size: 24rpx;
  color: #334155;
}

.quick-block {
  margin-top: 10rpx;
}

.quick-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.quick-item {
  display: flex;
  align-items: center;
  gap: 4rpx;
  padding: 6rpx 12rpx 6rpx 10rpx;
  border-radius: 999rpx;
  background: rgba(241, 245, 249, 0.95);
  border: 2rpx solid rgba(148, 163, 184, 0.55);
}

.quick-icon {
  width: 26rpx;
  height: 26rpx;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.quick-icon--tank {
  background-image: url('/static/icons/tank.svg');
}

.quick-icon--healer {
  background-image: url('/static/icons/healer.svg');
}

.quick-icon--dps {
  background-image: url('/static/icons/dps.svg');
}

.quick-num {
  font-size: 24rpx;
  color: #1d4ed8;
  font-weight: 700;
  border-bottom: 2rpx dashed rgba(29, 78, 216, 0.4);
}

.quick-chevron {
  font-size: 26rpx;
  color: #1d4ed8;
  font-weight: 700;
  line-height: 1;
  margin-left: 2rpx;
}

.side-btn {
  height: 56rpx;
  line-height: 56rpx;
  border-radius: 6rpx;
  border: 2rpx solid #94a3b8;
  background: #ffffff;
  color: #0f172a;
  font-size: 24rpx;
  padding: 0;
}

.side-btn::after {
  border: 0;
}

.side-btn--share {
  border-color: #16a34a;
  background: #22c55e;
  color: #ffffff;
  font-weight: 600;
}

.action-btn {
  flex: 1;
  height: 58rpx;
  line-height: 58rpx;
  padding: 0;
  border-radius: 6rpx;
  border: 2rpx solid #94a3b8;
  font-size: 30rpx;
  color: #0b3a67;
  background: #ffffff;
}

.action-btn::after {
  border: 0;
}

.action-btn--active {
  color: #ffffff;
  font-weight: 700;
  background: #133f67;
  border-color: #133f67;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 12rpx;
  background: #ffffff;
  padding: 10rpx 16rpx 12rpx;
  border-bottom: 2rpx solid #d1d5db;
}

.content {
  background: #e5e7eb;
  min-height: 800rpx;
}

.placeholder {
  text-align: center;
  color: #9ca3af;
  font-size: 34rpx;
  padding-top: 80rpx;
}

.signup-list-wrap {
  display: flex;
  flex-direction: row;
  gap: 18rpx;
  padding: 24rpx 18rpx;
}

.signup-left-summary {
  width: 240rpx;
  display: flex;
  flex-direction: column;
  gap: 14rpx;
  height: 800rpx;
  background: transparent;
}

.signup-left-item {
  background: #ffffff;
  border-radius: 16rpx;
  padding: 18rpx 16rpx;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12rpx;
  color: rgba(17, 24, 39, 0.55);
  font-size: 28rpx;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  border: 2rpx solid rgba(148, 163, 184, 0.35);
  position: relative;
}

.signup-left-item:active {
  opacity: 0.9;
}

.signup-left-item--active {
  color: #111827;
  font-weight: 700;
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.45);
}

.signup-left-item--active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 10rpx;
  bottom: 10rpx;
  width: 8rpx;
  border-radius: 8rpx;
  background: #16a34a;
}

.signup-left-item-dot {
  width: 14rpx;
  height: 14rpx;
  border-radius: 999rpx;
  background: rgba(16, 185, 129, 0.9);
  flex-shrink: 0;
}

.signup-left-item-dot--my {
  background: #16a34a;
}

.signup-left-empty {
  padding: 18rpx 16rpx;
  color: rgba(17, 24, 39, 0.35);
  font-size: 26rpx;
  text-align: center;
  background: #ffffff;
  border-radius: 16rpx;
}

.signup-groups {
  flex: 1;
  height: 800rpx;
}

.signup-left-summary,
.signup-groups {
  scrollbar-width: none; /* Firefox */
}

.signup-left-summary::-webkit-scrollbar,
.signup-groups::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
  width: 0;
  height: 0;
}

.signup-group-section {
  margin-bottom: 18rpx;
}

.signup-group-box {
  background: #ffffff;
  border-radius: 16rpx;
  overflow: hidden;
}

.signup-group-title {
  background: #ffffff;
  border-radius: 16rpx 16rpx 0 0;
  padding: 18rpx 18rpx;
  color: #111827;
  font-size: 30rpx;
  font-weight: 700;
  margin-bottom: 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12rpx;
}

.signup-group-title--colored {
  color: #ffffff;
}

.signup-group-dot {
  width: 14rpx;
  height: 14rpx;
  border-radius: 999rpx;
  flex-shrink: 0;
}

.signup-group-icon {
  width: 28rpx;
  height: 28rpx;
  flex-shrink: 0;
}

.signup-group-title-text {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.signup-group-empty {
  background: transparent;
  border-top: 1rpx solid rgba(148, 163, 184, 0.22);
  padding: 24rpx 18rpx;
  color: rgba(17, 24, 39, 0.45);
  font-size: 28rpx;
  text-align: center;
}

.signup-card-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.signup-person-card {
  background: transparent;
  border-radius: 0;
  padding: 18rpx 16rpx;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 14rpx;
  border-top: 1rpx solid rgba(148, 163, 184, 0.22);
  position: relative;
}

.signup-spec-bar {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 8rpx;
  pointer-events: none;
}

.signup-avatar {
  width: 66rpx;
  height: 66rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.signup-avatar-text {
  color: #ffffff;
  font-weight: 800;
  font-size: 26rpx;
}

.signup-person-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.signup-person-name {
  font-size: 28rpx;
  font-weight: 800;
  color: #111827;
}

.signup-person-meta-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12rpx;
}

.signup-meta-badge {
  font-size: 22rpx;
  color: rgba(17, 24, 39, 0.55);
  background: rgba(229, 231, 235, 0.7);
  padding: 6rpx 12rpx;
  border-radius: 999rpx;
}

.signup-person-time {
  font-size: 22rpx;
  color: rgba(17, 24, 39, 0.45);
}

.signup-person-more {
  width: 72rpx;
  height: 48rpx;
  border-radius: 14rpx;
  background: #ffffff;
  border: 2rpx solid rgba(148, 163, 184, 0.9);
  color: rgba(17, 24, 39, 0.55);
  font-size: 28rpx;
  padding: 0;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.signup-list-placeholder {
  padding: 60rpx 24rpx;
  text-align: center;
  color: rgba(17, 24, 39, 0.45);
  font-size: 30rpx;
}

.signup-list-count {
  display: block;
  margin-top: 18rpx;
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.55);
}

.modal-mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99;
}

.signup-modal {
  width: 640rpx;
  max-width: 90vw;
  background: #ffffff;
  border-radius: 18rpx;
  overflow: hidden;
}

.history-roles {
  width: 92vw;
  max-width: 720rpx;
  height: 80vh;
  background: #ffffff;
  border-radius: 18rpx;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.history-roles-list {
  flex: 1;
  padding: 0 20rpx 20rpx;
}

.history-roles-empty {
  padding: 60rpx 0;
  text-align: center;
  color: rgba(17, 24, 39, 0.45);
  font-size: 28rpx;
}

.history-roles-item {
  padding: 18rpx 0;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.history-roles-item:active {
  opacity: 0.9;
}

.history-roles-gameid {
  font-size: 28rpx;
  font-weight: 800;
  color: #111827;
}

.history-roles-role {
  margin-top: 6rpx;
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.6);
}

.signup-modal-header {
  padding: 18rpx 20rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.signup-modal-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #111827;
}

.signup-modal-close {
  width: 44rpx;
  height: 44rpx;
  border-radius: 14rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  font-size: 34rpx;
}

.info-modal {
  width: 640rpx;
  max-width: 90vw;
  background: #ffffff;
  border-radius: 18rpx;
  overflow: hidden;
}

.role-stat-modal {
  display: flex;
  flex-direction: column;
  max-height: 85vh;
}

.role-stat-scroll {
  flex: 1;
  max-height: 44vh;
  padding: 0 16rpx 8rpx;
  box-sizing: border-box;
}

.role-stat-inner {
  width: 100%;
}

.role-stat-empty {
  padding: 36rpx 0;
  text-align: center;
  color: rgba(17, 24, 39, 0.45);
  font-size: 26rpx;
}

.role-stat-tags {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: flex-start;
  padding: 4rpx 0 8rpx;
}

.role-stat-tag {
  display: inline-flex;
  align-items: center;
  max-width: 100%;
  margin: 0 8rpx 8rpx 0;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
  border-width: 2rpx;
  border-style: solid;
  box-sizing: border-box;
}

.role-stat-tag-text {
  font-size: 22rpx;
  font-weight: 700;
  line-height: 32rpx;
  word-break: break-all;
}

.quick-item:active {
  opacity: 0.78;
  background: rgba(219, 234, 254, 0.95);
}

.info-body {
  padding: 20rpx 20rpx 0;
  color: rgba(17, 24, 39, 0.75);
  font-size: 26rpx;
  line-height: 40rpx;
  min-height: 240rpx;
}

.limit-view {
  width: 100%;
}

.limit-missing {
  margin-bottom: 14rpx;
  padding: 12rpx 14rpx;
  border-radius: 12rpx;
  background: rgba(251, 191, 36, 0.18);
  color: rgba(17, 24, 39, 0.7);
  font-size: 24rpx;
  line-height: 34rpx;
}

.limit-grid {
  background: rgba(243, 244, 246, 0.7);
  border-radius: 14rpx;
  padding: 10rpx 14rpx;
}

.limit-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10rpx 0;
}

.limit-cell--label {
  width: 240rpx;
  display: flex;
  align-items: center;
  gap: 10rpx;
  color: rgba(17, 24, 39, 0.65);
  font-weight: 700;
}

.limit-role-icon {
  width: 26rpx;
  height: 26rpx;
}

.limit-cell--value {
  flex: 1;
  text-align: left;
  color: rgba(17, 24, 39, 0.65);
  font-weight: 800;
}

.limit-classes {
  margin-top: 14rpx;
}

.limit-class-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: nowrap;
  gap: 12rpx;
  padding: 14rpx 6rpx;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.limit-class-name {
  width: 150rpx;
  font-size: 26rpx;
  font-weight: 900;
}

.limit-class-limit {
  width: 56rpx;
  text-align: center;
  font-size: 26rpx;
  font-weight: 900;
  color: rgba(17, 24, 39, 0.55);
}

.limit-spec-pair {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 6rpx;
  flex-shrink: 0;
}

/* 与左侧「职业 / 职业限制」拉开距离，专精名不再贴左边 */
.limit-spec-pair--first {
  margin-left: 28rpx;
}

/* 与第一组专精拉开距离 */
.limit-spec-pair--second {
  margin-left: 24rpx;
}

.limit-spec-name-col {
  max-width: 120rpx;
  font-size: 22rpx;
  color: rgba(17, 24, 39, 0.55);
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.limit-spec-limit-col {
  min-width: 44rpx;
  text-align: center;
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.65);
  font-weight: 900;
  flex-shrink: 0;
}

.limit-tip {
  margin-top: 16rpx;
  padding: 10rpx 6rpx 0;
  color: rgba(17, 24, 39, 0.45);
  font-size: 22rpx;
}

.signup-form {
  padding: 10rpx 20rpx 0;
}

.form-row {
  padding: 18rpx 0;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.form-row--clickable {
  cursor: pointer;
}

.form-row--inline {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 14rpx;
}

.form-label--inline {
  width: 160rpx;
  margin: 0;
  padding-top: 6rpx;
}

.form-label {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.9);
  margin-bottom: 12rpx;
  font-weight: 600;
}

.form-right {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10rpx;
}

.form-value {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.5);
}

.form-arrow {
  font-size: 34rpx;
  color: rgba(17, 24, 39, 0.35);
  transform: translateY(-2rpx);
}

.form-input {
  height: 64rpx;
  border-radius: 12rpx;
  padding: 0 18rpx;
  background: #f3f4f6;
  font-size: 26rpx;
}

.form-textarea {
  min-height: 120rpx;
  border-radius: 12rpx;
  padding: 14rpx 18rpx;
  background: #f3f4f6;
  font-size: 26rpx;
}

.form-input--note {
  height: 64rpx;
  flex: 1;
  width: 100%;
  box-sizing: border-box;
}

.form-row--textarea-inline {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8rpx;
}

.form-label--textarea-inline {
  width: auto;
  margin: 0;
  padding-top: 6rpx;
  white-space: nowrap;
}

.form-row--textarea-inline .form-textarea {
  flex: 1;
  margin: 0;
  min-height: 96rpx;
}

.form-row--textarea-inline .form-input--note {
  flex: 1;
  margin: 0;
  min-height: 64rpx;
  width: 100%;
  box-sizing: border-box;
}

.signup-modal-footer {
  padding: 18rpx 20rpx 22rpx;
  display: flex;
  gap: 18rpx;
  justify-content: flex-end;
}

.actions-menu-mask {
  z-index: 120;
}

.actions-menu {
  width: 360rpx;
  max-width: 90vw;
  background: #ffffff;
  border-radius: 18rpx;
  overflow: hidden;
  box-shadow: 0 18rpx 40rpx rgba(0, 0, 0, 0.18);
  padding: 10rpx 0;
}

.actions-menu-item {
  padding: 18rpx 18rpx;
  text-align: center;
  font-size: 28rpx;
  color: rgba(17, 24, 39, 0.75);
}

.actions-menu-item:active {
  background: rgba(0, 0, 0, 0.04);
}

.actions-menu-item--danger {
  color: #ef4444;
}

.actions-menu-item--close {
  margin-top: 6rpx;
  color: rgba(17, 24, 39, 0.65);
}

.edit-note-modal {
  width: 560rpx;
  max-width: 90vw;
  background: #ffffff;
  border-radius: 18rpx;
  overflow: hidden;
}

.edit-note-body {
  padding: 20rpx 20rpx 0;
}

.edit-note-label {
  font-size: 26rpx;
  color: rgba(17, 24, 39, 0.9);
  font-weight: 600;
  margin-bottom: 12rpx;
}

.footer-btn {
  flex: 1;
  height: 74rpx;
  border-radius: 14rpx;
  font-size: 28rpx;
}

.footer-btn--ghost {
  background: #ffffff;
  border: 2rpx solid rgba(148, 163, 184, 1);
  color: #111827;
}

.footer-btn--primary {
  background: #22c55e;
  color: #ffffff;
}

.picker-pop {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  background: rgba(0, 0, 0, 0.35);
}

.picker-card {
  width: 560rpx;
  background: #ffffff;
  border-radius: 16rpx;
  overflow: hidden;
}

.picker-header {
  padding: 18rpx 20rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2rpx solid rgba(0, 0, 0, 0.06);
}

.picker-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #111827;
}

.picker-close {
  width: 44rpx;
  height: 44rpx;
  border-radius: 14rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  font-size: 34rpx;
}

.picker-list {
  width: 100%;
  max-height: 62vh;
  padding: 20rpx 16rpx 24rpx;
}

.picker-item {
  width: 25%;
  box-sizing: border-box;
  padding: 0;
}

.role-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx 14rpx;
}

.role-grid--spec {
  margin-top: 52rpx;
}

.role-option {
  width: 100%;
  height: 64rpx;
  border-radius: 12rpx;
  border: 2rpx solid rgba(148, 163, 184, 1);
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 6rpx;
}

.role-icon {
  width: 28rpx;
  height: 28rpx;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-color: #0b3a67;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  -webkit-mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
  mask-size: contain;
}

.role-icon--shendun {
  -webkit-mask-image: url('/static/icons/shendun.svg');
  mask-image: url('/static/icons/shendun.svg');
}

.role-icon--juren {
  -webkit-mask-image: url('/static/icons/juren.svg');
  mask-image: url('/static/icons/juren.svg');
}

.role-icon--leiying {
  -webkit-mask-image: url('/static/icons/leiying.svg');
  mask-image: url('/static/icons/leiying.svg');
}

.role-icon--qinglan {
  -webkit-mask-image: url('/static/icons/qinglan.svg');
  mask-image: url('/static/icons/qinglan.svg');
}

.role-icon--bingmo {
  -webkit-mask-image: url('/static/icons/bingmo.svg');
  mask-image: url('/static/icons/bingmo.svg');
}

.role-icon--shensheshou {
  -webkit-mask-image: url('/static/icons/shensheshou.svg');
  mask-image: url('/static/icons/shensheshou.svg');
}

.role-icon--senyuzhe {
  -webkit-mask-image: url('/static/icons/senyuzhe.svg');
  mask-image: url('/static/icons/senyuzhe.svg');
}

.role-icon--linghun {
  -webkit-mask-image: url('/static/icons/linghun.svg');
  mask-image: url('/static/icons/linghun.svg');
}

.role-label {
  font-size: 22rpx;
  color: #0b3a67;
  line-height: 1.1;
  text-align: center;
  padding: 0 6rpx;
}
</style>
