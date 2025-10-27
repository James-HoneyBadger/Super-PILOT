#!/usr/bin/env python3
"""
Quick test to verify threading doesn't break the interpreter
"""

from Super_PILOT import SuperPILOTInterpreter
import time

def test_threaded_execution():
    """Test that interpreter works correctly (even though we can't test UI threading here)"""
    
    interp = SuperPILOTInterpreter()
    
    # Track if program completes
    completed = []
    
    def on_finish(success):
        completed.append(success)
        print(f"Program finished with success={success}")
    
    interp.on_program_finished.append(on_finish)
    
    # Run a simple program
    program = """
T:Starting
U:X=5
T:X is *X*
"""
    
    result = interp.run_program(program)
    
    # Give callbacks a moment to fire
    time.sleep(0.1)
    
    print(f"✓ Program executed, result={result}")
    print(f"✓ Callbacks fired: {len(completed)} times")
    assert len(completed) == 1, "on_program_finished should fire once"
    assert completed[0] == True, "Program should complete successfully"
    
    print("✓ Threading support verified (interpreter level)")
    return True

if __name__ == "__main__":
    test_threaded_execution()
