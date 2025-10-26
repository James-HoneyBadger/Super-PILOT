#!/usr/bin/env python3
"""
Modern Time Warp IDE with PySide6 UI

A complete redesign using PySide6 for modern, responsive UI components.
"""

import sys
import os
import subprocess

# Ensure required packages are installed (skip PIL check for now)
REQUIRED_PACKAGES = []
missing = []
for pkg in REQUIRED_PACKAGES:
    try:
        __import__(pkg if pkg != "Pillow" else "PIL")
    except ImportError:
        missing.append(pkg)
if missing:
    print(f"❌ Missing required packages: {', '.join(missing)}")
    print("Attempting to install missing packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    print("✅ Packages installed. Please re-run the IDE.")
    sys.exit(1)

# Check PySide6 compatibility by running a subprocess test
try:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import PySide6; from PySide6.QtWidgets import QApplication; print('compatible')",
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )
    PYSIDE6_COMPATIBLE = result.returncode == 0 and "compatible" in result.stdout
except (subprocess.TimeoutExpired, subprocess.SubprocessError):
    PYSIDE6_COMPATIBLE = False

# If PySide6 is not compatible, explain the hardware limitation
if not PYSIDE6_COMPATIBLE:
    print("⚠️  PySide6 not compatible with this system (CPU architecture issue)")
    print()
    print("🔍 DIAGNOSIS:")
    print(
        "This system is running on a virtual CPU that lacks support for modern CPU instructions"
    )
    print(
        "(SSSE3, SSE4.1, SSE4.2, POPCNT) required by PySide6/Qt and other modern libraries."
    )
    print()
    print("💡 SOLUTIONS:")
    print(
        "1. Run on a physical machine or newer virtual environment with CPU instruction support"
    )
    print(
        "2. Use a different Linux distribution or container with proper CPU emulation"
    )
    print("3. Update QEMU/KVM to a version that supports newer CPU instructions")
    print("4. Use a cloud instance with modern CPU architecture")
    print()
    print("For development, you can try running the IDE on a different system.")
    print(
        "The Time Warp IDE requires a CPU with SSSE3, SSE4.1, SSE4.2, and POPCNT support."
    )
    sys.exit(1)

# Only continue with Qt imports if compatible
from typing import Optional, Dict, Any, List
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.interpreter import TimeWarpInterpreter
from core.plugin_system import PluginManager
from core.safe_expression_evaluator import safe_eval
from core.async_support import (
    init_async_support,
    get_async_runner,
    AsyncInterpreterRunner,
)

# Import modern UI
from ui.qt_ui import QtUIFactory, PYSIDE6_AVAILABLE

if not PYSIDE6_AVAILABLE:
    print("❌ PySide6 is not available. Please install PySide6 to use the modern UI.")
    print("Run: pip install PySide6")
    sys.exit(1)

from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QInputDialog
from PySide6.QtCore import QTimer, Qt

QT_AVAILABLE = True
UI_BACKEND = "PySide6"
UI_FACTORY_CLASS = QtUIFactory


