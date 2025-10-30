#!/usr/bin/env python3
"""Quick test to verify A: command works with thread-safe input mechanism"""

from Super_PILOT import TempleCodeInterpreter
from unittest.mock import Mock, patch

def test_a_command_in_console_mode():
    """Test A: command in console mode (no GUI)"""
    interp = TempleCodeInterpreter()
    
    # Mock console input
    with patch('builtins.input', return_value='TestUser'):
        program = """
T:Enter your name:
A:NAME
T:Hello, *NAME*!
"""
        output = []
        interp.on_output.append(lambda msg: output.append(msg))
        interp.run_program(program)
        
        assert 'TestUser' in interp.variables['NAME']
        assert 'Hello, TestUser!' in '\n'.join(output)
        print("✓ Console mode A: command works")

def test_a_command_with_ide_callback():
    """Test A: command with IDE input callback (simulated threading context)"""
    interp = TempleCodeInterpreter()
    
    # Simulate IDE environment by setting output_widget
    interp.output_widget = Mock()
    
    # Simulate the IDE's input request callback
    def mock_ide_input(prompt):
        return "IDEUser"
    
    interp._ide_input_request = mock_ide_input
    
    # Patch threading to simulate background thread
    import threading
    
    def mock_current_thread():
        thread = Mock()
        thread.name = "BackgroundThread"
        return thread
    
    def mock_main_thread():
        thread = Mock()
        thread.name = "MainThread"
        return thread
    
    with patch('threading.current_thread', side_effect=mock_current_thread), \
         patch('threading.main_thread', side_effect=mock_main_thread):
        program = """
T:Enter your name:
A:NAME
T:Hello, *NAME*!
"""
        output = []
        interp.on_output.append(lambda msg: output.append(msg))
        interp.run_program(program)
        
        assert 'IDEUser' in interp.variables.get('NAME', '')
        assert 'Hello, IDEUser!' in '\n'.join(output)
        print("✓ IDE callback mode A: command works")

if __name__ == '__main__':
    test_a_command_in_console_mode()
    test_a_command_with_ide_callback()
    print("\nAll A: command tests passed!")
