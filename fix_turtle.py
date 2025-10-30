#!/usr/bin/env python3
"""
Quick patch script to fix turtle origin and run tests
"""
import re
import sys

# Read the file
with open('Super_PILOT.py', 'r') as f:
    content = f.read()

# Fix turtle_x and turtle_y initialization in __init__
content = content.replace(
    "        self.turtle_x = 0  # logical x (0 = center)\n        self.turtle_y = 0  # logical y (0 = center)",
    "        self.turtle_x = 200  # logical x at canvas center\n        self.turtle_y = 200  # logical y at canvas center"
)

# Fix reset_turtle method
content = re.sub(
    r'(    def reset_turtle\(self\):.*?\n)        self\.turtle_x = 0\n        self\.turtle_y = 0',
    r'\1        self.turtle_x = 200\n        self.turtle_y = 200',
    content,
    flags=re.DOTALL
)

# Write back
with open('Super_PILOT.py', 'w') as f:
    f.write(content)

print("Fixed turtle origin to 200,200")
