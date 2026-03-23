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

function base64UrlDecode(input) {
  // base64url -> base64
  const b64 = input.replace(/-/g, '+').replace(/_/g, '/')
  const pad = b64.length % 4 === 0 ? '' : '='.repeat(4 - (b64.length % 4))
  const normalized = b64 + pad
  if (typeof atob !== 'function') return null
  const str = atob(normalized)
  // handle UTF-8 safely (H5/MP JS runtime 可能不完全一致)
  try {
    return decodeURIComponent(
      Array.prototype.map
        .call(str, (c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
  } catch {
    return str
  }
}

function decodeJwtPayload(token) {
  if (!token || typeof token !== 'string') return null
  const parts = token.split('.')
  if (parts.length < 2) return null
  const payloadStr = base64UrlDecode(parts[1])
  if (!payloadStr) return null
  try {
    return JSON.parse(payloadStr)
  } catch {
    return null
  }
}

export function getUserIdFromToken() {
  const token = getToken()
  const payload = decodeJwtPayload(token)
  if (!payload || !payload.sub) return ''
  return String(payload.sub)
}
