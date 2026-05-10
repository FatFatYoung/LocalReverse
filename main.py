# -*- coding: utf-8 -*-
"""
LocalReverse - 本地反向代理可视化管理工具 (V1.0)
支持自定义映射规则（本地端口 -> 目标网址），支持多规则并行
支持中英双语切换，移除系统托盘，纯窗口交互
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import requests
import sys
import os
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# 导入国际化模块
try:
    from i18n import i18n
except ImportError:
    class DummyI18n:
        def t(self, key, **kwargs): return key
        def switch(self): return 'zh'
        def get_current(self): return 'zh'
        def save_lang(self): pass
    i18n = DummyI18n()

# 配置文件
CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    'rules': []
}


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 忽略 favicon.ico 请求
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        
        target = f"{self.server.target_url}{self.path}"
        try:
            resp = requests.get(target, allow_redirects=False, timeout=30)
            
            self.send_response(resp.status_code)
            
            # 禁用浏览器缓存
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            
            for name, value in resp.headers.items():
                if name.lower() not in ['content-encoding', 'transfer-encoding', 'content-length', 'cache-control', 'pragma', 'expires']:
                    self.send_header(name, value)
            self.end_headers()
            self.wfile.write(resp.content)
            
            if hasattr(self.server, 'log_callback'):
                self.server.log_callback(f"[{datetime.now().strftime('%H:%M:%S')}] [{self.server.local_port}] GET {self.path} -> {resp.status_code}")
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-store, no-cache')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                error_html = f"<html><body><h1>代理错误</h1><p>{str(e)}</p></body></html>".encode('utf-8')
                self.wfile.write(error_html)
            except:
                pass
            
            if hasattr(self.server, 'log_callback'):
                self.server.log_callback(f"[{datetime.now().strftime('%H:%M:%S')}] [{self.server.local_port}] [错误] GET {self.path} - {str(e)}")
    
    def do_POST(self):
        self.do_GET()
    
    def do_HEAD(self):
        self.do_GET()
    
    def log_message(self, format, *args):
        pass


class ProxyServer:
    def __init__(self, local_port, target_url, log_callback):
        self.local_port = local_port
        self.target_url = target_url
        self.log_callback = log_callback
        self.server = None
        self.thread = None
        self.running = False
        self.stop_event = threading.Event()
    
    def start(self):
        try:
            self.server = HTTPServer(('127.0.0.1', self.local_port), ProxyHandler)
            self.server.local_port = self.local_port
            self.server.target_url = self.target_url
            self.server.log_callback = self.log_callback
            self.server.timeout = 0.5
            self.running = True
            self.stop_event.clear()
            
            self.thread = threading.Thread(target=self._serve_forever)
            self.thread.daemon = True
            self.thread.start()
            
            import time
            time.sleep(0.2)
            
            if self.running:
                return True, f"端口 {self.local_port} -> {self.target_url} 启动成功"
            else:
                return False, f"端口 {self.local_port} 启动失败"
        except OSError as e:
            if e.winerror == 10048:
                return False, f"端口 {self.local_port} 被占用，请关闭其他程序或以管理员身份运行"
            elif e.winerror == 10013:
                return False, f"端口 {self.local_port} 访问被拒绝，请以管理员身份运行"
            else:
                return False, f"端口 {self.local_port} 启动失败：{str(e)}"
    
    def _serve_forever(self):
        while self.running and not self.stop_event.is_set():
            try:
                self.server.handle_request()
            except:
                pass
    
    def stop(self):
        if self.server:
            self.running = False
            self.stop_event.set()
            try:
                self.server.server_close()
            except:
                pass
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=2.0)
            self.server = None
            self.thread = None
            return f"端口 {self.local_port} 已停止"
        return f"端口 {self.local_port} 未运行"


class ProxyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(i18n.t('window_title'))
        self.root.geometry("650x480")
        self.root.minsize(550, 400)
        
        self.config = self.load_config()
        self.proxy_servers = {}
        self.is_running = False
        self.lock = threading.Lock()
        
        self.setup_ui()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return json.loads(json.dumps(DEFAULT_CONFIG))
    
    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.log(i18n.t('log_config_save_fail', error=str(e)), "error")
            return False
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部控制区域
        ctrl_frame = tk.Frame(main_frame)
        ctrl_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 状态标签
        self.status_label = tk.Label(
            ctrl_frame, text=i18n.t('status_disconnected'),
            font=("Microsoft YaHei", 12, "bold"), fg="gray"
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 单一切换按钮（恢复原版逻辑）
        btn_text = i18n.t('btn_start') if not self.is_running else i18n.t('btn_stop')
        self.toggle_btn = tk.Button(
            ctrl_frame, text=btn_text, font=("Microsoft YaHei", 10), width=12,
            command=self.toggle_connection, bg="#4CAF50", fg="white",
            activebackground="#45a049", activeforeground="white"
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=5)
        
        # 语言切换按钮
        self.lang_btn = tk.Button(
            ctrl_frame, text=i18n.t('btn_switch_lang'), font=("Microsoft YaHei", 10), width=8,
            command=self.switch_language, bg="#2196F3", fg="white",
            activebackground="#1976D2", activeforeground="white"
        )
        self.lang_btn.pack(side=tk.LEFT, padx=5)
        
        # 退出按钮（放在连接按钮旁边）
        self.exit_btn = tk.Button(
            ctrl_frame, text=i18n.t('btn_exit'), font=("Microsoft YaHei", 10), width=8,
            command=self.on_exit, bg="#f44336", fg="white",
            activebackground="#da190b", activeforeground="white"
        )
        self.exit_btn.pack(side=tk.LEFT, padx=5)
        
        # 分隔线
        sep = tk.Frame(main_frame, height=2, bg="#ddd")
        sep.pack(fill=tk.X, pady=5)
        
        # 规则管理区域
        rule_frame = tk.Frame(main_frame)
        rule_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.rule_title = tk.Label(
            rule_frame, text=i18n.t('rule_title'),
            font=("Microsoft YaHei", 10, "bold"), anchor="w"
        )
        self.rule_title.pack(fill=tk.X, pady=(0, 5))
        
        # 规则表格
        self.tree = ttk.Treeview(rule_frame, columns=("port", "url", "enabled"), show="headings", height=4)
        self.tree.heading("port", text=i18n.t('col_port'))
        self.tree.heading("url", text=i18n.t('col_url'))
        self.tree.heading("enabled", text=i18n.t('col_enabled'))
        self.tree.column("port", width=100, anchor="center")
        self.tree.column("url", width=380, anchor="w")
        self.tree.column("enabled", width=60, anchor="center")
        
        scrollbar = ttk.Scrollbar(rule_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 双击切换启用/禁用
        self.tree.bind("<Double-1>", self.toggle_rule_enabled)
        
        # 规则操作按钮
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 5))
        
        self.add_btn = tk.Button(btn_frame, text=i18n.t('btn_add'), font=("Microsoft YaHei", 9), width=8, command=self.add_rule)
        self.add_btn.pack(side=tk.LEFT, padx=2)
        
        self.edit_btn = tk.Button(btn_frame, text=i18n.t('btn_edit'), font=("Microsoft YaHei", 9), width=8, command=self.edit_rule)
        self.edit_btn.pack(side=tk.LEFT, padx=2)
        
        self.del_btn = tk.Button(btn_frame, text=i18n.t('btn_delete'), font=("Microsoft YaHei", 9), width=8, command=self.delete_rule)
        self.del_btn.pack(side=tk.LEFT, padx=2)
        
        self.save_btn = tk.Button(btn_frame, text=i18n.t('btn_save'), font=("Microsoft YaHei", 9), width=8, command=self.save_and_refresh)
        self.save_btn.pack(side=tk.LEFT, padx=2)
        
        # 分隔线
        sep2 = tk.Frame(main_frame, height=2, bg="#ddd")
        sep2.pack(fill=tk.X, pady=5)
        
        # 日志区域
        self.log_title = tk.Label(
            main_frame, text=i18n.t('log_title'),
            font=("Microsoft YaHei", 10, "bold"), anchor="w"
        )
        self.log_title.pack(fill=tk.X, pady=(5, 0))
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame, font=("Consolas", 9), wrap=tk.WORD,
            bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", state=tk.DISABLED, height=8
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.log_text.tag_config("info", foreground="#4ec9b0")
        self.log_text.tag_config("success", foreground="#4CAF50")
        self.log_text.tag_config("error", foreground="#f44336")
        self.log_text.tag_config("warning", foreground="#ff9800")
        
        # 加载规则到表格
        self.refresh_rules()
    
    def switch_language(self):
        """切换语言"""
        i18n.switch()
        
        # 保存核心状态
        saved_servers = self.proxy_servers
        saved_running = self.is_running
        
        # 保存日志内容
        saved_log_content = ""
        if self.log_text:
            saved_log_content = self.log_text.get("1.0", tk.END)
        
        # 清空界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 更新窗口标题
        self.root.title(i18n.t('window_title'))
        
        # 重新创建界面
        self.setup_ui()
        
        # 恢复状态
        self.proxy_servers = saved_servers
        self.is_running = saved_running
        
        if self.is_running:
            self.toggle_btn.config(text=i18n.t('btn_stop'), bg="#f44336")
            self.status_label.config(text=i18n.t('status_connected', count=len(self.proxy_servers)), fg="#4CAF50")
        else:
            self.toggle_btn.config(text=i18n.t('btn_start'), bg="#4CAF50")
            self.status_label.config(text=i18n.t('status_disconnected'), fg="gray")
            
        # 恢复日志
        if self.log_text and saved_log_content:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert("1.0", saved_log_content)
            self.log_text.config(state=tk.DISABLED)
    
    def toggle_rule_enabled(self, event):
        """双击切换规则的启用/禁用状态"""
        selected = self.tree.selection()
        if not selected:
            return
        
        idx = int(selected[0])
        rule = self.config['rules'][idx]
        rule['enabled'] = not rule.get('enabled', True)
        self.save_config()
        self.refresh_rules()
        status = i18n.t('status_enabled') if rule['enabled'] else i18n.t('status_disabled')
        self.log(i18n.t('log_rule_toggled', port=rule['local_port'], status=status), "warning")
    
    def refresh_rules(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, rule in enumerate(self.config.get('rules', [])):
            enabled = rule.get('enabled', True)
            status_text = i18n.t('icon_enabled') if enabled else i18n.t('icon_disabled')
            self.tree.insert("", "end", values=(
                rule.get('local_port', ''),
                rule.get('target_url', ''),
                status_text
            ), iid=str(i))
    
    def add_rule(self):
        dialog = RuleDialog(self.root, i18n.t('dlg_add_title'))
        self.root.wait_window(dialog)
        
        if dialog.result:
            port = dialog.result.get('local_port')
            url = dialog.result.get('target_url')
            
            try:
                port_int = int(port)
                if port_int < 1 or port_int > 65535:
                    messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_port_range'))
                    return
            except ValueError:
                messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_port_number'))
                return
            
            if not url.startswith(('http://', 'https://')):
                messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_url_format'))
                return
            
            for rule in self.config.get('rules', []):
                if rule.get('local_port') == port_int:
                    messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_port_exists', port=port_int))
                    return
            
            self.config['rules'].append({
                'local_port': port_int,
                'target_url': url,
                'enabled': True
            })
            self.save_config()
            self.refresh_rules()
            self.log(i18n.t('log_rule_added', port=port_int, url=url), "success")
    
    def edit_rule(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(i18n.t('err_start_all'), i18n.t('warn_select_edit'))
            return
        
        idx = int(selected[0])
        rule = self.config['rules'][idx]
        
        dialog = RuleDialog(self.root, i18n.t('dlg_edit_title'), rule)
        self.root.wait_window(dialog)
        
        if dialog.result:
            port = dialog.result.get('local_port')
            url = dialog.result.get('target_url')
            
            try:
                port_int = int(port)
                if port_int < 1 or port_int > 65535:
                    messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_port_range'))
                    return
            except ValueError:
                messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_port_number'))
                return
            
            if not url.startswith(('http://', 'https://')):
                messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_url_format'))
                return
            
            for i, r in enumerate(self.config.get('rules', [])):
                if i != idx and r.get('local_port') == port_int:
                    messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_port_used', port=port_int))
                    return
            
            self.config['rules'][idx] = {
                'local_port': port_int,
                'target_url': url,
                'enabled': rule.get('enabled', True)
            }
            self.save_config()
            self.refresh_rules()
            self.log(i18n.t('log_rule_edited', port=port_int, url=url), "success")
    
    def delete_rule(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(i18n.t('err_start_all'), i18n.t('warn_select_delete'))
            return
        
        if messagebox.askyesno(i18n.t('confirm_delete'), i18n.t('confirm_delete')):
            idx = int(selected[0])
            rule = self.config['rules'][idx]
            self.config['rules'].pop(idx)
            self.save_config()
            self.refresh_rules()
            self.log(i18n.t('log_rule_deleted', port=rule['local_port']), "warning")
    
    def save_and_refresh(self):
        if self.save_config():
            self.refresh_rules()
            self.log(i18n.t('log_config_saved'), "success")
    
    def toggle_connection(self):
        if self.is_running:
            self.stop_all()
        else:
            self.start_all()
    
    def start_all(self):
        rules = self.config.get('rules', [])
        enabled_rules = [r for r in rules if r.get('enabled', True)]
        
        if not enabled_rules:
            messagebox.showwarning(i18n.t('err_start_all'), i18n.t('warn_no_rules'))
            return
        
        self.log(i18n.t('log_starting', count=len(enabled_rules)), "warning")
        self.status_label.config(text=i18n.t('status_connecting'), fg="orange")
        self.toggle_btn.config(state=tk.DISABLED)
        
        def _start_all():
            success_count = 0
            fail_count = 0
            
            for rule in enabled_rules:
                port = rule['local_port']
                url = rule['target_url']
                
                server = ProxyServer(
                    local_port=port,
                    target_url=url,
                    log_callback=self.log_callback
                )
                
                success, message = server.start()
                if success:
                    self.proxy_servers[port] = server
                    success_count += 1
                    self.log(i18n.t('log_started', port=port, url=url), "success")
                else:
                    fail_count += 1
                    self.log(message, "error")
            
            def _update():
                self.toggle_btn.config(state=tk.NORMAL)
                if success_count > 0:
                    self.is_running = True
                    self.toggle_btn.config(text=i18n.t('btn_stop'), bg="#f44336")
                    self.status_label.config(text=i18n.t('status_connected', count=success_count), fg="#4CAF50")
                else:
                    self.status_label.config(text=i18n.t('status_failed'), fg="#f44336")
                    messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_all_failed'))
            
            self.root.after(0, _update)
        
        thread = threading.Thread(target=_start_all, daemon=True)
        thread.start()
    
    def stop_all(self):
        self.log(i18n.t('log_stopping'), "warning")
        self.status_label.config(text=i18n.t('status_stopping'), fg="orange")
        self.toggle_btn.config(state=tk.DISABLED)
        
        def _stop_all():
            for port, server in self.proxy_servers.items():
                message = server.stop()
                self.log(i18n.t('log_stopped', port=port), "warning")
            
            self.proxy_servers.clear()
            self.is_running = False
            
            def _update():
                self.toggle_btn.config(state=tk.NORMAL)
                self.toggle_btn.config(text=i18n.t('btn_start'), bg="#4CAF50")
                self.status_label.config(text=i18n.t('status_disconnected'), fg="gray")
            
            self.root.after(0, _update)
        
        thread = threading.Thread(target=_stop_all, daemon=True)
        thread.start()
    
    def log_callback(self, message):
        if "错误" in message or "error" in message.lower():
            self.log(message, "error")
        elif "200" in message or "30" in message:
            self.log(message, "success")
        else:
            self.log(message, "info")
    
    def log(self, message, tag="info"):
        def _log():
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n", tag)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        self.root.after(0, _log)
    
    def on_closing(self):
        """关闭窗口时直接退出"""
        if messagebox.askyesno(i18n.t('confirm_exit'), i18n.t('confirm_exit')):
            self._cleanup_and_exit()
    
    def on_exit(self):
        if self.is_running:
            if messagebox.askyesno(i18n.t('confirm_exit'), i18n.t('confirm_exit')):
                self._cleanup_and_exit()
        else:
            self._cleanup_and_exit()
    
    def _cleanup_and_exit(self):
        self.log(i18n.t('log_exiting'), "warning")
        
        if self.is_running:
            for server in self.proxy_servers.values():
                server.stop()
            self.is_running = False
        
        self.root.after(100, self._do_exit)
    
    def _do_exit(self):
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
        finally:
            sys.exit(0)
    
    def run(self):
        self.log(i18n.t('log_startup'), "success")
        self.log(i18n.t('log_ready'), "info")
        self.log(i18n.t('log_double_click'), "info")
        
        self.root.mainloop()


class RuleDialog(tk.Toplevel):
    def __init__(self, parent, title, rule=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.result = None
        
        self.transient(parent)
        self.grab_set()
        
        # 居中显示
        self.update_idletasks()
        x = (parent.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (parent.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        # 表单
        form_frame = tk.Frame(self)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 端口
        tk.Label(form_frame, text=i18n.t('lbl_port'), font=("Microsoft YaHei", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.port_var = tk.StringVar(value=str(rule['local_port']) if rule else "")
        tk.Entry(form_frame, textvariable=self.port_var, width=30, font=("Microsoft YaHei", 10)).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # 目标网址
        tk.Label(form_frame, text=i18n.t('lbl_url'), font=("Microsoft YaHei", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.url_var = tk.StringVar(value=rule['target_url'] if rule else "")
        tk.Entry(form_frame, textvariable=self.url_var, width=30, font=("Microsoft YaHei", 10)).grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # 按钮
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text=i18n.t('btn_ok'), width=10, command=self.on_ok).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text=i18n.t('btn_cancel'), width=10, command=self.destroy).pack(side=tk.LEFT, padx=10)
        
        self.port_var.trace_add("write", self._on_input)
        self.url_var.trace_add("write", self._on_input)
    
    def _on_input(self, *args):
        pass
    
    def on_ok(self):
        port = self.port_var.get().strip()
        url = self.url_var.get().strip()
        
        if not port or not url:
            messagebox.showerror(i18n.t('err_start_all'), i18n.t('err_fill_all'))
            return
        
        self.result = {
            'local_port': port,
            'target_url': url
        }
        self.destroy()


def main():
    app = ProxyGUI()
    app.run()


if __name__ == '__main__':
    main()
