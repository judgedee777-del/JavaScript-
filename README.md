# 电商搜索工具

![App Screenshot](https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/ccv2%2F2026-05-07%2FMiniMax-M2.7-highspeed%2F2036601842686763899%2F2368fc2797159ab97460b2d68b14e27336ad4275ab495bd8fb22791da6643b5c..png?Expires=1778227089&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=o1dGd1vTkPwKMiJ4iGVOmEIpNjA%3D)

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

## 平台说明

| 平台 | 状态 | 说明 |
|------|------|------|
| 京东 | ✅ 可用 | 内置 cookie，需定期更新 |
| 淘宝 | ✅ 可用 | 内置 cookie，需定期更新 |
| 拼多多 | ⚠️ 需配置 | anti_content 动态生成，需配置环境 |

## 配置说明

`sources/` 目录下的文件包含敏感签名逻辑，请勿提交到仓库。

## License

MIT
