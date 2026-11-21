# -*- coding: utf-8 -*-
"""
本地代理演示版 (Demo)
功能：将本地 80 端口请求直接转发到 https://github.com/FatFatYoung
用途：演示如何无需修改浏览器地址栏即可通过 localhost 访问特定网站
注意：必须使用管理员权限运行（因为占用 80 端口）
"""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import requests
import sys
import ctypes

# --- 核心配置 ---
TARGET_URL = 'https://github.com/FatFatYoung'
LISTEN_PORT = 80
# ----------------

class ProxyHandler(BaseHTTPRequestHandler):
    # 逐跳头和 Host 不转发；Accept-Encoding 交给 requests 接管（自动解压）
    SKIP_HEADERS = {'host', 'connection', 'keep-alive', 'proxy-authenticate',
                    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
                    'upgrade', 'content-length', 'accept-encoding'}

    def _proxy(self, method, include_body):
        # 1. 构建目标 URL
        target = f"{TARGET_URL}{self.path}"
        try:
            # 2. 转发浏览器请求头和请求体到目标网站
            fwd = {k: v for k, v in self.headers.items() if k.lower() not in self.SKIP_HEADERS}
            length = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(length) if length > 0 else None
            resp = requests.request(method, target, headers=fwd, data=body,
                                    allow_redirects=False, timeout=30)
            # 3. 将服务器的响应返回给浏览器
            self.send_response(resp.status_code)
            for name, value in resp.headers.items():
                if name.lower() not in ['content-encoding', 'transfer-encoding', 'content-length']:
                    self.send_header(name, value)
            if include_body:
                self.send_header('Content-Length', str(len(resp.content)))
                self.end_headers()
                self.wfile.write(resp.content)
            else:
                # HEAD：沿用上游声明的长度（HEAD 响应体恒为空，不能用 len(content)）
                self.send_header('Content-Length', resp.headers.get('Content-Length') or '0')
                self.end_headers()
        except Exception as e:
            # 异常详情只进服务端日志，不回显给浏览器
            print(f"[{self.log_date_time_string()}] [错误] {method} {self.path} - {type(e).__name__}: {e}")
            sys.stdout.flush()
            try:
                self.send_response(502)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                error_html = f"""
                <!DOCTYPE html>
                <html><head><meta charset="utf-8"><title>代理演示错误</title></head>
                <body style="font-family:Microsoft YaHei;padding:50px;">
                <h1 style="color:red;">代理错误</h1>
                <p>请求地址：{target}</p>
                <p>无法连接目标网站，请检查目标网址或网络。</p>
                </body></html>
                """.encode('utf-8')
                self.wfile.write(error_html)
            except Exception:
                pass

    def do_GET(self):
        self._proxy('GET', True)

    def do_POST(self):
        self._proxy('POST', True)

    def do_PUT(self):
        self._proxy('PUT', True)

    def do_PATCH(self):
        self._proxy('PATCH', True)

    def do_DELETE(self):
        self._proxy('DELETE', True)

    def do_HEAD(self):
        self._proxy('HEAD', False)
    
    def log_message(self, format, *args):
        # 在控制台输出日志
        print(f"[{self.log_date_time_string()}] {format % args}")
        sys.stdout.flush()

def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    print("=" * 60)
    print("本地代理演示版 (Demo) -> 80 端口")
    print("=" * 60)
    print()
    print(f"目标网站：{TARGET_URL}")
    print(f"本地地址：http://127.0.0.1 (端口 80)")
    print()
    
    # 检查管理员权限
    if not is_admin():
        print("[错误] 需要使用管理员权限运行（80 端口需要管理员权限）")
        print()
        print("解决方法：")
        print("  1. 右键点击本程序")
        print("  2. 选择「以管理员身份运行」")
        print()
        input("按回车键退出...")
        sys.exit(1)
    
    print("[OK] 管理员权限检查通过")
    print("正在监听 80 端口...")
    print("在浏览器访问 http://127.0.0.1 即可看到 GitHub 主页")
    print()
    print("按 Ctrl+C 停止服务...")
    print("=" * 60)

    try:
        # 绑定 80 端口
        server = ThreadingHTTPServer(('127.0.0.1', LISTEN_PORT), ProxyHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        server.shutdown()
        print("服务已停止")
    except OSError as e:
        print(f"[错误] 无法启动：{e}")
        input("按回车键退出...")

if __name__ == '__main__':
    main()
