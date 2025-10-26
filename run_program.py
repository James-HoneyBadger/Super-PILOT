#!/usr/bin/env python3
"""
Simple test script to run PILOT programs without GUI
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Time_Warp import TimeWarpInterpreter


def run_program(filename):
    """Run a PILOT program from file"""
    try:
        with open(filename, "r") as f:
            program_text = f.read()

        interpreter = TimeWarpInterpreter()
        print(f"Running program: {filename}")
        print("=" * 50)

        success = interpreter.run_program(program_text)

        print("=" * 50)
        if success:
            print("Program completed successfully")
        else:
            print("Program failed or was stopped")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error running program: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 run_program.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    run_program(filename)
