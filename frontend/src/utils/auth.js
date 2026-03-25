const TOKEN_KEY = 'starhub_access_token'
const PROFILE_KEY = 'starhub_user_profile'

export function getToken() {
  try {
    return uni.getStorageSync(TOKEN_KEY) || ''
  } catch {
    return ''
  }
}

/** @param {Record<string, unknown> | null | undefined} [user] 来自登录接口的 user；传入则写入本地展示信息 */
export function setToken(token, user) {
  uni.setStorageSync(TOKEN_KEY, token || '')
  if (arguments.length < 2) return
  try {
    if (user && typeof user === 'object') {
      uni.setStorageSync(
        PROFILE_KEY,
        JSON.stringify({
          id: user.id,
          channel: user.channel,
          username: user.username || '',
          email: user.email || '',
        })
      )
    } else {
      uni.removeStorageSync(PROFILE_KEY)
    }
  } catch {
    // ignore
  }
}

export function clearToken() {
  try {
    uni.removeStorageSync(TOKEN_KEY)
  } catch {
    uni.setStorageSync(TOKEN_KEY, '')
  }
  try {
    uni.removeStorageSync(PROFILE_KEY)
  } catch {
    // ignore
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

function getStoredProfile() {
  try {
    const raw = uni.getStorageSync(PROFILE_KEY)
    if (!raw) return null
    return JSON.parse(raw)
  } catch {
    return null
  }
}

/** 「我的」等展示用：用户名 / 邮箱 / 渠道昵称；不含用户 ID */
export function getDisplayName() {
  const p = getStoredProfile()
  if (p) {
    if (p.username) return String(p.username)
    if (p.email) return String(p.email)
    if (p.channel === 'weixin_mp') return '微信用户'
    if (p.channel === 'qq_mp') return 'QQ 用户'
    if (p.channel === 'web') return '用户'
  }
  const payload = decodeJwtPayload(getToken())
  if (!payload) return ''
  if (payload.username) return String(payload.username)
  const ch = payload.channel
  if (ch === 'weixin_mp') return '微信用户'
  if (ch === 'qq_mp') return 'QQ 用户'
  if (ch === 'web') return '用户'
  return ''
}
