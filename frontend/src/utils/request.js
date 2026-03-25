import { API_BASE_URL } from './config'
import { clearToken, getToken } from './auth'

/** Uni-app H5 对 JSON 请求体常需手动序列化，否则后端收不到字段会返回 422 */
function prepareRequestData(method, headers, data) {
  const m = method.toUpperCase()
  if (data == null || m === 'GET' || m === 'HEAD') return data
  const ct = String(headers['Content-Type'] || headers['content-type'] || '').toLowerCase()
  if (!ct.includes('application/json')) return data
  if (typeof data !== 'object') return data
  if (data instanceof ArrayBuffer) return data
  if (typeof FormData !== 'undefined' && data instanceof FormData) return data
  return JSON.stringify(data)
}

export function formatApiError(res) {
  const d = res.data && res.data.detail
  if (Array.isArray(d)) {
    return d
      .map((x) => {
        const loc = Array.isArray(x.loc) ? x.loc.filter((p) => p !== 'body').join('.') : ''
        const msg = x.msg != null ? String(x.msg) : JSON.stringify(x)
        return loc ? `${loc}: ${msg}` : msg
      })
      .join('; ')
  }
  if (d != null && typeof d === 'object') return JSON.stringify(d)
  if (d != null) return String(d)
  return '请求失败'
}

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

  const data = prepareRequestData(method, headers, options.data)

  return new Promise((resolve, reject) => {
    uni.request({
      url,
      method: options.method || 'GET',
      data,
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
