# -*- coding: utf-8 -*-
"""
通用本地代理服务器
功能：将本地请求转发到指定的目标网站
支持自定义端口和目标网址
"""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import sys
import os
import threading
import time
import ctypes

# 全局变量
TARGET_URL = ''
PORT = 0
BIND_HOST = '127.0.0.1'

class ProxyHandler(BaseHTTPRequestHandler):
    # 逐跳头和 Host 不转发；Accept-Encoding 交给 requests 接管（自动解压）
    SKIP_HEADERS = {'host', 'connection', 'keep-alive', 'proxy-authenticate',
                    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
                    'upgrade', 'content-length', 'accept-encoding'}

    def _proxy(self, method, include_body):
        # 动态导入 requests，减少启动依赖报错
        import requests
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
                <html><head><meta charset="utf-8"><title>代理错误</title></head>
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
        print(f"[{self.log_date_time_string()}] {format % args}")
        sys.stdout.flush()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    global TARGET_URL, PORT, BIND_HOST

    print("=" * 60)
    print("本地代理服务器 - 通用版")
    print("=" * 60)
    print()
    
    # 1. 获取用户输入
    while True:
        input_url = input("请输入目标网址 (例如 https://github.com/FatFatYoung): ").strip()
        if input_url.startswith(('http://', 'https://')):
            TARGET_URL = input_url.rstrip('/') # 去掉末尾斜杠
            break
        else:
            print("[错误] 网址必须以 http:// 或 https:// 开头")

    while True:
        input_port = input("请输入本地监听端口 (1-65535): ").strip()
        try:
            port_val = int(input_port)
            if 1 <= port_val <= 65535:
                PORT = port_val
                break
            else:
                print("[错误] 端口必须在 1 到 65535 之间")
        except ValueError:
            print("[错误] 端口必须是纯数字")

    while True:
        input_mode = input("监听模式（1=本地 127.0.0.1，2=局域网 0.0.0.0，直接回车=1）: ").strip()
        if input_mode in ('', '1', '2'):
            BIND_HOST = '0.0.0.0' if input_mode == '2' else '127.0.0.1'
            break
        else:
            print("[错误] 请输入 1 或 2（直接回车默认本地模式）")

    print()
    print("-" * 40)
    print(f"目标网站：{TARGET_URL}")
    print(f"监听地址：http://{BIND_HOST}:{PORT}")
    
    # 2. 权限检查（仅针对低端口号）
    if PORT < 1024:
        if not is_admin():
            print(f"[错误] 端口 {PORT} < 1024，需要管理员权限！")
            print("请右键点击程序，选择【以管理员身份运行】。")
            input("按回车键退出...")
            sys.exit(1)
        print("[OK] 管理员权限检查通过")
    else:
        print(f"[OK] 端口 {PORT} > 1024，无需管理员权限")
    
    print("-" * 40)
    print("按 Ctrl+C 停止服务...")
    print("=" * 60)

    # 3. 启动服务器
    try:
        server = ThreadingHTTPServer((BIND_HOST, PORT), ProxyHandler)
        print(f"[OK] 服务启动成功，正在监听 {PORT} 端口...")
        server.serve_forever()
    except OSError as e:
        if e.winerror == 10048:
            print(f"[错误] 端口 {PORT} 已被占用！")
        elif e.winerror == 10013:
            print(f"[错误] 端口 {PORT} 访问被拒绝（可能需要管理员权限）！")
        else:
            print(f"[错误] {str(e)}")
        input("按回车键退出...")
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        server.shutdown()
        print("服务已停止")

if __name__ == '__main__':
    main()
