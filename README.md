# LocalReverse - 本地反向代理工具 (Visual Local Reverse Proxy)

一个轻量级、可视化的本地反向代理工具，专为 Windows 用户设计。

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

## ✨ 为什么需要 LocalReverse？

在本地开发中，我们经常遇到以下痛点：
- **跨域问题 (CORS)**: 前端调用后端 API 被浏览器拦截。
- **端口不一致**: 后端跑在 `8000`，前端却只能调 `80`。
- **调试 HTTPS**: 很多服务只允许 HTTPS 回调，本地却是 `http://localhost`。

LocalReverse 就像一个**交通指挥官**，帮你把发往 `localhost:任意端口` 的请求，悄悄转发到你想去的任何地址（比如你的开发服务器、外部 API 或测试环境），**完全不需要在浏览器里配置代理插件**。

## 🚀 核心特性

- **🖥️ 图形化界面 (GUI)**: 告别黑窗口和命令行，点点鼠标即可完成配置。
- **⚡️ 实时生效**: 添加或修改规则后，无需重启服务即可应用。
- **🔄 多规则并行**: 同时监听多个端口，转发到不同的目标网址。
- **🌐 跨域神器**: 轻松解决本地开发环境的 CORS 报错。
- **🌍 中英双语**: 支持一键切换界面语言。

## 📖 快速开始

### 方法一：使用预编译 EXE (推荐)
1. 从 [Releases](https://github.com/FatFatYoung/LocalReverse/releases) 下载 `LocalReverse.exe`。
2. 双击运行。
3. 添加规则，点击“启动所有服务”。

### 方法二：源码运行
```bash
git clone https://github.com/FatFatYoung/LocalReverse.git
cd LocalReverse
pip install requests
python main.py
```

## 🛠️ 使用场景示例

### 场景 1：解决跨域 (CORS)
- **你的前端**: `http://localhost:3000`
- **你的后端**: `http://192.168.1.100:8080` (没有配置 CORS 头)
- **LocalReverse 设置**:
    - 本地端口: `8080`
    - 目标网址: `http://192.168.1.100:8080`
- **结果**: 前端请求 `http://localhost:8080/api/user`，LocalReverse 帮你转发到后端，浏览器以为是你自己发的，不再拦截！

### 场景 2：模拟生产环境
- 你想测试 `https://api.example.com` 的回调，但本地是 `http`。
- **设置**: 监听本地 `80` 或 `443` 端口（需管理员权限），转发到 `https://api.example.com`。

## 📁 项目结构

```text
LocalReverse/
├── main.py           # 核心 GUI 主程序
├── i18n.py           # 国际化模块
├── proxy.py          # 命令行通用版 (可选)
├── demo.py           # 80 端口快速演示版 (可选)
├── build.bat         # 打包脚本 (Windows)
└── config.json       # 配置文件
```

## ⚙️ 进阶：命令行版本

如果你喜欢命令行，项目中也包含了两个脚本：
- `proxy.py`: 通用版，启动时提示输入端口和网址。
- `demo.py`: 演示版，直接将 `localhost:80` 转发到 GitHub 主页（需管理员权限）。

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request！

- GitHub: [@FatFatYoung](https://github.com/FatFatYoung)

## 📄 许可证

本项目采用 MIT License - 详见 [LICENSE](LICENSE) 文件。

第三方开源组件声明请参见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
