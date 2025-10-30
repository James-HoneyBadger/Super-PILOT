# TempleCode IDE (formerly TempleCode)

![CI](https://github.com/James-HoneyBadger/TempleCode/actions/workflows/ci.yml/badge.svg?branch=main)

**Educational Programming Environment with BASIC and Logo**

TempleCode IDE is a comprehensive educational programming environment that focuses on BASIC programming with integrated Logo turtle graphics and advanced animation tools. Perfect for teaching programming fundamentals with visual feedback.

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/James-HoneyBadger/TempleCode.git
cd TempleCode

# Install basic dependencies
python3 -m pip install -r requirements.txt

# For development (includes testing tools)
python3 -m pip install -r requirements-dev.txt

# Run the IDE (new)
python3 TempleCode.py

# Legacy entrypoint (still works)
python3 TempleCode.py
```

## GUI prerequisites (Linux / Windows)

TempleCode’s IDE uses Tk. On Linux you may need to install system Tk packages; on Windows the official Python installer typically includes Tk support.

If you see an error like `ImportError: libtk8.6.so: cannot open shared object file` on Linux, install your distro’s Tk packages:

- Debian/Ubuntu
  ```bash
  sudo apt update
  sudo apt install python3-tk tk
  ```
- Fedora / RHEL / CentOS (dnf)
  ```bash
  sudo dnf install python3-tkinter tk
  ```
- openSUSE
  ```bash
  sudo zypper install python3-tk tk
  ```
- Arch Linux (including ARM64/aarch64)
  ```bash
  sudo pacman -Syu tk
  ```

Verify Tk is available:

```bash
python3 -c "import tkinter as tk; print('Tk ok, version=', tk.TkVersion)"
```

Windows 11 quick checks

1. Install Python 3.10+ from https://python.org (choose the installer and enable "Add Python to PATH").
2. Verify Tkinter and Pillow are available:

```powershell
python -c "import tkinter as tk; print('Tk ok, version=', tk.TkVersion)"
python -m pip install --user -r requirements.txt
```

If the Tk import fails on Windows, reinstall Python using the official installer and ensure the "tcl/tk and IDLE" option is selected.

Headless/CI hint: to run GUI smoke checks without a display, use a virtual X server:

```bash
sudo pacman -S --needed xorg-server-xvfb  # Arch
# or: sudo apt-get install xvfb           # Debian/Ubuntu
xvfb-run -a python3 TempleCode.py
```

### Your First Program

Try this in the editor:

```pilot
T:Hello, World!
T:Let's draw a square...

CS
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]

T:Done!
```

Press **F5** to run!

## 📚 Documentation

Comprehensive documentation for all users:

- **[📖 Student Guide](docs/STUDENT_GUIDE.md)** - Learn programming from scratch with 16 progressive lessons
- **[👩‍🏫 Teacher Guide](docs/TEACHER_GUIDE.md)** - 16-week curriculum, teaching strategies, and assessment tools
- **[🔧 Technical Reference](docs/TECHNICAL_REFERENCE.md)** - Complete API documentation and language specifications
- **[💻 Developer Handbook](docs/DEVELOPER_HANDBOOK.md)** - Contributing guidelines and architecture deep dive

**[📑 Documentation Index](docs/README.md)** - Navigate all documentation

## ✨ Features

### BASIC with Logo Graphics

- **BASIC**: Classic programming with line numbers and mathematical operations
- **Logo**: Visual turtle graphics for creative programming
- **Text Commands**: Simple T: commands for output

### Professional IDE

- **Syntax Highlighting**: Color-coded commands for all three languages
- **Advanced Debugger**: Breakpoints, step-through execution, variable inspection
- **Integrated Graphics**: Real-time turtle graphics canvas
- **Settings System**: Customizable themes, fonts, and preferences
- **Recent Files**: Quick access to your projects

### Educational Focus

- Perfect for classroom use
- Progressive difficulty
- Immediate visual feedback
- Error messages designed for beginners
- Comprehensive teaching resources

### Hardware Integration

- Arduino support (with simulation mode)
- Raspberry Pi GPIO integration
- IoT device management
- Sensors and actuators

## 🎓 Learning Resources

### For Students

Start with the [Student Guide](docs/STUDENT_GUIDE.md) for step-by-step tutorials:

1. **BASIC Language** (Lessons 1-5): Math, IF statements, FOR loops, functions
2. **Logo Graphics** (Lessons 6-10): Turtle drawing, patterns, procedures
3. **Projects**: Quiz programs, drawing gallery, text adventures

### For Teachers

The [Teacher Guide](docs/TEACHER_GUIDE.md) includes:

- **16-week curriculum** with detailed lesson plans
- **Teaching strategies**: Pair programming, live coding, debugging as learning
- **Assessment tools**: Rubrics, exit tickets, code reviews
- **Differentiation**: Support for struggling and advanced students
- **20+ project ideas** categorized by difficulty

## 🔧 For Developers

### Using as a Library

```python
from TempleCode import TempleCodeInterpreter

