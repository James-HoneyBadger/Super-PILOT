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
        self.ide.plugin_manager.emit_event(event_name, **kwargs)

    def subscribe_event(self, event_name: str, callback: Callable):
        """Subscribe to an event"""
        self.ide.plugin_manager.subscribe_event(event_name, callback)

    def unsubscribe_event(self, event_name: str, callback: Callable):
        """Unsubscribe from an event"""
        self.ide.plugin_manager.unsubscribe_event(event_name, callback)

    # Resource management
    def register_resource(self, resource_type: str, name: str, resource: Any):
        """Register a resource"""
        self.ide.plugin_manager.register_resource(resource_type, name, resource)

    def unregister_resource(self, resource_type: str, name: str):
        """Unregister a resource"""
        self.ide.plugin_manager.unregister_resource(resource_type, name)

    def get_resource(self, resource_type: str, name: str) -> Any:
        """Get a registered resource"""
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
        try:
            # Load metadata
            metadata_path = plugin_path / "plugin.json"
            with open(metadata_path, "r") as f:
                metadata_dict = json.load(f)

            metadata = PluginMetadata(**metadata_dict)

            # Validate metadata
            self._validate_metadata(metadata)

            # Check dependencies
            if not self._check_dependencies(metadata):
                raise PluginLoadError(f"Dependencies not satisfied for {metadata.name}")

            # Load plugin module
            plugin_module = self._load_plugin_module(plugin_path, metadata)

            # Create plugin instance
            plugin_class = self._get_plugin_class(plugin_module, metadata)
            plugin = plugin_class(self.api, metadata)

            # Load configuration
            plugin.load_config()

            # Initialize plugin
            if plugin.initialize():
                self.plugins[metadata.name] = plugin
                self.api.log_info(f"Plugin '{metadata.name}' loaded successfully")
                return plugin
            else:
                raise PluginLoadError(f"Plugin '{metadata.name}' failed to initialize")

        except Exception as e:
            self.api.log_error(f"Failed to load plugin from {plugin_path}: {e}")
            return None

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        if plugin_name not in self.plugins:
            return False

        plugin = self.plugins[plugin_name]

        try:
            # Shutdown plugin
            if plugin.shutdown():
                # Save configuration
                plugin.save_config()

                # Remove from registry
                del self.plugins[plugin_name]

                self.api.log_info(f"Plugin '{plugin_name}' unloaded successfully")
                return True
            else:
                self.api.log_error(
                    f"Plugin '{plugin_name}' failed to shutdown properly"
                )
                return False
        except Exception as e:
            self.api.log_error(f"Error unloading plugin '{plugin_name}': {e}")
            return False

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
                raise PluginValidationError(f"Missing required field: {field}")

        valid_types = ["language", "ui", "tool", "integration"]
        if metadata.plugin_type not in valid_types:
            raise PluginValidationError(f"Invalid plugin type: {metadata.plugin_type}")

    def _check_dependencies(self, metadata: PluginMetadata) -> bool:
        """Check if plugin dependencies are satisfied"""
        for dep in metadata.dependencies:
            # For now, just check if the dependency plugin is loaded
            # In a more sophisticated system, this could check versions, etc.
            if dep not in self.plugins:
                self.api.log_warning(
                    f"Plugin '{metadata.name}' dependency '{dep}' not found"
                )
                return False
        return True

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
