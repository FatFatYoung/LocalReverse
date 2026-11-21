# LocalReverse - Visual Local Reverse Proxy

A lightweight, visual local reverse proxy tool designed for Windows users.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

## ✨ Why LocalReverse?

In local development, we often run into these pain points:
- **CORS issues**: Front-end calls to back-end APIs get blocked by the browser.
- **Port mismatch**: The back-end runs on `8000`, but the front-end can only call `80`.
- **HTTPS debugging**: Many services only allow HTTPS callbacks, while local development uses `http://localhost`.

LocalReverse works like a **traffic commander**: it quietly forwards requests sent to `localhost:any-port` to any address you choose (your dev server, an external API, or a test environment) — **with no browser proxy extensions required**.

## 🚀 Key Features

- **🖥️ Graphical Interface (GUI)**: No black windows or command lines — just point and click.
- **⚡️ Real-Time Changes**: Add or modify rules and they apply immediately, no service restart needed.
- **🔄 Multiple Rules in Parallel**: Listen on multiple local ports at once, forwarding to different targets.
- **🌐 CORS Problem Solver**: Effortlessly resolve CORS errors in local development.
- **🌍 Bilingual UI**: Switch between Chinese and English with one click.
- **🔌 Listen Mode Switch**: Listens on localhost (127.0.0.1) by default; switch to LAN mode (0.0.0.0) with one click so other devices on the same LAN can access it too.

## 📖 Quick Start

### Option 1: Precompiled EXE (Recommended)
1. Download `LocalReverse.exe` from [Releases](https://github.com/FatFatYoung/LocalReverse/releases).
2. Double-click to run.
3. Add a rule and click "Start All Services".

### Option 2: Run from Source
```bash
git clone https://github.com/FatFatYoung/LocalReverse.git
cd LocalReverse
pip install requests
python main.py
```

## 🛠️ Usage Examples

### Scenario 1: Fixing CORS
- **Your front-end**: `http://localhost:3000`
- **Your back-end**: `http://192.168.1.100:8080` (no CORS headers configured)
- **LocalReverse setup**:
    - Local port: `8080`
    - Target URL: `http://192.168.1.100:8080`
- **Result**: The front-end requests `http://localhost:8080/api/user`, LocalReverse forwards it to the back-end, and the browser treats it as a same-origin request — no more blocking!

### Scenario 2: Simulating the Production Environment
- You want to test callbacks to `https://api.example.com`, but locally you only have `http`.
- **Setup**: Listen on local port `80` or `443` (requires administrator privileges) and forward to `https://api.example.com`.

## 📁 Project Structure

```text
LocalReverse/
├── main.py           # Core GUI application
├── i18n.py           # Internationalization module
├── proxy.py          # Generic command-line version (optional)
├── demo.py           # Port 80 quick demo (optional)
├── build.bat         # Build script (Windows)
└── config.json       # Configuration file
```

## ⚙️ Advanced: Command-Line Versions

If you prefer the command line, the project includes two scripts:
- `proxy.py`: Generic version — prompts for the port and target URL at startup.
- `demo.py`: Demo version — forwards `localhost:80` straight to the GitHub homepage (requires administrator privileges).

## 🤝 Contributing & Feedback

Issues and Pull Requests are welcome!

- GitHub: [@FatFatYoung](https://github.com/FatFatYoung)

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

For third-party open-source component notices, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
