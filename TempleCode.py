#!/usr/bin/env python3
"""
TempleCode IDE launcher

This is the rebranded entrypoint for the IDE. It imports the shared
implementation from Super_PILOT.py and invokes the TempleCode-branded
main function to start the GUI when Tk is available.
"""

from Super_PILOT import (
    main_templecode,
    TK_AVAILABLE,
    MIN_DELTA_TIME_MS,
    MAX_DELTA_TIME_MS,
    TempleCodeInterpreter,
)

# Re-export constants expected by tests
__all__ = [
    "main_templecode",
    "TK_AVAILABLE",
    "MIN_DELTA_TIME_MS",
    "MAX_DELTA_TIME_MS",
    "TempleCodeInterpreter",
]

# Re-export ttk for UI tests that reference TempleCode.ttk
try:
    from tkinter import ttk
except Exception:
    ttk = None


def main():
    if not TK_AVAILABLE:
        # fall back to the same error handling in main_templecode
        main_templecode()
        return
    main_templecode()


if __name__ == "__main__":
    main()
