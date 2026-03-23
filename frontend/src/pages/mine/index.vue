<template>
  <view class="page">
    <text class="title">我的</text>
    <text class="desc">这里以后可以放“我的报名”、“个人信息”等内容。</text>
    <!-- #ifdef H5 -->
    <view v-if="!loggedIn" class="btn" @click="goLogin">
      <text class="btn-text">邮箱登录 / 注册</text>
    </view>
    <view v-else class="btn btn--ghost" @click="logout">
      <text class="btn-text btn-text--dark">退出登录</text>
    </view>
    <!-- #endif -->
  </view>
</template>

<script>
import { clearToken, isLoggedIn } from '../../utils/auth'

export default {
  name: 'MinePage',
  data() {
    return {
      loggedIn: false,
    }
  },
  onShow() {
    // #ifdef H5
    this.loggedIn = isLoggedIn()
    // #endif
  },
  methods: {
    goLogin() {
      uni.navigateTo({ url: '/pages/login/index' })
    },
    logout() {
      clearToken()
      this.loggedIn = false
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

