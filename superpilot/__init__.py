"""
TempleCode - A multi-language educational programming environment
Supports PILOT, BASIC, and Logo with turtle graphics and hardware integration
"""

__version__ = "3.0.0"

# Note: TempleCodeInterpreter is currently in TempleCode.py as monolithic
# Future versions may extract it to templecode.core.interpreter for modularity
from superpilot.runtime.templecode import (
    Tween, Timer, Particle, EASE_FUNCTIONS
)
from superpilot.runtime.hardware import (
    ArduinoController,
    RPiController,
    IoTDeviceManager,
    SmartHomeSystem,
)
from superpilot.runtime.audio import AudioMixer

__all__ = [
    # "TempleCodeInterpreter",  # Currently in TempleCode.py
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
