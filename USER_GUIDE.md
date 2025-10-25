# Time Warp IDE - User Guide

**© 2025 Honey Badger Universe**
**For support, contact: james@honey-badger.org**

---

## Welcome to Time Warp IDE

Time Warp IDE is a comprehensive educational programming environment that supports three integrated programming languages:

- **PILOT** - A teaching language designed for computer-assisted instruction
- **BASIC** - Classic structured programming constructs  
- **Logo** - Turtle graphics and procedural programming

## Getting Started

### Running Time Warp IDE

```bash
python3 SuperPILOT.py
```

### Basic Operation

1. **Editor Tab**: Write your programs using any combination of PILOT, BASIC, and Logo commands
2. **Output Tab**: View program execution results
3. **Watch Variables Tab**: Monitor variable values during execution
4. **Tutorials Tab**: Access interactive learning materials
5. **Exercises Tab**: Practice programming challenges

## Language Reference

### PILOT Commands

- `T:text` - Output text (supports *VARIABLE* interpolation)
- `A:variable` - Accept input into variable
- `Y:condition` - Set match flag if condition is true
- `N:condition` - Alternative conditional test
- `J:label` - Jump to label (conditional if follows Y:/N:)
- `M:label` - Jump to label if match flag is set
- `R:label` - Gosub to label (subroutine call)
- `C:` - Return from subroutine
- `L:label` - Label definition
- `U:var=expr` - Update/assign variable
- `END` - End program

### BASIC Commands

- `LET var = expr` - Variable assignment
- `PRINT expr` - Output expression or string
- `INPUT var` - Get user input
- `GOTO line` - Jump to line number
- `IF condition THEN command` - Conditional execution
- `FOR var = start TO end [STEP step]` - Loop construct
- `NEXT [var]` - End of FOR loop
- `GOSUB line` - Call subroutine
- `RETURN` - Return from subroutine
- `REM comment` - Comment line
- `END` - End program

### Logo Commands

- `FORWARD n` (or `FD n`) - Move turtle forward
- `BACK n` (or `BK n`) - Move turtle backward
- `LEFT n` (or `LT n`) - Turn turtle left
- `RIGHT n` (or `RT n`) - Turn turtle right
- `PENUP` (or `PU`) - Lift pen up
- `PENDOWN` (or `PD`) - Put pen down
- `CLEARSCREEN` (or `CS`) - Clear screen
- `HOME` - Return turtle to center
- `SETXY x y` - Set turtle position

### Built-in Functions

- `RND()` - Random number (0-1)
- `INT(expr)` - Convert to integer
- `VAL(string)` - Convert string to number
- `UPPER(string)` - Convert to uppercase
- `LOWER(string)` - Convert to lowercase
- `MID(string,start,length)` - Extract substring

## Advanced Features

### Debugging

- Set breakpoints by clicking in the line number area
- Use **Step** to execute one line at a time
- Use **Continue** to run until the next breakpoint
- Monitor variables in the Watch Variables tab

### Version Control

- Automatic version saving before each run
- Access version history through File → Version History

### Educational Features

- Interactive tutorials for each language
- Programming exercises with automatic checking
- Comprehensive help system
- Example programs included

## Example Programs

### Hello World (PILOT)
```
L:START
T:Hello, World!
T:This is Time Warp!
END
```

### Math Demo (Mixed Languages)
```
REM This is a BASIC comment
LET A = 15
LET B = 25
PRINT "A = "; A; ", B = "; B

L:PILOT_SECTION
U:SUM=*A*+*B*
T:Sum using PILOT: *SUM*
END
```

### Simple Drawing (Logo)
```
CLEARSCREEN
PENDOWN
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
FORWARD 50
HOME
```

## Keyboard Shortcuts

- `Ctrl+N` - New file
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+F` - Find text
- `Ctrl+H` - Replace text
- `F5` - Run program
- `F6` - Run with debugger
- `F8` - Stop program
- `F10` - Step over
- `F11` - Step into

## File Formats

Time Warp IDE supports:
- `.spt` - Time Warp program files
- `.txt` - Plain text files
- `.pil` - PILOT program files

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure Python 3.x is installed with tkinter support
2. **Missing Pillow**: Install with `pip install pillow`
3. **Display issues**: Ensure your system supports GUI applications

### Getting Help

- Access built-in help via the Help menu
- Visit tutorials for step-by-step guidance
- Try the included example programs
- Contact support: james@honey-badger.org

## System Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- Pillow library for enhanced graphics
- At least 50MB disk space

---

**Time Warp IDE - Empowering Educational Programming**

*© 2025 Honey Badger Universe - All Rights Reserved*

For technical support, feature requests, or educational licensing:
**james@honey-badger.org**