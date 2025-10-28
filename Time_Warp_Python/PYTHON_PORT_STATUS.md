# Time Warp IDE - Python Implementation

**Status:** In Progress  
**Version:** 2.0.0 (Ported from Rust)  
**Date:** October 28, 2025

## Overview

Complete Python port of Time Warp IDE from Rust implementation. Provides educational programming environment for PILOT, BASIC, and Logo languages with modern UI.

## Project Structure

```
Time_Warp_Python/
├── time_warp/              # Main package
│   ├── __init__.py
│   ├── core/               # Core interpreter engine
│   │   ├── __init__.py
│   │   └── interpreter.py  # ✅ COMPLETE (465 lines)
│   ├── graphics/           # Turtle graphics
│   │   ├── __init__.py
│   │   └── turtle_state.py # ✅ COMPLETE (155 lines)
│   ├── utils/              # Utilities
│   │   ├── __init__.py
│   │   ├── expression_evaluator.py  # ✅ COMPLETE (345 lines)
│   │   └── error_hints.py  # 🚧 TO CREATE
│   ├── languages/          # Language executors
│   │   ├── __init__.py     # 🚧 TO CREATE
│   │   ├── pilot.py        # 🚧 TO CREATE
│   │   ├── basic.py        # 🚧 TO CREATE
│   │   └── logo.py         # 🚧 TO CREATE
│   ├── compiler/           # TempleCode compiler
│   │   ├── __init__.py     # 🚧 TO CREATE
│   │   └── compiler.py     # 🚧 TO CREATE
│   └── ui/                 # UI layer (PySide6/tkinter)
│       ├── __init__.py     # 🚧 TO CREATE
│       ├── main_window.py  # 🚧 TO CREATE
│       ├── editor.py       # 🚧 TO CREATE
│       ├── output.py       # 🚧 TO CREATE
│       ├── canvas.py       # 🚧 TO CREATE
│       └── themes.py       # 🚧 TO CREATE
├── tests/                  # Test suite
│   └── test_*.py           # 🚧 TO CREATE (70+ tests)
├── examples/               # Sample programs
│   └── *.{pilot,bas,logo}  # 🚧 TO COPY (32 files)
├── docs/                   # Documentation
│   └── *.md                # 🚧 TO CREATE
├── setup.py                # 🚧 TO CREATE
├── pyproject.toml          # 🚧 TO CREATE
├── requirements.txt        # 🚧 TO CREATE
└── README.md               # 🚧 TO CREATE
```

## Completed Modules

### ✅ core/interpreter.py (465 lines)
**Status:** Complete, fully ported from Rust

**Key Classes:**
- `Interpreter`: Main execution engine
- `ExecutionResult`: Control flow enum (CONTINUE, END, JUMP, WAIT_FOR_INPUT)
- `ScreenMode`: Text/Graphics modes
- `Language`: PILOT/BASIC/Logo enum
- `ForContext`: FOR loop state
- `InputRequest`: Pending UI input

**Features:**
- Program loading and parsing
- Line number mapping (BASIC)
- Label extraction (PILOT)
- Execution with timeout (10s) and iteration limits (100k)
- Error recovery with enhanced error messages
- Variable interpolation (*VAR* syntax)
- Safe expression evaluation
- Input/output handling

**Security:**
- MAX_ITERATIONS = 100,000
- MAX_EXECUTION_TIME = 10 seconds
- Safe expression evaluator (no eval/exec)

### ✅ graphics/turtle_state.py (155 lines)
**Status:** Complete, fully ported from Rust

**Key Classes:**
- `TurtleState`: Turtle graphics state
- `TurtleLine`: Line segment dataclass

**Features:**
- Position tracking (x, y, heading)
- Pen control (up/down, color, width)
- Movement commands (forward, back, left, right)
- Absolute positioning (goto, home)
- Line history for rendering
- Background color
- Turtle visibility

**Canvas:**
- Coordinate system: (0,0) at center
- Y-axis inverted (up is negative)
- Default canvas: 800×600

### ✅ utils/expression_evaluator.py (345 lines)
**Status:** Complete, fully ported from Rust

**Features:**
- Safe expression evaluation (no eval/exec)
- Operators: +, -, *, /, %, ^ (power)
- Comparisons: <, >, <=, >=, ==, != (also <> → !=)
- Functions: sin, cos, tan, sqrt, abs, log, exp, min, max, pow, rand, floor, ceil, round
- Variables: Dynamic dictionary
- Token caching for performance
- Shunting Yard algorithm for RPN conversion
- Security: MAX_TOKENS = 1000

