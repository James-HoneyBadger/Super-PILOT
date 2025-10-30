#!/usr/bin/env python3
"""
TempleCode IDE - Windows Application Entry Point
A professional educational programming environment for Windows 11
"""

import sys
import os
import logging
from pathlib import Path


# Configure logging for Windows
def setup_logging():
    """Set up logging for Windows application."""
    log_dir = Path.home() / "AppData" / "Local" / "TempleCode"
    log_dir.mkdir(exist_ok=True, parents=True)

    log_file = log_dir / "templecode.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )


def main():
    """Main entry point for TempleCode IDE."""
    try:
        setup_logging()
        logger = logging.getLogger(__name__)

        logger.info("Starting TempleCode IDE for Windows 11")

        # Ensure the application can find its modules
        app_dir = Path(__file__).parent.absolute()
        if str(app_dir) not in sys.path:
            sys.path.insert(0, str(app_dir))

        # Import and launch the IDE
        try:
            import tkinter as tk
            from Super_PILOT import TempleCodeIDE

            logger.info("Launching TempleCode IDE GUI")
            root = tk.Tk()
            app = TempleCodeIDE(root)
            root.mainloop()

        except ImportError as e:
            logger.error(f"Failed to import TempleCode modules: {e}")
            # Fallback to command-line interface
            from Super_PILOT import TempleCodeInterpreter

            print("TempleCode IDE - Command Line Mode")
            print("GUI components unavailable, using headless interpreter")

            if len(sys.argv) > 1:
                # Run file provided as argument
                file_path = Path(sys.argv[1])
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        program = f.read()

                    interpreter = TempleCodeInterpreter()
                    interpreter.run_program(program)
                else:
                    print(f"Error: File not found: {file_path}")
                    sys.exit(1)
            else:
                print("Usage: templecode [program_file.spt]")
                sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback

        logger.error(traceback.format_exc())

        # Show error dialog if GUI is available
        try:
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.withdraw()  # Hide main window

            messagebox.showerror(
                "TempleCode IDE Error",
                f"An error occurred while starting TempleCode IDE:\n\n{e}\n\n"
                f"Please check the log file at:\n{Path.home() / 'AppData' / 'Local' / 'TempleCode' / 'templecode.log'}",
            )

        except ImportError:
            print(f"Error: {e}")

        sys.exit(1)


if __name__ == "__main__":
    main()
