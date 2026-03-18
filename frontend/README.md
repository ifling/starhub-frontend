# StarHub Frontend / 集合石前端

基于 [uni-app](https://uniapp.dcloud.net.cn/) + Vue 3 + Vite 的跨端前端项目，面向魔兽世界等游戏的**团队副本报名 / 集合石**场景。

## 技术栈

- **框架**: uni-app 3.x
- **前端**: Vue 3、Vite 5
- **多端**: 微信小程序、H5、支付宝小程序等（按需配置）

## 功能概览

- **首页**: 工具入口，包含「集合石」报名功能入口
- **集合石**: 活动管理
  - **我创建的**: 创建活动、搜索、时间排序、隐藏过期
  - **模板**: 创建/导入活动模板
  - **我参与的**: 查看已报名活动
  - **直达**: 输入活动码直达报名页
  - 创建活动时可填写：标题、类型（副本/PVP/其他）、报名截止日期与时间、限制转发、限制一人多报、活动描述等
- **消息**: 消息通知（占位）
- **我的**: 个人中心（占位）

## 本地开发

### 环境要求

- Node.js 16+
- npm 或 pnpm

### 安装依赖

```bash
npm install
```

### 运行

| 命令 | 说明 |
|------|------|
| `npm run dev:h5` | H5 开发 |
| `npm run dev:mp-weixin` | 微信小程序开发 |
| `npm run dev:mp-alipay` | 支付宝小程序开发 |

### 构建

```bash
# H5 构建
npm run build:h5

# 微信小程序构建
npm run build:mp-weixin
```

构建产物在 `dist/` 下对应子目录（如 `dist/build/h5`、`dist/build/mp-weixin`）。

## 项目结构（简要）

```
├── src/
│   ├── pages/           # 页面
│   │   ├── index/       # 首页
│   │   ├── message/     # 消息
│   │   ├── mine/        # 我的
│   │   └── stone/       # 集合石（活动/报名）
│   ├── App.vue
│   ├── main.js
│   ├── pages.json
│   ├── manifest.json
│   └── uni.scss
├── static/              # 静态资源（如图标）
├── index.html
├── vite.config.js
└── package.json
```

## 仓库

- GitHub: [https://github.com/ifling/starhub-frontend](https://github.com/ifling/starhub-frontend)

## License

MIT
