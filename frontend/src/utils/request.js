import { API_BASE_URL } from './config'
import { clearToken, getToken } from './auth'

export function request(path, options = {}) {
  const url = path.startsWith('http') ? path : `${API_BASE_URL}${path.startsWith('/') ? '' : '/'}${path}`
  const token = getToken()
  const method = (options.method || 'GET').toUpperCase()
  const headers = { ...(options.header || {}) }
  if (method !== 'GET' && method !== 'DELETE' && !headers['Content-Type'] && !headers['content-type']) {
    headers['Content-Type'] = 'application/json'
  }
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url,
      method: options.method || 'GET',
      data: options.data,
      header: headers,
      timeout: options.timeout || 15000,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
          return
        }
        if (res.statusCode === 401) {
          clearToken()
          // #ifdef H5
          const pages = getCurrentPages()
          const cur = pages[pages.length - 1]
          const route = cur && cur.route ? cur.route : ''
          if (route && !route.includes('pages/login')) {
            uni.showToast({ title: '请先登录', icon: 'none' })
            uni.navigateTo({ url: '/pages/login/index' })
          }
          // #endif
        }
        reject(res)
      },
      fail: reject,
    })
  })
}