## Remaining Work

### 🚧 Priority 1: Language Executors (Est. 600 lines total)

**languages/pilot.py** (~200 lines)
- Commands: T:, A:, U:, C:, Y:, N:, M:, J:, L:, E:, R:
- Pattern matching
- Conditional execution
- Label jumps
- Variable storage

**languages/basic.py** (~250 lines)
- Commands: PRINT, LET, INPUT, GOTO, IF/THEN, FOR/NEXT, GOSUB/RETURN
- Screen modes (SCREEN, CLS, LOCATE)
- INKEY$ support
- Expression evaluation

**languages/logo.py** (~150 lines)
- Turtle commands: FORWARD, BACK, LEFT, RIGHT, PENUP, PENDOWN
- Procedures: TO/END with parameters
- REPEAT loops
- Color commands: SETCOLOR, SETPENCOLOR, SETBGCOLOR

### 🚧 Priority 2: Error Hints & Utilities (Est. 150 lines)

**utils/error_hints.py** (~150 lines)
- Typo suggestions (50+ common typos)
- Levenshtein distance algorithm
- Syntax mistake detection
- Command suggestions

**utils/__init__.py**
- Module exports

### 🚧 Priority 3: Compiler (Est. 250 lines)

**compiler/compiler.py** (~250 lines)
- TempleCode → C transpiler
- Variable mapping (numeric/string)
- Expression translation
- System compiler invocation (gcc/clang)
- REM comment handling
- INPUT prompt support

### 🚧 Priority 4: UI Layer (Est. 800 lines)

Choose **PySide6** (preferred) or **tkinter**:

**ui/main_window.py** (~200 lines)
- Main application window
- Menu bar (File, Edit, Run, Help)
- Tab management (Editor, Output, Debug, Explorer, Help)
- Theme application
- Keyboard shortcuts

**ui/editor.py** (~150 lines)
- Code editor widget
- Syntax highlighting (optional)
- Line numbers
- Find/replace dialog
- Undo/redo integration

**ui/output.py** (~100 lines)
- Text output display
- Input prompt handling
- Scrolling
- Formatting

**ui/canvas.py** (~150 lines)
- Turtle graphics rendering
- Zoom/pan controls
- PNG export
- Line drawing with anti-aliasing

**ui/themes.py** (~100 lines)
- Theme definitions (8 themes)
- Color schemes
- Theme application
- Persistence

**ui/menubar.py** (~100 lines)
- Menu actions (New, Open, Save, Run, Step, Stop)
- File dialogs
- About dialog
- Help system

### 🚧 Priority 5: Testing (Est. 1500 lines)

Port 72 tests from Rust:

**tests/test_interpreter.py** (~300 lines)
- Program loading
- Execution flow
- Error recovery
- Timeout protection

**tests/test_pilot.py** (~250 lines)
- T:, A:, M:, Y:, N: commands
- Pattern matching
- Conditional execution

**tests/test_basic.py** (~300 lines)
- PRINT, LET, INPUT
- IF/THEN, FOR/NEXT
- GOTO, GOSUB/RETURN

**tests/test_logo.py** (~250 lines)
- Turtle movement
- Procedures
- REPEAT loops

**tests/test_expression_evaluator.py** (~200 lines)
- Arithmetic operations
- Functions
- Variables
- Error handling

**tests/test_compiler.py** (~100 lines)
- C code generation
- Compilation
- Execution

**tests/test_integration.py** (~100 lines)
- End-to-end workflows
- Multi-language programs

### 🚧 Priority 6: Package & Documentation (Est. 500 lines)

**setup.py / pyproject.toml** (~100 lines)
- Package metadata
- Dependencies
- Entry points
- Installation config

**requirements.txt** (~20 lines)
```txt
PySide6>=6.5.0  # or tkinter (stdlib)
# All other deps are stdlib
```

**README.md** (~200 lines)
- Project description
- Installation instructions
- Quick start guide
- Examples
- Screenshots

