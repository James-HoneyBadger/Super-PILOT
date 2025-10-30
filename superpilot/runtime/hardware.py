"""
Hardware integration for TempleCode
Provides Arduino, Raspberry Pi, IoT, and Smart Home controllers
"""


class ArduinoController:
    """Arduino hardware controller with simulation support"""

    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode
        self.connected = False


class RPiController:
    """Raspberry Pi hardware controller with simulation support"""

    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode
        self.gpio_available = False
        self.connected = False


class IoTDeviceManager:
    """Manage IoT devices with simulation fallback"""

    def __init__(self):
        self.devices = []
        self.simulation_mode = True


class SmartHomeSystem:
    """Smart home automation system"""

    def __init__(self):
        self.automation_rules = []
        self.devices = {}
        self.simulation_mode = True
