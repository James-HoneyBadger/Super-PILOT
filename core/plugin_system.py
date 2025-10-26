"""
Plugin System for Time Warp IDE

A robust and extensible plugin architecture that allows developers to extend
the functionality of Time Warp IDE with custom languages, UI components,
tools, and integrations.
"""

import sys
import importlib
import inspect
import json
import threading
import datetime
from typing import Dict, List, Any, Optional, Type, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PluginMetadata:
    """Metadata for a plugin"""

    name: str
    version: str
    description: str
    author: str
    plugin_type: str
    dependencies: List[str] = field(default_factory=list)
    config_schema: Dict[str, Any] = field(default_factory=dict)
    entry_point: str = ""
    min_ide_version: str = "1.0.0"
    max_ide_version: str = "*"
    license: str = "MIT"
    homepage: str = ""
    repository: str = ""


class PluginError(Exception):
    """Base exception for plugin-related errors"""

    pass


class PluginLoadError(PluginError):
    """Exception raised when a plugin fails to load"""

    pass


class PluginValidationError(PluginError):
    """Exception raised when plugin validation fails"""

    pass


class PluginInitializationError(PluginError):
    """Exception raised when plugin initialization fails"""

    pass


class PluginShutdownError(PluginError):
    """Exception raised when plugin shutdown fails"""

    pass


class PluginDependencyError(PluginError):
    """Exception raised when plugin dependencies are not satisfied"""

    pass


class PluginConfigurationError(PluginError):
    """Exception raised when plugin configuration operations fail"""

    pass


class PluginResourceError(PluginError):
    """Exception raised when plugin resource operations fail"""

    pass


class PluginEventError(PluginError):
    """Exception raised when plugin event operations fail"""

    pass


class PluginTimeoutError(PluginError):
    """Exception raised when plugin operations timeout"""

    pass


class PluginSecurityError(PluginError):
    """Exception raised when plugin security violations occur"""

    pass


class PluginAPI:
    """API interface provided to plugins"""

    def __init__(self, ide_instance):
        self.ide = ide_instance

    # Core IDE access
    @property
    def interpreter(self):
        """Access to the main interpreter"""
        return self.ide.interpreter

    @property
    def ui(self):
        """Access to the UI system"""
        return self.ide.ui

    @property
    def config(self):
        """Access to configuration system"""
        return self.ide.config

    # Plugin communication
    def emit_event(self, event_name: str, **kwargs):
        """Emit an event to other plugins"""
        if not isinstance(event_name, str) or not event_name.strip():
            raise PluginEventError("Event name must be a non-empty string")
        self.ide.plugin_manager.emit_event(event_name, **kwargs)

    def subscribe_event(self, event_name: str, callback: Callable):
        """Subscribe to an event"""
        if not isinstance(event_name, str) or not event_name.strip():
            raise PluginEventError("Event name must be a non-empty string")
        if not callable(callback):
            raise PluginEventError("Callback must be callable")
        self.ide.plugin_manager.subscribe_event(event_name, callback)

    def unsubscribe_event(self, event_name: str, callback: Callable):
        """Unsubscribe from an event"""
        if not isinstance(event_name, str) or not event_name.strip():
            raise PluginEventError("Event name must be a non-empty string")
        if not callable(callback):
            raise PluginEventError("Callback must be callable")
        self.ide.plugin_manager.unsubscribe_event(event_name, callback)

    # Resource management
    def register_resource(self, resource_type: str, name: str, resource: Any):
        """Register a resource"""
        if not isinstance(resource_type, str) or not resource_type.strip():
            raise PluginResourceError("Resource type must be a non-empty string")
        if not isinstance(name, str) or not name.strip():
            raise PluginResourceError("Resource name must be a non-empty string")
        self.ide.plugin_manager.register_resource(resource_type, name, resource)

    def unregister_resource(self, resource_type: str, name: str):
        """Unregister a resource"""
        if not isinstance(resource_type, str) or not resource_type.strip():
            raise PluginResourceError("Resource type must be a non-empty string")
        if not isinstance(name, str) or not name.strip():
            raise PluginResourceError("Resource name must be a non-empty string")
        self.ide.plugin_manager.unregister_resource(resource_type, name)

    def get_resource(self, resource_type: str, name: str) -> Any:
        """Get a registered resource"""
        if not isinstance(resource_type, str) or not resource_type.strip():
            raise PluginResourceError("Resource type must be a non-empty string")
        if not isinstance(name, str) or not name.strip():
            raise PluginResourceError("Resource name must be a non-empty string")
        return self.ide.plugin_manager.get_resource(resource_type, name)

    # Logging
    def log_info(self, message: str):
        """Log an info message"""
        if hasattr(self.ide, "log_output"):
            self.ide.log_output(f"[Plugin] {message}")
        else:
            print(f"[Plugin] {message}")

    def log_warning(self, message: str):
        """Log a warning message"""
        if hasattr(self.ide, "log_output"):
            self.ide.log_output(f"[Plugin WARNING] {message}")
        else:
            print(f"[Plugin WARNING] {message}")

    def log_error(self, message: str):
        """Log an error message"""
        if hasattr(self.ide, "log_output"):
            self.ide.log_output(f"[Plugin ERROR] {message}")
        else:
            print(f"[Plugin ERROR] {message}")


