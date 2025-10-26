#!/usr/bin/env python3
"""
Modern Time Warp IDE with PySide6 UI

A complete redesign using PySide6 for modern, responsive UI components.
"""

import sys
import os
import subprocess

# Ensure required packages are installed
REQUIRED_PACKAGES = ["PySide6", "Pillow"]
missing = []
for pkg in REQUIRED_PACKAGES:
    try:
        __import__(pkg if pkg != "Pillow" else "PIL")
    except ImportError:
        missing.append(pkg)
if missing:
    print(f"❌ Missing required packages: {', '.join(missing)}")
    print("Attempting to install missing packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    print("✅ Packages installed. Please re-run the IDE.")
    sys.exit(1)

from typing import Optional, Dict, Any, List
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.interpreter import TimeWarpInterpreter
from core.plugin_system import PluginManager
from core.safe_expression_evaluator import safe_eval
from core.async_support import (
    init_async_support,
    get_async_runner,
    AsyncInterpreterRunner,
)

# Import modern UI
from ui.qt_ui import QtUIFactory, PYSIDE6_AVAILABLE

if not PYSIDE6_AVAILABLE:
    print("❌ PySide6 is not available. Please install PySide6 to use the modern UI.")
    print("Run: pip install PySide6")
    sys.exit(1)

from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QInputDialog
from PySide6.QtCore import QTimer, Qt
