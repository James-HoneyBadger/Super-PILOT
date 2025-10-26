#!/usr/bin/env python3
"""
Modern Time Warp IDE with PySide6 UI

A complete redesign using PySide6 for modern, responsive UI components.
"""

import sys
import os
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

# ...existing code truncated for brevity...
