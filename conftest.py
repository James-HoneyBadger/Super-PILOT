"""
pytest configuration and fixtures for TempleCode testing framework
"""

import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch
from pathlib import Path

# Add TempleCode to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Super_PILOT import TempleCodeInterpreter, TempleCodeII
import tkinter as tk


@pytest.fixture
def interpreter():
    """Create a clean TempleCode interpreter instance for testing"""
    interp = TempleCodeInterpreter()
    interp.output_widget = None  # Disable GUI output for testing
    return interp


@pytest.fixture
def mock_output():
    """Mock output widget for capturing interpreter output"""
    mock_widget = Mock()
    mock_widget.insert = Mock()
    mock_widget.config = Mock()
    mock_widget.see = Mock()
    return mock_widget


@pytest.fixture
def headless_ide():
    """Create a headless IDE instance for UI testing (no actual window)"""
    with patch("tkinter.Tk") as mock_tk:
        mock_root = Mock()
        mock_tk.return_value = mock_root

        # Mock common tkinter methods
        mock_root.title = Mock()
        mock_root.geometry = Mock()
        mock_root.configure = Mock()
        mock_root.winfo_children = Mock(return_value=[])
        mock_root.after = Mock()
        mock_root.clipboard_clear = Mock()
        mock_root.clipboard_append = Mock()

        with patch("TempleCode.ttk.Style"):
            ide = TempleCodeII(mock_root)
            return ide


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for testing file operations"""
    temp_dir = tempfile.mkdtemp(prefix="templecode_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_pilot_program():
    """Sample PILOT program for testing"""
    return """T:Welcome to TempleCode!
T:What's your name?
A:NAME
T:Hello *NAME*!
U:AGE=0
T:How old are you?
A:AGE
C:*AGE*<18
Y:T:You're quite young!
N:T:You're an adult!
END"""


@pytest.fixture
def sample_logo_program():
    """Sample Logo program for testing"""
    return """FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90"""


@pytest.fixture
def sample_basic_program():
    """Sample BASIC program for testing"""
    return """10 LET X = 100
20 LET Y = 50
30 PRINT "Drawing square with side"; X
40 FORWARD X
50 RIGHT 90
60 FORWARD X
70 RIGHT 90
80 FORWARD X
90 RIGHT 90
100 FORWARD X"""


@pytest.fixture
def mock_hardware():
    """Mock hardware components for testing hardware integration"""
    hardware_mocks = {"arduino": Mock(), "rpi": Mock(), "sensors": Mock()}

    # Configure Arduino mock
    hardware_mocks["arduino"].connect = Mock(return_value=True)
    hardware_mocks["arduino"].disconnect = Mock()
    hardware_mocks["arduino"].send_command = Mock()
    hardware_mocks["arduino"].read_sensor = Mock(return_value=42)

    # Configure RPi mock
    hardware_mocks["rpi"].setup_pin = Mock()
    hardware_mocks["rpi"].digital_write = Mock()
    hardware_mocks["rpi"].digital_read = Mock(return_value=1)
    hardware_mocks["rpi"].cleanup = Mock()

    # Configure sensors mock
    hardware_mocks["sensors"].read_temperature = Mock(return_value=25.5)
    hardware_mocks["sensors"].read_humidity = Mock(return_value=60.0)
    hardware_mocks["sensors"].read_distance = Mock(return_value=15.2)

    return hardware_mocks


@pytest.fixture(autouse=True)
def cleanup_interpreter_state():
    """Ensure clean state between tests"""
    yield
    # Clean up any global state or side effects


class TestCase:
    """Base test case with utility methods"""

    def run_program_and_capture_output(self, interpreter, program):
        """Helper to run program and capture all output"""
        captured_output = []

        # Mock the log_output method to capture output
        original_log_output = interpreter.log_output

        def mock_log_output(text):
            captured_output.append(str(text))

        interpreter.log_output = mock_log_output

        try:
            result = interpreter.run_program(program)
            return result, "\n".join(captured_output)
        finally:
            interpreter.log_output = original_log_output

    def assert_variables_equal(self, interpreter, expected_vars):
        """Assert that interpreter variables match expected values"""
        for var_name, expected_value in expected_vars.items():
            actual_value = interpreter.variables.get(var_name)
            assert (
                actual_value == expected_value
            ), f"Variable {var_name}: expected {expected_value}, got {actual_value}"

    def assert_turtle_position(
        self, interpreter, expected_x, expected_y, expected_heading=None
    ):
        """Assert turtle position and optional heading"""
        if hasattr(interpreter, "turtle_x") and hasattr(interpreter, "turtle_y"):
            assert (
                abs(interpreter.turtle_x - expected_x) < 0.1
            ), f"Turtle X: expected {expected_x}, got {interpreter.turtle_x}"
            assert (
                abs(interpreter.turtle_y - expected_y) < 0.1
            ), f"Turtle Y: expected {expected_y}, got {interpreter.turtle_y}"

            if expected_heading is not None and hasattr(interpreter, "turtle_heading"):
                # Normalize headings to 0-360 range
                actual_heading = interpreter.turtle_heading % 360
                expected_heading = expected_heading % 360
                assert (
                    abs(actual_heading - expected_heading) < 0.1
                ), f"Turtle heading: expected {expected_heading}, got {actual_heading}"
