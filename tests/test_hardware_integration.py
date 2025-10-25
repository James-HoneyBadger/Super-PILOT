#!/usr/bin/env python3
"""
Test hardware integration features including Arduino, RPi, sensors, robots, and game controllers.
All tests run in simulation mode without requiring actual hardware.
"""

import unittest
from Time_Warp import TimeWarpInterpreter


class HardwareIntegrationTests(unittest.TestCase):
    def setUp(self):
        """Set up interpreter for each test"""
        self.interp = TimeWarpInterpreter()
        self.interp.output_widget = None

    def test_arduino_simulation_mode(self):
        """Test Arduino controller works in simulation mode"""
        # Test Arduino connection simulation
        self.assertTrue(hasattr(self.interp, "arduino"))
        self.assertIsNotNone(self.interp.arduino)

        # Arduino should work in simulation mode
        self.assertFalse(self.interp.arduino.connected)  # Should start disconnected

    def test_rpi_simulation_mode(self):
        """Test Raspberry Pi controller works in simulation mode"""
        # Test RPi controller exists and is in simulation mode
        self.assertTrue(hasattr(self.interp, "rpi"))
        self.assertIsNotNone(self.interp.rpi)
        self.assertFalse(self.interp.rpi.gpio_available)  # Should be in simulation mode

    def test_arduino_runtime_commands(self):
        """Test Arduino R: runtime commands in simulation"""
        prog = """
R: ARDUINO CONNECT /dev/ttyUSB0 9600
R: ARDUINO SEND LED_ON
R: ARDUINO READ SENSOR_VALUE
T:Arduino test completed
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Should have attempted Arduino operations (in simulation)
        self.assertEqual(
            self.interp.variables.get("SENSOR_VALUE", "NOTSET"), "NOTSET"
        )  # Won't be set in simulation

    def test_rpi_runtime_commands(self):
        """Test Raspberry Pi R: runtime commands in simulation"""
        prog = """
R: RPI PIN 18 OUTPUT  
R: RPI WRITE 18 1
R: RPI READ 19 PIN19_VAL
T:RPi GPIO test completed  
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Should work in simulation mode
        self.assertEqual(
            self.interp.variables.get("PIN19_VAL", 0), 0
        )  # Default simulation value

    def test_robot_programming_interface(self):
        """Test robot programming commands via R: runtime commands"""
        prog = """
R: ROBOT FORWARD 100
R: ROBOT LEFT 90  
R: ROBOT DISTANCE DIST_VAL
R: ROBOT LIGHT LIGHT_VAL
ROBOTSTOP
T:Robot test completed
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Robot interface should exist
        self.assertTrue(hasattr(self.interp, "robot"))

        # Variables should be set by sensor reads (simulated values)
        self.assertIn("DIST_VAL", self.interp.variables)
        self.assertIn("LIGHT_VAL", self.interp.variables)

    def test_robot_runtime_commands(self):
        """Test robot R: runtime commands"""
        prog = """
R: ROBOT FORWARD 75
R: ROBOT DISTANCE DIST
R: ROBOT LIGHT BRIGHTNESS  
T:Robot runtime test completed
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Should have set sensor variables
        self.assertIn("DIST", self.interp.variables)
        self.assertIn("BRIGHTNESS", self.interp.variables)

    def test_game_controller_commands(self):
        """Test game controller integration"""
        prog = """
CONTROLLERUPDATE
R: CONTROLLER BUTTON 1 BTN1_STATE
R: CONTROLLER AXIS 0 STICK_X
T:Controller test completed
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Controller variables should be set (simulated values)
        self.assertIn("BTN1_STATE", self.interp.variables)
        self.assertIn("STICK_X", self.interp.variables)

    def test_sensor_data_visualization(self):
        """Test sensor data visualization features"""
        prog = """
# First we need turtle graphics for sensor visualization
CLEARSCREEN
R: SENSOR ADD Temperature 25.5
R: SENSOR ADD Humidity 60.0
R: SENSOR ADD Pressure 1013.25
SENSORCHART 10 10 300 200
T:Sensor visualization test completed
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Sensor visualizer should be available after turtle graphics init
        # (This tests the integration without requiring actual GUI)

    def test_home_automation_simulation(self):
        """Test home automation commands"""
        prog = """
R: HOME LIGHT livingroom ON
R: HOME LIGHT bedroom OFF  
R: HOME TEMP kitchen 22.5
R: HOME TEMP bedroom 20.0
T:Home automation test completed
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Home automation should set variables
        self.assertEqual(self.interp.variables.get("LIGHT_livingroom"), 1)
        self.assertEqual(self.interp.variables.get("LIGHT_bedroom"), 0)
        self.assertEqual(self.interp.variables.get("TEMP_kitchen"), 22.5)
        self.assertEqual(self.interp.variables.get("TEMP_bedroom"), 20.0)

    def test_hardware_error_handling(self):
        """Test that hardware commands handle errors gracefully"""
        prog = """
# These should not crash even with invalid parameters
R: ARDUINO CONNECT invalid_port 0
R: RPI PIN 999 INVALID_MODE
R: ROBOT FORWARD invalid_speed
T:Error handling test completed
END"""

        result = self.interp.run_program(prog)
        self.assertTrue(result)  # Should complete without crashing

    def test_cross_platform_compatibility(self):
        """Test that hardware integration works across platforms"""
        # All hardware controllers should initialize without importing actual hardware
        self.assertIsNotNone(self.interp.arduino)
        self.assertIsNotNone(self.interp.rpi)
        self.assertIsNotNone(self.interp.robot)
        self.assertIsNotNone(self.interp.controller)

        # RPi.GPIO should be safely handled
        self.assertFalse(
            self.interp.rpi.gpio_available
        )  # Should be False on non-RPi systems

        # Arduino should work without pyserial
        self.assertFalse(self.interp.arduino.connected)  # Should start disconnected

    def test_hardware_variables_persist(self):
        """Test hardware-set variables persist in single program run"""
        prog = """
R: HOME TEMP living 25.0
T:First command sets temperature
T:Temperature is *TEMP_living* degrees
U:CHECK=*TEMP_living*+5
T:Check value: *CHECK*
END"""

        # Run program
        result = self.interp.run_program(prog)
        self.assertTrue(result)

        # Variables should be set and accessible within same program
        self.assertEqual(self.interp.variables.get("TEMP_living"), 25.0)
        self.assertEqual(self.interp.variables.get("CHECK"), 30.0)


if __name__ == "__main__":
    unittest.main()