# Create interpreter
interp = TempleCodeInterpreter()

# Register callbacks
interp.on_output.append(lambda text: print(text))
interp.on_variable_changed.append(lambda name, val: print(f"{name} = {val}"))

# Execute program
program = """
T:Computing factorial...
U:N=5
U:RESULT=1
"""
success = interp.run_program(program)
```

See the [Technical Reference](docs/TECHNICAL_REFERENCE.md) for complete API documentation.

### Contributing

We welcome contributions! See the [Developer Handbook](docs/DEVELOPER_HANDBOOK.md) for:

- Development environment setup
- Code style guidelines
- Testing requirements
- Pull request process

```bash
# Run tests
python -m pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Format code
black .
isort .
```

## 📋 Language Quick Reference

### Text Output Commands

```templecode
T:text          Output text
```

### BASIC Commands

```basic
PRINT           Output text/numbers
LET var = val   Assign variable
INPUT var       Get user input
IF...THEN       Conditional execution
FOR...NEXT      Loop with counter
GOTO linenum    Jump to line number
```

### Logo Commands

```logo
FORWARD n       Move turtle forward
RIGHT n         Turn right (degrees)
LEFT n          Turn left (degrees)
PENUP/PENDOWN   Lift/lower pen
REPEAT n [...]  Loop n times
CS              Clear screen
```

## 🎯 Example Programs

### Hello World

```basic
10 PRINT "What is your name?"
20 INPUT NAME$
30 PRINT "Hello, "; NAME$
40 PRINT "Welcome to TempleCode!"
```

### Number Guessing Game (BASIC)

```basic
10 LET SECRET = INT(RND(10)) + 1
20 PRINT "Guess a number (1-10):"
30 INPUT GUESS
40 IF GUESS = SECRET THEN GOTO 70
50 PRINT "Wrong! Try again."
60 GOTO 20
70 PRINT "Correct! The number was "; SECRET
80 END
```

### Drawing Patterns (Logo)

```logo
CS
REPEAT 36 [
  REPEAT 4 [
    FORWARD 100
    RIGHT 90
  ]
  RIGHT 10
]
```

More examples in the [examples/](examples/) directory.

## 🎮 Version History

### Version 3.0.0 (Current)

**Turtle / Logo Extensions:**
- New commands: `COLOR`, `TRACE`, `KEEP_CANVAS`, `CENTER`, `PENSTYLE`, `DEBUGLINES`, `FIT`
- Pen style customization: `PENSTYLE solid|dashed|dotted`
- Auto color cycle per shape
- Pen-down start markers with optional tracing
- Auto-pan and dynamic scroll region
- Canvas preservation toggle
- Geometry inspection tools

**Interpreter / Core:**
- Conditional jump sentinel consumption (`Y:`/`N:` + `J:`/`T:`)
- Compute assignment: `C:VAR=EXPR`
- Nested `REPEAT` loops
- Macro system: `DEFINE` and `CALL`
- Performance profiling: `PROFILE ON/OFF/REPORT`
- Style-aware line metadata

**IDE / UX:**
- Output pane context menu (Copy/Clear)
- Dedicated Turtle menu
- Theme switching (dark/light mode)
- Extended syntax highlighting
- Breakpoint debugging with gutter
- Enhanced variables panel
- Settings persistence

### Version 2.0.0

- Modular architecture with event system
- Non-blocking execution with threading
- Enhanced debugger UI
- Settings system with JSON persistence
- Keyboard shortcuts
- Recent files menu

### Version 1.0.0

- Initial monolithic implementation
- Three-language support (PILOT, BASIC, Logo)
- Basic turtle graphics
- Simple IDE

## 🗺️ Roadmap

**Planned for >3.0.0:**
- Polygon fill & EXPORT (PNG/SVG) commands
- Persistent settings (trace, themes, profiling)
- BOUNDS and ZOOM/ZOOMRESET viewport helpers
- FILL mode for teaching geometry
- Sandboxed expression evaluator (remove eval)
- Live variable watch + time-travel execution

## 🧪 Testing

Run the comprehensive test suite:

```bash
# All tests
python -m pytest

