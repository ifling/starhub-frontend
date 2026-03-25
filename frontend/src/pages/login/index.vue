<template>
  <view class="page">
    <view class="segment">
      <view
        class="seg-item"
        :class="{ 'seg-item--active': mode === 'login' }"
        @click="mode = 'login'"
      >
        <text class="seg-text">登录</text>
      </view>
      <view
        class="seg-item"
        :class="{ 'seg-item--active': mode === 'register' }"
        @click="mode = 'register'"
      >
        <text class="seg-text">注册</text>
      </view>
    </view>

    <view class="card">
      <view class="field">
        <text class="label">用户名</text>
        <input
          class="input"
          v-model="username"
          type="text"
          placeholder="3-32 位字母、数字、下划线或中文"
          placeholder-class="ph"
        />
      </view>
      <view class="field">
        <text class="label">密码</text>
        <input
          class="input"
          v-model="password"
          password
          placeholder="至少 8 位"
          placeholder-class="ph"
        />
      </view>
      <view v-if="mode === 'register'" class="field">
        <text class="label">确认密码</text>
        <input
          class="input"
          v-model="password2"
          password
          placeholder="再次输入密码"
          placeholder-class="ph"
        />
      </view>

      <view class="btn" @click="onSubmit">
        <text class="btn-text">{{ mode === 'login' ? '登录' : '注册' }}</text>
      </view>
    </view>

    <text class="tip">网页端使用用户名注册；微信 / QQ 小程序请使用各端一键登录。</text>
  </view>
</template>

<script>
import { formatApiError, request } from '../../utils/request'
import { webAuthBody } from '../../utils/webAuth'
import { setToken } from '../../utils/auth'

export default {
  data() {
    return {
      mode: 'login',
      username: '',
      password: '',
      password2: '',
    }
  },
  methods: {
    toast(title) {
      uni.showToast({ title, icon: 'none' })
    },
    async onSubmit() {
      const username = (this.username || '').trim()
      const password = this.password || ''
      if (!username || !password) {
        this.toast('请填写用户名和密码')
        return
      }
      if (this.mode === 'register') {
        if (password.length < 8) {
          this.toast('密码至少 8 位')
          return
        }
        if (password !== this.password2) {
          this.toast('两次密码不一致')
          return
        }
        uni.showLoading({ title: '注册中', mask: true })
        let ok = false
        let errMsg = null
        try {
          const data = await request('/auth/web/register', {
            method: 'POST',
            data: webAuthBody(username, password),
          })
          setToken(data.access_token)
          ok = true
        } catch (e) {
          errMsg = formatApiError(e)
        } finally {
          uni.hideLoading()
        }
        if (errMsg) {
          this.toast(errMsg)
          return
        }
        if (ok) {
          this.toast('注册成功')
          setTimeout(() => uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/index/index' }) }), 300)
        }
        return
      }

      uni.showLoading({ title: '登录中', mask: true })
      let loginOk = false
      let loginErr = null
      try {
        const data = await request('/auth/web/login', {
          method: 'POST',
          data: webAuthBody(username, password),
        })
        setToken(data.access_token)
        loginOk = true
      } catch (e) {
        loginErr = formatApiError(e)
      } finally {
        uni.hideLoading()
      }
      if (loginErr) {
        this.toast(loginErr)
        return
      }
      if (loginOk) {
        this.toast('登录成功')
        setTimeout(() => uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/index/index' }) }), 300)
      }
    },
  },
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  padding: 40rpx 32rpx;
  background: #f6f7fb;
}
.segment {
  display: flex;
  flex-direction: row;
  background: #e5e7eb;
  border-radius: 16rpx;
  padding: 6rpx;
  margin-bottom: 32rpx;
}
.seg-item {
  flex: 1;
  padding: 20rpx 0;
  align-items: center;
  justify-content: center;
  border-radius: 12rpx;
}
.seg-item--active {
  background: #fff;
}
.seg-text {
  font-size: 28rpx;
  color: #111827;
}
.card {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx;
  border: 2rpx solid rgba(0, 0, 0, 0.06);
}
.field {
  margin-bottom: 24rpx;
}
.label {
  display: block;
  font-size: 24rpx;
  color: #6b7280;
  margin-bottom: 10rpx;
}
.input {
  height: 80rpx;
  padding: 0 20rpx;
  background: #f3f4f6;
  border-radius: 12rpx;
  font-size: 28rpx;
}
.ph {
  color: #9ca3af;
}
.btn {
  margin-top: 16rpx;
  height: 88rpx;
  border-radius: 14rpx;
  background: #10b981;
  align-items: center;
  justify-content: center;
  display: flex;
}
.btn-text {
  color: #fff;
  font-size: 30rpx;
  font-weight: 700;
}
.tip {
  display: block;
  margin-top: 28rpx;
  font-size: 24rpx;
  color: #9ca3af;
  line-height: 40rpx;
}
</style>
