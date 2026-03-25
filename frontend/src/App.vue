<script>
import { request } from './utils/request'
import { getToken, setToken } from './utils/auth'

export default {
  onLaunch() {
    // #ifdef MP-WEIXIN
    if (!getToken()) {
      uni.login({
        provider: 'weixin',
        success: (res) => {
          if (!res.code) return
          request('/auth/weixin/mp', { method: 'POST', data: { code: res.code } })
            .then((data) => {
              if (data && data.access_token) setToken(data.access_token, data.user)
            })
            .catch((e) => {
              console.warn('WeChat silent login failed', e)
            })
        },
        fail: (e) => console.warn('uni.login weixin', e),
      })
    }
    // #endif
    // #ifdef MP-QQ
    if (!getToken()) {
      uni.login({
        success: (res) => {
          if (!res.code) return
          request('/auth/qq/mp', { method: 'POST', data: { code: res.code } })
            .then((data) => {
              if (data && data.access_token) setToken(data.access_token, data.user)
            })
            .catch((e) => {
              console.warn('QQ silent login failed', e)
            })
        },
        fail: (e) => console.warn('uni.login qq', e),
      })
    }
    // #endif
  },
  onShow() {},
  onHide() {},
}
</script>

<style>
/*每个页面公共css */
page {
  background-color: #f6f7fb;
  color: #111827;
}

view,
text {
  box-sizing: border-box;
}
</style>
