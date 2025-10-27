# SuperPILOT Developer Handbook

**Contributing to and Extending SuperPILOT**

Version 2.0 | Last Updated: October 27, 2025

---

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Architecture Deep Dive](#architecture-deep-dive)
3. [Contributing Guidelines](#contributing-guidelines)
4. [Testing Strategy](#testing-strategy)
5. [Adding New Features](#adding-new-features)
6. [Performance Optimization](#performance-optimization)
7. [API Integration](#api-integration)
8. [Deployment](#deployment)

---

## 1. Development Environment Setup

### Prerequisites

```bash
# Check Python version (3.8+ required)
python3 --version

# Clone repository
git clone https://github.com/yourusername/SuperPILOT.git
cd SuperPILOT

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### requirements-dev.txt

```text
# Core dependencies
Pillow>=9.0.0          # Image processing for graphics

# Testing
pytest>=7.0.0          # Test framework
pytest-cov>=3.0.0      # Coverage reporting
pytest-mock>=3.6.0     # Mocking utilities

# Development tools
black>=22.0.0          # Code formatter
flake8>=4.0.0          # Linter
mypy>=0.950            # Type checker
isort>=5.10.0          # Import sorter

# Documentation
sphinx>=4.5.0          # Documentation generator
sphinx-rtd-theme>=1.0  # ReadTheDocs theme

# Hardware (optional)
pyserial>=3.5          # Arduino/serial communication
# RPi.GPIO>=0.7.1      # Raspberry Pi (only on RPi)
```

### IDE Configuration

#### VS Code Settings (.vscode/settings.json)

```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

#### PyCharm Configuration

1. Settings → Tools → Python Integrated Tools
2. Set default test runner to pytest
3. Enable Black formatter
4. Set line length to 88

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_interpreter.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_pilot"
```

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and test
# Edit code...
pytest

# 3. Format and lint
black .
isort .
flake8

# 4. Commit changes
git add .
git commit -m "Add feature: description"

# 5. Push and create PR
git push origin feature/your-feature-name
```

---

## 2. Architecture Deep Dive

### Core Components

```
SuperPILOT Architecture
│
├─ Presentation Layer (IDE)
│  ├─ SuperPILOTII (Main Window)
│  ├─ AdvancedDebugger (Debug Panel)
│  └─ Settings (Configuration)
│
├─ Business Logic Layer
│  ├─ SuperPILOTInterpreter (Execution Engine)
│  ├─ Language Executors
│  │  ├─ execute_pilot_command()
│  │  ├─ execute_basic_command()
│  │  └─ execute_logo_command()
│  └─ Expression Evaluator
│
└─ Runtime Systems Layer
   ├─ templecode.py (Animation)
   ├─ hardware.py (IoT/Robotics)
   └─ audio.py (Sound)
```

### SuperPILOTInterpreter Class

#### Core Data Structures

```python
class SuperPILOTInterpreter:
    def __init__(self, output_widget=None):
        # Execution state
        self.program_lines = []        # [(line_num, command), ...]
        self.current_line = 0          # Execution pointer (0-indexed)
        self.running = False           # Is program executing?
        self.debug_mode = False        # Step-by-step debugging?
        self.max_iterations = 10000    # Infinite loop protection
        
        # Variable storage
        self.variables = {}            # {name: value}
        self.labels = {}               # {label: line_index}
        
        # Conditional execution
        self.match_flag = False        # Result of Y:/N: test
        self._last_match_set = False   # Was match_flag just set?
        
        # Turtle graphics state
        self.turtle_x = 0              # Current X position
        self.turtle_y = 0              # Current Y position
        self.turtle_heading = 0        # Direction (0=right, 90=up)
        self.pen_down = True           # Is pen touching canvas?
        self.pen_color = "black"       # Current draw color
        self.pen_size = 2              # Line thickness
        
        # Debugging
        self.breakpoints = set()       # Set of line numbers with breakpoints
        
        # BASIC-specific
        self.data_statements = []      # DATA values
        self.data_pointer = 0          # Current READ position
        self.for_loops = {}            # Active FOR loops
        self.gosub_stack = []          # GOSUB return addresses
        
        # Logo-specific
        self.procedures = {}           # Custom procedures {name: (params, body)}
        
        # Runtime systems
        self.tweens = []               # Active animations
        self.timers = []               # Active timers
        self.particles = []            # Particle effects
        
        # Hardware controllers (simulation by default)
        self.arduino = ArduinoController(simulation_mode=True)
        self.rpi = RPiController(simulation_mode=True)
        self.iot_devices = IoTDeviceManager()
        
        # Event callbacks (Observer pattern)
        self.on_output = []            # [(text) -> None]
        self.on_variable_changed = []  # [(name, value) -> None]
        self.on_line_executed = []     # [(line_num) -> None]
        self.on_program_started = []   # [() -> None]
        self.on_program_finished = []  # [(success) -> None]
        self.on_breakpoint_hit = []    # [(line_num) -> None]
```

#### Execution Flow

```python
def run_program(self, program_text: str) -> bool:
    """
    Main execution entry point.
    
    Flow:
    1. load_program() - Parse and prepare
    2. Fire on_program_started callbacks
    3. Main loop (max 10,000 iterations):
       a. Check breakpoints (debug mode)
       b. Get current command
       c. Determine language type
       d. Execute command
       e. Update runtime systems (tweens, timers, particles)
       f. Fire callbacks
       g. Check if ended
    4. Fire on_program_finished callbacks
    5. Return success status
    """
    # Implementation details...
```

### Language Detection Algorithm

```python
def determine_command_type(self, command: str) -> str:
    """
    Determine which language a command belongs to.
    
    Priority order:
    1. PILOT - Commands with colon after letter (T:, U:, A:, etc.)
    2. BASIC - Keywords (PRINT, LET, IF, FOR, etc.)
    3. Logo - Turtle commands (FORWARD, RIGHT, etc.)
    4. Unknown - Unrecognized syntax
    
    Returns: 'pilot', 'basic', 'logo', or 'unknown'
    """
    command = command.strip()
    if not command or command.startswith('REM'):
        return 'unknown'
    
    # PILOT: Single letter followed by colon
    if len(command) >= 2 and command[0].isalpha() and command[1] == ':':
        return 'pilot'
    
    # BASIC: Check for keywords
    cmd_upper = command.upper()
    basic_keywords = [
        'PRINT', 'LET', 'INPUT', 'IF', 'THEN', 'GOTO', 'GOSUB',
        'RETURN', 'FOR', 'NEXT', 'DIM', 'DATA', 'READ', 'RESTORE',
        'END', 'STOP'
    ]
    if any(cmd_upper.startswith(kw) for kw in basic_keywords):
        return 'basic'
    
    # Logo: Check for turtle commands
    logo_commands = [
        'FORWARD', 'FD', 'BACK', 'BK', 'LEFT', 'LT', 'RIGHT', 'RT',
        'PENUP', 'PU', 'PENDOWN', 'PD', 'CLEARSCREEN', 'CS', 'HOME',
        'SETXY', 'SETHEADING', 'SETH', 'SETCOLOR', 'PENSIZE',
        'HIDETURTLE', 'HT', 'SHOWTURTLE', 'ST', 'REPEAT', 'TO', 'END'
    ]
    if any(cmd_upper.startswith(cmd) for cmd in logo_commands):
        return 'logo'
    
    return 'unknown'
```

### Expression Evaluation

```python
def evaluate_expression(self, expr: str) -> Any:
    """
    Safely evaluate mathematical expressions with variables.
    
    Security model:
    - Uses restricted eval() with limited namespace
    - Only allows math functions and safe built-ins
    - Variable names substituted before evaluation
    
    Example:
        variables = {'X': 10, 'Y': 5}
        evaluate_expression("X * 2 + Y")  # Returns 25
    
    Warning: Naive string replacement can cause issues:
        variables = {'X': 10, 'EX': 5}
        evaluate_expression("X")  # Might replace EX first!
    
    Solution: Sort by length descending to replace longest first.
    """
    # Replace variables (longest first to avoid partial matches)
    for var_name in sorted(self.variables.keys(), key=len, reverse=True):
        value = self.variables[var_name]
        if isinstance(value, str):
            expr = expr.replace(var_name, f'"{value}"')
        else:
            expr = expr.replace(var_name, str(value))
    
    # Safe evaluation namespace
    safe_dict = {
        '__builtins__': {},
        # Math functions
        'abs': abs, 'int': int, 'float': float,
        'round': round, 'pow': pow,
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'sqrt': math.sqrt, 'log': math.log,
        # String functions
        'len': len, 'str': str,
        'upper': str.upper, 'lower': str.lower,
        # Custom functions
        'RND': lambda x: random.randint(0, x),
        'INT': int,
        'MID': lambda s, start, length: s[start:start+length],
        'LEFT': lambda s, n: s[:n],
        'RIGHT': lambda s, n: s[-n:],
    }
    
    try:
        result = eval(expr, safe_dict)
        return result
    except Exception as e:
        self._output(f"Error evaluating expression '{expr}': {e}")
        return 0
```

### Event System Implementation

```python
def _fire_callbacks(self, callback_list, *args):
    """
    Fire all callbacks in a list with error handling.
    
    Args:
        callback_list: List of callback functions
        *args: Arguments to pass to each callback
    
    Note: Catches and logs exceptions to prevent one bad
          callback from breaking all observers.
    """
    for callback in callback_list:
        try:
            callback(*args)
        except Exception as e:
            print(f"Error in callback {callback.__name__}: {e}")

def set_variable(self, name: str, value: Any) -> None:
    """
    Set variable and notify observers.
    
    This is the correct way to modify variables - it ensures
    the on_variable_changed event is always fired.
    """
    self.variables[name] = value
    self._fire_callbacks(self.on_variable_changed, name, value)

def _output(self, text: str) -> None:
    """
    Output text and notify observers.
    
    Prefer this over direct widget manipulation.
    """
    self._fire_callbacks(self.on_output, text + '\n')
```

---

## 3. Contributing Guidelines

### Code Style

#### Python Style Guide (PEP 8 + Black)

```python
# Good: Clear naming, proper spacing
def execute_pilot_command(self, command: str) -> str:
    """Execute a PILOT language command."""
    if command.startswith('T:'):
        text = command[2:].strip()
        self._output(self.interpolate_text(text))
        return "ok"
    return "unknown"

# Bad: Poor naming, cramped
def ex(self,c):
    if c.startswith('T:'):self._output(c[2:])
    return "ok"
```

#### Type Hints

```python
# Use type hints for function signatures
def set_variable(self, name: str, value: Any) -> None:
    """Set a variable value."""
    self.variables[name] = value

def get_variable(self, name: str, default: Any = None) -> Any:
    """Get a variable value with optional default."""
    return self.variables.get(name, default)

# Use type hints for complex structures
from typing import List, Dict, Tuple, Optional, Callable

class SuperPILOTInterpreter:
    program_lines: List[Tuple[int, str]]
    variables: Dict[str, Any]
    labels: Dict[str, int]
    on_output: List[Callable[[str], None]]
```

#### Documentation

```python
def evaluate_expression(self, expr: str) -> Any:
    """
    Safely evaluate a mathematical expression.
    
    This method performs variable substitution and evaluates
    the expression in a restricted namespace for security.
    
    Args:
        expr: String expression to evaluate (e.g., "X * 2 + 5")
    
    Returns:
        Evaluated result (int, float, or str)
    
    Raises:
        No exceptions are raised. Errors are logged and 0 is returned.
    
    Examples:
        >>> interp = SuperPILOTInterpreter()
        >>> interp.variables['X'] = 10
        >>> interp.evaluate_expression("X * 2")
        20
        
        >>> interp.variables['NAME'] = "Alice"
        >>> interp.evaluate_expression("len(NAME)")
        5
    
    Security:
        Uses eval() with restricted __builtins__. Only mathematical
        and string operations are allowed. No file I/O, imports, etc.
    
    Known Issues:
        Variable name collision in string replacement can cause
        incorrect substitution (e.g., X replaced in EXP).
        Current workaround: Sort by length descending.
    """
    # Implementation...
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring (no feature/bug change)
- `test`: Adding or updating tests
- `chore`: Maintenance (dependencies, build, etc.)

**Examples:**

```
feat(interpreter): Add support for WHILE loops

Implement WHILE...WEND loop structure for BASIC language.
Includes condition evaluation and loop exit logic.

Closes #42
```

```
fix(logo): Correct turtle heading after HOME command

HOME command was not resetting turtle heading to 0 degrees.
This caused subsequent FORWARD commands to move in wrong direction.

Fixes #67
```

```
docs(readme): Update installation instructions

Add troubleshooting section for common tkinter issues on Linux.
Include apt package names for different distributions.
```

### Pull Request Process

1. **Fork and branch**
   ```bash
   git clone https://github.com/yourusername/SuperPILOT.git
   cd SuperPILOT
   git checkout -b feat/my-new-feature
   ```

2. **Develop with tests**
   - Write tests first (TDD) or alongside code
   - Ensure all tests pass
   - Add documentation

3. **Format and lint**
   ```bash
   black .
   isort .
   flake8
   mypy Super_PILOT.py
   ```

4. **Update changelog**
   Add entry to CHANGELOG.md under "Unreleased"

5. **Create PR**
   - Push to your fork
   - Open PR against `main` branch
   - Fill out PR template:
     ```markdown
     ## Description
     Brief description of changes
     
     ## Type of Change
     - [ ] Bug fix
     - [ ] New feature
     - [ ] Breaking change
     - [ ] Documentation update
     
     ## Testing
     - [ ] All existing tests pass
     - [ ] New tests added
     - [ ] Manual testing completed
     
     ## Checklist
     - [ ] Code follows style guidelines
     - [ ] Self-review completed
     - [ ] Comments added for complex code
     - [ ] Documentation updated
     - [ ] No new warnings
     ```

6. **Code review**
   - Address reviewer feedback
   - Make requested changes
   - Mark conversations as resolved

7. **Merge**
   - Squash and merge (preferred)
   - Or rebase and merge for clean history

---

## 4. Testing Strategy

### Test Organization

```
tests/
├── test_interpreter.py              # Core interpreter tests
├── test_pilot_commands.py           # PILOT language tests
├── test_basic_commands.py           # BASIC language tests
├── test_logo_commands.py            # Logo language tests
├── test_expressions.py              # Expression evaluation
├── test_variables.py                # Variable management
├── test_event_callbacks.py          # Observer pattern
├── test_threading.py                # Concurrency
├── test_hardware_integration.py     # Hardware mocking
├── test_templecode_integration.py   # Animation systems
├── test_security.py                 # Security constraints
├── test_performance.py              # Performance benchmarks
└── test_ide_smoke.py                # GUI smoke tests
```

### Unit Test Examples

#### Testing Commands

```python
def test_pilot_output():
    """Test PILOT T: command outputs text."""
    interp = SuperPILOTInterpreter()
    output = []
    interp.on_output.append(lambda text: output.append(text))
    
    program = "T:Hello World"
    interp.run_program(program)
    
    assert len(output) == 1
    assert "Hello World" in output[0]

def test_pilot_variable_assignment():
    """Test PILOT U: command sets variables."""
    interp = SuperPILOTInterpreter()
    
    program = "U:NAME=Alice"
    interp.run_program(program)
    
    assert 'NAME' in interp.variables
    assert interp.variables['NAME'] == 'Alice'

def test_basic_let_statement():
    """Test BASIC LET command."""
    interp = SuperPILOTInterpreter()
    
    program = "10 LET X = 42"
    interp.run_program(program)
    
    assert interp.variables['X'] == 42

def test_logo_forward():
    """Test Logo FORWARD command moves turtle."""
    interp = SuperPILOTInterpreter()
    
    program = """
    CS
    FORWARD 100
    """
    interp.run_program(program)
    
    # Turtle starts at (0, 0), heading 0 (right)
    # After FORWARD 100, should be at (100, 0)
    assert interp.turtle_x == 100
    assert interp.turtle_y == 0
```

#### Testing Event Callbacks

```python
def test_variable_changed_callback():
    """Test on_variable_changed fires when variables are set."""
    interp = SuperPILOTInterpreter()
    
    changes = []
    def track_change(name, value):
        changes.append((name, value))
    
    interp.on_variable_changed.append(track_change)
    
    interp.set_variable('X', 10)
    interp.set_variable('Y', 20)
    
    assert len(changes) == 2
    assert changes[0] == ('X', 10)
    assert changes[1] == ('Y', 20)
```

#### Testing Error Handling

```python
def test_infinite_loop_protection():
    """Test max iterations prevents infinite loops."""
    interp = SuperPILOTInterpreter()
    
    # Infinite loop program
    program = """
    L:LOOP
    J:LOOP
    """
    
    result = interp.run_program(program)
    
    # Should stop at max_iterations, not hang forever
    assert result is False  # Failed due to max iterations
    assert interp.current_line < len(interp.program_lines)
```

### Integration Tests

```python
def test_pilot_basic_logo_integration():
    """Test program using all three languages."""
    interp = SuperPILOTInterpreter()
    
    program = """
    T:Drawing a square
    10 LET SIZE = 100
    CS
    REPEAT 4 [
      FORWARD SIZE
      RIGHT 90
    ]
    T:Done!
    """
    
    output = []
    interp.on_output.append(lambda text: output.append(text))
    
    result = interp.run_program(program)
    
    assert result is True
    assert len(output) == 2  # Two T: commands
    assert "Drawing" in output[0]
    assert "Done" in output[1]
    # Turtle should be back at origin after square
    assert abs(interp.turtle_x) < 1  # Floating point tolerance
    assert abs(interp.turtle_y) < 1
```

### Mocking Hardware

```python
import pytest
from unittest.mock import Mock, patch

def test_arduino_simulation():
    """Test Arduino in simulation mode."""
    from superpilot.runtime.hardware import ArduinoController
    
    arduino = ArduinoController(simulation_mode=True)
    arduino.connect('/dev/ttyUSB0', 9600)
    
    # Should not raise error in simulation
    arduino.digital_write(13, 1)
    value = arduino.analog_read(0)
    
    assert arduino.connected
    assert isinstance(value, int)

def test_arduino_real_hardware():
    """Test Arduino with real serial connection."""
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value = Mock()
        
        arduino = ArduinoController(simulation_mode=False)
        arduino.connect('/dev/ttyUSB0', 9600)
        
        mock_serial.assert_called_once_with('/dev/ttyUSB0', 9600)
```

### Performance Tests

```python
import time
import pytest

def test_execution_speed():
    """Ensure interpreter executes quickly."""
    interp = SuperPILOTInterpreter()
    
    # Program with 100 simple commands
    program = "\n".join([f"10{i} LET X = {i}" for i in range(100)])
    
    start = time.time()
    result = interp.run_program(program)
    elapsed = time.time() - start
    
    assert result is True
    assert elapsed < 1.0  # Should complete in under 1 second

@pytest.mark.benchmark
def test_expression_evaluation_performance(benchmark):
    """Benchmark expression evaluation."""
    interp = SuperPILOTInterpreter()
    interp.variables = {'X': 10, 'Y': 20, 'Z': 30}
    
    result = benchmark(interp.evaluate_expression, "X * Y + Z ** 2")
    
    assert result == 10 * 20 + 30 ** 2
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_interpreter.py

# Specific test function
pytest tests/test_interpreter.py::test_pilot_output

# With coverage
pytest --cov=. --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf

# Skip slow tests
pytest -m "not slow"

# Parallel execution
pytest -n auto
```

---

## 5. Adding New Features

### Example: Adding WHILE Loop to BASIC

#### Step 1: Design

**Syntax:**
```basic
10 LET X = 0
20 WHILE X < 10
30   PRINT X
40   LET X = X + 1
50 WEND
60 END
```

**Data structures needed:**
- Stack to track active WHILE loops
- Store: line number, condition, loop start

#### Step 2: Write Tests First (TDD)

```python
# tests/test_while_loop.py

def test_while_loop_basic():
    """Test simple WHILE loop."""
    interp = SuperPILOTInterpreter()
    
    program = """
    10 LET X = 0
    20 WHILE X < 3
    30   PRINT X
    40   LET X = X + 1
    50 WEND
    60 END
    """
    
    output = []
    interp.on_output.append(lambda text: output.append(text))
    
    result = interp.run_program(program)
    
    assert result is True
    assert "0" in output[0]
    assert "1" in output[1]
    assert "2" in output[2]
    assert interp.variables['X'] == 3

def test_while_loop_skip():
    """Test WHILE loop that doesn't execute."""
    interp = SuperPILOTInterpreter()
    
    program = """
    10 LET X = 10
    20 WHILE X < 5
    30   PRINT "Should not print"
    40 WEND
    50 PRINT "After loop"
    60 END
    """
    
    output = []
    interp.on_output.append(lambda text: output.append(text))
    
    result = interp.run_program(program)
    
    assert result is True
    assert len(output) == 1
    assert "After loop" in output[0]

def test_nested_while_loops():
    """Test nested WHILE loops."""
    interp = SuperPILOTInterpreter()
    
    program = """
    10 LET I = 0
    20 WHILE I < 2
    30   LET J = 0
    40   WHILE J < 2
    50     PRINT I * 10 + J
    60     LET J = J + 1
    70   WEND
    80   LET I = I + 1
    90 WEND
    100 END
    """
    
    output = []
    interp.on_output.append(lambda text: output.append(text))
    
    result = interp.run_program(program)
    
    assert result is True
    assert len(output) == 4  # 2x2 = 4 iterations
```

#### Step 3: Implement Feature

```python
# In SuperPILOTInterpreter class

def __init__(self, ...):
    # ... existing init code ...
    self.while_loops = []  # Stack: [(line_num, condition), ...]

def execute_basic_command(self, command: str) -> str:
    """Execute BASIC command - add WHILE/WEND handling."""
    cmd_upper = command.upper().strip()
    
    # ... existing BASIC commands ...
    
    if cmd_upper.startswith('WHILE '):
        return self._handle_while(command)
    
    if cmd_upper == 'WEND':
        return self._handle_wend()
    
    # ... rest of commands ...

def _handle_while(self, command: str) -> str:
    """
    Handle WHILE statement.
    
    Evaluates condition. If true, continue execution.
    If false, jump past matching WEND.
    Pushes loop info onto stack for WEND to use.
    """
    # Extract condition
    condition = command[5:].strip()  # Skip 'WHILE '
    
    # Evaluate condition
    try:
        result = self.evaluate_expression(condition)
        condition_true = bool(result)
    except:
        self._output("Error in WHILE condition")
        return "error"
    
    if condition_true:
        # Enter loop - push onto stack
        self.while_loops.append({
            'start_line': self.current_line,
            'condition': condition
        })
        return "ok"
    else:
        # Skip loop - find matching WEND
        wend_line = self._find_matching_wend(self.current_line)
        if wend_line is None:
            self._output("WHILE without matching WEND")
            return "error"
        self.current_line = wend_line
        return "ok"

def _handle_wend(self) -> str:
    """
    Handle WEND statement.
    
    Jumps back to WHILE and re-evaluates condition.
    Pops loop from stack when condition is false.
    """
    if not self.while_loops:
        self._output("WEND without matching WHILE")
        return "error"
    
    # Get current loop
    loop = self.while_loops[-1]
    
    # Re-evaluate condition
    try:
        result = self.evaluate_expression(loop['condition'])
        condition_true = bool(result)
    except:
        self._output("Error in WHILE condition")
        return "error"
    
    if condition_true:
        # Continue loop - jump back to WHILE
        self.current_line = loop['start_line']
        return "ok"
    else:
        # Exit loop - pop from stack
        self.while_loops.pop()
        return "ok"

def _find_matching_wend(self, start_line: int) -> Optional[int]:
    """
    Find the WEND that matches a WHILE at start_line.
    
    Handles nested WHILE loops by counting depth.
    """
    depth = 1
    for i in range(start_line + 1, len(self.program_lines)):
        _, cmd = self.program_lines[i]
        cmd_upper = cmd.upper().strip()
        
        if cmd_upper.startswith('WHILE '):
            depth += 1
        elif cmd_upper == 'WEND':
            depth -= 1
            if depth == 0:
                return i
    
    return None  # No matching WEND found
```

#### Step 4: Update Documentation

```python
# In execute_basic_command docstring, add:
"""
WHILE loops:
    WHILE condition
      ... loop body ...
    WEND
    
    Executes loop body while condition is true.
    Supports nested WHILE loops.
"""
```

Update USER_GUIDE.md, TECHNICAL_REFERENCE.md with examples.

#### Step 5: Run Tests

```bash
pytest tests/test_while_loop.py -v
```

#### Step 6: Manual Testing

Create `test_while.bas`:
```basic
10 PRINT "Counting to 5:"
20 LET I = 1
30 WHILE I <= 5
40   PRINT "  "; I
50   LET I = I + 1
60 WEND
70 PRINT "Done!"
80 END
```

Run in IDE and verify output.

---

## 6. Performance Optimization

### Profiling

#### Using cProfile

```bash
python3 -m cProfile -o profile.stats Super_PILOT.py
```

Analyze results:
```python
import pstats
from pstats import SortKey

p = pstats.Stats('profile.stats')
p.sort_stats(SortKey.CUMULATIVE)
p.print_stats(20)  # Top 20 functions
```

#### Using line_profiler

```bash
pip install line_profiler

# Add @profile decorator to functions
kernprof -l -v Super_PILOT.py
```

### Optimization Strategies

#### 1. Cache Expensive Computations

```python
from functools import lru_cache

class SuperPILOTInterpreter:
    @lru_cache(maxsize=128)
    def _parse_expression(self, expr: str) -> Any:
        """Cache parsed expressions to avoid re-parsing."""
        # Parsing logic...
        return parsed_expr
```

#### 2. Reduce String Operations

```python
# Slow: Repeated string concatenation
output = ""
for line in program_lines:
    output += line + "\n"

# Fast: Use list and join
output = []
for line in program_lines:
    output.append(line)
result = "\n".join(output)

# Or: Use io.StringIO
from io import StringIO
output = StringIO()
for line in program_lines:
    output.write(line)
    output.write("\n")
result = output.getvalue()
```

#### 3. Optimize Hot Paths

```python
# Before: Looking up variable repeatedly
for i in range(1000):
    x = self.variables.get('X', 0)
    y = self.variables.get('Y', 0)
    result = x + y

# After: Cache variable lookup
x = self.variables.get('X', 0)
y = self.variables.get('Y', 0)
for i in range(1000):
    result = x + y
```

#### 4. Use Generators for Large Datasets

```python
# Before: Load all in memory
def get_all_commands(self):
    return [line for line in self.program_lines]

# After: Stream with generator
def get_all_commands(self):
    for line in self.program_lines:
        yield line
```

### Memory Optimization

#### 1. Use __slots__ for Fixed Attributes

```python
class TurtleState:
    __slots__ = ['x', 'y', 'heading', 'pen_down', 'color', 'size']
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.heading = 0
        self.pen_down = True
        self.color = "black"
        self.size = 2
```

#### 2. Clear Large Data Structures

```python
def run_program(self, program_text: str) -> bool:
    try:
        # ... execution ...
    finally:
        # Clean up to free memory
        self.tweens.clear()
        self.timers.clear()
        self.particles.clear()
```

---

## 7. API Integration

### REST API Example

Create web API for headless execution:

```python
# api/server.py

from flask import Flask, request, jsonify
from Super_PILOT import SuperPILOTInterpreter
import threading

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_program():
    """Execute SuperPILOT program and return output."""
    try:
        data = request.json
        program = data.get('program', '')
        
        # Create interpreter
        interp = SuperPILOTInterpreter()
        
        # Capture output
        output = []
        interp.on_output.append(lambda text: output.append(text))
        
        # Execute
        success = interp.run_program(program)
        
        # Return results
        return jsonify({
            'success': success,
            'output': ''.join(output),
            'variables': interp.variables,
            'graphics': {
                'turtle_x': interp.turtle_x,
                'turtle_y': interp.turtle_y,
                'turtle_heading': interp.turtle_heading
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Usage:
```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{"program": "T:Hello from API\nU:X=42\nT:X is *X*"}'
```

### WebSocket for Real-Time Updates

```python
# api/websocket_server.py

from flask import Flask
from flask_socketio import SocketIO, emit
from Super_PILOT import SuperPILOTInterpreter

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('execute')
def handle_execute(data):
    """Execute program with real-time output updates."""
    program = data.get('program', '')
    
    interp = SuperPILOTInterpreter()
    
    # Send output in real-time
    def send_output(text):
        emit('output', {'text': text})
    
    def send_variable(name, value):
        emit('variable', {'name': name, 'value': value})
    
    def send_line(line_num):
        emit('line', {'line': line_num})
    
    interp.on_output.append(send_output)
    interp.on_variable_changed.append(send_variable)
    interp.on_line_executed.append(send_line)
    
    # Execute
    success = interp.run_program(program)
    
    emit('finished', {'success': success})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
```

Client example:
```javascript
const socket = io('http://localhost:5001');

socket.on('output', (data) => {
  console.log('Output:', data.text);
});

socket.on('variable', (data) => {
  console.log(`${data.name} = ${data.value}`);
});

socket.on('finished', (data) => {
  console.log('Finished:', data.success);
});

socket.emit('execute', {
  program: 'T:Hello from WebSocket\nU:X=100'
});
```

---

## 8. Deployment

### Desktop Application (PyInstaller)

```bash
# Install PyInstaller
pip install pyinstaller

# Create spec file
pyi-makespec --windowed --name SuperPILOT Super_PILOT.py

# Edit SuperPILOT.spec to include data files
# Then build:
pyinstaller SuperPILOT.spec

# Executable will be in dist/SuperPILOT/
```

### Docker Container

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application
COPY . .

# Expose port for API
EXPOSE 5000

# Run API server
CMD ["python", "api/server.py"]
```

Build and run:
```bash
docker build -t superpilot:latest .
docker run -p 5000:5000 superpilot:latest
```

### Raspberry Pi Deployment

```bash
# On Raspberry Pi
git clone https://github.com/yourusername/SuperPILOT.git
cd SuperPILOT

# Install dependencies
sudo apt-get install python3-tk python3-pil python3-pip
pip3 install -r requirements-dev.txt

# Run
python3 Super_PILOT.py
```

### Cloud Deployment (AWS Lambda)

```python
# lambda_handler.py

import json
from Super_PILOT import SuperPILOTInterpreter

def lambda_handler(event, context):
    """AWS Lambda handler for SuperPILOT execution."""
    try:
        program = event.get('program', '')
        
        interp = SuperPILOTInterpreter()
        
        output = []
        interp.on_output.append(lambda text: output.append(text))
        
        success = interp.run_program(program)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': success,
                'output': ''.join(output),
                'variables': interp.variables
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

---

## Appendix: Useful Resources

### Documentation Tools

- **Sphinx**: Generate API docs from docstrings
- **MkDocs**: Markdown-based documentation
- **Read the Docs**: Host documentation online

### Testing Tools

- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **hypothesis**: Property-based testing
- **tox**: Test multiple Python versions

### Code Quality Tools

- **black**: Code formatter
- **isort**: Import sorter
- **flake8**: Linter
- **pylint**: Advanced linter
- **mypy**: Type checker
- **bandit**: Security linter

### Performance Tools

- **cProfile**: CPU profiling
- **memory_profiler**: Memory profiling
- **py-spy**: Sampling profiler
- **pyinstrument**: Statistical profiler

### Debugging Tools

- **pdb**: Python debugger
- **ipdb**: IPython debugger
- **pudb**: Visual debugger
- **python-devtools**: Debug printing

---

## Contact & Support

- **GitHub**: https://github.com/yourusername/SuperPILOT
- **Issues**: https://github.com/yourusername/SuperPILOT/issues
- **Discussions**: https://github.com/yourusername/SuperPILOT/discussions
- **Email**: dev@superpilot.org

**Happy coding!** 🚀
