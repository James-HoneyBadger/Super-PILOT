# Time Warp IDE Plugin System

This directory contains plugins that extend the functionality of Time Warp IDE. Plugins can add new programming languages, UI components, tools, and integrations.

## Plugin Types

### Language Plugins
Add support for new programming languages to the IDE.

**Example:** `sample_language_plugin/`
- Implements a simple "Sample" language
- Supports `.sample` and `.spl` file extensions
- Provides basic commands like HELLO, PRINT, VERSION

### UI Plugins
Extend the user interface with new components and panels.

**Example:** `sample_ui_plugin/`
- Adds status panels and buttons to the IDE
- Demonstrates component registration and callbacks

### Tool Plugins
Add utility functions and tools that can be used by other plugins or the IDE.

**Example:** `sample_tool_plugin/`
- Provides calculator, text formatter, and validator tools
- Functions can be called by other components

### Integration Plugins
Connect to external services, APIs, and systems.

**Example:** `sample_integration_plugin/`
- Demonstrates API, database, and webhook integrations
- Shows event-driven communication with external services

## Creating a Plugin

### 1. Create Plugin Directory
```
plugins/your_plugin_name/
├── plugin.json          # Plugin metadata
└── your_plugin_name.py  # Plugin implementation
```

### 2. Plugin Metadata (plugin.json)
```json
{
  "name": "Your Plugin Name",
  "version": "1.0.0",
  "description": "Description of what your plugin does",
  "author": "Your Name",
  "plugin_type": "language|ui|tool|integration",
  "dependencies": ["other_plugin_name"],
  "entry_point": "your_plugin_name.py"
}
```

### 3. Plugin Implementation
Create a class that inherits from the appropriate plugin base class:

- `LanguagePlugin` - for adding programming languages
- `UIPlugin` - for adding UI components
- `ToolPlugin` - for adding utility functions
- `IntegrationPlugin` - for external service integration

### 4. Required Methods
All plugins must implement:
- `initialize() -> bool` - Initialize the plugin
- `shutdown() -> bool` - Clean up resources

## Plugin API

Plugins have access to the IDE through the `self.api` object:

### Logging
```python
self.api.log_info("Info message")
self.api.log_warning("Warning message")
self.api.log_error("Error message")
```

### Event System
```python
# Subscribe to events
self.api.subscribe_event("event_name", callback_function)

# Emit events
self.api.emit_event("event_name", arg1="value1", arg2="value2")

# Unsubscribe from events
self.api.unsubscribe_event("event_name", callback_function)
```

### Resource Management
```python
# Register resources
self.api.register_resource("resource_type", "name", resource_object)

# Get resources
resource = self.api.get_resource("resource_type", "name")

# Unregister resources
self.api.unregister_resource("resource_type", "name")
```

### Configuration
```python
# Set config values
self.set_config_value("key", "value")

# Get config values
value = self.get_config_value("key", "default")

# Save/load config
self.save_config()
self.load_config()
```

## Installation

1. Place your plugin directory in the `plugins/` folder
2. Restart Time Warp IDE
3. Plugins are automatically discovered and loaded

## Development Tips

- Test your plugin thoroughly before distribution
- Handle errors gracefully in all methods
- Use descriptive names for resources and events
- Document your plugin's API and usage
- Follow PEP 8 style guidelines
- Keep plugin dependencies minimal

## Sample Plugins

This directory includes four sample plugins demonstrating each plugin type:

- `sample_language_plugin/` - Basic language implementation
- `sample_ui_plugin/` - UI component addition
- `sample_tool_plugin/` - Utility function provision
- `sample_integration_plugin/` - External service integration

Use these as templates for your own plugins!