class ModernTimeWarpIDE:
    """Modern Time Warp IDE with PySide6 UI"""

    def __init__(self):
        """Initialize the modern IDE"""
        # Initialize asyncio support
        init_async_support()

        # Create UI factory and application
        self.ui_factory = UI_FACTORY_CLASS()
        self.app = self.ui_factory.create_application()

        # Create main window
        self.window = self.app.create_main_window(
            f"Time Warp IDE - {UI_BACKEND} Edition", 1400, 900
        )

        # Set up attributes required by PluginAPI
        self.ui = self.window  # Main window for plugin UI access
        self.config = {}  # Simple config dictionary for plugins

        # Initialize interpreter
        self.interpreter = TimeWarpInterpreter()

        # Initialize plugin system
        self.plugin_manager = PluginManager(self)

        # Create UI components
        self.setup_ui()

        # Connect signals
        self.connect_signals()

        # Load plugins
        self.load_plugins()

        # Center window on screen
        self.window.center_on_screen()

    def setup_ui(self) -> None:
        """Set up the user interface"""
        # Create menu bar
        self.menu_bar = self.window.create_menu_bar()
        self.setup_menus()

        # Create status bar
        self.status_bar = self.window.create_status_bar()
        self.status_bar.set_text("Ready")

        # Create editor
        self.editor = self.window.create_text_editor()

        # Create output panel
        self.output = self.window.create_output_panel()

        # Create canvas
        self.canvas = self.window.create_canvas(600, 500)

        # Create variables tree
        self.variables_tree = self.window.create_variables_tree()

        # Connect interpreter to output
        self.interpreter.output_widget = self.output
        self.interpreter.graphics_widget = self.canvas

    def setup_menus(self) -> None:
        """Set up application menus"""
        # File menu
        file_menu = self.menu_bar.add_menu("&File")
        file_menu.add_command("New", self.new_file, "Ctrl+N")
        file_menu.add_command("Open...", self.open_file, "Ctrl+O")
        file_menu.add_command("Save", self.save_file, "Ctrl+S")
        file_menu.add_command("Save As...", self.save_file_as, "Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command("Exit", self.quit_app, "Ctrl+Q")

        # Edit menu
        edit_menu = self.menu_bar.add_menu("&Edit")
        edit_menu.add_command("Undo", lambda: self.editor.widget.undo(), "Ctrl+Z")
        edit_menu.add_command("Redo", lambda: self.editor.widget.redo(), "Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command("Cut", lambda: self.editor.widget.cut(), "Ctrl+X")
        edit_menu.add_command("Copy", lambda: self.editor.widget.copy(), "Ctrl+C")
        edit_menu.add_command("Paste", lambda: self.editor.widget.paste(), "Ctrl+V")

        # Run menu
        run_menu = self.menu_bar.add_menu("&Run")
        run_menu.add_command("Run Program", self.run_program, "F5")
        run_menu.add_command("Stop Program", self.stop_program, "F6")
        run_menu.add_command("Debug Program", self.debug_program, "F7")
        run_menu.add_command("Step Over", self.step_program, "F10")

        # Examples menu
        examples_menu = self.menu_bar.add_menu("&Examples")
        examples_menu.add_command("Hello World", self.load_hello_world)
        examples_menu.add_command("Math Demo", self.load_math_demo)
        examples_menu.add_command("Quiz Game", self.load_quiz_game)
        examples_menu.add_command("Turtle Graphics", self.load_turtle_demo)
        examples_menu.add_command("Game Demo", self.load_game_demo)

        # View menu
        view_menu = self.menu_bar.add_menu("&View")
        view_menu.add_command("Clear Output", self.clear_output)
        view_menu.add_command("Clear Graphics", self.clear_graphics)

        # Plugins menu
        plugins_menu = self.menu_bar.add_menu("&Plugins")
        plugins_menu.add_command("Reload Plugins", self.reload_plugins)
        plugins_menu.add_separator()
        plugins_menu.add_command("Plugin Manager", self.show_plugin_manager)

        # Help menu
        help_menu = self.menu_bar.add_menu("&Help")
        help_menu.add_command("Language Reference", self.show_help)
        help_menu.add_command("About", self.show_about)

    def connect_signals(self) -> None:
        """Connect UI signals to handlers"""
        # Connect toolbar buttons
        if hasattr(self.window, "run_button"):
            self.window.run_button.clicked.connect(self.run_program)
        if hasattr(self.window, "stop_button"):
            self.window.stop_button.clicked.connect(self.stop_program)

        # Connect language selector
        if hasattr(self.window, "language_combo"):
            self.window.language_combo.currentTextChanged.connect(
                self.on_language_changed
            )

    def on_language_changed(self, language: str) -> None:
        """Handle language selection change"""
        self.status_bar.set_text(f"Language: {language}")

    def run_program(self) -> None:
        """Run the program asynchronously"""
        try:
            code = self.editor.get_text().strip()
            if not code:
                self.show_message("No code to run", "Please enter some code first.")
                return

            self.status_bar.set_text("Running program...")

            # Reset interpreter
            self.interpreter.reset()
            self.output.clear()
            self.canvas.clear()

            # Split code into lines for async execution
            program_lines = [line.strip() for line in code.split("\n") if line.strip()]

            # Create async interpreter runner
            runner = get_async_runner()
            async_runner = AsyncInterpreterRunner(self.interpreter.__class__, runner)

            # Run program asynchronously
            async def run_async():
                try:
                    result = await async_runner.execute_program_async(
                        program_lines, self.interpreter.variables.copy()
                    )
                    # Update variables after execution
                    self.interpreter.variables.update(result.get("variables", {}))
                    self.update_variables_display()
                    self.status_bar.set_text("Program completed successfully")
                except Exception as e:
                    self.log_output(f"Async execution error: {e}")
                    self.status_bar.set_text("Program execution failed")

            # Schedule the async task
            runner.run_async(run_async())

        except Exception as e:
            self.show_error("Error", f"Failed to run program: {e}")

    def stop_program(self) -> None:
        """Stop program execution"""
        self.interpreter.running = False
        self.status_bar.set_text("Program stopped")

    def debug_program(self) -> None:
        """Run program in debug mode"""
        self.show_message("Debug Mode", "Debug mode not yet implemented in modern UI")

    def step_program(self) -> None:
        """Step through program execution"""
        self.show_message(
            "Step Mode", "Step execution not yet implemented in modern UI"
        )

    def new_file(self) -> None:
        """Create a new file"""
        self.editor.set_text("")
        self.status_bar.set_text("New file")

    def open_file(self) -> None:
        """Open a file"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self.window.window,
                "Open File",
                "",
                "Time Warp files (*.tw *.txt);;All files (*.*)",
            )
            if filename:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                self.editor.set_text(content)
                self.status_bar.set_text(f"Opened: {Path(filename).name}")
        except Exception as e:
            self.show_error("Error", f"Failed to open file: {e}")

    def save_file(self) -> None:
        """Save current file"""
        self.save_file_as()

    def save_file_as(self) -> None:
        """Save file with dialog"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self.window.window,
                "Save File",
                "",
                "Time Warp files (*.tw);;All files (*.*)",
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.editor.get_text())
                self.status_bar.set_text(f"Saved: {Path(filename).name}")
        except Exception as e:
            self.show_error("Error", f"Failed to save file: {e}")

    def load_hello_world(self) -> None:
        """Load Hello World example"""
        code = """T:Hello World!
T:Welcome to Time Warp IDE with PySide6 UI
A:name
T:*name*, nice to meet you!
END"""
        self.editor.set_text(code)
        self.status_bar.set_text("Loaded: Hello World example")

    def load_math_demo(self) -> None:
        """Load Math Demo example"""
        code = """U:x=15
U:y=7
T:Math Demo
T:x = *x*, y = *y*
T:Sum: *x+y*
T:Difference: *x-y*
T:Product: *x*y*
T:Quotient: *x/y*
END"""
        self.editor.set_text(code)
        self.status_bar.set_text("Loaded: Math Demo")

    def load_quiz_game(self) -> None:
        """Load Quiz Game example"""
        code = """T:Math Quiz Game
T:What is 2 + 2?
A:answer
Y:*answer*=4
T:Correct! Well done.
N:*answer*=4
T:Sorry, the answer is 4.
END"""
        self.editor.set_text(code)
        self.status_bar.set_text("Loaded: Quiz Game")

    def load_turtle_demo(self) -> None:
        """Load Turtle Graphics demo"""
        code = """T:Turtle Graphics Demo
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
HOME
PENUP
FORWARD 50
PENDOWN
CIRCLE 30
END"""
        self.editor.set_text(code)
        self.status_bar.set_text("Loaded: Turtle Graphics Demo")

    def load_game_demo(self) -> None:
        """Load Game Development demo"""
        code = """T:Simple Game Demo
GAME:CREATE player sprite 200 200 32 32
GAME:MOVE player 10 0 5
GAME:RENDER
T:Game object created and moved!
END"""
        self.editor.set_text(code)
        self.status_bar.set_text("Loaded: Game Demo")

    def clear_output(self) -> None:
        """Clear the output panel"""
        self.output.clear()
        self.status_bar.set_text("Output cleared")

    def clear_graphics(self) -> None:
        """Clear the graphics canvas"""
        self.canvas.clear()
        self.status_bar.set_text("Graphics cleared")

    def load_plugins(self) -> None:
        """Load all plugins"""
        try:
            loaded_count = self.plugin_manager.load_all_plugins()
            self.log_output(f"Plugin system initialized: {loaded_count} plugins loaded")
            if loaded_count > 0:
                self.status_bar.set_text(f"Loaded {loaded_count} plugins")
        except Exception as e:
            self.log_output(f"Error loading plugins: {e}")
            self.show_error("Plugin Error", f"Failed to load plugins: {e}")

    def reload_plugins(self) -> None:
        """Reload all plugins"""
        try:
            unloaded_count = self.plugin_manager.unload_all_plugins()
            loaded_count = self.plugin_manager.load_all_plugins()
            self.status_bar.set_text(f"Reloaded {loaded_count} plugins")
            self.show_message(
                "Plugins Reloaded", f"Successfully reloaded {loaded_count} plugins"
            )
        except Exception as e:
            self.log_output(f"Error reloading plugins: {e}")
            self.show_error("Plugin Error", f"Failed to reload plugins: {e}")

    def show_plugin_manager(self) -> None:
        """Show plugin manager dialog"""
        self.show_message(
            "Plugin Manager", "Plugin manager not yet implemented in modern UI"
        )

    def show_help(self) -> None:
        """Show language reference"""
        help_text = """
TIME WARP LANGUAGE REFERENCE

=== PILOT COMMANDS ===
T:text          - Output text (variables in *VAR* format)
A:variable      - Accept input into variable
Y:condition     - Set match flag when condition is TRUE
N:condition     - Set match flag when condition is FALSE
J:label         - Jump to label
M:pattern       - Pattern matching
R:command       - Runtime/Resource commands
C:              - Return from subroutine
L:label         - Label definition
U:var=expr      - Update/Set variable
END             - End program

=== BASIC COMMANDS ===
LET var = expr  - Assign expression to variable
PRINT expr      - Output expression
INPUT var       - Get input into variable
GOTO line       - Jump to line number
IF condition THEN - Conditional execution
FOR...NEXT      - Loop construct
GOSUB...RETURN  - Subroutine calls
END             - End program

=== LOGO COMMANDS ===
FORWARD n       - Move turtle forward
BACK n          - Move turtle backward
LEFT n          - Turn turtle left
RIGHT n         - Turn turtle right
PENUP/PENDOWN   - Pen control
CLEARSCREEN     - Clear graphics
HOME            - Return to center
SETXY x y       - Set position
REPEAT n [...]  - Repeat commands

=== GAME COMMANDS ===
GAME:CREATE     - Create game objects
GAME:MOVE       - Move objects
GAME:PHYSICS    - Set physics properties
GAME:COLLISION  - Check collisions
GAME:RENDER     - Render scene
"""
        self.show_message("Language Reference", help_text)

    def show_about(self) -> None:
        """Show about dialog"""
        about_text = f"""Time Warp IDE - {UI_BACKEND} Edition

A modern, educational programming environment supporting multiple languages with turtle graphics.

Features:
• Multi-language support (PILOT, BASIC, Logo, Python, JavaScript, Perl)
• Modern PySide6 UI with syntax highlighting
• Asynchronous program execution
• Turtle graphics and game development
• Plugin system for extensibility
• Hardware integration (Arduino, Raspberry Pi)

Version: {UI_BACKEND} Edition
Built with: Python 3.11+ and {UI_BACKEND}
"""
        self.show_message("About Time Warp IDE", about_text)

    def quit_app(self) -> None:
        """Quit the application"""
        self.app.quit()

    def update_variables_display(self) -> None:
        """Update the variables tree display"""
        self.variables_tree.clear()
        for var_name, var_value in self.interpreter.variables.items():
            item = self.variables_tree.addTopLevelItem(
                self.variables_tree.headerItem().clone()
            )
            item.setText(0, str(var_name))
            item.setText(1, str(var_value))

    def log_output(self, message: str) -> None:
        """Log a message to the output widget"""
        if self.output:
            self.output.append_text(str(message) + "\n")

    def show_message(self, title: str, message: str) -> None:
        """Show an information message dialog"""
        QMessageBox.information(self.window.window, title, message)

    def show_error(self, title: str, message: str) -> None:
        """Show an error message dialog"""
        QMessageBox.critical(self.window.window, title, message)

    def run(self) -> int:
        """Run the application"""
        self.window.show()
        return self.app.run_event_loop()


def main():
    """Main entry point"""
    try:
        # Create and run the modern IDE
        ide = ModernTimeWarpIDE()
        return ide.run()
    except Exception as e:
        print(f"❌ Failed to start Time Warp IDE: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
