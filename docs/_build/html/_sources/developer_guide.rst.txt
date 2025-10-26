Developer Guide
===============

This guide is for developers who want to extend, modify, or contribute to Time Warp IDE. It covers the architecture, development workflows, and best practices.

Architecture Overview
======================

Time Warp IDE follows a modular architecture designed for educational programming. The system is built with Python and tkinter, featuring a plugin-based design for extensibility.

Core Components
---------------

Main Application (Time_Warp.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main application file orchestrates all components:

* **UI Management**: Main window, menus, tabs, and canvas
* **Component Integration**: Coordinates between interpreter, plugins, and UI
* **Event Handling**: Processes user interactions and program execution
* **Configuration**: Manages settings and preferences

Key classes:

.. code-block:: python

   class TimeWarpApp:
       def __init__(self):
           # Initialize UI components
           # Set up interpreter
           # Load plugins
           # Configure themes

       def run_program(self):
           # Execute current program
           # Handle output display
           # Manage turtle graphics

Interpreter System (core/interpreter.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The central execution engine that dispatches commands to language-specific executors.

.. code-block:: python

   class Time_WarpInterpreter:
       def __init__(self):
           self.executors = {
               'PILOT': PilotExecutor(),
               'BASIC': BasicExecutor(),
               'LOGO': LogoExecutor()
           }

       def execute_command(self, command, language):
           executor = self.executors.get(language)
           if executor:
               return executor.execute_command(command)
           else:
               raise ValueError(f"Unknown language: {language}")

Language Executors (core/languages/)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Individual language implementations in separate modules:

* **pilot.py**: PILOT language executor
* **basic.py**: BASIC language executor
* **logo.py**: Logo language executor

Each executor implements:

.. code-block:: python

   class LanguageExecutor:
       def execute_command(self, command):
           # Parse command
           # Execute logic
           # Return result or error

Plugin System (plugins/)
^^^^^^^^^^^^^^^^^^^^^^^

Extensible architecture for adding new features:

.. code-block:: python

   class PluginManager:
       def __init__(self):
           self.plugins = []

       def load_plugins(self):
           # Discover and load plugins
           # Initialize plugin instances

       def execute_hook(self, hook_name, *args):
           # Call plugin hooks
           for plugin in self.plugins:
               if hasattr(plugin, hook_name):
                   getattr(plugin, hook_name)(*args)

Theme System (tools/theme.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manages visual appearance with multiple theme support:

.. code-block:: python

   class ThemeManager:
       def __init__(self):
           self.themes = self.load_themes()
           self.current_theme = 'default'

       def apply_theme(self, theme_name):
           # Apply theme colors to UI
           # Update component styles

Game Engine (games/engine/)
^^^^^^^^^^^^^^^^^^^^^^^^^^

2D game development framework:

* **game_engine.py**: Core game loop and entity management
* **physics.py**: Collision detection and movement
* **rendering.py**: Graphics rendering system

Development Setup
=================

Prerequisites
-------------

* Python 3.8+
* tkinter (included with Python)
* Development dependencies:

  .. code-block:: bash

     pip install -r requirements-dev.txt

Setting Up Development Environment
----------------------------------

1. **Clone Repository**:

   .. code-block:: bash

      git clone https://github.com/your-repo/Time_Warp.git
      cd Time_Warp

2. **Create Virtual Environment**:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**:

   .. code-block:: bash

      pip install -r requirements-dev.txt
      pip install -r requirements.txt

4. **Run Tests**:

   .. code-block:: bash

      python -m pytest tests/

5. **Start Development**:

   .. code-block:: bash

      python Time_Warp.py

Development Workflow
====================

Code Style
----------

Follow these conventions:

* **PEP 8**: Python style guide compliance
* **Docstrings**: Use Google-style docstrings
* **Naming**: descriptive names, snake_case for functions/variables
* **Comments**: Clear, concise comments for complex logic

Example:

.. code-block:: python

   def calculate_area(width: float, height: float) -> float:
       """Calculate the area of a rectangle.

       Args:
           width: The width of the rectangle
           height: The height of the rectangle

       Returns:
           The area of the rectangle
       """
       return width * height

Version Control
---------------

* **Branching**: Use feature branches for new work
* **Commits**: Atomic commits with clear messages
* **Pull Requests**: Code review required for all changes

Testing
-------

Run the comprehensive test suite:

.. code-block:: bash

   # Run all tests
   python -m pytest

   # Run specific test file
   python -m pytest tests/test_interpreter.py

   # Run with coverage
   python -m pytest --cov=time_warp

Add tests for new features:

.. code-block:: python

   def test_new_feature(self):
       # Arrange
       setup_test_data()

       # Act
       result = execute_feature()

       # Assert
       self.assertEqual(result, expected_value)

Adding New Languages
====================

To add support for a new programming language:

1. **Create Language Executor**:

   .. code-block:: python

      # core/languages/new_language.py
      class NewLanguageExecutor:
          def execute_command(self, command):
              # Parse and execute command
              pass

2. **Register Language**:

   .. code-block:: python

      # core/interpreter.py
      from core.languages.new_language import NewLanguageExecutor

      self.executors['NEW_LANGUAGE'] = NewLanguageExecutor()

3. **Add Syntax Highlighting**:

   Update the main UI to recognize the new language's syntax.

4. **Create Examples**:

   Add example programs in ``examples/`` directory.

5. **Update Documentation**:

   Add language reference in ``docs/language_reference.rst``.

Plugin Development
==================

Creating Plugins
----------------

Plugins extend Time Warp IDE's functionality:

.. code-block:: python

   # plugins/my_plugin/__init__.py
   class MyPlugin:
       def __init__(self, app):
           self.app = app

       def initialize(self):
           # Plugin setup
           pass

       def on_program_run(self, program):
           # Hook called when program runs
           pass

       def on_program_end(self, result):
           # Hook called when program ends
           pass

Plugin Structure
----------------

.. code-block:: text

   plugins/my_plugin/
   ├── __init__.py          # Main plugin class
   ├── plugin.json          # Plugin metadata
   └── resources/           # Plugin resources

Plugin Metadata (plugin.json):

.. code-block:: json

   {
       "name": "My Plugin",
       "version": "1.0.0",
       "description": "Description of plugin functionality",
       "author": "Your Name",
       "hooks": ["on_program_run", "on_program_end"]
   }

Installing Plugins
------------------

Plugins are automatically discovered from the ``plugins/`` directory.

Theme Development
=================

Creating Themes
---------------

Themes define the visual appearance:

.. code-block:: python

   # themes.json
   {
       "my_theme": {
           "background": "#2d2d2d",
           "foreground": "#ffffff",
           "accent": "#007acc",
           "error": "#ff6b6b",
           "success": "#51cf66"
       }
   }

Apply themes in the UI components:

.. code-block:: python

   def apply_theme(self, theme):
       self.root.configure(bg=theme['background'])
       # Apply to all UI elements

Game Development
================

Using the Game Engine
---------------------

The built-in game engine provides:

* **Entity Management**: Game objects with properties
* **Physics**: Collision detection and movement
* **Rendering**: 2D graphics with sprites
* **Input Handling**: Keyboard and mouse input

Example game:

.. code-block:: python

   from games.engine.game_engine import GameEngine

   class MyGame:
       def __init__(self):
           self.engine = GameEngine()
           self.player = self.engine.create_entity('player', x=100, y=100)

       def update(self):
           # Game logic
           if self.engine.is_key_pressed('left'):
               self.player.x -= 5

       def run(self):
           self.engine.run(self.update)

API Reference
=============

For detailed API documentation, see :doc:`api_reference`.

Contributing
============

Contribution Guidelines
-----------------------

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Add** tests for new functionality
5. **Ensure** all tests pass
6. **Submit** a pull request

Code Review Process
-------------------

* All changes require code review
* Maintain code quality standards
* Ensure backward compatibility
* Update documentation for API changes

Reporting Issues
----------------

Use GitHub issues for:

* Bug reports
* Feature requests
* Documentation improvements
* General questions

Include:

* Clear description of the issue
* Steps to reproduce (for bugs)
* Expected vs. actual behavior
* System information

Building and Distribution
=========================

Building for Distribution
-------------------------

Create executable distributions:

.. code-block:: bash

   # Using PyInstaller
   pip install pyinstaller
   pyinstaller --onefile --windowed Time_Warp.py

   # Using cx_Freeze
   pip install cx-Freeze
   python setup.py build

Packaging Requirements
----------------------

* **setup.py**: Python package configuration
* **MANIFEST.in**: Additional files to include
* **requirements.txt**: Runtime dependencies
* **requirements-dev.txt**: Development dependencies

Cross-Platform Considerations
-----------------------------

* **tkinter**: Ensure available on target platform
* **File paths**: Use ``os.path`` for cross-platform compatibility
* **External dependencies**: Bundle or document installation requirements

Troubleshooting Development Issues
===================================

Common Issues
-------------

**Import Errors**
   Ensure all dependencies are installed and Python path is correct.

**UI Display Issues**
   Check tkinter installation and system GUI support.

**Plugin Loading Failures**
   Verify plugin structure and required methods.

**Test Failures**
   Run tests individually to isolate issues.

Debugging Tips
--------------

* Use Python's ``pdb`` debugger for stepping through code
* Add logging statements for debugging
* Use the IDE's built-in debugger for program execution
* Check console output for error messages

Performance Optimization
========================

Identifying Bottlenecks
-----------------------

* Use Python's ``cProfile`` for performance analysis
* Monitor memory usage with ``memory_profiler``
* Profile rendering performance in games

Optimization Techniques
-----------------------

* **Caching**: Cache expensive computations
* **Lazy Loading**: Load resources on demand
* **Efficient Algorithms**: Use appropriate data structures
* **UI Updates**: Minimize unnecessary redraws

Memory Management
-----------------

* Clean up unused objects
* Use weak references for circular dependencies
* Monitor for memory leaks in long-running programs

Future Development
==================

Planned Features
----------------

* **Web Interface**: Browser-based version
* **Mobile Support**: iOS and Android apps
* **Cloud Integration**: Save/load programs online
* **Collaborative Editing**: Real-time multi-user editing
* **AI Assistance**: Code completion and suggestions

Architecture Improvements
-------------------------

* **Modular UI**: Component-based interface system
* **Async Execution**: Non-blocking program execution
* **Plugin API v2**: Enhanced plugin capabilities
* **Database Storage**: Persistent program storage

Community and Support
=====================

Getting Help
------------

* **Documentation**: Comprehensive docs at ``docs/``
* **GitHub Issues**: Bug reports and feature requests
* **Discussions**: Community forum for questions
* **Email**: james@honey-badger.org

Contributing to Documentation
-----------------------------

* Update docstrings for API changes
* Add examples for new features
* Improve tutorials and guides
* Translate documentation

Code of Conduct
---------------

* Be respectful and inclusive
* Provide constructive feedback
* Help newcomers learn
* Maintain professional communication

License
=======

Time Warp IDE is released under the MIT License. See ``LICENSE`` file for details.