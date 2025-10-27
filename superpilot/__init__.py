"""
SuperPILOT - A multi-language educational programming environment
Supports PILOT, BASIC, and Logo with turtle graphics and hardware integration
"""

__version__ = "2.0.0"

# Note: SuperPILOTInterpreter still in Super_PILOT.py until extraction complete
# from superpilot.core.interpreter import SuperPILOTInterpreter
from superpilot.runtime.templecode import Tween, Timer, Particle, EASE_FUNCTIONS
from superpilot.runtime.hardware import (
    ArduinoController,
    RPiController,
    IoTDeviceManager,
    SmartHomeSystem,
)
from superpilot.runtime.audio import AudioMixer

__all__ = [
    # "SuperPILOTInterpreter",  # TODO: uncomment after extraction
    "Tween",
    "Timer",
    "Particle",
    "EASE_FUNCTIONS",
    "ArduinoController",
    "RPiController",
    "IoTDeviceManager",
    "SmartHomeSystem",
    "AudioMixer",
]
