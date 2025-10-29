#!/usr/bin/env python3
from Super_PILOT import SuperPILOTInterpreter

program = """
TO SQUARE SIZE
REPEAT 4 [FD SIZE RT 90]
END
SQUARE 100
"""

interp = SuperPILOTInterpreter()
interp.run_program(program)

print(f"\nDEBUG: logo_procedures attribute exists: {hasattr(interp, 'logo_procedures')}")
if hasattr(interp, 'logo_procedures'):
    print(f"DEBUG: logo_procedures = {interp.logo_procedures}")
