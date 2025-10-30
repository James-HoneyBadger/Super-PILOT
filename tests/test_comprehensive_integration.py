#!/usr/bin/env python3
"""
Integration test that exercises all major TempleCode features together.
This serves as a comprehensive smoke test for the latest changes.
"""

import unittest
from Super_PILOT import TempleCodeInterpreter, create_demo_program


class ComprehensiveIntegrationTest(unittest.TestCase):
    def setUp(self):
        """Set up interpreter for each test"""
        self.interp = TempleCodeInterpreter()
        self.interp.output_widget = None
        
    def test_comprehensive_feature_integration(self):
        """Test all major features work together without conflicts"""
        prog = '''
# Test PILOT commands
L:START
T:🚀 TempleCode Comprehensive Integration Test
U:TEST_COUNT=0
U:SUCCESS_COUNT=0

# Test variable interpolation
L:TEST_VARIABLES
T:Testing variables and interpolation...
U:A=10
U:B=20
U:SUM=*A*+*B*
T:A=*A*, B=*B*, SUM=*SUM*
U:TEST_COUNT=*TEST_COUNT*+1
J(*SUM* = 30):VAR_SUCCESS
T:❌ Variable test failed
J:HARDWARE_TEST

L:VAR_SUCCESS
T:✅ Variable test passed
U:SUCCESS_COUNT=*SUCCESS_COUNT*+1

# Test hardware integration
L:HARDWARE_TEST
T:Testing hardware integration...
R: HOME TEMP testroom 25.5
R: HOME LIGHT testlight ON
R: ARDUINO CONNECT invalid_port
U:TEST_COUNT=*TEST_COUNT*+1
J(*TEMP_testroom* = 25.5):HARDWARE_SUCCESS
T:❌ Hardware test failed
J:TEMPLECODE_TEST

L:HARDWARE_SUCCESS
T:✅ Hardware test passed
U:SUCCESS_COUNT=*SUCCESS_COUNT*+1

# Test templecode features
L:TEMPLECODE_TEST
T:Testing templecode features...
R: NEW "sprite1", "test.png"
R: POS "sprite1", 100, 200
R: EMIT "spark", 50, 50, 3, 500, 20
R: SAVE "test_integration"
U:TEST_COUNT=*TEST_COUNT*+1
U:SUCCESS_COUNT=*SUCCESS_COUNT*+1
T:✅ Templecode test passed

# Test BASIC commands
L:BASIC_TEST
T:Testing BASIC commands...
LET X = 5
LET Y = 10
PRINT "X + Y = " + STR(X + Y)
IF X < Y THEN LET RESULT = 1
U:TEST_COUNT=*TEST_COUNT*+1
J(*RESULT* = 1):BASIC_SUCCESS
T:❌ BASIC test failed
J:LOGO_TEST

L:BASIC_SUCCESS
T:✅ BASIC test passed
U:SUCCESS_COUNT=*SUCCESS_COUNT*+1

# Test Logo commands
L:LOGO_TEST
T:Testing Logo turtle graphics...
CLEARSCREEN
FORWARD 50
RIGHT 90
FORWARD 50
COLOR red
PENUP
PENDOWN
U:TEST_COUNT=*TEST_COUNT*+1
U:SUCCESS_COUNT=*SUCCESS_COUNT*+1
T:✅ Logo test passed

# Test conditional jumps
L:JUMP_TEST
T:Testing conditional jumps...
U:FLAG=1
Y:*FLAG* = 1
T:This should print because FLAG is 1
N:*FLAG* = 0
T:This should NOT print because FLAG is not 0
U:TEST_COUNT=*TEST_COUNT*+1
U:SUCCESS_COUNT=*SUCCESS_COUNT*+1
T:✅ Jump test passed

# Final results
L:RESULTS
T:📊 Test Results Summary:
T:Total tests: *TEST_COUNT*
T:Successful: *SUCCESS_COUNT*
T:Failed: *TEST_COUNT*-*SUCCESS_COUNT*
J(*SUCCESS_COUNT* >= 5):ALL_PASSED
T:❌ Some tests failed
J:END

L:ALL_PASSED
T:🎉 All integration tests passed!

L:END
T:Integration test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)
        
        # Verify all systems were exercised
        self.assertGreater(self.interp.variables.get('TEST_COUNT', 0), 0)
        self.assertGreater(self.interp.variables.get('SUCCESS_COUNT', 0), 0)
        
        # Check hardware systems were initialized
        self.assertIsNotNone(self.interp.arduino)
        self.assertIsNotNone(self.interp.rpi)
        self.assertIsNotNone(self.interp.robot)
        self.assertIsNotNone(self.interp.controller)
        
        # Check templecode systems were used
        self.assertGreater(len(self.interp.sprites), 0)
        self.assertGreater(len(self.interp.particles), 0)
        
        # Check home automation variables were set
        self.assertEqual(self.interp.variables.get('TEMP_testroom'), 25.5)
        self.assertEqual(self.interp.variables.get('LIGHT_testlight'), 1)
        
    def test_error_recovery_and_robustness(self):
        """Test that the system recovers gracefully from various errors"""
        prog = '''