class Plugin(ABC):
    """Base class for all plugins"""

    def __init__(self, api: PluginAPI, metadata: PluginMetadata):
        self.api = api
        self.metadata = metadata
        self.config: Dict[str, Any] = {}
        self._initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin. Return True if successful."""
        pass

    @abstractmethod
    def shutdown(self) -> bool:
        """Shutdown the plugin. Return True if successful."""
        pass

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(key, default)

    def set_config_value(self, key: str, value: Any):
        """Set a configuration value"""
        self.config[key] = value

    def save_config(self):
        """Save plugin configuration"""
        config_path = self._get_config_path()
        try:
            with open(config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.api.log_error(f"Failed to save config for {self.metadata.name}: {e}")

    def load_config(self):
        """Load plugin configuration"""
        config_path = self._get_config_path()
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    self.config = json.load(f)
            except Exception as e:
                self.api.log_error(
                    f"Failed to load config for {self.metadata.name}: {e}"
                )
                self.config = {}

    def _get_config_path(self) -> Path:
        """Get the path to the plugin's config file"""
        config_dir = Path.home() / ".time_warp" / "plugins" / self.metadata.name
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"


class LanguagePlugin(Plugin):
    """Plugin that adds support for a new programming language"""

    @abstractmethod
    def get_language_name(self) -> str:
        """Return the name of the language this plugin supports"""
        pass

    @abstractmethod
    def get_file_extensions(self) -> List[str]:
        """Return file extensions associated with this language"""
        pass

    @abstractmethod
    def create_executor(self):
        """Create and return a language executor instance"""
        pass

    def initialize(self) -> bool:
        """Initialize the language plugin"""
        try:
            # Register the language with the interpreter
            executor = self.create_executor()
            # Store executor in interpreter for plugin languages
            if not hasattr(self.api.interpreter, "plugin_executors"):
                self.api.interpreter.plugin_executors = {}
            self.api.interpreter.plugin_executors[self.get_language_name()] = executor

            # Register file extensions
            for ext in self.get_file_extensions():
                self.api.register_resource(
                    "file_extension", ext, self.get_language_name()
                )

            self.api.log_info(f"Language plugin '{self.metadata.name}' initialized")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to initialize language plugin '{self.metadata.name}': {e}"
            )
            return False

    def shutdown(self) -> bool:
        """Shutdown the language plugin"""
        try:
            # Unregister the language
            if hasattr(self.api.interpreter, "plugin_executors"):
                if self.get_language_name() in self.api.interpreter.plugin_executors:
                    del self.api.interpreter.plugin_executors[self.get_language_name()]

            # Unregister file extensions
            for ext in self.get_file_extensions():
                self.api.unregister_resource("file_extension", ext)

            self.api.log_info(f"Language plugin '{self.metadata.name}' shutdown")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to shutdown language plugin '{self.metadata.name}': {e}"
            )
            return False


