# CHANGELOG

## [1.0.1.0] - 2026-11-21

### 🔒 Security & Robustness
- **Threading server**: switched to `ThreadingHTTPServer`; concurrent requests no longer block each other and slow clients can no longer stall the service.
- **Request header forwarding**: browser headers (Cookie, User-Agent, Authorization, etc.) are now forwarded to the target (hop-by-hop headers stripped).
- **Error pages no longer expose exception details**; details go to the server-side log only.

### 🐛 Fixes
- **Request body forwarding**: POST/PUT/PATCH/DELETE bodies are now read and forwarded instead of being silently dropped.
- **Response `Content-Length`**: sent with the correct value instead of being stripped.
- **HEAD**: responses no longer carry a body.
- **Rule changes take effect immediately**: editing a rule hot-updates the running proxy target (no restart); a port change migrates & rebuilds the proxy; deleting a rule stops its proxy.

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
