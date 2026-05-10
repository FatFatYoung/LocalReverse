# 第三方开源组件声明 (Third-Party Notices)

LocalReverse 项目（以下简称“本项目”）基于 Python 开发。为满足开源合规性及透明度要求，以下列出本项目开发、构建及运行过程中涉及的开源组件及其许可信息。

## 1. 运行时依赖

### Requests
- **用途**：用于处理 HTTP/HTTPS 请求转发，替代标准库以获得更稳健的连接管理和超时控制。
- **许可协议**: Apache License 2.0
- **版权声明**: Copyright 2019 Kenneth Reitz
- **项目地址**: https://github.com/psf/requests

### Python 标准库 (Standard Library)
- **包含组件**: `tkinter`, `http.server`, `threading`, `os`, `sys`, `json`, `datetime` 等。
- **许可协议**: [Python Software Foundation License (PSF)](https://docs.python.org/3/license.html)
- **版权声明**: Copyright © 2001-2026 Python Software Foundation.

### Tcl/Tk (GUI Framework)
- **包含组件**: `tkinter` (底层依赖系统 Tcl/Tk 库)
- **许可协议**: [Tcl/Tk License](https://www.tcl.tk/software/tcltk/license.html)
- **版权声明**: Copyright © 1993-1994 The Regents of the University of California. Copyright © 1994-1996 Sun Microsystems, Inc.

## 2. 构建工具

### PyInstaller
- **用途**: 将 Python 源码打包为单文件可执行程序 (.exe)。
- **许可协议**: GNU General Public License v2 (GPL-2.0) (附带 Bootloader Exception)
- **版权声明**: Copyright © 2005-2026 PyInstaller Development Team.
- **合规说明**: 
    - PyInstaller 采用 GPL 协议，但包含 **Bootloader Exception** 条款。
    - 该条款明确指出：仅使用 PyInstaller 打包生成的可执行文件，**不** 视为 PyInstaller 的衍生作品，因此打包后的程序无需强制开源，允许与本项目采用的 MIT 协议共存。

---

### 本项目许可

本项目（LocalReverse）自身的代码及资源采用 **MIT License** 授权。

Copyright (c) 2026 FatFatYoung
