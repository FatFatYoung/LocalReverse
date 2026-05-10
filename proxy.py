# -*- coding: utf-8 -*-
"""
通用本地代理服务器
功能：将本地请求转发到指定的目标网站
支持自定义端口和目标网址
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os
import threading
import time
import ctypes

# 全局变量
TARGET_URL = ''
PORT = 0
SECRET_HEADER = {'X-Local-Proxy': 'MyFatYoungSSSagent'}

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 动态导入 requests，减少启动依赖报错
        import requests
        # 1. 构建目标 URL
        target = f"{TARGET_URL}{self.path}"
        try:
            # 2. 带着暗号头转发请求
            resp = requests.get(target, headers=SECRET_HEADER, allow_redirects=False, timeout=30)
            
            # 3. 将服务器的响应返回给浏览器
            self.send_response(resp.status_code)
            for name, value in resp.headers.items():
                if name.lower() not in ['content-encoding', 'transfer-encoding', 'content-length']:
                    self.send_header(name, value)
            self.end_headers()
            self.wfile.write(resp.content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            error_html = f"""
            <!DOCTYPE html>
            <html><head><meta charset="utf-8"><title>代理错误</title></head>
            <body style="font-family:Microsoft YaHei;padding:50px;">
            <h1 style="color:red;">代理错误</h1>
            <p>请求地址：{target}</p>
            <p>错误信息：{str(e)}</p>
            </body></html>
            """.encode('utf-8')
            self.wfile.write(error_html)
    
    def do_POST(self):
        self.do_GET()
    
    def do_HEAD(self):
        self.do_GET()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")
        sys.stdout.flush()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    global TARGET_URL, PORT

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

    print()
    print("-" * 40)
    print(f"目标网站：{TARGET_URL}")
    print(f"监听地址：http://127.0.0.1:{PORT}")
    
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
        server = HTTPServer(('127.0.0.1', PORT), ProxyHandler)
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
