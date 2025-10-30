#!/usr/bin/env python3
"""
Comprehensive test suite to verify interpreter functionality before/after extraction
"""

from Super_PILOT import TempleCodeInterpreter
import time


def test_interpreter_comprehensive():
    """Test all major interpreter features"""
    
    print("Testing TempleCode Interpreter...")
    
    interp = TempleCodeInterpreter()
    
    # Test 1: Basic PILOT commands
    print("  Test 1: PILOT commands (T:, U:)...", end=" ")
    program1 = """
T:Hello World
U:X=5
U:Y=10
T:X is *X* and Y is *Y*
"""
    result = interp.run_program(program1)
    assert result == True
    assert interp.variables.get('X') == 5
    assert interp.variables.get('Y') == 10
    print("✓")
    
    # Test 2: BASIC commands
    print("  Test 2: BASIC commands (LET, PRINT)...", end=" ")
    interp = TempleCodeInterpreter()
    program2 = """
10 LET A = 100
20 LET B = 200
30 LET C = A + B
40 PRINT C
50 END
"""
    result = interp.run_program(program2)
    assert result == True
    assert interp.variables.get('A') == 100
    assert interp.variables.get('C') == 300
    print("✓")
    
    # Test 3: Logo commands
    print("  Test 3: Logo commands (FORWARD, RIGHT)...", end=" ")
    interp = TempleCodeInterpreter()
    program3 = """
FORWARD 50
RIGHT 90
FORWARD 50
"""
    result = interp.run_program(program3)
    assert result == True
    # Turtle should have moved
    assert interp.turtle_x != 200 or interp.turtle_y != 200
    print("✓")
    
    # Test 4: Conditionals (Y:, N:)
    print("  Test 4: Conditionals (Y:, N:)...", end=" ")
    interp = TempleCodeInterpreter()
    program4 = """
U:X=5
Y:X == 5
T:X is five
U:FLAG=1
"""
    result = interp.run_program(program4)
    assert result == True
    assert interp.variables.get('FLAG') == 1
    print("✓")
    
    # Test 5: Variable operations
    print("  Test 5: Variable operations...", end=" ")
    interp = TempleCodeInterpreter()
    program5 = """
U:A=10
U:B=20
U:C=30
"""
    result = interp.run_program(program5)
    assert result  # Simpler assertion
    assert interp.variables.get('A') == 10
    assert interp.variables.get('B') == 20
    assert interp.variables.get('C') == 30
    print("✓")
    
    # Test 6: Labels and jumps
    print("  Test 6: Labels (L:)...", end=" ")
    interp = TempleCodeInterpreter()
    program6 = """
L:START
U:X=100
T:At label START
"""
    result = interp.run_program(program6)
    assert result
    assert 'START' in interp.labels
    assert interp.variables.get('X') == 100
    print("✓")
    
    # Test 7: Event callbacks
    print("  Test 7: Event callbacks...", end=" ")
    interp = TempleCodeInterpreter()
    events = {'started': 0, 'finished': 0, 'lines': 0}
    
    interp.on_program_started.append(lambda: events.update({'started': events['started'] + 1}))
    interp.on_program_finished.append(lambda s: events.update({'finished': events['finished'] + 1}))
    interp.on_line_executed.append(lambda l: events.update({'lines': events['lines'] + 1}))
    
    program7 = "T:Test\nU:X=1"
    result = interp.run_program(program7)
    
    assert events['started'] == 1
    assert events['finished'] == 1
    assert events['lines'] >= 2
    print("✓")
    
    # Test 8: Expression evaluation
    print("  Test 8: Expression evaluation...", end=" ")
    interp = TempleCodeInterpreter()
    assert interp.evaluate_expression("2 + 3") == 5
    assert interp.evaluate_expression("10 * 5") == 50
    interp.variables['X'] = 10
    assert interp.evaluate_expression("X * 2") == 20
    print("✓")
    
    # Test 9: String operations
    print("  Test 9: String operations...", end=" ")
    interp = TempleCodeInterpreter()
    interp.variables['NAME'] = "Alice"
    text = interp.interpolate_text("Hello *NAME*!")
    assert "Alice" in text
    print("✓")
    
    # Test 10: Hardware stubs
    print("  Test 10: Hardware stubs...", end=" ")
    interp = TempleCodeInterpreter()
    assert interp.arduino is not None
    assert interp.rpi is not None
    assert interp.iot_devices is not None
    print("✓")
    
    print("\n✅ All interpreter tests passed!")
    return True


if __name__ == "__main__":
    test_interpreter_comprehensive()
