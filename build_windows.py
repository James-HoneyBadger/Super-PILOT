"""
Build script for creating Windows executable using PyInstaller
Generates a standalone TempleCode IDE executable for Windows 11
"""

import PyInstaller.__main__
import sys
import os
from pathlib import Path


# Configuration for the Windows executable
def build_windows_exe():
    """Build Windows executable with PyInstaller."""

    app_dir = Path(__file__).parent
    main_script = app_dir / "templecode_app.py"

    # Icon file (will be created next)
    icon_file = app_dir / "assets" / "templecode.ico"

    # Build arguments for PyInstaller
    args = [
        str(main_script),
        "--name=TempleCode",
        "--windowed",  # No console window for GUI app
        f"--icon={icon_file}" if icon_file.exists() else "",
        "--onefile",  # Single executable file
        "--optimize=2",  # Python optimization
        # Include data files
        f"--add-data={app_dir / 'examples'}:examples",
        f"--add-data={app_dir / 'sample_programs'}:sample_programs",
        f"--add-data={app_dir / 'docs'}:docs",
        f"--add-data={app_dir / 'assets'}:assets",
        f"--add-data={app_dir / 'README.md'}:.",
        f"--add-data={app_dir / 'VERSION'}:.",
        # Include Python modules
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.scrolledtext",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.simpledialog",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=winsound",
        # Windows-specific options
        f"--version-file={app_dir / 'version_info.txt'}",
        f"--manifest={app_dir / 'templecode.manifest'}",
        # Output directory
        "--distpath=dist/windows",
        "--workpath=build/windows",
        "--specpath=build",
        # Clean previous build
        "--clean",
        # Verbose output
        "--log-level=INFO",
    ]

    # Remove empty arguments
    args = [arg for arg in args if arg]

    print("Building Windows executable with PyInstaller...")
    print(f"Arguments: {args}")

    PyInstaller.__main__.run(args)

    print("\\nBuild complete!")
    print(f"Executable created: {app_dir / 'dist' / 'windows' / 'TempleCode.exe'}")


if __name__ == "__main__":
    build_windows_exe()