class UIPlugin(Plugin):
    """Plugin that extends the user interface"""

    @abstractmethod
    def create_ui_components(self) -> Dict[str, Any]:
        """Create and return UI components to be added to the IDE"""
        pass

    def initialize(self) -> bool:
        """Initialize the UI plugin"""
        try:
            components = self.create_ui_components()

            # Register UI components
            for component_name, component in components.items():
                self.api.register_resource("ui_component", component_name, component)
                # Add to UI if method exists
                if hasattr(self.api.ui, "add_plugin_component"):
                    self.api.ui.add_plugin_component(component_name, component)

            self.api.log_info(f"UI plugin '{self.metadata.name}' initialized")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to initialize UI plugin '{self.metadata.name}': {e}"
            )
            return False

    def shutdown(self) -> bool:
        """Shutdown the UI plugin"""
        try:
            # Remove UI components
            if hasattr(self.api.ui, "remove_plugin_components"):
                self.api.ui.remove_plugin_components(self.metadata.name)

            # Unregister components
            # Note: In a real implementation, we'd track registered components
            self.api.log_info(f"UI plugin '{self.metadata.name}' shutdown")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to shutdown UI plugin '{self.metadata.name}': {e}"
            )
            return False


class ToolPlugin(Plugin):
    """Plugin that adds tools and utilities"""

    @abstractmethod
    def get_tools(self) -> Dict[str, Callable]:
        """Return a dictionary of tool functions"""
        pass

    def initialize(self) -> bool:
        """Initialize the tool plugin"""
        try:
            tools = self.get_tools()

            # Register tools
            for tool_name, tool_func in tools.items():
                self.api.register_resource("tool", tool_name, tool_func)
                # Add to tools menu if available
                if hasattr(self.api.ui, "add_tool"):
                    self.api.ui.add_tool(tool_name, tool_func)

            self.api.log_info(f"Tool plugin '{self.metadata.name}' initialized")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to initialize tool plugin '{self.metadata.name}': {e}"
            )
            return False

    def shutdown(self) -> bool:
        """Shutdown the tool plugin"""
        try:
            # Remove tools from UI
            if hasattr(self.api.ui, "remove_tools"):
                self.api.ui.remove_tools(self.metadata.name)

            self.api.log_info(f"Tool plugin '{self.metadata.name}' shutdown")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to shutdown tool plugin '{self.metadata.name}': {e}"
            )
            return False


class IntegrationPlugin(Plugin):
    """Plugin that integrates with external services"""

    @abstractmethod
    def get_integrations(self) -> Dict[str, Any]:
        """Return integration configurations"""
        pass

    def initialize(self) -> bool:
        """Initialize the integration plugin"""
        try:
            integrations = self.get_integrations()

            # Register integrations
            for integration_name, integration_config in integrations.items():
                self.api.register_resource(
                    "integration", integration_name, integration_config
                )

            self.api.log_info(f"Integration plugin '{self.metadata.name}' initialized")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to initialize integration plugin '{self.metadata.name}': {e}"
            )
            return False

    def shutdown(self) -> bool:
        """Shutdown the integration plugin"""
        try:
            self.api.log_info(f"Integration plugin '{self.metadata.name}' shutdown")
            return True
        except Exception as e:
            self.api.log_error(
                f"Failed to shutdown integration plugin '{self.metadata.name}': {e}"
            )
            return False


