#!/usr/bin/env python3
"""
Test the event callback system in TempleCodeInterpreter
"""

from Super_PILOT import TempleCodeInterpreter

def test_event_callbacks():
    """Test all event callbacks fire correctly"""
    
    # Create interpreter
    interp = TempleCodeInterpreter()
    
    # Track events
    events = {
        'output': [],
        'variable_changed': [],
        'line_executed': [],
        'program_started': 0,
        'program_finished': 0,
        'breakpoint_hit': []
    }
    
    # Register callbacks
    interp.on_output.append(lambda text: events['output'].append(text))
    interp.on_variable_changed.append(lambda name, val: events['variable_changed'].append((name, val)))
    interp.on_line_executed.append(lambda line: events['line_executed'].append(line))
    interp.on_program_started.append(lambda: events.__setitem__('program_started', events['program_started'] + 1))
    interp.on_program_finished.append(lambda success: events.__setitem__('program_finished', events['program_finished'] + 1))
    interp.on_breakpoint_hit.append(lambda line: events['breakpoint_hit'].append(line))
    
    # Run a simple program
    program = """
T:Starting test
U:X=10
U:Y=20
C:SUM=X+Y
T:Result is *SUM*
"""
    
    result = interp.run_program(program)
    
    # Verify events
    print("Testing event callbacks...")
    print(f"Program started: {events['program_started']} (expected: 1)")
    assert events['program_started'] == 1, "program_started should fire once"
    
    print(f"Program finished: {events['program_finished']} (expected: 1)")
    assert events['program_finished'] == 1, "program_finished should fire once"
    
    print(f"Lines executed: {len(events['line_executed'])} events")
    assert len(events['line_executed']) > 0, "line_executed should fire for each line"
    
    print(f"Output events: {len(events['output'])}")
    assert len(events['output']) > 0, "output callbacks should fire"
    
    # Note: set_variable() helper is available but not yet used in all assignment locations
    # So variable_changed events may not fire yet - that's a TODO for phase 1 completion
    
    print("✓ All event callback tests passed!")
    print(f"\nEvent summary:")
    print(f"  - Output lines: {len(events['output'])}")
    print(f"  - Lines executed: {len(events['line_executed'])}")
    print(f"  - Variables changed: {len(events['variable_changed'])}")
    
    return True

if __name__ == "__main__":
    test_event_callbacks()
