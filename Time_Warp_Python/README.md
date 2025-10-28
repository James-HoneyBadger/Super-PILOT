# Time Warp IDE - Python Port (TempleCode)

Educational TempleCode programming environment — a unified language combining BASIC, PILOT, and Logo.

## Overview

Time Warp IDE is a modern educational programming platform built around **TempleCode** — a single, unified language that blends the strengths of three classics:

- **PILOT-style** text/label commands (e.g., T:, A:, M:, Y:/N:, L:, E:)
- **BASIC-style** control flow and expressions (PRINT, INPUT, IF/THEN, FOR/NEXT)
- **Logo-style** turtle graphics (FORWARD, LEFT/RIGHT, PENUP/PENDOWN, REPEAT)

Aligned with the Rust TempleCode implementation with functional parity.

## Features

- ✅ Unified TempleCode combining BASIC, PILOT, and Logo
- ✅ Turtle graphics with zoom/pan
- ✅ Safe expression evaluation (no eval/exec)
- ✅ Error detection with helpful suggestions
- ✅ TempleCode compiler (transpile to C)
- ✅ Comprehensive test suite
- ✅ Cross-platform support

## Installation

### From Source

```bash
git clone https://github.com/James-HoneyBadger/Time_Warp.git
cd Time_Warp/Time_Warp_Python
pip install -e .
```

### Requirements

- Python 3.8 or higher
- PySide6 (for GUI) or tkinter (stdlib alternative)
- Standard library only for core functionality

## Quick Start

### Desktop IDE (Recommended)

Launch the full graphical IDE:

```bash
cd Time_Warp/Time_Warp_Python
python time_warp_ide.py
```

Or open a specific file (TempleCode .tc is recommended):

```bash
python time_warp_ide.py examples/demo_templecode.tc
```

**Features:**
- Code editor with syntax highlighting
- Turtle graphics canvas with zoom/pan
- Output panel with colored text
- File menu with recent files
- 8 beautiful themes (Dracula, Monokai, Solarized, etc.)
- Run/Stop execution controls

### CLI Usage

Run programs from command line:

```python
from time_warp.core.interpreter import Interpreter
from time_warp.graphics.turtle_state import TurtleState

# Create interpreter and turtle
interp = Interpreter()
turtle = TurtleState()

# Load and run a program
program = """
T:Hello from PILOT
C:X = 5 + 3
U:X
E:
"""

interp.load_program(program)
output = interp.execute(turtle)
print(output)
```

### PILOT-style Example (TempleCode)

```pilot
L:START
T:What is your name?
A:NAME
T:Hello *NAME*!
M:yes
Y:CONTINUE
N:START
L:CONTINUE
T:Nice to meet you!
E:
```

### BASIC-style Example (TempleCode)

```basic
10 PRINT "Countdown"
20 FOR I = 10 TO 1 STEP -1
30 PRINT I
40 NEXT I
50 PRINT "Blastoff!"
```

### Logo-style Example (TempleCode)

```logo
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

## Architecture

```
time_warp/
├── core/              # Core interpreter engine
│   └── interpreter.py # Main execution engine
├── languages/         # Language executors
│   ├── templecode.py  # Unified TempleCode executor (BASIC/PILOT/Logo)
│   ├── pilot.py       # Compatibility shim → templecode
│   ├── basic.py       # Compatibility shim → templecode
│   └── logo.py        # Compatibility shim → templecode
├── graphics/          # Turtle graphics
│   └── turtle_state.py
├── utils/             # Utilities
│   ├── expression_evaluator.py  # Safe math eval
│   └── error_hints.py           # Typo detection
├── compiler/          # TempleCode compiler
│   └── compiler.py    # C code generation
└── ui/                # GUI (PySide6/tkinter)
    └── (to be implemented)
```

## Testing

```bash
# Run basic functionality tests
python test_basic_functionality.py

# Run full test suite (when implemented)
pytest tests/
```

## API Reference

### Interpreter

```python
from time_warp.core.interpreter import Interpreter

interp = Interpreter()
interp.load_program(source_code)
output = interp.execute(turtle)
```

### Turtle Graphics

```python
from time_warp.graphics.turtle_state import TurtleState

turtle = TurtleState()
turtle.forward(100)
turtle.right(90)
turtle.penup()
turtle.goto(0, 0)
```

### Expression Evaluator

```python
from time_warp.utils.expression_evaluator import ExpressionEvaluator

evaluator = ExpressionEvaluator({'X': 5, 'Y': 3})
result = evaluator.evaluate('X * 2 + Y')  # Returns 13.0
```

### Compiler

```python
from time_warp.compiler import compile_to_c, compile_to_executable

# Generate C code
c_code = compile_to_c(basic_source)

# Compile to executable
success = compile_to_executable(basic_source, 'program')
```

## Security Features

- **Iteration Limit**: 100,000 max iterations prevents infinite loops
- **Timeout Protection**: 10-second execution limit
- **Safe Evaluation**: No eval() or exec() - all expressions parsed manually
- **Token Limit**: Expression evaluator limits complexity

## Development Status

**Current Version**: 2.0.0-alpha

- ✅ Core interpreter (100%)
- ✅ Language executors (100%)
- ✅ Turtle graphics (100%)
- ✅ Expression evaluator (100%)
- ✅ Error hints (100%)
- ✅ Compiler (100%)
- ⏳ GUI (0% - planned)
- ⏳ Full test suite (20% - basic tests only)
- ⏳ Documentation (50%)

## Comparison with Rust Version

| Feature | Rust | Python | Status |
|---------|------|--------|--------|
| PILOT interpreter | ✅ | ✅ | Complete |
| BASIC interpreter | ✅ | ✅ | Complete |
| Logo interpreter | ✅ | ✅ | Complete |
| Turtle graphics | ✅ | ✅ | Complete |
| Expression eval | ✅ | ✅ | Complete |
| Error hints | ✅ | ✅ | Complete |
| Compiler | ✅ | ✅ | Complete |
| GUI (egui) | ✅ | ⏳ | Planned (PySide6) |
| Tests | 72 tests | 5 tests | In progress |

## Contributing

Contributions welcome! Areas needing work:

1. **GUI Implementation** - PySide6-based UI
2. **Test Coverage** - Port remaining 67 tests from Rust
3. **Documentation** - API docs, tutorials, examples
4. **Logo Procedures** - TO/END procedure system
5. **BASIC Extensions** - Additional commands (DIM, DATA, READ)

## License

See LICENSE file in repository root.

## Credits

**Original Rust Implementation**: James Temple (@James-HoneyBadger)  
**Python Port**: James Temple  
**Inspiration**: Classic educational computing environments

## Links

- **Repository**: https://github.com/James-HoneyBadger/Time_Warp
- **Rust Version**: Time_Warp_Rust/
- **Issues**: https://github.com/James-HoneyBadger/Time_Warp/issues

---

*Time Warp IDE - Bringing classic educational programming into the modern era* 🚀
