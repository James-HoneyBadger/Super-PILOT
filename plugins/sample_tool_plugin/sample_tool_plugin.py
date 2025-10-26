"""
Sample Tool Plugin for Time Warp IDE

This plugin demonstrates how to add tools and utilities to Time Warp IDE.
It provides sample utility functions that can be used by other plugins
or the IDE itself.
"""

from typing import Dict, Callable, Any
from core.plugin_system import ToolPlugin


class SampleToolPlugin(ToolPlugin):
    """Sample tool plugin that demonstrates adding utility functions."""

    def get_tools(self) -> Dict[str, Callable]:
        """Return a dictionary of tool functions."""
        return {
            "sample_calculator": self._sample_calculator,
            "sample_formatter": self._sample_formatter,
            "sample_validator": self._sample_validator,
        }

    def _sample_calculator(self, a: float, b: float, operation: str = "add") -> float:
        """A simple calculator tool."""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b if b != 0 else 0
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def _sample_formatter(self, text: str, format_type: str = "upper") -> str:
        """A text formatting tool."""
        if format_type == "upper":
            return text.upper()
        elif format_type == "lower":
            return text.lower()
        elif format_type == "title":
            return text.title()
        else:
            return text

    def _sample_validator(self, value: Any, validation_type: str = "string") -> bool:
        """A value validation tool."""
        if validation_type == "string":
            return isinstance(value, str)
        elif validation_type == "number":
            return isinstance(value, (int, float))
        elif validation_type == "positive":
            return isinstance(value, (int, float)) and value > 0
        else:
            return False

    def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            self.api.log_info("Sample Tool Plugin initialized")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to initialize Sample Tool Plugin: {e}")
            return False

    def shutdown(self) -> bool:
        """Shutdown the plugin."""
        try:
            self.api.log_info("Sample Tool Plugin shutdown")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to shutdown Sample Tool Plugin: {e}")
            return False
