/**
 * 未升级的远端仍使用「邮箱注册」接口（请求体必填 email）。
 * 对仅含英文、数字、下划线的用户名附带合成邮箱，旧服务可识别 email；新服务只认 username，并忽略 email。
 * 含中文等字符的用户名无法生成合法本地部分，必须升级后端为「用户名注册」接口。
 */
const LEGACY_EMAIL_DOMAIN = 'web.starhub.local'
const ASCII_USERNAME = /^[a-zA-Z0-9_]{3,32}$/

export function webAuthBody(username, password) {
  const u = (username || '').trim()
  const body = { username: u, password }
  if (ASCII_USERNAME.test(u)) {
    body.email = `${u}@${LEGACY_EMAIL_DOMAIN}`
  }
  return body
}