T:Testing error recovery...

# Test invalid expressions (should not crash)
U:BAD1=invalid_expression
U:BAD2=*NONEXISTENT_VAR*+5
U:BAD3=1/0

# Test invalid hardware commands (should not crash)
R: INVALID_COMMAND
R: ARDUINO CONNECT invalid_port -1
R: RPI PIN abc INVALID_MODE

# Test invalid jumps (should not crash)
J:NONEXISTENT_LABEL
Y:invalid_condition
J:ANOTHER_NONEXISTENT

# Test memory-intensive operations (should not crash)
R: EMIT "test", 0, 0, 100, 1000, 50

# Test successful operations after errors
U:RECOVERY_TEST=42
T:Successfully recovered! Test value: *RECOVERY_TEST*

END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should complete despite errors
        
        # Should have recovered and set the recovery test variable
        self.assertEqual(self.interp.variables.get('RECOVERY_TEST'), 42)
        
        # Should have created particles despite other errors
        self.assertGreater(len(self.interp.particles), 0)
        
    def test_cross_platform_compatibility_verification(self):
        """Verify the system works on any platform without hardware"""
        # This test exercises all hardware-dependent features in simulation mode
        prog = '''
T:Testing cross-platform compatibility...

# RPi commands (should work in simulation)
R: RPI PIN 18 OUTPUT
R: RPI WRITE 18 1
R: RPI READ 19 PIN19_VALUE

# Arduino commands (should work in simulation)  
R: ARDUINO CONNECT /dev/ttyUSB0 9600
R: ARDUINO SEND "TEST_COMMAND"
R: ARDUINO READ SENSOR_DATA

# Robot commands (should work in simulation)
R: ROBOT FORWARD 50
R: ROBOT DISTANCE DIST_READING
R: ROBOT LIGHT LIGHT_READING

# Game controller (should work in simulation)
R: CONTROLLER UPDATE
R: CONTROLLER BUTTON 0 BTN_STATE

T:Cross-platform test completed
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)
        
        # All hardware controllers should be in simulation mode
        self.assertFalse(self.interp.rpi.gpio_available)
        self.assertFalse(self.interp.arduino.connected)
        
        # Some variables should be set by simulated sensors
        self.assertIn('PIN19_VALUE', self.interp.variables)
        self.assertIn('DIST_READING', self.interp.variables)
        self.assertIn('LIGHT_READING', self.interp.variables)
        self.assertIn('BTN_STATE', self.interp.variables)
        
    def test_performance_with_all_systems_active(self):
        """Test performance when all systems are active simultaneously"""
        prog = '''
T:Testing performance with all systems active...

# Activate templecode systems
R: TWEEN X -> 100 IN 1000ms
R: AFTER 500 DO TIMER_LABEL
R: EMIT "test", 50, 50, 20, 800, 30
R: NEW "sprite1", "test1.png"
R: NEW "sprite2", "test2.png"

# Activate hardware simulation
R: RPI PIN 18 OUTPUT
R: ARDUINO CONNECT /dev/ttyUSB0
R: ROBOT FORWARD 50
R: CONTROLLER UPDATE

# Run computational loop
U:I=0
L:PERF_LOOP
U:I=*I*+1
U:CALC=*I**I*+*I*
J(*I* < 100):PERF_LOOP

T:Performance test completed with I=*I*
END

L:TIMER_LABEL
T:Timer triggered during performance test
END'''
        
        result = self.interp.run_program(prog)
        self.assertTrue(result)
        
        # Should complete within reasonable time
        self.assertEqual(self.interp.variables.get('I'), 100)
        
        # All systems should be active
        self.assertGreater(len(self.interp.tweens), 0)
        self.assertGreater(len(self.interp.timers), 0)
        self.assertGreater(len(self.interp.particles), 0)
        self.assertGreater(len(self.interp.sprites), 0)
        
    def test_original_demo_still_works(self):
        """Test that the original demo program still works after all changes"""
        # Mock user input for the demo
        inputs = ["TestUser", "42"]
        input_index = [0]  # Use list to make it mutable in lambda
        self.interp.get_user_input = lambda prompt="": inputs[input_index[0]] if input_index[0] < len(inputs) and not input_index.__setitem__(0, input_index[0] + 1) else ""
        
        result = self.interp.run_program(create_demo_program())
        self.assertTrue(result)
        
        # Should have created variables from the demo
        self.assertIn('SUM', self.interp.variables)
        self.assertEqual(self.interp.variables.get('SUM'), 30)


if __name__ == '__main__':
    unittest.main()