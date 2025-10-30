#!/usr/bin/env python3
"""Verify that turtle graphics are working correctly"""

import sys
sys.path.insert(0, '/home/james/Super-PILOT')

from Super_PILOT import TempleCodeInterpreter, TK_AVAILABLE

print("="*60)
print("TempleCode Graphics Verification")
print("="*60)
print()

# Test 1: Check Tk availability
print("1. Checking Tk availability...")
print(f"   TK_AVAILABLE: {TK_AVAILABLE}")
if TK_AVAILABLE:
    print("   ✓ Tkinter is installed and available")
else:
    print("   ✗ Tkinter not available")
    print("   Install with: sudo pacman -Syu tk")
    sys.exit(1)

# Test 2: Headless turtle state
print()
print("2. Testing headless turtle state (no display)...")
interp = TempleCodeInterpreter()
print(f"   Initial position: ({interp.turtle_x}, {interp.turtle_y})")
print(f"   Initial heading: {interp.turtle_heading}°")

program = """
FORWARD 100
RIGHT 90
FORWARD 50
"""

result = interp.run_program(program)
print(f"   After FORWARD 100, RIGHT 90, FORWARD 50:")
print(f"   Position: ({interp.turtle_x:.2f}, {interp.turtle_y:.2f})")
print(f"   Heading: {interp.turtle_heading}°")

if abs(interp.turtle_x - 50.0) < 0.01 and abs(interp.turtle_y - 100.0) < 0.01:
    print("   ✓ Turtle movement calculations correct")
else:
    print(f"   ✗ Unexpected position")

# Test 3: Graphics display
if TK_AVAILABLE:
    import tkinter as tk
    
    print()
    print("3. Testing graphics display...")
    print("   Creating window with canvas...")
    
    root = tk.Tk()
    root.title("Graphics Verification")
    root.geometry("450x500")
    
    canvas = tk.Canvas(root, width=400, height=400, bg="white", bd=2, relief="solid")
    canvas.pack(padx=10, pady=10)
    
    # New interpreter with canvas
    interp2 = TempleCodeInterpreter()
    interp2.graphics_widget = canvas
    interp2.canvas_width = 400
    interp2.canvas_height = 400
    interp2.origin_x = 200
    interp2.origin_y = 200
    
    # Draw test pattern
    test_program = """
CS
T:Drawing test square...
FORWARD 80
RIGHT 90
FORWARD 80
RIGHT 90
FORWARD 80
RIGHT 90
FORWARD 80
RIGHT 90
T:Square complete!
END
"""
    
    result = interp2.run_program(test_program)
    canvas.update()
    
    items = canvas.find_all()
    print(f"   Canvas items drawn: {len(items)}")
    
    if len(items) == 4:
        print("   ✓ All 4 sides of square drawn")
        
        # Check coordinates are visible
        all_visible = True
        for item in items:
            coords = canvas.coords(item)
            for coord in coords:
                if coord < 0 or coord > 400:
                    all_visible = False
                    break
        
        if all_visible:
            print("   ✓ All lines within visible canvas area")
        else:
            print("   ⚠ Some lines outside visible area")
    else:
        print(f"   ✗ Expected 4 lines, got {len(items)}")
    
    print()
    print("="*60)
    print("✓ GRAPHICS VERIFICATION COMPLETE")
    print("="*60)
    print()
    print("A window should be open showing a square.")
    print("If you see the square, graphics are working correctly!")
    print("Close the window to exit.")
    print()
    
    root.mainloop()

print("Verification complete.")
