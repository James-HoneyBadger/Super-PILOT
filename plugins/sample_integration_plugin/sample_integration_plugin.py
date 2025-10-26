"""
Sample Integration Plugin for Time Warp IDE

This plugin demonstrates how to integrate with external services
and APIs in Time Warp IDE. It provides sample integrations that
could connect to web services, databases, or other systems.
"""

from typing import Dict, Any
from core.plugin_system import IntegrationPlugin, PluginAPI, PluginMetadata


class SampleIntegrationPlugin(IntegrationPlugin):
    """Sample integration plugin that demonstrates external service integration."""

    def __init__(self, api: PluginAPI, metadata: PluginMetadata):
        super().__init__(api, metadata)

    def get_integrations(self) -> Dict[str, Any]:
        """Return integration configurations."""
        return {
            "sample_api": {
                "type": "api",
                "base_url": "https://api.example.com",
                "endpoints": {"status": "/status", "data": "/data"},
                "auth_required": False,
            },
            "sample_database": {
                "type": "database",
                "connection_string": "sample://localhost:5432/sampledb",
                "tables": ["users", "projects", "settings"],
            },
            "sample_webhook": {
                "type": "webhook",
                "url": "https://webhook.example.com/timewarp",
                "events": ["plugin_loaded", "command_executed"],
            },
        }

    def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            # Register event listeners for webhook integration
            self.api.subscribe_event("plugin_loaded", self._on_plugin_loaded)
            self.api.subscribe_event("command_executed", self._on_command_executed)

            self.api.log_info("Sample Integration Plugin initialized")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to initialize Sample Integration Plugin: {e}")
            return False

    def shutdown(self) -> bool:
        """Shutdown the plugin."""
        try:
            # Unregister event listeners
            self.api.unsubscribe_event("plugin_loaded", self._on_plugin_loaded)
            self.api.unsubscribe_event("command_executed", self._on_command_executed)

            self.api.log_info("Sample Integration Plugin shutdown")
            return True
        except Exception as e:
            self.api.log_error(f"Failed to shutdown Sample Integration Plugin: {e}")
            return False

    def _on_plugin_loaded(self, plugin_name: str, **kwargs):
        """Handle plugin loaded events."""
        self.api.log_info(f"Integration: Plugin '{plugin_name}' was loaded")
        # In a real implementation, this could send data to external services

    def _on_command_executed(self, language: str, command: str, **kwargs):
        """Handle command executed events."""
        self.api.log_info(
            f"Integration: Command executed in {language}: {command[:50]}..."
        )
        # In a real implementation, this could log to external
        # monitoring systems
