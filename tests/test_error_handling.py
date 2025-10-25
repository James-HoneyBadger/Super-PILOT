#!/usr/bin/env python3
"""
Test error handling and edge cases for the latest SuperPILOT changes.
Focus on robustness and graceful failure modes.
"""

import unittest
from Super_PILOT import SuperPILOTInterpreter


class ErrorHandlingTests(unittest.TestCase):
    def setUp(self):
        """Set up interpreter for each test"""
        self.interp = SuperPILOTInterpreter()
        self.interp.output_widget = None
        
    def test_hardware_import_failures(self):
        """Test graceful handling of missing hardware modules"""
        # This test verifies that the recent RPi.GPIO import fix works
        
        # RPi controller should initialize without crashing
        self.assertIsNotNone(self.interp.rpi)
        self.assertFalse(self.interp.rpi.gpio_available)  # Should be in simulation mode
        
        # Arduino controller should work without pyserial
        self.assertIsNotNone(self.interp.arduino)
        self.assertFalse(self.interp.arduino.connected)  # Should start disconnected
        
    def test_malformed_runtime_commands(self):
        """Test handling of malformed R: commands"""
        prog = '''
R: 
R: INVALID
R: TWEEN
R: AFTER
R: ARDUINO
R: RPI
T:Malformed command test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should not crash
        
    def test_invalid_hardware_parameters(self):
        """Test invalid parameters to hardware commands"""
        prog = '''
R: ARDUINO CONNECT "" -1
R: RPI PIN abc OUTPUT
R: RPI WRITE 18 xyz
R: ROBOT FORWARD not_a_number
READBUTTON invalid_id VAR
READAXIS -999 VAR2
T:Invalid parameter test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle errors gracefully
        
    def test_division_by_zero_in_expressions(self):
        """Test division by zero handling in expressions"""
        prog = '''
U:X=10
U:Y=0
U:RESULT=*X*/*Y*
T:Division test completed - result is *RESULT*
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle division by zero
        
    def test_undefined_variable_interpolation(self):
        """Test interpolation of undefined variables"""
        prog = '''
T:Value of undefined variable: *UNDEFINED_VAR*
T:Expression with undefined: *UNDEFINED_VAR* + 5
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle undefined variables gracefully
        
    def test_invalid_jump_labels(self):
        """Test jumping to nonexistent labels"""
        prog = '''
J:NONEXISTENT_LABEL
T:This should still execute
Y:1 > 0
J:ANOTHER_NONEXISTENT
T:Test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle missing labels gracefully
        
    def test_infinite_loop_protection(self):
        """Test that infinite loops are prevented by max iterations"""
        prog = '''
L:LOOP
J:LOOP
T:This should never print due to loop
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should terminate due to max iterations
        
    def test_stack_overflow_protection(self):
        """Test protection against stack overflow in nested calls"""
        prog = '''
L:RECURSIVE
G:RECURSIVE
T:This creates infinite recursion
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should be protected by max iterations
        
    def test_malformed_expressions(self):
        """Test handling of malformed mathematical expressions"""
        prog = '''
U:BAD1=((((
U:BAD2=++++
U:BAD3=*missing*+
U:BAD4=RND(
U:BAD5=MID("test"
T:Malformed expression test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle syntax errors gracefully
        
    def test_memory_intensive_operations(self):
        """Test handling of operations that could consume excessive memory"""
        prog = '''
# Large number of particles
R: EMIT "test", 0, 0, 1000, 10000, 100
# Many sprites
U:I=0
L:SPRITE_LOOP
R: NEW "sprite*I*", "test.png"
U:I=*I*+1
J(*I* < 100):SPRITE_LOOP
T:Memory test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle large operations
        
    def test_concurrent_system_updates(self):
        """Test system updates with overlapping timers and tweens"""
        prog = '''
# Multiple overlapping tweens
R: TWEEN X -> 100 IN 1000ms
R: TWEEN Y -> 200 IN 800ms  
R: TWEEN Z -> 50 IN 1200ms
# Multiple timers
R: AFTER 100 DO LABEL1
R: AFTER 200 DO LABEL2
R: AFTER 150 DO LABEL3
T:Concurrent systems test
END

L:LABEL1
T:Timer 1 fired
END

L:LABEL2  
T:Timer 2 fired
END

L:LABEL3
T:Timer 3 fired
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)
        
        # Should have created multiple tweens and timers
        self.assertEqual(len(self.interp.tweens), 3)
        self.assertEqual(len(self.interp.timers), 3)
        
    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters"""
        prog = '''
T:Unicode test: 你好世界 🌍 🚀 ⭐
U:EMOJI=🎮
T:Emoji variable: *EMOJI*
R: NEW "unicode_sprite", "🎯.png"
T:Unicode filename test
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle unicode gracefully
        
    def test_very_long_variable_names(self):
        """Test handling of extremely long variable names"""
        long_name = "VERY_LONG_VARIABLE_NAME_THAT_KEEPS_GOING_AND_GOING_AND_GOING_FOR_A_VERY_LONG_TIME"
        prog = f'''
U:{long_name}=42
T:Long variable test: *{long_name}*
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)
        self.assertEqual(self.interp.variables.get(long_name), 42)
        
    def test_deeply_nested_expressions(self):
        """Test deeply nested mathematical expressions"""
        prog = '''
U:NESTED=((((((1+2)*3)+4)*5)+6)*7)
T:Nested expression result: *NESTED*
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)
        # Should evaluate: ((((((1+2)*3)+4)*5)+6)*7) = (((((3*3)+4)*5)+6)*7) = ((((9+4)*5)+6)*7) = (((13*5)+6)*7) = ((65+6)*7) = (71*7) = 497
        self.assertEqual(self.interp.variables.get('NESTED'), 497)
        
    def test_file_system_errors(self):
        """Test handling of file system errors in save/load"""
        prog = '''
# Try to save to invalid path
R: SAVE "/invalid/path/that/does/not/exist/savefile"
# Try to load nonexistent file
R: LOAD "completely_nonexistent_file"
T:File system error test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle file errors gracefully
        
    def test_turtle_graphics_without_display(self):
        """Test turtle graphics commands without display (headless)"""
        prog = '''
CLEARSCREEN
FORWARD 100
RIGHT 90
PENUP
PENDOWN
COLOR red
REPEAT 4 [ FORWARD 50 RIGHT 90 ]
T:Turtle graphics test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should work in headless mode
        
    def test_system_resource_cleanup(self):
        """Test that system resources are properly cleaned up"""
        # Create resources
        prog = '''
R: ARDUINO CONNECT /dev/ttyUSB0
R: EMIT "test", 0, 0, 50, 1000, 30
R: NEW "sprite1", "test.png"
R: TWEEN X -> 100 IN 1000ms
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)
        
        # Resources should exist
        initial_particles = len(self.interp.particles)
        initial_sprites = len(self.interp.sprites)
        initial_tweens = len(self.interp.tweens)
        
        # Reset should clean up
        self.interp.reset()
        
        self.assertEqual(len(self.interp.particles), 0)
        self.assertEqual(len(self.interp.sprites), 0)
        self.assertEqual(len(self.interp.tweens), 0)
        
    def test_cross_platform_file_paths(self):
        """Test file path handling across different platforms"""
        prog = '''
# Test various path formats
R: SAVE "normal_filename"
R: SAVE "path/with/slashes"  
R: SAVE "path\\with\\backslashes"
R: NEW "sprite", "images/sprite.png"
R: NEW "another", "images\\another.png"
T:Cross-platform path test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should handle different path formats


if __name__ == '__main__':
    unittest.main()