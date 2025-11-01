# Time Warp IDE

**Educational Programming Environment for TempleCode**

Time Warp IDE is a modern, cross-platform educational programming environment that implements **TempleCode** — a unified language combining the best features of BASIC, PILOT, and Logo. Available in multiple implementations: Rust (native, high-performance), Python (portable, educational), Web (browser-based), DOS (retro computing), and Windows (native Windows).

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Rust](https://img.shields.io/badge/Rust-1.70+-orange.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Stable-success.svg)

---

## 🎯 What is TempleCode?

TempleCode is a single, unified programming language that seamlessly blends three classic educational languages:

- **BASIC**: Variables, expressions, control flow (`PRINT`, `LET`, `IF...THEN`, `FOR...NEXT`, `GOSUB`)
- **PILOT**: Interactive text commands with pattern matching (`T:`, `A:`, `M:`, `Y:/N:`, jumps with `J:`)
- **Logo**: Turtle graphics with procedures (`FORWARD`, `LEFT/RIGHT`, `REPEAT`, `TO/END`, colors)

You can **mix all three styles** in a single program! For example:

```templecode
10 PRINT "Starting turtle demo"
20 LET SIZE = 100

T:Drawing a colorful square
SETCOLOR blue
PENWIDTH 10
REPEAT 4 [
  FORWARD SIZE
  RIGHT 90
]

30 PRINT "All done!"
```

---

## 📦 Implementations

### Rust Implementation (Recommended for Production)

**Location**: `Time_Warp_Rust/`

- **Performance**: Native compiled executable with egui UI
- **Features**: Full TempleCode support, async execution, PNG export, compiler (experimental)
- **Platforms**: Linux, macOS, Windows
- **Documentation**: [Rust README](Time_Warp_Rust/README.md) | [User Guide](Time_Warp_Rust/USER_GUIDE.md)

```bash
cd Time_Warp_Rust
cargo run --release
```

### Python Implementation (Educational & Development)

**Location**: `Time_Warp_Python/`

- **Portability**: Pure Python with PySide6 GUI
- **Features**: Full TempleCode support, comprehensive test suite, easy to extend
- **Platforms**: Cross-platform (Python 3.8+)
- **Documentation**: [Python README](Time_Warp_Python/README.md) | [Quick Start](Time_Warp_Python/QUICKSTART.md)

```bash
cd Time_Warp_Python
python time_warp_ide.py
```

### Web Implementation (Browser-Based)

**Location**: `Time_Warp_Web/`

- **Accessibility**: Run directly in any modern web browser
- **Features**: Full TempleCode support, working turtle graphics, comprehensive debugging tools
- **Platforms**: Any device with a web browser (desktop, tablet, mobile)
- **Documentation**: [Web README](Time_Warp_Web/README.md)

```bash
cd Time_Warp_Web
# Open index.html in your browser or serve via HTTP
python -m http.server 8080
```

### DOS Implementation (Retro Computing)

**Location**: `Time_Warp_DOS/`

- **Retro Compatibility**: Single-file C89 interpreter for MS-DOS and DOSBox
- **Features**: Text-mode interface, full BASIC/PILOT/Logo support, no external dependencies
- **Platforms**: MS-DOS, DOSBox, Windows 95/98/ME DOS prompt
- **Documentation**: [DOS README](Time_Warp_DOS/README.md)

```bash
cd Time_Warp_DOS
# Build with OpenWatcom or DJGPP (see README for details)
dosbox -conf dosbox-timewarp.conf
```

### Windows Implementation (Native Windows)

**Location**: `Time_Warp_Windows/`

- **Platform Integration**: Native Windows launchers and installers
- **Features**: PowerShell helpers, batch file launchers, Windows-specific packaging
- **Platforms**: Windows (all modern versions)
- **Documentation**: [Windows README](Time_Warp_Windows/README.md)

```batch
cd Time_Warp_Windows
Launch-TimeWarp.cmd
```

---

## ✨ Key Features

### Language Features

- ✅ **Unified TempleCode**: Mix BASIC, PILOT, and Logo in one program
- ✅ **Turtle Graphics**: Full Logo-compatible turtle with procedures, colors, and pen control
- ✅ **50+ Commands**: Complete command set verified and tested
- ✅ **Expression Evaluation**: Safe math expressions with operator precedence
- ✅ **Pattern Matching**: PILOT-style text matching with wildcards
- ✅ **User Procedures**: Define reusable procedures with parameters (`TO/END`)
- ✅ **Multi-line Loops**: `REPEAT` blocks with proper nesting
- ✅ **Color Support**: Named colors (red, blue, green, etc.), hex (#FF69B4), and RGB

### IDE Features

- 🎨 **Modern UI**: Clean, responsive interface with syntax highlighting
- 🐢 **Turtle Canvas**: Zoom/pan graphics canvas with coordinate system
- 🎨 **8 Themes**: Dracula, Monokai, Solarized Dark, Ocean, Spring, Sunset, Candy, Forest
- 📁 **File Management**: Open/save with recent files list
- ▶️ **Run Controls**: Execute, stop, clear output/canvas
- 📊 **Real-time Output**: Colored text output with emoji indicators
- 🔍 **Error Help**: Syntax error detection with helpful suggestions

### Educational Features

- 📚 **33+ Example Programs**: Organized by language style and difficulty
- 📖 **Complete Documentation**: Guides for students, teachers, and developers
- 🎓 **Lesson Plans**: 8-week curriculum included (Rust version)
- 💡 **Interactive Learning**: PILOT-style questions and pattern matching
- 🎮 **Game Development**: INKEY$ support for interactive programs

---

## 🚀 Quick Start

From the repository root:

```bash
./run.sh python       # Launch Python IDE
./run.sh rust --release  # Launch Rust IDE (release)
```

### Option 1: Rust (Fast & Native)

```bash
# Clone the repository
git clone https://github.com/James-HoneyBadger/Time_Warp.git
cd Time_Warp/Time_Warp_Rust

# Build and run
cargo run --release

# Or build once and run executable
cargo build --release
./target/release/time-warp
```

### Option 2: Python (Portable & Educational)

```bash
# Clone the repository
git clone https://github.com/James-HoneyBadger/Time_Warp.git
cd Time_Warp/Time_Warp_Python

# Install dependencies
pip install PySide6 pillow

# Run the IDE
python time_warp_ide.py

# Or run CLI
python run_time_warp.py examples/logo_flower.logo
```

---

## 📚 Documentation

### For Users

- **[User Guide](USER_GUIDE.md)** - Unified guide for both Python and Rust
- **[Getting Started](Time_Warp_Rust/docs/GETTING_STARTED.md)** - Your first 5 minutes
- **[Quick Reference](Time_Warp_Rust/docs/QUICK_REFERENCE.md)** - Complete command reference
- **[Turtle Graphics Reference](Time_Warp_Python/docs/TURTLE_GRAPHICS_REFERENCE.md)** - All graphics commands
- **[Student Guide](Time_Warp_Rust/docs/STUDENT_GUIDE.md)** - Language cheatsheets

### For Teachers

- **[Lesson Plans](Time_Warp_Rust/docs/LESSON_PLANS.md)** - 8-week curriculum
- **[Teacher Guide](Time_Warp_Rust/docs/TEACHER_GUIDE.md)** - Session outlines
- **[Programming Challenges](Time_Warp_Rust/docs/PROGRAMMING_CHALLENGES.md)** - 12 challenges with solutions

### For Developers

- **[Python API Reference](Time_Warp_Python/README.md#api-usage)** - Interpreter API
- **[Rust Developer Reference](Time_Warp_Rust/docs/DEVELOPER_REFERENCE.md)** - Extension guide
- **[Architecture](Time_Warp_Rust/ARCHITECTURE.md)** - System design
- **[Contributing](Time_Warp_Rust/CONTRIBUTING.md)** - How to contribute

---

## 🎨 Example Programs

The `examples/` directory contains 33+ programs demonstrating all language features:

### BASIC Programs (10)
- `basic_guess.bas` - Number guessing game
- `basic_hangman.bas` - Word guessing game
- `basic_rock_paper_scissors.bas` - Interactive game
- `basic_inkey_demo.bas` - Keyboard input demo
- And more...

### PILOT Programs (7)
- `pilot_quiz.pilot` - Simple quiz system
- `pilot_dragon_adventure.pilot` - Text adventure game
- `pilot_calculator.pilot` - Interactive calculator
- And more...

### Logo Programs (15)
- `logo_flower.logo` - Colorful flower pattern
- `logo_koch_snowflake.logo` - Fractal generation
- `logo_spirograph.logo` - Complex geometric patterns
- `logo_starburst_blue.logo` - Starburst with colors
- And more...

### TempleCode (1)
- `demo.tc` - Mixed language demonstration

---

## 🧪 Testing

### Python Tests

```bash
cd Time_Warp_Python

# Run all tests
python test_ide.py

# Run specific test suites
python test_graphics.py
python test_all_turtle_commands.py
python verify_commands.py

# With pytest
pytest tests/ -v
```

### Rust Tests

```bash
cd Time_Warp_Rust

# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_name
```

---

## 🔧 Project Structure

```
Time_Warp/
├── Time_Warp_Python/          # Python implementation
│   ├── time_warp/             # Main package
│   │   ├── core/              # Interpreter engine
│   │   ├── languages/         # TempleCode executor
│   │   ├── graphics/          # Turtle graphics
│   │   ├── ui/                # PySide6 UI components
│   │   └── utils/             # Expression evaluator, error hints
│   ├── examples/              # 34 example programs
│   ├── tests/                 # Test suite
│   ├── docs/                  # Documentation
│   ├── time_warp_ide.py       # GUI entry point
│   └── run_time_warp.py       # CLI entry point
│
├── Time_Warp_Rust/            # Rust implementation
│   ├── src/                   # Source code
│   │   ├── interpreter/       # Core interpreter
│   │   ├── languages/         # Language modules
│   │   ├── graphics/          # Turtle & canvas
│   │   ├── ui/                # egui UI
│   │   ├── compiler/          # TempleCode compiler (experimental)
│   │   └── main.rs            # Entry point
│   ├── docs/                  # Comprehensive docs
│   ├── tests/                 # Rust test suite
│   └── Cargo.toml             # Rust dependencies
│
└── examples/                  # Shared examples (33 programs)
```

---

## 🎯 Turtle Graphics Commands

All turtle graphics commands are fully verified and working:

### Movement
- `FORWARD n` / `FD n` - Move forward
- `BACK n` / `BK n` / `BACKWARD n` - Move backward
- `LEFT n` / `LT n` - Turn left (degrees)
- `RIGHT n` / `RT n` - Turn right (degrees)
- `HOME` - Return to center
- `SETXY x y` - Move to position
- `SETHEADING angle` / `SETH angle` - Set heading

### Pen Control
- `PENUP` / `PU` - Lift pen
- `PENDOWN` / `PD` - Lower pen
- `PENWIDTH n` / `SETPENWIDTH n` / `SETPW n` / `SETPENSIZE n` - Set pen width

### Colors
- `SETCOLOR name` - Use color name (red, blue, green, yellow, cyan, magenta, orange, purple, pink, brown, gray, white, black)
- `SETCOLOR #RRGGBB` - Use hex color
- `SETCOLOR r g b` - Use RGB (0-255)
- `SETPENCOLOR r g b` / `SETPC r g b` - Set pen color (RGB)
- `SETBGCOLOR r g b` / `SETBG r g b` - Set background color

### Screen Control
- `CLEARSCREEN` / `CS` / `CLEAR` - Clear all drawings
- `HIDETURTLE` / `HT` - Hide turtle cursor
- `SHOWTURTLE` / `ST` - Show turtle cursor

### Loops & Procedures
- `REPEAT n [ commands ]` - Single-line loop
- Multi-line REPEAT:
  ```logo
  REPEAT count [
    commands
  ]
  ```
- User procedures:
  ```logo
  TO SQUARE :SIZE
    REPEAT 4 [
      FORWARD :SIZE
      RIGHT 90
    ]
  END
  
  SQUARE 100
  ```

**All 50+ commands verified!** See [Turtle Graphics Reference](Time_Warp_Python/docs/TURTLE_GRAPHICS_REFERENCE.md) for complete details.

---

## 🤝 Contributing

Contributions are welcome! Both implementations are actively maintained:

1. **Fork the repository**
2. **Create your feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** (follow existing code style)
4. **Run tests** (Python: `python test_ide.py`, Rust: `cargo test`)
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

See [CONTRIBUTING.md](Time_Warp_Rust/CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Inspired by classic educational languages: BASIC, PILOT, and Logo
- Built with modern tools: Rust, Python, egui, PySide6
- Designed for education, learning, and creative expression

---

## 📧 Contact

**Author**: James Temple  
**Email**: james@honey-badger.org  
**GitHub**: https://github.com/James-HoneyBadger/Time_Warp

---

## 🚦 Status

- ✅ **Rust Implementation**: Feature complete with compiler (recommended for production)
- ✅ **Python Implementation**: Feature complete, all tests passing
- ✅ **Web Implementation**: Browser-based IDE with working turtle graphics
- ✅ **DOS Implementation**: Text-mode C89 interpreter for retro computing
- ✅ **Windows Implementation**: Native Windows launchers and packaging
- ✅ **Documentation**: Comprehensive guides and references
- ✅ **Examples**: 33+ working programs
- ✅ **Tests**: Full coverage for all implementations

**Ready for educational use across all platforms!**
