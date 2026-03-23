const TOKEN_KEY = 'starhub_access_token'

export function getToken() {
  try {
    return uni.getStorageSync(TOKEN_KEY) || ''
  } catch {
    return ''
  }
}

export function setToken(token) {
  uni.setStorageSync(TOKEN_KEY, token || '')
}

export function clearToken() {
  try {
    uni.removeStorageSync(TOKEN_KEY)
  } catch {
    uni.setStorageSync(TOKEN_KEY, '')
  }
}

export function isLoggedIn() {
  return !!getToken()
}
