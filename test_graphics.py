#!/usr/bin/env python3
"""Test turtle graphics display"""

import sys
sys.path.insert(0, '/home/james/Super-PILOT')

from Super_PILOT import TK_AVAILABLE

if not TK_AVAILABLE:
    print("ERROR: Tkinter not available. Install with: sudo pacman -Syu tk")
    sys.exit(1)

import tkinter as tk
from Super_PILOT import TempleCodeInterpreter

def test_graphics():
    """Test graphics display with a simple square"""
    print("Creating test window...")
    
    root = tk.Tk()
    root.title("TempleCode Graphics Test")
    root.geometry("500x500")
    
    # Create canvas
    canvas = tk.Canvas(root, width=400, height=400, bg="white", bd=2, relief="solid")
    canvas.pack(padx=10, pady=10)
    
    # Create interpreter
    interp = TempleCodeInterpreter()
    
    # Connect canvas to interpreter
    interp.graphics_widget = canvas
    interp.canvas_width = 400
    interp.canvas_height = 400
    interp.origin_x = 200
    interp.origin_y = 200
    
    print("Interpreter initialized")
    print(f"Graphics widget: {interp.graphics_widget}")
    print(f"Origin: ({interp.origin_x}, {interp.origin_y})")
    print(f"Turtle at: ({interp.turtle_x}, {interp.turtle_y})")
    
    # Run a simple program
    program = """
CS
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
END
"""
    
    print("\nRunning program...")
    result = interp.run_program(program)
    print(f"Program result: {result}")
    print(f"Final turtle position: ({interp.turtle_x}, {interp.turtle_y})")
    
    # Force canvas update
    canvas.update()
    
    # Check what was drawn
    items = canvas.find_all()
    print(f"\nCanvas items: {len(items)}")
    for item in items:
        item_type = canvas.type(item)
        coords = canvas.coords(item)
        print(f"  Item {item}: type={item_type}, coords={coords}")
    
    print("\n✓ Window should show a square")
    print("Close the window to exit")
    
    root.mainloop()

if __name__ == "__main__":
    test_graphics()