# With coverage report
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_interpreter.py

# Verbose output
pytest -v
```

Test coverage includes:
- ✅ Core interpreter functionality
- ✅ All three language implementations
- ✅ Event callback system
- ✅ Threading and concurrency
- ✅ Hardware integration (mocked)
- ✅ Expression evaluation
- ✅ Security constraints

## 🤝 Contributing

Contributions are welcome! Please read the [Developer Handbook](docs/DEVELOPER_HANDBOOK.md) for:

1. **Development setup** - Environment configuration
2. **Code style** - PEP 8, Black formatting, type hints
3. **Testing** - Write tests for all new features
4. **Documentation** - Update relevant docs
5. **Pull requests** - Follow conventional commits

### Quick Contribution Workflow

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/TempleCode.git
cd TempleCode

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and test
# ... edit code ...
pytest

# 4. Format and lint
black .
isort .
flake8

# 5. Commit and push
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature-name

# 6. Create pull request on GitHub
```

## 📜 License

TempleCode IDE is released under the MIT License. See [LICENSE](LICENSE) file for details.

Documentation is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

## 🙏 Acknowledgments

TempleCode builds on decades of educational programming language research:

- **PILOT** - Developed by John Starkweather (1968)
- **BASIC** - Developed by John Kemeny and Thomas Kurtz (1964)
- **Logo** - Developed by Seymour Papert and colleagues (1967)

Special thanks to all contributors and educators using TempleCode in classrooms worldwide.

## 📞 Support & Community

- **📖 Documentation**: [docs/README.md](docs/README.md)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/James-HoneyBadger/TempleCode/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/James-HoneyBadger/TempleCode/discussions)
- **✉️ Email**: support@templecode.org

## ⭐ Star History

If you find TempleCode IDE useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for educators and students learning to program**

## Version 3 Highlights (3.0.0)

**Turtle / Logo Extensions:**
- New commands: `COLOR`, `TRACE`, `KEEP_CANVAS`, `CENTER`, `PENSTYLE`, `DEBUGLINES`, `FIT`, aliases (`SETCOLOR/SETCOLOUR`, `SETPENSIZE`).
- Pen style customization: `PENSTYLE solid|dashed|dotted` (teaching different stroke semantics).
- Auto color cycle per shape (each PENUP→PENDOWN transition advances palette).
- Pen-down start markers (small dots) + optional tracing (movement, heading, pen state).
- Auto-pan and dynamic scrollregion (shapes no longer appear to "disappear" off canvas).
- Canvas preservation toggle via command or Turtle menu.
- Geometry inspection: `DEBUGLINES` prints first N line segments & metadata; `FIT` recenters viewport to drawing bounds.

**Interpreter / Core:**

- Conditional jump sentinel consumption (`Y:`/`N:` + subsequent `J:` / `T:` logic stabilized).
- Compute assignment form: `C:VAR=EXPR`.
- Nested `REPEAT` loops: `REPEAT 3 [ REPEAT 2 [ FORWARD 50 RIGHT 90 ] LEFT 45 ]`.
- Macro system: `DEFINE STAR [ REPEAT 5 [ FORWARD 80 RIGHT 144 ] ]` then `CALL STAR`.
- Performance profiling: `PROFILE ON`, run program, `PROFILE REPORT` (per-command counts, avg, max, total ms).
- Style-aware line metadata tracked for debugging & future analytics.

IDE / UX:

- Output pane context menu (Copy / Copy All / Clear).
- Dedicated Turtle menu: Trace toggle, Preserve Canvas, Clear.
- Accent theme switching + dark/light mode.
- Auto-completion & syntax highlighting extended for: `DEFINE`, `CALL`, `REPEAT` (nested), `PENSTYLE`, `DEBUGLINES`, `FIT`, `PROFILE`.

## Roadmap (Planned >3.0.0)

- Polygon fill & EXPORT (PNG/SVG) commands.
- Settings persistence (trace / keep-canvas / last theme, profiling preference).
- BOUNDS and ZOOM/ZOOMRESET viewport helpers.
- FILL mode or SHAPE capture API for teaching geometry.
- Sandboxed expression evaluator refactor (remove eval).
- Live variable watch + time-travel execution (stretch goal).

## Running tests

From project root:

```bash
PYTHONPATH=. pytest -q
```

If you want me to open a pull request for these changes, tell me the target
branch (default `main`) and whether to create a descriptive PR title and body.
