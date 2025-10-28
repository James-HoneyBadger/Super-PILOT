# Time Warp IDE Desktop - Quick Start Guide

## Installation

### 1. Install Python Requirements

```bash
cd Time_Warp/Time_Warp_Python
pip install -e ".[gui]"
```

This installs PySide6 (Qt6) for the desktop interface.

### 2. Launch the IDE

```bash
python time_warp_ide.py
```

Or open a specific file:

```bash
python time_warp_ide.py examples/logo_square.logo
```

## Interface Overview

### Main Window Components

1. **Menu Bar**
   - **File**: New, Open, Save, Recent Files, Exit
   - **Edit**: Undo, Redo, Cut, Copy, Paste, Find
   - **Run**: Run (F5), Stop (Shift+F5), Clear Output, Clear Canvas
   - **View**: Themes, Zoom In/Out
   - **Help**: Example Programs, About

2. **Toolbar**
   - Quick access to New, Open, Save, Run, Stop, Clear

3. **Code Editor** (left panel)
   - Line numbers
   - Syntax highlighting for all 3 languages
   - Find/Replace (F3)
   - Zoom (Ctrl+Plus/Minus)

4. **Output/Canvas Tabs** (right panel)
   - **Output**: Text output with colored messages
   - **Graphics**: Turtle graphics canvas

### Turtle Graphics Canvas

- **Zoom**: Mouse wheel or View menu
- **Pan**: Middle-click drag or Ctrl+Left-click drag
- **Reset View**: Clear Canvas button
- **Coordinate System**: (0,0) at center, Y-axis up

## Running Your First Program

### PILOT Example

1. Click **File → New**
2. Enter this code:

```pilot
T:Welcome to Time Warp!
T:What is 5 + 3?
A:ANSWER
M:8
Y:CORRECT
T:Try again!
J:START
L:CORRECT
T:Correct! Well done.
E:
```

3. Press **F5** or click **Run**
4. Type your answer in the input dialog

### BASIC Example

```basic
10 PRINT "Countdown!"
20 FOR I = 10 TO 1 STEP -1
30 PRINT I
40 NEXT I
50 PRINT "Blastoff!"
```

### Logo Example

```logo
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

Watch the turtle draw a square in the Graphics tab!

## Themes

Switch themes via **View → Theme**:

- **Dracula** - Dark purple theme
- **Monokai** - Dark with bright colors
- **Solarized Light** - Easy on the eyes
- **Solarized Dark** - Dark variant
- **Ocean** - Blue-gray theme
- **Spring** - Light and fresh
- **Sunset** - Warm orange tones
- **Candy** - Purple pink theme

Theme preference is saved automatically.

## Keyboard Shortcuts

- **F5** - Run program
- **Shift+F5** - Stop execution
- **Ctrl+N** - New file
- **Ctrl+O** - Open file
- **Ctrl+S** - Save file
- **Ctrl+Shift+S** - Save As
- **F3** - Find
- **Ctrl+Plus** - Zoom In
- **Ctrl+Minus** - Zoom Out
- **Ctrl+Z** - Undo
- **Ctrl+Y** - Redo

## Example Programs

Browse example programs via **Help → Example Programs**:

- **PILOT**: Interactive quizzes, adventures, calculators
- **BASIC**: Games, graphics, screen modes
- **Logo**: Fractals, spirals, shapes, snowflakes

## Tips

1. **Save Often**: IDE warns about unsaved changes
2. **Recent Files**: Quick access to last 10 files opened
3. **Error Messages**: Includes suggestions for typos
4. **Canvas Controls**: Zoom and pan to see details
5. **Threaded Execution**: UI remains responsive during long programs

## Troubleshooting

### PySide6 Not Installed

```bash
pip install PySide6
```

### Window Doesn't Appear

Check for errors in terminal:

```bash
python time_warp_ide.py 2>&1 | tee ide_log.txt
```

### Turtle Graphics Not Showing

1. Run a Logo program first
2. Switch to Graphics tab
3. Check if canvas is cleared (might be zoomed out)

### Theme Not Persisting

Check QSettings path:
- Linux: `~/.config/TimeWarp/IDE.conf`
- macOS: `~/Library/Preferences/com.timewarp.IDE.plist`
- Windows: Registry under `HKEY_CURRENT_USER\Software\TimeWarp\IDE`

## Next Steps

- Explore example programs in `examples/` directory
- Read language documentation in `docs/`
- Try compiling TempleCode to C (see `docs/compiler.md`)
- Contribute your own examples!

## Support

For issues or questions:
- GitHub: https://github.com/James-HoneyBadger/Time_Warp
- Email: james@honey-badger.org
