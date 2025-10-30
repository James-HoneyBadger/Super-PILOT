# TempleCode Quick Start - Arch Linux (ARM64)

This guide is specifically for Arch Linux ARM64 (aarch64) systems.

## Current Status

✅ **Core interpreter**: Works without GUI (headless mode)  
❌ **GUI/IDE**: Requires system Tk package installation

## Install GUI Dependencies

```bash
# Install Tk for GUI support
sudo pacman -Syu tk

# Verify installation
python3 -c "import tkinter as tk; print('Tk version:', tk.TkVersion)"
```

## Run TempleCode

### With GUI (after installing Tk)
```bash
python3 TempleCode.py
```

### Headless Mode (no Tk needed)
```python
from TempleCode import TempleCodeInterpreter

interp = TempleCodeInterpreter()
program = """
T:Hello, World!
U:X=42
T:The answer is *X*
END
"""
interp.run_program(program)
```

## Check GUI Availability Programmatically

```python
from TempleCode import TK_AVAILABLE

if TK_AVAILABLE:
    print("GUI is available")
    # Launch full IDE
else:
    print("Running in headless mode")
    # Use interpreter only
```

## Optional: Headless GUI Testing (CI/Servers)

```bash
# Install virtual X server
sudo pacman -S --needed xorg-server-xvfb

# Run with virtual display
xvfb-run -a python3 TempleCode.py
```

## Troubleshooting

### Error: `ImportError: libtk8.6.so`
**Solution**: Install Tk with `sudo pacman -Syu tk`

### Error when running `python3 TempleCode.py`
The script now detects missing Tk and shows installation instructions automatically.

### Want to use headless mode only?
No Tk installation needed! Just import and use `TempleCodeInterpreter` directly in your Python code.

## What Changed

As of version 3.0.2 (October 28, 2025):
- ✅ Tkinter import is now optional (no crash on import)
- ✅ `TK_AVAILABLE` flag indicates GUI availability
- ✅ Clear error messages guide Tk installation
- ✅ Full headless support for automation/testing
- ✅ Modular components work independently

See `CHANGELOG.md` for complete details.
