# Third-Party Notices

The LocalReverse project ("this project") is developed in Python. For open-source compliance and transparency, the open-source components involved in the development, build, and runtime of this project are listed below along with their license information.

## 1. Runtime Dependencies

### Requests
- **Purpose**: Handles HTTP/HTTPS request forwarding; used instead of the standard library for more robust connection management and timeout control.
- **License**: Apache License 2.0
- **Copyright**: Copyright 2019 Kenneth Reitz
- **Project URL**: https://github.com/psf/requests

### Python Standard Library
- **Components**: `tkinter`, `http.server`, `threading`, `os`, `sys`, `json`, `datetime`, etc.
- **License**: [Python Software Foundation License (PSF)](https://docs.python.org/3/license.html)
- **Copyright**: Copyright © 2001-2026 Python Software Foundation.

### Tcl/Tk (GUI Framework)
- **Components**: `tkinter` (backed by the system Tcl/Tk libraries)
- **License**: [Tcl/Tk License](https://www.tcl.tk/software/tcltk/license.html)
- **Copyright**: Copyright © 1993-1994 The Regents of the University of California. Copyright © 1994-1996 Sun Microsystems, Inc.

## 2. Build Tools

### PyInstaller
- **Purpose**: Packages Python source code into a single-file executable (.exe).
- **License**: GNU General Public License v2 (GPL-2.0) (with Bootloader Exception)
- **Copyright**: Copyright © 2005-2026 PyInstaller Development Team.
- **Compliance notes**:
    - PyInstaller is licensed under the GPL, but includes a **Bootloader Exception** clause.
    - That clause explicitly states that executables merely produced by running PyInstaller are **not** considered derivative works of PyInstaller; therefore the packaged program does not need to be open-sourced, and may coexist with the MIT license of this project.

---

### License of This Project

The code and resources of this project (LocalReverse) itself are licensed under the **MIT License**.

Copyright (c) 2026 FatFatYoung
