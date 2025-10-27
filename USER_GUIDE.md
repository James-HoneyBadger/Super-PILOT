# Time Warp IDE — User Guide

Welcome to Time Warp IDE, a retromodern learning environment supporting PILOT, BASIC, and Logo with turtle graphics. This guide covers daily use across the Python and Rust IDEs.

For help: <james@honey-badger.org>

---

## Getting Started

Pick one IDE:

- Python (modern, PySide6): `python Time_Warp_IDE.py`
- Python (classic, Tkinter): `python Time_Warp.py`
- Rust (egui):

```bash
cd Time_Warp_Rust
cargo run
```

## Core Workflow

1. Open or create files from File → Open or File → New.
2. Edit code in the Editor tab. Multiple files can be open in tabs.
3. Run the program (▶️) to view output and graphics in the unified Screen.
4. When prompted for input (📝), type your response and press Enter.
5. Save often via File → Save or Ctrl+S. Unsaved files show a modified indicator.

Notes:

- Examples are in `examples/` and top-level `*.spt`, `*.pilot`, `*.logo`.
- Turtle graphics render on the canvas (Python IDE) or unified canvas (Rust IDE).

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
- `INPUT var` - Get user input (blocking, waits for Enter)
- `LET var$ = INKEY$` - Get key press (non-blocking, for game loops)
- `SCREEN mode[, w, h]` - Switch between text/graphics modes (0=text, 1=640x480, 2=1024x768)
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

## Tips & Good Practices

- Keep programs small and focused; split into multiple files when helpful.
- Save before running to avoid losing changes.
- Explore example programs to learn language features quickly.

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

- `Ctrl+N` — New file
- `Ctrl+O` — Open file
- `Ctrl+S` — Save file
- `Ctrl+Z` / `Ctrl+Y` — Undo/Redo
- `Ctrl+F` — Find
- `F5` — Run

## File Formats

Time Warp IDE supports:
- `.spt` - Time Warp program files
- `.txt` - Plain text files
- `.pil` - PILOT program files

## Troubleshooting

Common issues:

1. Python GUI fails to start: verify PySide6 (modern) or tkinter (classic) is installed.
2. Turtle graphics not showing: ensure your system supports GUI apps (X11/Wayland on Linux).
3. Rust IDE build fails: run `rustup update` and `cargo clean && cargo build`.

Getting help:

- See examples and `docs/`
- Contact support: <james@honey-badger.org>

## System Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- Pillow library for enhanced graphics
- At least 50MB disk space

---

Empowering educational programming — © 2025 Honey Badger Universe
