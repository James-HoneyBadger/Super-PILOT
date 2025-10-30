#!/usr/bin/env python3
from Super_PILOT import TempleCodeInterpreter

program = """
TO SQUARE SIZE
REPEAT 4 [FD SIZE RT 90]
END
SQUARE 100
"""

interp = TempleCodeInterpreter()
try:
    interp.run_program(program)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
