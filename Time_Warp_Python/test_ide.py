#!/usr/bin/env python3
"""Test script to verify Time Warp IDE functionality."""

import sys
from pathlib import Path

print("🔍 Testing Time Warp IDE components...")
print()

# Test 1: Import all UI components
print("1. Testing imports...")
try:
    import time_warp.ui as _tw_ui  # noqa: F401
    print("   ✅ All UI components imported successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Import core library
print("2. Testing core library imports...")
try:
    from time_warp.core.interpreter import Interpreter
    from time_warp.graphics.turtle_state import TurtleState
    from time_warp.languages import templecode  # noqa: F401
    print("   ✅ Core library imported successfully (TempleCode)")
except Exception as e:
    print(f"   ❌ Core import failed: {e}")
    sys.exit(1)

# Test 3: Check PySide6
print("3. Testing PySide6...")
try:
    import PySide6  # type: ignore[import]
    # type: ignore[import]
    from PySide6.QtWidgets import QApplication  # noqa: F401
    print(f"   ✅ PySide6 version {PySide6.__version__}")
except Exception as e:
    print(f"   ❌ PySide6 not found: {e}")
    sys.exit(1)

# Test 4: Test interpreter execution
print("4. Testing interpreter execution...")
try:
    interp = Interpreter()
    turtle = TurtleState()
    
    # Test PILOT
    interp.load_program("T:Hello from PILOT\nE:")
    output = interp.execute(turtle)
    assert "Hello from PILOT" in output
    
    # Test BASIC
    interp.load_program("10 PRINT \"Hello from BASIC\"")
    output = interp.execute(turtle)
    assert "Hello from BASIC" in output
    
    # Test Logo
    turtle = TurtleState()  # Reset turtle
    interp.load_program("FORWARD 50\nRIGHT 90\nFORWARD 50")
    output = interp.execute(turtle)
    assert len(turtle.lines) >= 1  # At least one line segment drawn
    
    print("   ✅ TempleCode styles execute correctly")
except Exception as e:
    import traceback
    print(f"   ❌ Execution test failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 5: Check example programs
print("5. Checking example programs...")
examples_dir = Path(__file__).parent / "examples"
if examples_dir.exists():
    tc_files = list(examples_dir.glob("*.tc"))
    pilot_files = list(examples_dir.glob("*.pilot"))
    basic_files = list(examples_dir.glob("*.bas"))
    logo_files = list(examples_dir.glob("*.logo"))
    
    total = (
        len(tc_files) + len(pilot_files) + len(basic_files) + len(logo_files)
    )
    print(f"   ✅ Found {total} example programs:")
    if tc_files:
        print(f"      - {len(tc_files)} TempleCode (.tc) programs")
    print(f"      - {len(pilot_files)} TempleCode (PILOT-style) programs")
    print(f"      - {len(basic_files)} TempleCode (BASIC-style) programs")
    print(f"      - {len(logo_files)} TempleCode (Logo-style) programs")
else:
    print(f"   ⚠️  Examples directory not found at {examples_dir}")

# Test 6: Test ThemeManager
print("6. Testing ThemeManager...")
try:
    tm = _tw_ui.ThemeManager()
    themes = tm.get_theme_names()
    assert len(themes) == 8, f"Expected 8 themes, found {len(themes)}"
    assert 'Dracula' in themes
    assert 'Monokai' in themes
    print(f"   ✅ ThemeManager working with {len(themes)} themes")
except Exception as e:
    print(f"   ❌ ThemeManager test failed: {e}")
    sys.exit(1)

# Test 7: Check documentation
print("7. Checking documentation...")
docs = [
    "README.md",
    "DESKTOP_QUICKSTART.md",
    "GUI_IMPLEMENTATION_STATUS.md",
    "PROJECT_COMPLETE.md"
]
doc_path = Path(__file__).parent
found_docs = sum(1 for doc in docs if (doc_path / doc).exists())
print(f"   ✅ Found {found_docs}/{len(docs)} documentation files")

print()
print("=" * 60)
print("🎉 All tests passed! Time Warp IDE is ready to use.")
print("=" * 60)
print()
print("To launch the IDE:")
print("  python time_warp_ide.py")
print()
print("Or use the launch script:")
print("  ./launch_ide.sh")
print()
