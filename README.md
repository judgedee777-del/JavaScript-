# 电商搜索工具

跨平台电商商品搜索工具，支持京东、淘宝、拼多多三大电商平台。

## 功能特性

- 🛒 **多平台支持** - 京东、淘宝、拼多多一键切换
- 🔍 **关键词搜索** - 输入商品名称或品牌搜索
- 🎨 **现代化 UI** - 借鉴 Shopify 设计语言的深色主题界面
- ⚡ **快速响应** - Python 调用 JS 处理签名，直接返回搜索结果

## 技术栈

- **桌面应用** - Electron
- **前端** - HTML + CSS + JavaScript
- **后端** - Node.js 调用 Python 脚本
- **签名处理** - Python 调用各平台 JS 签名文件

## 目录结构

```
├── src/
│   ├── main/
│   │   ├── index.js      # Electron 主进程
│   │   └── search.js     # 搜索调度器
│   ├── preload.js        # 预加载脚本
│   └── renderer/
│       ├── index.html    # 页面
│       ├── renderer.js   # 前端逻辑
│       └── styles.css    # 样式
├── sources/              # 各平台签名源文件（需自行配置）
│   ├── jd/              # 京东
│   ├── tb/              # 淘宝
│   └── pdd/             # 拼多多
└── userData/            # 用户数据目录
```

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置平台签名文件

从原始分析目录复制以下文件到 `sources/` 对应目录：

**京东 (sources/jd/)**
- `env.js`
- `produre.js`

**淘宝 (sources/tb/)**
- `分析.js`

**拼多多 (sources/pdd/)**
- `env.js`
- `pack.js`

> 注意：这些文件包含敏感签名逻辑，请勿提交到仓库

### 3. 启动应用

```bash
npm start
```

### 4. 打包构建

```bash
npm run build
```

## 平台说明

| 平台 | 状态 | 说明 |
|------|------|------|
| 京东 | ✅ 可用 | 内置 cookie，需定期更新 |
| 淘宝 | ✅ 可用 | 内置 cookie，需定期更新 |
| 拼多多 | ⚠️ 需配置 | anti_content 动态生成，需配置环境 |

## 注意事项

- `sources/` 目录下的文件包含敏感信息，已通过 `.gitignore` 排除
- `userData/` 目录用于存储用户数据，不会上传到仓库
- 各平台 cookie 会有时效性，如搜索失败请更新对应平台的 cookie

## License

MIT
