# Time Warp IDE — User Guide

A friendly guide to installing, running, and learning with Time Warp IDE. This document covers the full project: the native Rust app and the educational Python app, the unified TempleCode language, example programs, graphics, and troubleshooting.

---

## What is TempleCode?

TempleCode is a unified educational language that blends three classics:
- BASIC: PRINT, variables, IF/THEN, FOR/NEXT, GOTO/GOSUB
- PILOT: Simple interactive dialogs with T:, A:, L: labels, J: jumps
- Logo: Turtle graphics, REPEAT, and procedures with TO … END

You can mix all three styles in the same program.

Example (TempleCode mix):

```templecode
T:Drawing a square...
LET SIZE = 100
SETCOLOR blue
PENWIDTH 6
REPEAT 4 [
  FORWARD SIZE
  RIGHT 90
]
PRINT "Done!"
```

---

## Which version should I use?

- Rust (Time_Warp_Rust/)
  - Best performance, native binary, egui UI
  - Great for classrooms and production use
  - Requires Rust toolchain (cargo)
- Python (Time_Warp_Python/)
  - Easiest to extend and tinker
  - PySide6 GUI, portable across platforms
  - Requires Python 3.8+

Both support the same TempleCode features and the shared examples in the root `examples/` folder (33 programs).

---

## Install and Run (Rust)

Prerequisites: Rust toolchain installed.

```bash
# From repository root
cd Time_Warp_Rust

# Build and run (debug)
cargo run

# Build release and run
cargo build --release
./target/release/time-warp

# Run tests
cargo test
```

Optional: experimental compiler (TempleCode → C): see `Time_Warp_Rust/README.md`.

---

## Install and Run (Python)

Prerequisites: Python 3.8+.

```bash
# From repository root
cd Time_Warp_Python

# Install dependencies
pip install PySide6 pillow

# Launch the desktop IDE
python time_warp_ide.py

# Or run a source file via CLI
python run_time_warp.py ../examples/logo_flower.logo
```

If you prefer a virtual environment, create and activate it before installing packages.

---

## Using the Desktop IDE (Python)

- Editor & Output
  - Code editor on the left; Output and Graphics tabs on the right
  - Run (F5), Stop (Shift+F5), Clear Output, Clear Canvas
  - Recent Files menu remembers your last projects
- Themes (8 built-in)
  - Dracula, Monokai, Solarized Dark, Ocean, Spring, Sunset, Candy, Forest
  - Theme selection is persisted between sessions
- Turtle Canvas
  - Pans/zooms, shows all drawn lines and the turtle cursor
  - Auto-switches to Graphics tab when drawing occurs
- Output Indicators (emoji)
  - ❌ error, ℹ️ info, 🎨 theme, 🚀 run, 🐢 turtle, ✅ success

---

## Language Quick Start

- BASIC
  ```basic
  10 LET A = 5
  20 IF A > 3 THEN PRINT "Greater"
  30 PRINT "A:", A
  ```

- PILOT
  ```pilot
  T:What is your name?
  A:NAME
  T:Hello *NAME*!
  ```

- Logo (Turtle)
  ```logo
  SETCOLOR #FF8800
  PENWIDTH 4
  REPEAT 36 [
    FORWARD 100
    RIGHT 170
  ]
  ```

- Procedures (Logo)
  ```logo
  TO POLYGON :SIDES :SIZE
    REPEAT :SIDES [
      FORWARD :SIZE
      RIGHT 360 / :SIDES
    ]
  END
  POLYGON 6 80
  ```

- Mixing styles (TempleCode)
  ```templecode
  T:Drawing...
  LET N = 5
  REPEAT N [ FORWARD 40 RIGHT 144 ]
  PRINT "Done"
  ```

Tip: Expressions are evaluated safely (no eval). Use variables in math like `RIGHT 360 / :SIDES`.

---

## Turtle Graphics Cheatsheet

- Move: `FORWARD n`/`FD n`, `BACK n`/`BK n`/`BACKWARD n`
- Turn: `LEFT n`/`LT n`, `RIGHT n`/`RT n`
- Go: `HOME`, `SETXY x y`, `SETHEADING a`/`SETH a`
- Pen: `PENUP`/`PU`, `PENDOWN`/`PD`, `PENWIDTH n` (`SETPENWIDTH`, `SETPW`, `SETPENSIZE`)
- Colors:
  - `SETCOLOR red|blue|...` (named), `SETCOLOR #RRGGBB`, `SETCOLOR r g b`
  - `SETPENCOLOR r g b`/`SETPC r g b`, `SETBGCOLOR r g b`/`SETBG r g b`
- Screen: `CLEARSCREEN`/`CS`/`CLEAR`, `HIDETURTLE`/`HT`, `SHOWTURTLE`/`ST`
- Loops/Procedures: `REPEAT n [ ... ]`, `TO NAME ... END`

See the full reference: `Time_Warp_Python/docs/TURTLE_GRAPHICS_REFERENCE.md`.

---

## Examples

- Root shared examples: `examples/` (33 files: BASIC, PILOT, Logo, plus `demo.tc`)
  - Try: `logo_flower.logo`, `logo_koch_snowflake.logo`, `basic_guess.bas`, `pilot_quiz.pilot`
- Python-only examples: `Time_Warp_Python/examples/` (34 files)

Run from the IDE (Open → Run) or via CLI (Python) or within the Rust app after opening files.

---

## Troubleshooting

- Python: `ModuleNotFoundError: PySide6`
  - Install dependencies: `pip install PySide6 pillow`
- Python: Window starts but no drawing appears
  - Ensure commands draw with pen down (default). Use `PENDOWN` or remove `PENUP`
- Rust: `cargo` not found
  - Install Rust toolchain; then `cargo run` in `Time_Warp_Rust/`
- Rust compiler feature (TempleCode→C)
  - Requires a system C compiler (cc/gcc/clang) on PATH
- General: Examples not found
  - Use paths relative to repo root, e.g., `examples/logo_flower.logo`

---

## Where to go next

- Project overview: `README.md` (root)
- Python docs: `Time_Warp_Python/README.md`, `Time_Warp_Python/QUICKSTART.md`, `Time_Warp_Python/DESKTOP_QUICKSTART.md`, `Time_Warp_Python/STATUS.md`
- Rust docs: `Time_Warp_Rust/README.md` and `Time_Warp_Rust/docs/`
- Turtle reference: `Time_Warp_Python/docs/TURTLE_GRAPHICS_REFERENCE.md`

Happy coding! 🐢🚀
