import { API_BASE_URL } from './config'

function getClientId() {
  const key = 'starhub_client_id'
  let cid = uni.getStorageSync(key)
  if (cid) return cid
  cid = `c_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`
  uni.setStorageSync(key, cid)
  return cid
}

export function request(path, options = {}) {
  const url = path.startsWith('http') ? path : `${API_BASE_URL}${path.startsWith('/') ? '' : '/'}${path}`
  const headers = { ...(options.header || {}), 'X-Client-Id': getClientId() }

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
        reject(res)
      },
      fail: reject,
    })
  })
}