class PluginManager:
    """Manages plugin discovery, loading, and lifecycle"""

    def __init__(self, ide_instance):
        self.ide = ide_instance
        self.api = PluginAPI(ide_instance)
        self.plugins: Dict[str, Plugin] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.event_listeners: Dict[str, List[Callable]] = {}
        self.plugin_dirs = [
            Path.home() / ".time_warp" / "plugins",
            Path(__file__).parent.parent / "plugins",
        ]

        # Global configuration
        self.global_config: Dict[str, Any] = {}
        self._load_global_config()

        # Timeout settings
        self.init_timeout = self.global_config.get(
            "plugin_init_timeout", 30.0
        )  # seconds
        self.shutdown_timeout = self.global_config.get(
            "plugin_shutdown_timeout", 10.0
        )  # seconds

        # Error reporting
        self.error_reports: List[Dict[str, Any]] = []
        self.max_error_reports = self.global_config.get("max_error_reports", 100)

        # Recovery mechanisms
        self.operation_backups: Dict[str, Dict[str, Any]] = {}
        self.enable_recovery = self.global_config.get("enable_operation_recovery", True)

    def _run_with_timeout(self, func: Callable, timeout: float, *args, **kwargs) -> Any:
        """Run a function with a timeout"""
        result = [None]
        exception = [None]

        def target():
            try:
                result[0] = func(*args, **kwargs)
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            raise PluginTimeoutError(f"Operation timed out after {timeout} seconds")
        if exception[0]:
            raise exception[0]
        return result[0]

    def _get_global_config_path(self) -> Path:
        """Get the path to the global plugin configuration file"""
        config_dir = Path.home() / ".time_warp"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "plugin_config.json"

    def _load_global_config(self):
        """Load global plugin configuration"""
        config_path = self._get_global_config_path()
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    self.global_config = json.load(f)
            except Exception as e:
                self.api.log_error(f"Failed to load global plugin config: {e}")
                self.global_config = self._get_default_global_config()
        else:
            self.global_config = self._get_default_global_config()

    def _save_global_config(self):
        """Save global plugin configuration"""
        config_path = self._get_global_config_path()
        try:
            with open(config_path, "w") as f:
                json.dump(self.global_config, f, indent=2)
        except Exception as e:
            self.api.log_error(f"Failed to save global plugin config: {e}")

    def _get_default_global_config(self) -> Dict[str, Any]:
        """Get default global configuration"""
        return {
            "auto_load_plugins": True,
            "plugin_dirs": [
                str(Path.home() / ".time_warp" / "plugins"),
                str(Path(__file__).parent.parent / "plugins"),
            ],
            "disabled_plugins": [],
            "plugin_load_order": [],
            "config_backup_enabled": True,
            "max_config_backups": 5,
        }

    def get_global_config_value(self, key: str, default: Any = None) -> Any:
        """Get a global configuration value"""
        return self.global_config.get(key, default)

    def set_global_config_value(self, key: str, value: Any):
        """Set a global configuration value"""
        self.global_config[key] = value
        self._save_global_config()

    def add_plugin_directory(self, directory: str):
        """Add a custom plugin directory"""
        if directory not in self.global_config["plugin_dirs"]:
            self.global_config["plugin_dirs"].append(directory)
            self.plugin_dirs.append(Path(directory))
            self._save_global_config()

    def remove_plugin_directory(self, directory: str):
        """Remove a custom plugin directory"""
        if directory in self.global_config["plugin_dirs"]:
            self.global_config["plugin_dirs"].remove(directory)
            self.plugin_dirs = [Path(d) for d in self.global_config["plugin_dirs"]]
            self._save_global_config()

    def disable_plugin(self, plugin_name: str):
        """Disable a plugin from auto-loading"""
        if plugin_name not in self.global_config["disabled_plugins"]:
            self.global_config["disabled_plugins"].append(plugin_name)
            self._save_global_config()

    def enable_plugin(self, plugin_name: str):
        """Enable a plugin for auto-loading"""
        if plugin_name in self.global_config["disabled_plugins"]:
            self.global_config["disabled_plugins"].remove(plugin_name)
            self._save_global_config()

    def is_plugin_disabled(self, plugin_name: str) -> bool:
        """Check if a plugin is disabled"""
        return plugin_name in self.global_config["disabled_plugins"]

    def set_plugin_load_order(self, plugin_names: List[str]):
        """Set the order in which plugins should be loaded"""
        self.global_config["plugin_load_order"] = plugin_names
        self._save_global_config()

    def get_plugin_load_order(self) -> List[str]:
        """Get the configured plugin load order"""
        return self.global_config.get("plugin_load_order", [])

    def discover_plugins(self) -> List[Path]:
        """Discover plugin directories"""
        plugin_paths = []

        for plugin_dir in self.plugin_dirs:
            if plugin_dir.exists():
                for item in plugin_dir.iterdir():
                    if item.is_dir() and (item / "plugin.json").exists():
                        plugin_paths.append(item)

        return plugin_paths

    def load_plugin(self, plugin_path: Path) -> Optional[Plugin]:
        """Load a plugin from a directory"""
        plugin_name = "unknown"
        operation_id = (
            f"load_plugin_{plugin_path.name}_{datetime.datetime.now().timestamp()}"
        )

        # Backup current state
        self._backup_operation_state(operation_id)

        try:
            # Load metadata
            metadata_path = plugin_path / "plugin.json"
            if not metadata_path.exists():
                raise PluginLoadError(f"No plugin.json found in {plugin_path}")

            with open(metadata_path, "r") as f:
                metadata_dict = json.load(f)

            metadata = PluginMetadata(**metadata_dict)
            plugin_name = metadata.name

            # Validate metadata
            self._validate_metadata(metadata)

            # Check dependencies
            if not self._check_dependencies(metadata):
                raise PluginDependencyError(
                    f"Dependencies not satisfied for {metadata.name}"
                )

            # Load plugin module
            plugin_module = self._load_plugin_module(plugin_path, metadata)

            # Create plugin instance
            plugin_class = self._get_plugin_class(plugin_module, metadata)
            plugin = plugin_class(self.api, metadata)

            # Load configuration
            try:
                plugin.load_config()
            except Exception as e:
                self.api.log_warning(
                    f"Failed to load config for plugin '{plugin_name}': {e}"
                )
                # Continue with default config

            # Initialize plugin
            try:
                init_success = self._run_with_timeout(
                    plugin.initialize, self.init_timeout
                )
                if init_success:
                    self.plugins[metadata.name] = plugin
                    self.api.log_info(f"Plugin '{metadata.name}' loaded successfully")
                    # Clean up backup on success
                    self._cleanup_operation_backup(operation_id)
                    return plugin
                else:
                    raise PluginInitializationError(
                        f"Plugin '{metadata.name}' failed to initialize"
                    )
            except PluginTimeoutError:
                raise PluginInitializationError(
                    f"Plugin '{metadata.name}' initialization timed out after "
                    f"{self.init_timeout} seconds"
                )

        except PluginError as e:
            # Attempt recovery
            if self._restore_operation_state(operation_id):
                self.api.log_warning(
                    f"Recovered from failed plugin load for '{plugin_name}'"
                )
            # Record the error and re-raise
            self._record_error(
                "plugin_load",
                plugin_name,
                e,
                {
                    "plugin_path": str(plugin_path),
                    "metadata": metadata.__dict__ if "metadata" in locals() else None,
                },
            )
            raise
        except json.JSONDecodeError as e:
            # Attempt recovery
            self._restore_operation_state(operation_id)
            error = PluginLoadError(
                f"Invalid JSON in plugin.json for '{plugin_name}': {e}"
            )
            self._record_error(
                "json_parse", plugin_name, error, {"plugin_path": str(plugin_path)}
            )
            raise error
        except FileNotFoundError as e:
            # Attempt recovery
            self._restore_operation_state(operation_id)
            error = PluginLoadError(f"Plugin file not found: {e}")
            self._record_error(
                "file_not_found", plugin_name, error, {"plugin_path": str(plugin_path)}
            )
            raise error
        except ImportError as e:
            # Attempt recovery
            self._restore_operation_state(operation_id)
            error = PluginLoadError(
                f"Failed to import plugin module for '{plugin_name}': {e}"
            )
            self._record_error(
                "import_error", plugin_name, error, {"plugin_path": str(plugin_path)}
            )
            raise error
        except Exception as e:
            # Attempt recovery
            self._restore_operation_state(operation_id)
            # Catch any other unexpected errors
            import traceback

            error_details = traceback.format_exc()
            error = PluginLoadError(
                f"Unexpected error loading plugin from {plugin_path}: {e}\n"
                f"Stack trace:\n{error_details}"
            )
            self._record_error(
                "unexpected_error",
                plugin_name,
                error,
                {"plugin_path": str(plugin_path)},
            )
            raise error

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        if plugin_name not in self.plugins:
            raise PluginLoadError(f"Plugin '{plugin_name}' is not loaded")

        plugin = self.plugins[plugin_name]

        try:
            # Shutdown plugin
            try:
                shutdown_success = self._run_with_timeout(
                    plugin.shutdown, self.shutdown_timeout
                )
                if not shutdown_success:
                    raise PluginShutdownError(
                        f"Plugin '{plugin_name}' failed to shutdown properly"
                    )
            except PluginTimeoutError:
                raise PluginShutdownError(
                    f"Plugin '{plugin_name}' shutdown timed out after "
                    f"{self.shutdown_timeout} seconds"
                )

            # Save configuration
            try:
                plugin.save_config()
            except Exception as e:
                self.api.log_warning(
                    f"Failed to save config for plugin '{plugin_name}': {e}"
                )
                # Continue with unload despite config save failure

            # Remove from registry
            del self.plugins[plugin_name]

            self.api.log_info(f"Plugin '{plugin_name}' unloaded successfully")
            return True

        except PluginShutdownError as e:
            # Plugin failed to shutdown cleanly, but we'll still remove it from registry
            # to prevent it from being in an inconsistent state
            self._record_error(
                "plugin_shutdown", plugin_name, e, {"force_unload": True}
            )
            self.api.log_error(
                f"Forcing unload of plugin '{plugin_name}' due to shutdown failure"
            )
            if plugin_name in self.plugins:
                del self.plugins[plugin_name]
            raise
        except Exception as e:
            # Unexpected error during unload
            import traceback

            error_details = traceback.format_exc()
            self._record_error("plugin_unload", plugin_name, e, {"force_unload": True})
            self.api.log_error(
                f"Unexpected error unloading plugin '{plugin_name}': {e}\n"
                f"Stack trace:\n{error_details}"
            )
            # Force removal from registry even on unexpected errors
            if plugin_name in self.plugins:
                del self.plugins[plugin_name]
            raise PluginShutdownError(f"Failed to unload plugin '{plugin_name}': {e}")

    def load_all_plugins(self) -> int:
        """Load all discovered plugins.

        Return number of successfully loaded plugins."""
        plugin_paths = self.discover_plugins()
        loaded_count = 0

        for plugin_path in plugin_paths:
            if self.load_plugin(plugin_path):
                loaded_count += 1

        self.api.log_info(f"Loaded {loaded_count} out of {len(plugin_paths)} plugins")
        return loaded_count

    def unload_all_plugins(self) -> int:
        """Unload all plugins.

        Return number of successfully unloaded plugins."""
        plugin_names = list(self.plugins.keys())
        unloaded_count = 0

        for plugin_name in plugin_names:
            if self.unload_plugin(plugin_name):
                unloaded_count += 1

        self.api.log_info(
            f"Unloaded {unloaded_count} out of {len(plugin_names)} plugins"
        )
        return unloaded_count

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a loaded plugin by name"""
        return self.plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List all loaded plugin names"""
        return list(self.plugins.keys())

    def emit_event(self, event_name: str, **kwargs):
        """Emit an event to all listeners"""
        if event_name in self.event_listeners:
            for callback in self.event_listeners[event_name]:
                try:
                    callback(**kwargs)
                except Exception as e:
                    self.api.log_error(
                        f"Error in event listener for '{event_name}': {e}"
                    )

    def subscribe_event(self, event_name: str, callback: Callable):
        """Subscribe to an event"""
        if event_name not in self.event_listeners:
            self.event_listeners[event_name] = []
        self.event_listeners[event_name].append(callback)

    def unsubscribe_event(self, event_name: str, callback: Callable):
        """Unsubscribe from an event"""
        if event_name in self.event_listeners:
            try:
                self.event_listeners[event_name].remove(callback)
            except ValueError:
                pass  # Callback not found

    def register_resource(self, resource_type: str, name: str, resource: Any):
        """Register a resource"""
        if resource_type not in self.resources:
            self.resources[resource_type] = {}
        self.resources[resource_type][name] = resource

    def unregister_resource(self, resource_type: str, name: str):
        """Unregister a resource"""
        if resource_type in self.resources and name in self.resources[resource_type]:
            del self.resources[resource_type][name]

    def get_resource(self, resource_type: str, name: str) -> Any:
        """Get a registered resource"""
        return self.resources.get(resource_type, {}).get(name)

    def list_resources(self, resource_type: str) -> List[str]:
        """List resources of a specific type"""
        return list(self.resources.get(resource_type, {}).keys())

    def _validate_metadata(self, metadata: PluginMetadata):
        """Validate plugin metadata"""
        required_fields = ["name", "version", "description", "author", "plugin_type"]
        for required_field in required_fields:
            if not getattr(metadata, required_field):
                raise PluginValidationError(
                    f"Plugin '{getattr(metadata, 'name', 'unknown')}': "
                    f"Missing required field '{required_field}'"
                )

        valid_types = ["language", "ui", "tool", "integration"]
        if metadata.plugin_type not in valid_types:
            raise PluginValidationError(
                f"Plugin '{metadata.name}': Invalid plugin type '{metadata.plugin_type}'. "
                f"Valid types are: {', '.join(valid_types)}"
            )

        # Validate version format (basic semantic versioning check)
        import re

        if not re.match(r"^\d+\.\d+\.\d+", metadata.version):
            raise PluginValidationError(
                f"Plugin '{metadata.name}': Invalid version format '{metadata.version}'. "
                "Expected semantic version (e.g., '1.0.0')"
            )

    def _check_dependencies(self, metadata: PluginMetadata) -> bool:
        """Check if plugin dependencies are satisfied"""
        # Check for circular dependencies
        self._detect_circular_dependencies(metadata)

        for dep in metadata.dependencies:
            # For now, just check if the dependency plugin is loaded
            # In a more sophisticated system, this could check versions, etc.
            if dep not in self.plugins:
                raise PluginDependencyError(
                    f"Plugin '{metadata.name}' dependency '{dep}' not found. "
                    f"Required dependencies: {', '.join(metadata.dependencies)}"
                )
        return True

    def _detect_circular_dependencies(
        self, metadata: PluginMetadata, visited: Optional[set] = None
    ) -> None:
        """Detect circular dependencies in plugin requirements"""
        if visited is None:
            visited = set()

        if metadata.name in visited:
            cycle = list(visited) + [metadata.name]
            cycle_start = cycle.index(metadata.name)
            circular_deps = cycle[cycle_start:]
            raise PluginDependencyError(
                f"Circular dependency detected: {' -> '.join(circular_deps)}"
            )

        visited.add(metadata.name)

        # Check each dependency recursively
        for dep_name in metadata.dependencies:
            # Find the dependency plugin metadata (could be from loaded plugins or plugin paths)
            dep_metadata = self._get_plugin_metadata_by_name(dep_name)
            if dep_metadata:
                self._detect_circular_dependencies(dep_metadata, visited.copy())

        visited.remove(metadata.name)

    def _get_plugin_metadata_by_name(
        self, plugin_name: str
    ) -> Optional[PluginMetadata]:
        """Get plugin metadata by name from discovered plugins"""
        for plugin_path in self.discover_plugins():
            try:
                metadata_path = plugin_path / "plugin.json"
                if metadata_path.exists():
                    with open(metadata_path, "r") as f:
                        metadata_dict = json.load(f)
                    if metadata_dict.get("name") == plugin_name:
                        return PluginMetadata(**metadata_dict)
            except Exception:
                continue
        return None

    def _load_plugin_module(self, plugin_path: Path, metadata: PluginMetadata):
        """Load the plugin's Python module"""
        # Add plugin directory to Python path
        plugin_dir = str(plugin_path)
        if plugin_dir not in sys.path:
            sys.path.insert(0, plugin_dir)

        try:
            # Import the plugin module
            if metadata.entry_point:
                module_name = metadata.entry_point
            else:
                module_name = f"plugin_{metadata.name.lower().replace(' ', '_')}"

            return importlib.import_module(module_name)
        except ImportError as e:
            raise PluginLoadError(f"Failed to import plugin module: {e}")

    def _get_plugin_class(self, module, metadata: PluginMetadata) -> Type[Plugin]:
        """Get the plugin class from the module"""
        # Look for a class that inherits from the appropriate plugin type
        plugin_type_map = {
            "language": LanguagePlugin,
            "ui": UIPlugin,
            "tool": ToolPlugin,
            "integration": IntegrationPlugin,
        }

        base_class = plugin_type_map.get(metadata.plugin_type)
        if not base_class:
            raise PluginLoadError(f"Unknown plugin type: {metadata.plugin_type}")

        # Find a class in the module that inherits from the base class
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, base_class)
                and obj != base_class
            ):
                return obj

        raise PluginLoadError(
            f"No plugin class found in module that inherits from {base_class.__name__}"
        )

    def _record_error(
        self,
        error_type: str,
        plugin_name: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Record an error for diagnostic purposes"""
        import traceback
        import datetime

        error_report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "error_type": error_type,
            "plugin_name": plugin_name,
            "error_message": str(error),
            "error_class": error.__class__.__name__,
            "stack_trace": traceback.format_exc(),
            "context": context or {},
        }

        self.error_reports.append(error_report)

        # Keep only the most recent errors
        if len(self.error_reports) > self.max_error_reports:
            self.error_reports.pop(0)

    def get_error_reports(
        self, plugin_name: Optional[str] = None, error_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get error reports, optionally filtered by plugin name or error type"""
        reports = self.error_reports

        if plugin_name:
            reports = [r for r in reports if r["plugin_name"] == plugin_name]

        if error_type:
            reports = [r for r in reports if r["error_type"] == error_type]

        return reports

    def generate_diagnostic_report(self) -> str:
        """Generate a comprehensive diagnostic report"""
        import datetime

        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("TIME WARP IDE PLUGIN SYSTEM DIAGNOSTIC REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {datetime.datetime.now().isoformat()}")
        report_lines.append("")

        # System information
        report_lines.append("SYSTEM INFORMATION:")
        report_lines.append(f"- Loaded plugins: {len(self.plugins)}")
        report_lines.append(
            f"- Registered resources: {sum(len(r) for r in self.resources.values())}"
        )
        report_lines.append(
            f"- Event listeners: {sum(len(l) for l in self.event_listeners.values())}"
        )
        report_lines.append(f"- Error reports: {len(self.error_reports)}")
        report_lines.append("")

        # Loaded plugins
        if self.plugins:
            report_lines.append("LOADED PLUGINS:")
            for name, plugin in self.plugins.items():
                report_lines.append(f"- {name} (v{plugin.metadata.version})")
            report_lines.append("")

        # Recent errors
        if self.error_reports:
            report_lines.append("RECENT ERRORS:")
            for error in self.error_reports[-10:]:  # Last 10 errors
                report_lines.append(
                    f"- {error['timestamp']}: {error['error_type']} "
                    f"in {error['plugin_name']}: {error['error_message']}"
                )
            report_lines.append("")

        # Plugin directories
        report_lines.append("PLUGIN DIRECTORIES:")
        for plugin_dir in self.plugin_dirs:
            status = "exists" if plugin_dir.exists() else "missing"
            report_lines.append(f"- {plugin_dir} ({status})")
        report_lines.append("")

        # Discovered plugins
        discovered = self.discover_plugins()
        report_lines.append(f"DISCOVERED PLUGINS: {len(discovered)}")
        for plugin_path in discovered:
            metadata_path = plugin_path / "plugin.json"
            if metadata_path.exists():
                try:
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                    name = metadata.get("name", "unknown")
                    version = metadata.get("version", "unknown")
                    report_lines.append(f"- {name} (v{version}) at {plugin_path}")
                except Exception as e:
                    report_lines.append(f"- Error reading {plugin_path}: {e}")
            else:
                report_lines.append(f"- No plugin.json in {plugin_path}")
        report_lines.append("")

        return "\n".join(report_lines)

    def clear_error_reports(self):
        """Clear all error reports"""
        self.error_reports.clear()

    def _backup_operation_state(self, operation_id: str):
        """Backup current system state before an operation"""
        if not self.enable_recovery:
            return

        backup = {
            "plugins": dict(self.plugins),  # Shallow copy of plugin registry
            "resources": {
                k: dict(v) for k, v in self.resources.items()
            },  # Copy resource registry
            "event_listeners": dict(self.event_listeners),  # Copy event listeners
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.operation_backups[operation_id] = backup

    def _restore_operation_state(self, operation_id: str) -> bool:
        """Restore system state from backup after failed operation"""
        if not self.enable_recovery or operation_id not in self.operation_backups:
            return False

        backup = self.operation_backups[operation_id]

        try:
            # Restore plugin registry
            self.plugins = backup["plugins"]

            # Restore resource registry
            self.resources = backup["resources"]

            # Restore event listeners
            self.event_listeners = backup["event_listeners"]

            self.api.log_warning(
                f"Restored system state from backup for operation {operation_id}"
            )
            return True
        except Exception as e:
            self.api.log_error(f"Failed to restore system state: {e}")
            return False
        finally:
            # Clean up backup
            if operation_id in self.operation_backups:
                del self.operation_backups[operation_id]

    def _cleanup_operation_backup(self, operation_id: str):
        """Clean up operation backup after successful completion"""
        if operation_id in self.operation_backups:
            del self.operation_backups[operation_id]
