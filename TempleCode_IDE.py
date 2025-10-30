#!/usr/bin/env python3
"""
TempleCode IDE launcher (alternative entrypoint)

This provides an alternative name for launching the IDE.
Use TempleCode.py for the primary entrypoint.
"""

from Super_PILOT import TempleCodeInterpreter, TempleCodeIDE, TK_AVAILABLE, main_templecode

# Legacy alias for compatibility
TempleCode_IDE = TempleCodeIDE
TempleCode_Interpreter = TempleCodeInterpreter


if __name__ == "__main__":
    main_templecode()
