#!/usr/bin/env python3
"""
Time Warp IDE - CLI Runner

Simple command-line interface for running Time Warp programs.
"""

import sys
import argparse
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from time_warp.core.interpreter import Interpreter
from time_warp.graphics.turtle_state import TurtleState


def run_program(filepath: str, show_turtle: bool = False):
    """Run a Time Warp program.
    
    Args:
        filepath: Path to program file
        show_turtle: Whether to display turtle state
    """
    # Read program
    try:
        with open(filepath, 'r') as f:
            program = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        return 1
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 1
    
    # Display program info
    print("=" * 60)
    print(f"Time Warp IDE - Running: {Path(filepath).name}")
    print("=" * 60)
    print()
    
    # Create interpreter and turtle
    interp = Interpreter()
    turtle = TurtleState()
    
    # Load and execute
    try:
        interp.load_program(program)
        output = interp.execute(turtle)
        
        # Display output
        if output:
            print("Program Output:")
            print("-" * 60)
            for line in output:
                print(line)
            print("-" * 60)
        else:
            print("(No text output)")
        
        # Display turtle info if requested
        if show_turtle and turtle.lines:
            print()
            print("Turtle Graphics:")
            print(f"  Position: ({turtle.x:.1f}, {turtle.y:.1f})")
            print(f"  Heading: {turtle.heading:.1f}°")
            print(f"  Lines drawn: {len(turtle.lines)}")
            print(f"  Pen: {'down' if turtle.pen_down else 'up'}")
            print(f"  Color: RGB({turtle.pen_color[0]}, {turtle.pen_color[1]}, {turtle.pen_color[2]})")
            
            if len(turtle.lines) <= 10:
                print("\n  Line segments:")
                for i, line in enumerate(turtle.lines, 1):
                    print(f"    {i}. ({line.start_x:.1f},{line.start_y:.1f}) -> ({line.end_x:.1f},{line.end_y:.1f})")
        
        print()
        print("✅ Execution completed successfully")
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Execution interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Execution error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def interactive_mode():
    """Run in interactive mode (REPL)."""
    print("=" * 60)
    print("Time Warp IDE - Interactive Mode")
    print("=" * 60)
    print("Enter commands line by line. Type 'exit' or 'quit' to exit.")
    print("Type 'help' for language help.\n")
    
    interp = Interpreter()
    turtle = TurtleState()
    
    while True:
        try:
            line = input(">>> ").strip()
            
            if not line:
                continue
            
            if line.lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
            
            if line.lower() == 'help':
                print("""
Time Warp IDE supports three languages:

PILOT: T:text  A:var  M:pattern  Y:label  N:label  C:var=expr  U:var  J:label  E:
BASIC: PRINT, LET, INPUT, GOTO, IF/THEN, FOR/NEXT, GOSUB/RETURN
Logo:  FORWARD, BACK, LEFT, RIGHT, PENUP, PENDOWN, HOME, REPEAT

Type commands directly at the >>> prompt.
""")
                continue
            
            if line.lower() == 'clear':
                turtle.clear()
                interp.output.clear()
                print("Cleared turtle and output")
                continue
            
            if line.lower() == 'turtle':
                print(f"Position: ({turtle.x:.1f}, {turtle.y:.1f})")
                print(f"Heading: {turtle.heading:.1f}°")
                print(f"Lines: {len(turtle.lines)}")
                continue
            
            # Execute single line
            interp.load_program(line)
            output = interp.execute(turtle)
            
            if output:
                for out_line in output:
                    print(out_line)
            
        except KeyboardInterrupt:
            print("\nUse 'exit' or 'quit' to exit")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Time Warp IDE - Multi-language educational programming environment',
        epilog='Supports PILOT, BASIC, and Logo languages'
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Program file to execute (.pilot, .bas, .logo)'
    )
    
    parser.add_argument(
        '-t', '--turtle',
        action='store_true',
        help='Show turtle graphics state after execution'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode (REPL)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Time Warp IDE 2.0.0-alpha (Python)'
    )
    
    parser.add_argument(
        '--examples',
        action='store_true',
        help='List available example programs'
    )
    
    args = parser.parse_args()
    
    # List examples
    if args.examples:
        examples_dir = Path(__file__).parent / 'examples'
        if examples_dir.exists():
            print("Available example programs:")
            print()
            for ext, lang in [('.pilot', 'PILOT'), ('.bas', 'BASIC'), ('.logo', 'Logo')]:
                files = sorted(examples_dir.glob(f'*{ext}'))
                if files:
                    print(f"{lang}:")
                    for f in files:
                        print(f"  - {f.name}")
                    print()
        return 0
    
    # Interactive mode
    if args.interactive or not args.file:
        if not args.file:
            print("No file specified. Starting interactive mode...")
            print()
        return interactive_mode()
    
    # Run file
    return run_program(args.file, args.turtle)


if __name__ == '__main__':
    sys.exit(main())
