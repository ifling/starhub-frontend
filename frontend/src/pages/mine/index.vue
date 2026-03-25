<template>
  <view class="page">
    <text class="title">我的</text>
    <text class="desc">这里以后可以放“我的报名”、“个人信息”等内容。</text>
    <view v-if="loggedIn" class="id-box">
      <text class="id-label">用户名</text>
      <text class="id-value">{{ displayName || '—' }}</text>
    </view>
    <view v-else class="id-box id-box--muted">
      <text class="id-label">用户名</text>
      <text class="id-value">未登录</text>
    </view>

    <!-- #ifdef H5 -->
    <view v-if="!loggedIn" class="btn" @click="goLogin">
      <text class="btn-text">用户名登录 / 注册</text>
    </view>
    <view v-else class="btn btn--ghost" @click="logout">
      <text class="btn-text btn-text--dark">退出登录</text>
    </view>
    <!-- #endif -->
  </view>
</template>

<script>
import { clearToken, getDisplayName, isLoggedIn } from '../../utils/auth'

export default {
  name: 'MinePage',
  data() {
    return {
      loggedIn: false,
      displayName: '',
    }
  },
  onShow() {
    this.loggedIn = isLoggedIn()
    this.displayName = getDisplayName()
  },
  methods: {
    goLogin() {
      uni.navigateTo({ url: '/pages/login/index' })
    },
    logout() {
      clearToken()
      this.loggedIn = false
      this.displayName = ''
      uni.showToast({ title: '已退出', icon: 'none' })
    },
  },
}
</script>

<style>
.page {
  padding: 32rpx;
}

.title {
  font-size: 36rpx;
  font-weight: 600;
  margin-bottom: 16rpx;
}

.desc {
  font-size: 28rpx;
  color: #888;
}

.id-box {
  margin-top: 26rpx;
  padding: 20rpx 18rpx;
  border-radius: 16rpx;
  background: #ffffff;
  border: 2rpx solid rgba(0, 0, 0, 0.06);
}

.id-box--muted {
  background: rgba(229, 231, 235, 0.6);
}

.id-label {
  display: block;
  font-size: 24rpx;
  color: rgba(17, 24, 39, 0.6);
  margin-bottom: 10rpx;
}

.id-value {
  display: block;
  font-size: 26rpx;
  color: #111827;
  font-weight: 600;
  word-break: break-all;
}

.btn {
  margin-top: 40rpx;
  height: 88rpx;
  border-radius: 14rpx;
  background: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn--ghost {
  background: #e5e7eb;
}

.btn-text {
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
}

.btn-text--dark {
  color: #111827;
}
</style>

