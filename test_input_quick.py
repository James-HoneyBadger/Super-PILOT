#!/usr/bin/env python3
"""Quick test to verify input mechanism works"""

from Super_PILOT import SuperPILOTInterpreter

# Create a simple program that uses INPUT
test_program = """
T:Testing INPUT command...
INPUT "Enter your name: "; NAME$
T:Hello *NAME$*!
END
"""

print("Testing INPUT command with headless interpreter...")
interp = SuperPILOTInterpreter()

# Mock user input
original_input = input
def mock_input(prompt):
    print(f"[MOCK INPUT] Prompt: {prompt}")
    return "TestUser"

import builtins
builtins.input = mock_input

try:
    interp.run_program(test_program)
    print("\n✓ Headless INPUT test passed")
except Exception as e:
    print(f"\n✗ Headless INPUT test failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    builtins.input = original_input

print("\nTo test with GUI, run: python3 Super_PILOT.py input_field_test.spt")
print("You should see:")
print("1. NO minimap (middle screen)")
print("2. Prompt text in output area")
print("3. Input field at BOTTOM with label, text box, and Submit button")
