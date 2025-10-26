"""
Sample UI Plugin for Time Warp IDE

This plugin demonstrates how to add UI components to Time Warp IDE.
It adds a simple status panel and a sample button.
"""

from typing import Dict, Any
from core.plugin_system import UIPlugin


class SampleUIPlugin(UIPlugin):
    """Sample UI plugin that demonstrates adding UI components."""

    def create_ui_components(self) -> Dict[str, Any]:
        """Create and return UI components to be added to the IDE."""
        components = {}

        # Create a simple status panel component
        components["sample_status_panel"] = {
            "type": "panel",
            "title": "Sample Plugin Status",
            "content": "Plugin loaded successfully! 🎨",
            "position": "bottom",
        }

        # Create a sample button component
        components["sample_button"] = {
            "type": "button",
            "label": "Sample Action",
            "command": "sample_plugin_action",
            "tooltip": "Click me for a sample action!",
        }

        return components

    def _sample_button_callback(self):
        """Callback for the sample button."""
        self.api.log_info("Sample button clicked!")
        # In a real implementation, this could show a dialog
        # or perform an action

    def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            self.api.log_info("Sample UI Plugin initialized")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to initialize Sample UI Plugin: {e}")
            return False

    def shutdown(self) -> bool:
        """Shutdown the plugin."""
        try:
            self.api.log_info("Sample UI Plugin shutdown")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to shutdown Sample UI Plugin: {e}")
            return False
