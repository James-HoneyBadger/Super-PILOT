#!/usr/bin/env python3
import sys
from Super_PILOT import TempleCodeInterpreter

# Mock input function to simulate user input
original_input = input
inputs = iter(["42", "TestUser"])

def mock_input(prompt=""):
    val = next(inputs, "")
    print(f"{prompt}{val}")
    return val

# Replace input temporarily
import builtins
builtins.input = mock_input

program = """
T:Testing INPUT command
INPUT X
T:You entered: *X*

T:Testing A: command  
T:What is your name?
A:NAME
T:Hello *NAME*!

T:Done
"""

interp = TempleCodeInterpreter()
try:
    interp.run_program(program)
    print("\n=== Variables ===")
    print(f"X = {interp.variables.get('X', 'NOT SET')}")
    print(f"NAME = {interp.variables.get('NAME', 'NOT SET')}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    builtins.input = original_input
