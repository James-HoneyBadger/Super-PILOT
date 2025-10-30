"""
Compatibility shim module.

Some tests and external code import `TempleCode` (without the underscore).
This thin wrapper re-exports the public API from the main module `TempleCode`.
Also exposes tkinter.ttk at module scope so tests can patch TempleCode.ttk.Style.
"""
# Compatibility shim for tests and external imports expecting `TempleCode`
# Re-export the main implementation from TempleCode.py
from Super_PILOT import *  # noqa: F401,F403

# Expose tkinter and ttk for tests that patch TempleCode.ttk.Style
import tkinter as tk  # noqa: F401
from tkinter import ttk  # noqa: F401

# Ensure the MIN_DELTA_TIME_MS constant is available at module scope
try:
    MIN_DELTA_TIME_MS  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    MIN_DELTA_TIME_MS = 1
