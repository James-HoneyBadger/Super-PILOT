"""
Sample Language Plugin for Time Warp IDE

This plugin demonstrates how to add a new programming language
to Time Warp IDE. It implements a simple "Hello World" language
that prints messages.
"""

from typing import List
from core.plugin_system import LanguagePlugin


class SampleLanguage(LanguagePlugin):
    """Sample language plugin that demonstrates basic language
    implementation."""

    def get_language_name(self) -> str:
        """Return the name of the language this plugin supports."""
        return "Sample"

    def get_file_extensions(self) -> List[str]:
        """Return file extensions associated with this language."""
        return [".sample", ".spl"]

    def create_executor(self):
        """Create and return a language executor instance."""
        return SampleExecutor()

    def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            self.api.log_info("Sample Language Plugin initialized")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to initialize Sample Language Plugin: {e}")
            return False

    def shutdown(self) -> bool:
        """Shutdown the plugin."""
        try:
            self.api.log_info("Sample Language Plugin shutdown")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to shutdown Sample Language Plugin: {e}")
            return False


class SampleExecutor:
    """Executor for the Sample language."""

    def execute_command(self, command: str) -> str:
        """
        Execute a command in the Sample language.

        Supported commands:
        - HELLO: Print a greeting
        - PRINT <message>: Print a custom message
        - VERSION: Show plugin version
        """
        command = command.strip().upper()

        if command == "HELLO":
            return "Hello from Sample Language Plugin! 🎉"

        elif command.startswith("PRINT "):
            message = command[6:]  # Remove "PRINT "
            return f"Sample Language says: {message}"

        elif command == "VERSION":
            return "Sample Language Plugin v1.0.0"

        else:
            return (
                f"Unknown command: {command}. " "Try HELLO, PRINT <message>, or VERSION"
            )