**docs/** (~200 lines)
- API_REFERENCE.md
- DEVELOPER_GUIDE.md
- USER_GUIDE.md

## Dependencies

### Required (Stdlib)
- `re` - Regular expressions
- `math` - Mathematical functions
- `time` - Timing
- `random` - Random numbers
- `enum` - Enumerations
- `dataclasses` - Data structures
- `typing` - Type hints

### UI Framework (Choose One)
- **PySide6** (recommended): Modern, Qt6-based, cross-platform
- **tkinter**: Stdlib, lightweight, platform-native

### Testing
- `pytest` - Test framework
- `pytest-cov` - Coverage reports

## Mapping: Rust → Python

| Rust Feature | Python Equivalent |
|--------------|-------------------|
| `anyhow::Result<T>` | `try/except` with custom exceptions |
| `std::collections::HashMap` | `dict` |
| `Vec<T>` | `list` |
| `Option<T>` | `Optional[T]` from `typing` |
| `enum` | `Enum` from `enum` module |
| `once_cell::Lazy` | `@functools.lru_cache` or module-level globals |
| `regex::Regex` | `re.compile()` |
| `eframe/egui` | `PySide6` or `tkinter` |
| `Cargo.toml` | `setup.py` / `pyproject.toml` |
| `#[derive]` macros | `@dataclass` decorator |
| `&str` / `String` | `str` |
| `f64` | `float` |
| `usize` | `int` |

## Architecture Principles (Maintained from Rust)

1. **Stateless Executors**: Language modules (pilot, basic, logo) are stateless - all state in Interpreter
2. **Error Recovery**: Continue execution on non-fatal errors, log to output
3. **Security First**: Timeout protection, iteration limits, no eval/exec
4. **Type Safety**: Use type hints throughout
5. **Performance**: Cache compiled regexes, pre-allocate lists
6. **Testing**: Comprehensive test coverage (72+ tests)

## Development Workflow

### Step 1: Complete Core Modules
- [x] interpreter.py
- [x] turtle_state.py
- [x] expression_evaluator.py
- [ ] error_hints.py

### Step 2: Implement Language Executors
- [ ] pilot.py (200 lines)
- [ ] basic.py (250 lines)
- [ ] logo.py (150 lines)

### Step 3: Add Compiler
- [ ] compiler.py (250 lines)

### Step 4: Build UI
- [ ] Choose framework (PySide6 recommended)
- [ ] main_window.py
- [ ] editor.py
- [ ] output.py
- [ ] canvas.py
- [ ] themes.py

### Step 5: Port Tests
- [ ] Port 72 tests from Rust test suite
- [ ] Achieve 100% test pass rate

### Step 6: Package
- [ ] Create setup.py
- [ ] Write documentation
- [ ] Copy 32 example programs
- [ ] Create entry point script

## Code Quality Standards

- **PEP 8**: Follow Python style guide
- **Type Hints**: Use throughout for IDE support
- **Docstrings**: Google-style for all public APIs
- **Testing**: pytest with 80%+ coverage
- **Linting**: pylint / flake8 / ruff
- **Formatting**: black / autopep8

## Estimated Completion

- **Total Lines of Code**: ~4,500 lines (vs Rust: ~5,000)
- **Development Time**: 2-3 days for complete port
- **Testing Time**: 1 day
- **Documentation**: 0.5 days

**Total Estimate**: 3.5-4.5 days for production-ready Python version

## Current Progress

- ✅ Project structure created
- ✅ Core interpreter complete (465 lines)
- ✅ Turtle graphics complete (155 lines)
- ✅ Expression evaluator complete (345 lines)
- ✅ Error hints complete (325 lines)
- ✅ PILOT executor complete (162 lines)
- ✅ BASIC executor complete (412 lines)
- ✅ Logo executor complete (383 lines)
- ✅ Language executors wired into interpreter
- ✅ Compiler module complete (215 lines)
- ✅ Basic functionality tests passing (5/5)
- ✅ README.md created
- ✅ setup.py and requirements.txt created
- 🚧 **Next**: UI layer (PySide6), full test suite

**Completion**: ~60% (3,262 / ~5,000 lines estimated)

## Running the Python Version (Future)

```bash
# Install
pip install -e .

# Run IDE
time-warp

# Run program
time-warp myprogram.pilot

# Compile program
time-warp --compile myprogram.bas -o myprogram
```

## Advantages of Python Version

1. **Ease of Installation**: `pip install` vs Rust toolchain
2. **Rapid Prototyping**: Faster iteration for educational use
3. **Library Ecosystem**: Rich Python libraries for extensions
4. **Accessibility**: More educators know Python than Rust
5. **Cross-Platform**: Python runs everywhere

## Maintaining Parity with Rust

- Same test suite (72 tests)
- Same features and commands
- Same security protections
- Same example programs (32 files)
- Same documentation structure

---

**Next Steps**: Continue implementation following priority order. Focus on language executors next to enable program execution.
