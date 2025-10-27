# SuperPILOT Technical Reference Manual

**Version 2.0**  
**Last Updated: October 27, 2025**

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Language Specifications](#language-specifications)
4. [API Reference](#api-reference)
5. [Event System](#event-system)
6. [Extension Development](#extension-development)

---

## 1. Introduction

### 1.1 Overview

SuperPILOT is a multi-language educational programming environment that integrates three programming paradigms:

- **PILOT**: Text-based educational language with simple command syntax
- **BASIC**: Classic procedural programming with line numbers
- **Logo**: Turtle graphics for visual programming education

### 1.2 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux, Raspberry Pi
- **RAM**: 512MB minimum, 1GB recommended
- **Display**: 1024x768 minimum resolution
- **Dependencies**: tkinter (included with Python), Pillow (optional)

### 1.3 Architecture Overview

```
SuperPILOT/
├── Super_PILOT.py          # Main application and interpreter
├── superpilot/             # Modular components
│   ├── runtime/            # Runtime systems
│   │   ├── templecode.py   # Animation (Tween, Timer, Particle)
│   │   ├── hardware.py     # Hardware controllers (Arduino, RPi)
│   │   └── audio.py        # Sound playback
│   └── ide/                # IDE components
│       └── settings.py     # Settings management
└── tests/                  # Test suite

```

---

## 2. System Architecture

### 2.1 Core Components

#### SuperPILOTInterpreter

The central execution engine that processes all three language types.

**Responsibilities:**
- Program parsing and line-by-line execution
- Variable and label management
- Command routing to appropriate language handlers
- Event callback system
- Turtle graphics state management

**Key Attributes:**
```python
self.variables = {}           # Variable storage
self.labels = {}             # Label -> line number mapping
self.program_lines = []      # Parsed program (line_num, command)
self.current_line = 0        # Execution pointer
self.running = False         # Execution state
self.breakpoints = set()     # Debugger breakpoints
```

#### Event Callback System

Observer pattern implementation for decoupling:

```python
self.on_output = []              # Callback(text: str)
self.on_variable_changed = []    # Callback(name: str, value: Any)
self.on_line_executed = []       # Callback(line_num: int)
self.on_program_started = []     # Callback()
self.on_program_finished = []    # Callback(success: bool)
self.on_breakpoint_hit = []      # Callback(line_num: int)
```

### 2.2 Execution Flow

```
1. load_program(text)
   ↓
2. Parse lines → (line_number, command)
   ↓
3. Collect labels (L:NAME)
   ↓
4. Main execution loop:
   ├─→ Check breakpoints (debug mode)
   ├─→ determine_command_type()
   ├─→ Route to handler:
   │   ├─→ execute_pilot_command()
   │   ├─→ execute_basic_command()
   │   └─→ execute_logo_command()
   ├─→ Update runtime systems
   └─→ Fire callbacks
   ↓
5. Program completion
```

### 2.3 Language Detection

The interpreter automatically detects language type:

```python
def determine_command_type(self, command):
    # PILOT: Commands with colon (T:, U:, A:, etc.)
    if ':' in command and command[0].isalpha():
        return 'pilot'
    
    # BASIC: Keywords (PRINT, LET, IF, FOR, etc.)
    if any(kw in command.upper() for kw in BASIC_KEYWORDS):
        return 'basic'
    
    # Logo: Turtle commands (FORWARD, RIGHT, etc.)
    if any(cmd in command.upper() for cmd in LOGO_COMMANDS):
        return 'logo'
    
    return 'unknown'
```

---

## 3. Language Specifications

### 3.1 PILOT Language

#### Command Reference

| Command | Syntax | Description |
|---------|--------|-------------|
| `T:` | `T:text` | Output text to console |
| `A:` | `A:variable` | Accept input from user |
| `U:` | `U:variable=value` | Set variable (Use) |
| `Y:` | `Y:condition` | Yes - set match flag if true |
| `N:` | `N:condition` | No - set match flag (variant) |
| `J:` | `J:label` | Jump to label |
| `L:` | `L:name` | Define label |
| `M:` | `M:text` | Match against input |
| `E:` | `E:` | End program |
| `C:` | `C:variable=expr` | Compute expression |
| `R:` | `R:command args` | Runtime command |

#### Variable Interpolation

Use `*VAR*` syntax to insert variable values:

```pilot
U:NAME=Alice
T:Hello, *NAME*!
```

Output: `Hello, Alice!`

#### Conditional Execution

```pilot
U:X=5
Y:X == 5
T:X equals five
```

The `Y:` command sets an internal match flag. The immediately following `T:` or `J:` consumes this flag for conditional behavior.

#### Example Program

```pilot
L:START
T:Welcome to SuperPILOT!
A:NAME
T:Hello, *NAME*!

U:X=10
U:Y=20
T:X is *X* and Y is *Y*

Y:X < Y
T:X is less than Y
E:
```

### 3.2 BASIC Language

#### Supported Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `PRINT` | `PRINT expr` | Output expression |
| `LET` | `LET var = expr` | Assign variable |
| `INPUT` | `INPUT var` | Get user input |
| `IF...THEN` | `IF cond THEN stmt` | Conditional execution |
| `GOTO` | `GOTO linenum` | Jump to line |
| `FOR...NEXT` | `FOR var = start TO end` | Loop |
| `DIM` | `DIM arr(size)` | Declare array |
| `DATA` | `DATA val1, val2, ...` | Define data |
| `READ` | `READ var` | Read from DATA |
| `RESTORE` | `RESTORE` | Reset DATA pointer |
| `GOSUB` | `GOSUB linenum` | Call subroutine |
| `RETURN` | `RETURN` | Return from subroutine |
| `END` | `END` | End program |
| `REM` | `REM comment` | Comment |

#### Line Numbers

BASIC programs use line numbers:

```basic
10 REM Simple BASIC Program
20 LET X = 100
30 LET Y = 200
40 LET SUM = X + Y
50 PRINT "Sum is: "; SUM
60 END
```

#### Expressions

Supported operators:
- Arithmetic: `+`, `-`, `*`, `/`, `**` (power), `%` (modulo)
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `AND`, `OR`, `NOT`

#### Built-in Functions

- `RND(max)` - Random number 0 to max
- `INT(x)` - Integer part
- `ABS(x)` - Absolute value
- `SIN(x)`, `COS(x)`, `TAN(x)` - Trigonometry (radians)
- `LEN(s)` - String length
- `MID(s, start, len)` - Substring
- `LEFT(s, n)` - Left n characters
- `RIGHT(s, n)` - Right n characters

### 3.3 Logo Language

#### Turtle Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `FORWARD` / `FD` | `FORWARD dist` | Move forward |
| `BACK` / `BK` | `BACK dist` | Move backward |
| `LEFT` / `LT` | `LEFT angle` | Turn left (degrees) |
| `RIGHT` / `RT` | `RIGHT angle` | Turn right (degrees) |
| `PENUP` / `PU` | `PENUP` | Lift pen (no drawing) |
| `PENDOWN` / `PD` | `PENDOWN` | Lower pen (drawing) |
| `CLEARSCREEN` / `CS` | `CS` | Clear graphics |
| `HOME` | `HOME` | Return to center |
| `SETXY` | `SETXY x y` | Set position |
| `SETHEADING` / `SETH` | `SETH angle` | Set direction |
| `SETCOLOR` | `SETCOLOR n` | Set pen color |
| `PENSIZE` | `PENSIZE width` | Set pen width |
| `HIDETURTLE` / `HT` | `HT` | Hide turtle cursor |
| `SHOWTURTLE` / `ST` | `ST` | Show turtle cursor |

#### Coordinate System

- Center: (0, 0)
- Heading: 0° = right, 90° = up, 180° = left, 270° = down
- Canvas: 400x400 pixels

#### REPEAT Loops

```logo
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

#### Macros

Define reusable procedures:

```logo
TO SQUARE :SIZE
  REPEAT 4 [
    FORWARD :SIZE
    RIGHT 90
  ]
END

SQUARE 50
```

---

## 4. API Reference

### 4.1 SuperPILOTInterpreter Class

#### Constructor

```python
SuperPILOTInterpreter(output_widget=None)
```

**Parameters:**
- `output_widget` (optional): tkinter Text widget for legacy output

**Example:**
```python
from Super_PILOT import SuperPILOTInterpreter

interp = SuperPILOTInterpreter()
```

#### Methods

##### run_program(program_text: str) -> bool

Execute a complete program.

**Parameters:**
- `program_text`: Multi-line string containing the program

**Returns:**
- `True` if execution completed successfully
- `False` if errors occurred or max iterations reached

**Example:**
```python
program = """
T:Hello World
U:X=42
T:The answer is *X*
"""
success = interp.run_program(program)
```

##### load_program(program_text: str) -> bool

Parse and load a program without executing.

**Returns:**
- `True` if parsing successful
- `False` if syntax errors detected

##### step() -> str

Execute one line in debug mode.

**Returns:**
- `"ok"` - Line executed successfully
- `"end"` - Program ended
- `"error"` - Execution error
- `"jump:N"` - Jumped to line N

##### evaluate_expression(expr: str) -> Any

Safely evaluate a mathematical expression.

**Parameters:**
- `expr`: String expression with variables

**Returns:**
- Evaluated result (int, float, or str)

**Example:**
```python
interp.variables['X'] = 10
result = interp.evaluate_expression("X * 2 + 5")  # Returns 25
```

##### interpolate_text(text: str) -> str

Replace `*VAR*` tokens with variable values.

**Example:**
```python
interp.variables['NAME'] = "Alice"
output = interp.interpolate_text("Hello, *NAME*!")
# Returns: "Hello, Alice!"
```

##### set_variable(name: str, value: Any) -> None

Set a variable and fire change callbacks.

**Example:**
```python
interp.set_variable("SCORE", 100)
```

##### stop_program() -> None

Stop the currently running program.

##### set_debug_mode(enabled: bool) -> None

Enable or disable debug mode.

##### toggle_breakpoint(line_number: int) -> None

Toggle breakpoint at specified line (0-indexed).

### 4.2 Event Callbacks

Register callbacks to receive execution events:

```python
# Output event
def on_output(text: str):
    print(f"Output: {text}")
    
interp.on_output.append(on_output)

# Variable changed
def on_var_change(name: str, value: Any):
    print(f"{name} = {value}")
    
interp.on_variable_changed.append(on_var_change)

# Line executed
def on_line(line_num: int):
    print(f"Executing line {line_num}")
    
interp.on_line_executed.append(on_line)

# Program lifecycle
interp.on_program_started.append(lambda: print("Started"))
interp.on_program_finished.append(lambda success: print(f"Finished: {success}"))
interp.on_breakpoint_hit.append(lambda line: print(f"Breakpoint at {line}"))
```

### 4.3 Runtime Systems

#### Tween (Animation)

```python
from superpilot.runtime.templecode import Tween

# Create smooth transition
tween = Tween(
    start_value=0,
    end_value=100,
    duration_ms=1000,
    ease_function="quadOut"
)

# Update each frame
dt_ms = 16  # ~60 FPS
value = tween.update(dt_ms)
```

#### Timer (Delayed Actions)

```python
from superpilot.runtime.templecode import Timer

def on_timer():
    print("Timer fired!")

timer = Timer(delay_ms=1000, callback=on_timer)

# Update each frame
timer.update(dt_ms)
```

#### Hardware Controllers

```python
from superpilot.runtime.hardware import ArduinoController, RPiController

# Arduino (simulation mode)
arduino = ArduinoController(simulation_mode=True)
arduino.connect('/dev/ttyUSB0', 9600)
arduino.digital_write(13, 1)  # LED on
value = arduino.analog_read(0)

# Raspberry Pi GPIO
rpi = RPiController(simulation_mode=True)
rpi.setup_pin(18, 'OUTPUT')
rpi.digital_write(18, 1)
```

---

## 5. Event System

### 5.1 Architecture

The event system uses the Observer pattern to decouple the interpreter from UI:

```
┌─────────────────────┐
│  SuperPILOT        │
│  Interpreter       │
└──────┬──────────────┘
       │ Fires Events
       │
       ├──→ on_output
       ├──→ on_variable_changed
       ├──→ on_line_executed
       ├──→ on_program_started
       ├──→ on_program_finished
       └──→ on_breakpoint_hit
       
       ↓ Multiple Observers
       
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  IDE         │  │  Logger      │  │  Custom      │
│  UI Update   │  │  System      │  │  Handler     │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 5.2 Callback Signatures

```python
# Output callback
def on_output_callback(text: str) -> None:
    """Called when program outputs text"""
    pass

# Variable changed callback
def on_variable_changed_callback(name: str, value: Any) -> None:
    """Called when variable is modified"""
    pass

# Line executed callback
def on_line_executed_callback(line_num: int) -> None:
    """Called after each line executes (0-indexed)"""
    pass

# Program started callback
def on_program_started_callback() -> None:
    """Called when program begins execution"""
    pass

# Program finished callback
def on_program_finished_callback(success: bool) -> None:
    """Called when program ends
    
    Args:
        success: True if completed normally, False if error/stopped
    """
    pass

# Breakpoint hit callback
def on_breakpoint_hit_callback(line_num: int) -> None:
    """Called when breakpoint is encountered"""
    pass
```

### 5.3 Thread Safety

When running in threaded mode (IDE), use `root.after()` for UI updates:

```python
def on_output(text):
    # Thread-safe UI update
    root.after(0, lambda: output_widget.insert(tk.END, text))

interp.on_output.append(on_output)
```

---

## 6. Extension Development

### 6.1 Adding Custom Commands

Extend PILOT with runtime commands:

```python
# In execute_pilot_command(), add new R: command handler:

if command.startswith('R:'):
    runtime_command = command[2:].strip().upper()
    
    if runtime_command.startswith('CUSTOM'):
        # Your custom command logic
        args = runtime_command[6:].strip()
        self.handle_custom_command(args)
        return "ok"
```

### 6.2 Creating Hardware Controllers

```python
from superpilot.runtime.hardware import HardwareController

class MyController:
    def __init__(self, simulation_mode=True):
        self.simulation_mode = simulation_mode
        self.connected = False
    
    def connect(self, port, baudrate=9600):
        if self.simulation_mode:
            print(f"[SIM] Connected to {port}")
            self.connected = True
        else:
            # Real hardware connection
            import serial
            self.serial = serial.Serial(port, baudrate)
            self.connected = True
    
    def send_command(self, cmd):
        if self.simulation_mode:
            print(f"[SIM] Command: {cmd}")
        else:
            self.serial.write(cmd.encode())
```

### 6.3 Settings Integration

```python
from superpilot.ide.settings import Settings

# Create custom settings
settings = Settings()
settings.set("my_extension", {"enabled": True, "value": 42})
settings.save()

# Load settings
config = settings.get("my_extension")
```

---

## Appendix A: Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Maximum iterations reached` | Infinite loop | Add loop counter or break condition |
| `Invalid label` | Jump to undefined label | Check label spelling and definition |
| `Syntax error in expression` | Invalid Python expression | Check operators and parentheses |
| `Variable not found` | Undefined variable | Use `U:` to define before use |
| `Unknown command` | Typo or unsupported command | Check command spelling |

## Appendix B: Performance Tips

1. **Limit loop iterations**: Max 10,000 iterations per run
2. **Breakpoint overhead**: Debug mode is slower
3. **Graphics**: Clear canvas periodically with `CS`
4. **Variables**: Use local scope when possible
5. **Callbacks**: Keep callback functions lightweight

## Appendix C: Version History

- **2.0** - Modular architecture, event system, Phase 2/3 features
- **1.0** - Initial monolithic implementation
