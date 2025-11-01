# Time Warp IDE User Guide

**🎯 Complete User Manual for All Time Warp Implementations**

Welcome to the comprehensive Time Warp IDE User Guide! This manual covers everything you need to know to install, configure, and master Time Warp IDE across all platforms. Whether you're a student learning your first programming language, an educator setting up a classroom, or a developer exploring retro computing, this guide has you covered.

---

## 📚 Table of Contents

### 🚀 **Getting Started**
1. [What is Time Warp IDE?](#-what-is-time-warp-ide)
2. [Choosing Your Implementation](#-choosing-your-implementation)  
3. [System Requirements](#-system-requirements)
4. [Quick Start Guide](#-quick-start-guide)

### 💻 **Installation & Setup**
5. [Rust Implementation Setup](#-rust-implementation-setup)
6. [Python Implementation Setup](#-python-implementation-setup)
7. [Web Implementation Setup](#-web-implementation-setup)
8. [DOS Implementation Setup](#-dos-implementation-setup)
9. [Windows Implementation Setup](#-windows-implementation-setup)
10. [Apple Implementation Setup](#-apple-implementation-setup)

### 🎨 **Using the IDE**
11. [Interface Overview](#-interface-overview)
12. [Writing Your First Program](#-writing-your-first-program)
13. [Code Editor Features](#-code-editor-features)
14. [Running Programs](#-running-programs)
15. [Turtle Graphics Canvas](#-turtle-graphics-canvas)
16. [File Management](#-file-management)

### 📖 **TempleCode Programming**
17. [TempleCode Overview](#-templecode-overview)
18. [BASIC Programming](#-basic-programming)
19. [PILOT Programming](#-pilot-programming)
20. [Logo Programming](#-logo-programming)
21. [Mixed Language Programming](#-mixed-language-programming)

### 🎯 **Advanced Features**
22. [Themes and Customization](#-themes-and-customization)
23. [Debugging and Troubleshooting](#-debugging-and-troubleshooting)
24. [Performance Optimization](#-performance-optimization)
25. [Accessibility Features](#-accessibility-features)

### 🏫 **Educational Use**
26. [Classroom Setup](#-classroom-setup)
27. [Student Management](#-student-management)
28. [Assignment Creation](#-assignment-creation)
29. [Progress Tracking](#-progress-tracking)

### 🛠️ **Troubleshooting**
30. [Common Issues](#-common-issues)
31. [Error Messages](#-error-messages)
32. [Platform-Specific Problems](#-platform-specific-problems)
33. [Getting Help](#-getting-help)

---

## 🎯 What is Time Warp IDE?

Time Warp IDE is a revolutionary educational programming environment that combines three classic programming languages—BASIC, PILOT, and Logo—into a single, unified experience called **TempleCode**. 

### 🌟 **Key Benefits**

#### **🎓 Educational Focus**
- **Progressive Learning**: Start with simple commands and build to complex programs
- **Visual Feedback**: See your code come alive with turtle graphics
- **Error Guidance**: Helpful error messages that teach while debugging
- **Multiple Approaches**: Learn different programming paradigms in one environment

#### **🔄 Unified Language Experience**
- **BASIC**: Traditional line-numbered programming with variables and loops
- **PILOT**: Interactive text-based programming with pattern matching
- **Logo**: Visual programming with turtle graphics and procedures
- **Mixed Programs**: Combine all three styles in a single program

#### **🌍 Multi-Platform Availability**
- **Native Performance**: Rust implementation for maximum speed
- **Educational Access**: Python implementation for easy modification and learning
- **Universal Access**: Web implementation runs on any device with a browser
- **Retro Computing**: DOS implementation for authentic vintage experience
- **Legacy Support**: Windows implementation for institutional environments
- **Modern Mobile**: Apple implementation with iOS and macOS integration

### 🎨 **What Makes TempleCode Special?**

Traditional programming education often forces students to learn one language at a time, missing connections between different programming paradigms. TempleCode breaks down these barriers:

```templecode
10 PRINT "Welcome to Time Warp!"
20 LET AGE = 0

T:What's your age?
A:$AGE

30 IF AGE >= 13 THEN GOSUB 100
40 GOTO 200

*100 REM Teenager graphics
TO COOLSHAPE :SIZE
  REPEAT 8 [
    FORWARD :SIZE
    RIGHT 45
  ]
END

SETCOLOR blue
COOLSHAPE 50
RETURN

*200 PRINT "Thanks for trying Time Warp!"
```

This program demonstrates:
- **BASIC syntax** (line numbers, PRINT, LET, IF...THEN, GOSUB)
- **PILOT interaction** (T: for text output, A: for input with variables)
- **Logo graphics** (TO/END procedures, REPEAT loops, turtle commands)
- **Seamless integration** between all three paradigms

---

## 🚀 Choosing Your Implementation

Time Warp IDE offers six different implementations, each optimized for specific use cases. Choose the one that best fits your needs:

### 🦀 **Rust Implementation** - *The Performance Champion*

**🎯 Best For:**
- Production educational environments
- Advanced programming projects  
- Performance-critical applications
- Schools with modern computer labs

**✨ Advantages:**
- Fastest execution speed
- Native desktop integration
- Advanced compiler features
- Professional development tools
- Minimal system resource usage

**⚠️ Considerations:**
- Requires compilation from source OR pre-built binaries
- More technical setup process
- Best suited for intermediate to advanced users

### 🐍 **Python Implementation** - *The Educational Favorite*

**🎯 Best For:**
- Learning and teaching programming
- Classroom environments
- Curriculum development
- Experimentation and modification

**✨ Advantages:**
- Easy to install and modify
- Extensive documentation
- Clear, readable codebase
- Comprehensive test suite
- Great for understanding how interpreters work

**⚠️ Considerations:**
- Requires Python 3.8+ installation
- Slower execution than compiled versions
- Larger memory footprint

### 🌐 **Web Implementation** - *The Universal Solution*

**🎯 Best For:**
- BYOD (Bring Your Own Device) classrooms
- Quick demonstrations
- Tablets and mobile devices
- No-installation environments

**✨ Advantages:**
- Zero installation required
- Works on any modern browser
- Automatic updates
- Easy sharing of programs
- Cross-platform compatibility

**⚠️ Considerations:**
- Requires internet connection for initial load
- Limited file system access
- Performance limited by browser JavaScript engine

### 💾 **DOS Implementation** - *The Retro Experience*

**🎯 Best For:**
- Computer history education
- Retro computing enthusiasts
- Minimal system requirements
- Understanding programming evolution

**✨ Advantages:**
- Authentic vintage computing experience
- Runs on very old hardware
- Educational value for computer history
- Single executable file

**⚠️ Considerations:**
- Text-mode interface only
- Limited graphics capabilities
- Requires DOSBox for modern systems
- Advanced users only

### 🪟 **Windows Implementation** - *The Enterprise Choice*

**🎯 Best For:**
- Windows-only environments
- Educational institutions with Windows policies
- Legacy system support
- Enterprise deployments

**✨ Advantages:**
- Native Windows integration
- Professional installer
- System administration support
- Familiar Windows interface

**⚠️ Considerations:**
- Windows-only (obviously)
- Larger download size
- May require administrator privileges

### 🍎 **Apple Implementation** - *The Modern Mobile Experience*

**🎯 Best For:**
- iPad classrooms
- macOS environments
- iOS app development education
- Apple ecosystem integration

**✨ Advantages:**
- Native iOS and macOS experience
- Touch-friendly interface
- iCloud synchronization
- App Store distribution

**⚠️ Considerations:**
- Apple devices only
- App Store approval process
- iOS version requirements

---

## 💻 System Requirements

### 🦀 **Rust Implementation**

#### **Minimum Requirements:**
- **OS**: Linux, macOS 10.15+, Windows 10+
- **CPU**: x86_64 or ARM64 (Apple M1/M2)
- **RAM**: 512 MB available memory
- **Storage**: 50 MB free space
- **Graphics**: Basic OpenGL 3.0+ support

#### **Recommended Requirements:**
- **RAM**: 2 GB available memory
- **Storage**: 200 MB free space (for examples and documentation)
- **Graphics**: Dedicated GPU with OpenGL 4.0+ for smooth animations

#### **Development Requirements (Building from Source):**
- **Rust**: 1.70.0 or later
- **Cargo**: Included with Rust
- **Build Tools**: Platform-specific C compiler
- **Storage**: 1 GB free space for build artifacts

### 🐍 **Python Implementation**

#### **Minimum Requirements:**
- **OS**: Any platform with Python 3.8+ support
- **Python**: 3.8 or later (3.10+ recommended)
- **RAM**: 256 MB available memory
- **Storage**: 100 MB free space

#### **Recommended Requirements:**
- **Python**: 3.11 or later for best performance
- **RAM**: 1 GB available memory
- **Storage**: 500 MB free space (for virtual environment and examples)

#### **Dependencies:**
```bash
# Core dependencies (automatically installed)
PySide6 >= 6.0.0          # GUI framework
Pillow >= 9.0.0           # Image processing
numpy >= 1.20.0           # Numerical computations

# Development dependencies (optional)
pytest >= 7.0.0           # Testing framework
black >= 22.0.0           # Code formatter
mypy >= 0.991             # Type checker
```

---

## ⚡ Quick Start Guide

### 🚀 **The 5-Minute Time Warp Experience**

Let's get you up and running with Time Warp in just 5 minutes! We'll use the Python implementation for the fastest start.

#### **Step 1: Install Time Warp (2 minutes)**

```bash
# Clone repository
git clone https://github.com/James-HoneyBadger/Time_Warp.git
cd Time_Warp/Time_Warp_Python

# Install dependencies
pip install PySide6 pillow

# Launch Time Warp IDE
python time_warp_ide.py
```

#### **Step 2: Your First TempleCode Program (2 minutes)**

Copy and paste this program into the code editor:

```templecode
T:Welcome to Time Warp IDE!
T:Let's draw a colorful square...

SETCOLOR red
PENWIDTH 5

TO SQUARE :SIZE
  REPEAT 4 [
    FORWARD :SIZE
    RIGHT 90
  ]
END

SQUARE 100
T:Beautiful! Now let's make it interactive.

T:What's your name?
A:$NAME
T:Hello $NAME! Let's draw a shape for you.

SETCOLOR blue
SQUARE 150

10 PRINT "Program complete, "; NAME; "!"
20 PRINT "You just mixed BASIC, PILOT, and Logo!"
```

#### **Step 3: Run and Explore (1 minute)**

1. **Click Run**: Press the ▶️ Run button or F5
2. **Watch the Magic**: See the turtle draw your square
3. **Interact**: Type your name when prompted
4. **Experiment**: Try changing colors, sizes, or adding new commands

**🎉 Congratulations!** You've just experienced the power of TempleCode - three programming languages unified in one environment!

---

## 🔧 Installation Guide

### 🦀 **Rust Implementation Setup**

#### **Option 1: Pre-Built Binaries (Recommended)**

1. **Visit Releases**: Go to [Time Warp Releases](https://github.com/James-HoneyBadger/Time_Warp/releases)
2. **Download Your Platform**:
   - `time-warp-linux-x64.tar.gz` - Linux x86_64
   - `time-warp-macos-intel.tar.gz` - macOS Intel
   - `time-warp-macos-arm64.tar.gz` - macOS Apple Silicon
   - `time-warp-windows-x64.zip` - Windows x64

3. **Extract and Run**:
   ```bash
   # Linux/macOS
   tar -xzf time-warp-*.tar.gz
   cd time-warp/
   ./time-warp
   
   # Windows: Extract ZIP and double-click time-warp.exe
   ```

#### **Option 2: Build from Source**

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Clone and build
git clone https://github.com/James-HoneyBadger/Time_Warp.git
cd Time_Warp/Time_Warp_Rust
cargo build --release
cargo run --release
```

### 🐍 **Python Implementation Setup**

#### **Simple Installation:**
```bash
git clone https://github.com/James-HoneyBadger/Time_Warp.git
cd Time_Warp/Time_Warp_Python
pip install -r requirements.txt
python time_warp_ide.py
```

#### **Virtual Environment (Recommended):**
```bash
python3 -m venv timewarp_env
source timewarp_env/bin/activate  # Windows: timewarp_env\Scripts\activate
pip install -r requirements.txt
python time_warp_ide.py
```

---

## 🎨 Interface Overview

### 🖥️ **Main Interface Components**

#### **📝 Code Editor Panel**
- **Line Numbers**: Optional line numbering for easy reference
- **Syntax Highlighting**: Color-coded keywords for BASIC, PILOT, and Logo
- **Auto-Indentation**: Smart indentation for nested structures
- **Find & Replace**: Powerful search functionality
- **Bracket Matching**: Highlight matching brackets and parentheses

#### **🐢 Turtle Graphics Canvas**
- **Resizable Canvas**: Adjust size to fit your projects
- **Zoom Controls**: Zoom in/out for detailed work
- **Pan Support**: Move around large drawings
- **Export Options**: Save graphics as PNG or SVG
- **Animation Controls**: Speed up or slow down turtle movements

#### **📋 Output Panel**
- **Colored Output**: Different colors for different message types
- **Error Highlighting**: Clear marking of error messages
- **Copy Support**: Easy copying of output text
- **History**: Scroll through previous outputs

#### **🔧 Toolbar**
- **▶️ Run**: Execute the current program (F5)
- **⏹️ Stop**: Halt program execution (Shift+F5)
- **💾 Save**: Save current program to file
- **📂 Open**: Load program from file
- **🆕 New**: Create new blank program
- **🎨 Clear Canvas**: Reset turtle graphics canvas

### 🎨 **Theme System**

#### **🌅 Light Themes:**
- **Classic Light**: Traditional white background, black text
- **Educational**: High contrast for classroom projectors

#### **🌙 Dark Themes:**
- **Dracula**: Popular purple-tinted dark theme
- **Monokai**: Classic dark theme with vibrant colors
- **Ocean**: Deep blue theme for comfortable coding

---

## ✍️ Writing Your First Program

### 🎯 **Hello World Examples**

#### **Simple BASIC:**
```templecode
10 PRINT "Hello, World!"
20 PRINT "Welcome to Time Warp IDE!"
```

#### **Interactive PILOT:**
```templecode
T:What's your name?
A:$NAME
T:Hello, $NAME! Welcome to programming!
```

#### **Visual Logo:**
```templecode
SETCOLOR blue
PENWIDTH 3
REPEAT 4 [
  FORWARD 50
  RIGHT 90
]
PRINT "Drew a blue square!"
```

#### **Mixed TempleCode:**
```templecode
10 PRINT "=== Time Warp Demo ==="

T:What's your favorite color?
A:$COLOR
T:Great choice! Let's draw with $COLOR.

SETCOLOR $COLOR
TO FLOWER
  REPEAT 8 [
    FORWARD 50
    RIGHT 45
  ]
END
FLOWER

20 PRINT "Beautiful flower in "; COLOR; "!"
```

### 🎮 **Interactive Game Example**

```templecode
10 PRINT "🎯 Guess My Number!"
20 LET SECRET = INT(RND * 100) + 1
30 LET TRIES = 0

*GAME_LOOP
T:Guess a number (1-100):
A:$GUESS
40 LET TRIES = TRIES + 1

50 IF VAL(GUESS) = SECRET THEN J:WIN
60 IF VAL(GUESS) < SECRET THEN T:Too low!
70 IF VAL(GUESS) > SECRET THEN T:Too high!

REM Visual hint
CLEARSCREEN
SETCOLOR purple
FORWARD VAL(GUESS)

J:GAME_LOOP

*WIN
T:🎉 Correct! The number was $SECRET
T:You guessed it in $TRIES tries!

REM Victory animation
CLEARSCREEN
SETCOLOR gold
REPEAT 36 [
  FORWARD 10
  RIGHT 10
]
```

---

## 📖 TempleCode Programming Reference

### 🔤 **BASIC Commands**

#### **Variables and Math:**
```templecode
10 LET X = 5
20 LET Y = X * 2 + 3
30 PRINT "X ="; X; "Y ="; Y
```

#### **Control Flow:**
```templecode
10 FOR I = 1 TO 5
20   PRINT "Count:", I
30 NEXT I

40 IF X > 10 THEN PRINT "Big number!"
50 IF Y < 0 THEN GOTO 100
```

#### **Procedures:**
```templecode
10 GOSUB 1000  REM Call subroutine
20 END

1000 REM Subroutine starts here
1010 PRINT "In subroutine"
1020 RETURN
```

### 🗣️ **PILOT Commands**

#### **Text and Input:**
```templecode
T:This displays text and waits for ENTER
A:$VARIABLE    REM Gets input into $VARIABLE
TN:No wait     REM Display without waiting
```

#### **Pattern Matching:**
```templecode
T:What's your favorite color?
A:$COLOR
M:red,blue: T:Primary color!
M:green,yellow: T:Nice choice!
M:*: T:Interesting color!
```

#### **Jumps and Labels:**
```templecode
T:Starting the program...
J:MIDDLE      REM Jump to *MIDDLE

*MIDDLE
T:This is the middle section
J:END

*END
T:Program finished!
```

### 🐢 **Logo Commands**

#### **Basic Movement:**
```templecode
FORWARD 50    REM Move forward 50 units
BACK 25       REM Move backward 25 units
RIGHT 90      REM Turn right 90 degrees
LEFT 45       REM Turn left 45 degrees
```

#### **Pen Control:**
```templecode
PENUP         REM Lift pen (move without drawing)
PENDOWN       REM Put pen down (draw while moving)
SETCOLOR red  REM Set pen color
PENWIDTH 5    REM Set pen thickness
```

#### **Procedures:**
```templecode
TO SQUARE :SIZE
  REPEAT 4 [
    FORWARD :SIZE
    RIGHT 90
  ]
END

SQUARE 100    REM Call procedure with parameter
```

---

## 🛠️ Troubleshooting

### ❌ **Common Error Messages**

#### **"Unknown command 'FORWRD'"**
- **Cause**: Misspelled command
- **Solution**: Check spelling - should be `FORWARD`

#### **"Variable 'X' not defined"**
- **Cause**: Using variable before setting it
- **Solution**: Use `LET X = 5` before using `X`

#### **"Procedure 'SQUARE' not found"**
- **Cause**: Calling procedure before defining it
- **Solution**: Define procedures with `TO...END` before calling

### 🔧 **Platform-Specific Issues**

#### **Python: "No module named 'PySide6'"**
```bash
pip install PySide6
# Or for development:
pip install -r requirements.txt
```

#### **Rust: "command not found: cargo"**
```bash
# Install Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### **Graphics not appearing:**
- Check that turtle canvas is visible (Graphics tab)
- Ensure `PENDOWN` is set before drawing
- Try `CLEARSCREEN` to reset canvas

### 📞 **Getting Help**

- **Documentation**: Check `docs/` folder for detailed guides
- **Examples**: Browse `examples/` for sample programs  
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join discussions on GitHub Discussions

---

**🎓 Happy coding with Time Warp IDE!** Whether you're learning your first programming language or exploring the connections between different paradigms, TempleCode provides a unique and powerful environment for computational creativity.
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


