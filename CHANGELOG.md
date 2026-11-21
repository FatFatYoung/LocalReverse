# CHANGELOG

## [1.0.1.0] - 2026-11-21

### ✨ Features
- **Listen mode switch**: GUI toggle / `listen_mode` config field switches between local (`127.0.0.1`) and LAN (`0.0.0.0`) listening; running proxies rebind immediately.

### 🔒 Security & Robustness
- **Threading server**: switched to `ThreadingHTTPServer`; concurrent requests no longer block each other and slow clients can no longer stall the service.
- **Request header forwarding**: browser headers (Cookie, User-Agent, Authorization, etc.) are now forwarded to the target (hop-by-hop headers stripped).
- **Error pages no longer expose exception details**; details go to the server-side log only.

### 🐛 Fixes
- **Request body forwarding**: POST/PUT/PATCH/DELETE bodies are now read and forwarded instead of being silently dropped.
- **Response `Content-Length`**: sent with the correct value instead of being stripped.
- **HEAD**: responses no longer carry a body.
- **Rule changes take effect immediately**: editing a rule hot-updates the running proxy target (no restart); a port change migrates & rebuilds the proxy; deleting a rule stops its proxy.
- **Mode switch cannot fail partially or silently**: malformed rules (missing `target_url`, numeric/string port mismatch) are skipped with an error log instead of aborting the switch mid-way; every proxy start logs its actual bound address so the active listen mode is visible in the GUI log.

## [1.0.0] - 2026-05-10

### ✨ Initial Release
- **GUI Interface**: Full-featured Tkinter interface for managing reverse proxy rules.
- **Multi-Rule Support**: Map multiple local ports to different target URLs simultaneously.
- **i18n**: Support for Chinese and English.
- **Dynamic Rules**: Add, edit, or disable rules without restarting the service.

### 📦 Included Tools
- `main.py`: The main GUI application.
- `proxy.py`: Command-line generic version.
- `demo.py`: One-click demo (Port 80 -> GitHub).
