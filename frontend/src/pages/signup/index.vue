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
          <view class="signup-pair">
            <view class="signup-icon"></view>
            <text class="signup-count">{{ signupCount }}</text>
          </view>
        </view>
        <view class="quick-row">
          <view class="quick-item">
            <view class="quick-icon quick-icon--tank"></view>
            <text class="quick-num">0</text>
          </view>
          <view class="quick-item">
            <view class="quick-icon quick-icon--healer"></view>
            <text class="quick-num">0</text>
          </view>
          <view class="quick-item">
            <view class="quick-icon quick-icon--dps"></view>
            <text class="quick-num">0</text>
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
        v-for="tab in tabs"
        :key="tab.key"
        class="action-btn"
        :class="{ 'action-btn--active': activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </view>

    <view class="content">
      <view v-if="loading" class="placeholder">加载中...</view>
      <view v-else-if="activeTab === 'intro'" class="placeholder">
        {{ activity.desc || '暂无简介。' }}
      </view>
      <view v-else-if="activeTab === 'limit'" class="placeholder">限制信息暂未接入。</view>
      <view v-else-if="activeTab === 'log'" class="placeholder">日志暂未接入。</view>
      <view v-else class="placeholder">尚无玩家报名。</view>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  name: 'SignupPage',
  data() {
    return {
      activityId: '',
      loading: false,
      activeTab: 'signup',
      tabs: [
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
      },
      signupCount: 0,
    }
  },
  onLoad(query) {
    this.activityId = query && query.activityId ? String(query.activityId) : ''
    this.reload()
  },
  methods: {
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
        this.signupCount = Array.isArray(signups) ? signups.length : 0
      } catch (e) {
        uni.showToast({ title: '加载失败', icon: 'none' })
      } finally {
        this.loading = false
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
  justify-content: flex-start;
}

.created-type {
  font-size: 30rpx;
  color: #111827;
}

.signup-pair {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-left: 12rpx;
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

.quick-row {
  display: flex;
  align-items: center;
  gap: 14rpx;
  margin-top: 10rpx;
}

.quick-item {
  display: flex;
  align-items: center;
  gap: 6rpx;
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
  color: #334155;
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
</style>
