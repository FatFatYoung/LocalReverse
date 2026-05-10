# -*- coding: utf-8 -*-
"""
本地代理服务 - 国际化模块
支持中英文切换
"""
import os
import json

# 语言包
LANGUAGES = {
    'zh': {
        'window_title': '本地代理服务 - 多端口映射',
        'status_disconnected': '● 未连接',
        'status_connecting': '● 正在启动...',
        'status_connected': '● 已连接 ({count} 个)',
        'status_stopping': '● 正在停止...',
        'status_failed': '● 启动失败',
        'btn_start': '开始连接',
        'btn_stop': '断开连接',
        'btn_exit': '退出',
        'btn_switch_lang': 'English',
        'rule_title': '映射规则（双击切换启用/禁用）',
        'col_port': '本地端口',
        'col_url': '目标网址',
        'col_enabled': '状态',
        'icon_enabled': '✔',
        'icon_disabled': '✘',
        'btn_add': '添加',
        'btn_edit': '编辑',
        'btn_delete': '删除',
        'btn_save': '保存',
        'log_title': '运行日志',
        'log_startup': '本地代理服务启动 (多端口映射版)',
        'log_ready': '就绪，点击「开始连接」启动服务',
        'log_double_click': '提示：双击表格可切换规则启用/禁用',
        'log_exiting': '正在退出程序...',
        'log_starting': '正在启动 {count} 个服务...',
        'log_started': '端口 {port} -> {url} 启动成功',
        'log_start_fail': '端口 {port} 启动失败',
        'log_port_occupied': '端口 {port} 被占用，请关闭其他程序或以管理员身份运行',
        'log_port_denied': '端口 {port} 访问被拒绝，请以管理员身份运行',
        'log_stopping': '正在停止所有服务...',
        'log_stopped': '端口 {port} 已停止',
        'log_config_saved': '配置已保存',
        'log_config_save_fail': '保存配置失败：{error}',
        'log_rule_added': '添加规则：端口 {port} -> {url}',
        'log_rule_edited': '编辑规则：端口 {port} -> {url}',
        'log_rule_deleted': '删除规则：端口 {port}',
        'log_rule_toggled': '规则 {port} -> {status}',
        'dlg_add_title': '添加规则',
        'dlg_edit_title': '编辑规则',
        'lbl_port': '本地端口:',
        'lbl_url': '目标网址:',
        'btn_ok': '确定',
        'btn_cancel': '取消',
        'err_fill_all': '请填写所有字段',
        'err_port_range': '端口必须在 1-65535 之间',
        'err_port_number': '端口必须是数字',
        'err_url_format': '目标网址必须以 http:// 或 https:// 开头',
        'err_port_exists': '端口 {port} 已存在',
        'err_port_used': '端口 {port} 已被其他规则使用',
        'warn_select_edit': '请先选择要编辑的规则',
        'warn_select_delete': '请先选择要删除的规则',
        'warn_no_rules': '没有启用的规则，请先添加并启用规则',
        'confirm_delete': '确定要删除选中的规则吗？',
        'confirm_exit': '服务正在运行，确定要退出吗？',
        'err_start_all': '启动失败',
        'err_all_failed': '所有服务启动失败',
        'status_enabled': '启用',
        'status_disabled': '禁用',
    },
    'en': {
        'window_title': 'Local Proxy Service - Multi-Port Mapping',
        'status_disconnected': '● Disconnected',
        'status_connecting': '● Starting...',
        'status_connected': '● Connected ({count})',
        'status_stopping': '● Stopping...',
        'status_failed': '● Start Failed',
        'btn_start': 'Connect',
        'btn_stop': 'Disconnect',
        'btn_exit': 'Exit',
        'btn_switch_lang': '中文',
        'rule_title': 'Mapping Rules (Double-click to toggle)',
        'col_port': 'Local Port',
        'col_url': 'Target URL',
        'col_enabled': 'Status',
        'icon_enabled': '✔',
        'icon_disabled': '✘',
        'btn_add': 'Add',
        'btn_edit': 'Edit',
        'btn_delete': 'Delete',
        'btn_save': 'Save',
        'log_title': 'Log',
        'log_startup': 'Local Proxy Service Started (Multi-Port)',
        'log_ready': 'Ready, click "Connect" to start',
        'log_double_click': 'Tip: Double-click table to toggle rule',
        'log_exiting': 'Exiting...',
        'log_starting': 'Starting {count} services...',
        'log_started': 'Port {port} -> {url} started',
        'log_start_fail': 'Port {port} start failed',
        'log_port_occupied': 'Port {port} occupied, close other apps or run as admin',
        'log_port_denied': 'Port {port} access denied, run as admin',
        'log_stopping': 'Stopping all services...',
        'log_stopped': 'Port {port} stopped',
        'log_config_saved': 'Config saved',
        'log_config_save_fail': 'Save config failed: {error}',
        'log_rule_added': 'Added rule: port {port} -> {url}',
        'log_rule_edited': 'Edited rule: port {port} -> {url}',
        'log_rule_deleted': 'Deleted rule: port {port}',
        'log_rule_toggled': 'Rule {port} -> {status}',
        'dlg_add_title': 'Add Rule',
        'dlg_edit_title': 'Edit Rule',
        'lbl_port': 'Local Port:',
        'lbl_url': 'Target URL:',
        'btn_ok': 'OK',
        'btn_cancel': 'Cancel',
        'err_fill_all': 'Please fill all fields',
        'err_port_range': 'Port must be between 1-65535',
        'err_port_number': 'Port must be a number',
        'err_url_format': 'URL must start with http:// or https://',
        'err_port_exists': 'Port {port} already exists',
        'err_port_used': 'Port {port} used by another rule',
        'warn_select_edit': 'Please select a rule to edit',
        'warn_select_delete': 'Please select a rule to delete',
        'warn_no_rules': 'No enabled rules, please add and enable rules first',
        'confirm_delete': 'Are you sure to delete the selected rule?',
        'confirm_exit': 'Service is running, are you sure to exit?',
        'err_start_all': 'Start Failed',
        'err_all_failed': 'All services failed to start',
        'status_enabled': 'Enabled',
        'status_disabled': 'Disabled',
    }
}


class I18n:
    def __init__(self):
        self.current_lang = 'zh'
        self.config_file = 'lang.json'
        self._load_saved_lang()
    
    def _load_saved_lang(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_lang = data.get('lang', 'zh')
        except:
            pass
    
    def save_lang(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'lang': self.current_lang}, f, indent=2)
        except:
            pass
    
    def t(self, key, **kwargs):
        text = LANGUAGES.get(self.current_lang, {}).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text
    
    def switch(self):
        self.current_lang = 'en' if self.current_lang == 'zh' else 'zh'
        self.save_lang()
        return self.current_lang
    
    def get_current(self):
        return self.current_lang


# 全局单例
i18n = I18n()
