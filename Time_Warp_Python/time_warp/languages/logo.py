"""Logo language executor for Time Warp IDE.

Logo is an educational programming language with turtle graphics,
procedures, and simple list processing.
"""

from typing import TYPE_CHECKING, List, Optional
import re

if TYPE_CHECKING:
    from ..core.interpreter import Interpreter
    from ..graphics.turtle_state import TurtleState


def execute_logo(
    interpreter: 'Interpreter',
    command: str,
    turtle: 'TurtleState'
) -> str:
    """Execute a Logo command.
    
    Args:
        interpreter: Interpreter instance with variables and state
        command: Logo command string
        turtle: Turtle state for graphics
        
    Returns:
        Output text (or empty string)
    """
    cmd = command.strip().upper()
    words = cmd.split()
    
    if not words:
        return ""
    
    cmd_name = words[0]
    args = words[1:] if len(words) > 1 else []
    
    # Turtle movement commands
    if cmd_name in ['FORWARD', 'FD']:
        return _execute_forward(interpreter, turtle, args)
    
    if cmd_name in ['BACK', 'BK', 'BACKWARD']:
        return _execute_back(interpreter, turtle, args)
    
    if cmd_name in ['LEFT', 'LT']:
        return _execute_left(interpreter, turtle, args)
    
    if cmd_name in ['RIGHT', 'RT']:
        return _execute_right(interpreter, turtle, args)
    
    # Pen control
    if cmd_name in ['PENUP', 'PU']:
        turtle.penup()
        return ""
    
    if cmd_name in ['PENDOWN', 'PD']:
        turtle.pendown()
        return ""
    
    # Turtle state
    if cmd_name == 'HOME':
        turtle.home()
        return ""
    
    if cmd_name in ['CLEARSCREEN', 'CS', 'CLEAR']:
        turtle.clear()
        return ""
    
    if cmd_name == 'HIDETURTLE' or cmd_name == 'HT':
        turtle.hideturtle()
        return ""
    
    if cmd_name == 'SHOWTURTLE' or cmd_name == 'ST':
        turtle.showturtle()
        return ""
    
    # Positioning
    if cmd_name == 'SETXY':
        return _execute_setxy(interpreter, turtle, args)
    
    if cmd_name == 'SETX':
        return _execute_setx(interpreter, turtle, args)
    
    if cmd_name == 'SETY':
        return _execute_sety(interpreter, turtle, args)
    
    if cmd_name in ['SETHEADING', 'SETH']:
        return _execute_setheading(interpreter, turtle, args)
    
    # Color commands
    if cmd_name == 'SETPENCOLOR' or cmd_name == 'SETPC':
        return _execute_setpencolor(interpreter, turtle, args)
    
    if cmd_name == 'SETBGCOLOR' or cmd_name == 'SETBG':
        return _execute_setbgcolor(interpreter, turtle, args)
    
    if cmd_name == 'SETPENWIDTH' or cmd_name == 'SETPW':
        return _execute_setpenwidth(interpreter, turtle, args)
    
    # Control structures
    if cmd_name == 'REPEAT':
        return _execute_repeat(interpreter, turtle, command)
    
    # Procedure definition
    if cmd_name == 'TO':
        return _execute_to(interpreter, command)
    
    if cmd_name == 'END':
        return _execute_end_procedure(interpreter)
    
    # Output
    if cmd_name == 'PRINT':
        return _execute_print(interpreter, ' '.join(args))
    
    return f"❌ Unknown Logo command: {cmd_name}\n"


def _evaluate_arg(interpreter: 'Interpreter', arg: str) -> float:
    """Evaluate an argument (number or expression)"""
    try:
        # Variable reference (starts with : in Logo)
        if arg.startswith(':'):
            var_name = arg[1:].upper()
            return interpreter.variables.get(var_name, 0)
        
        return interpreter.evaluate_expression(arg)
    except Exception:
        return 0.0


def _execute_forward(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute FORWARD command"""
    if not args:
        return "❌ FORWARD requires distance\n"
    
    distance = _evaluate_arg(interpreter, args[0])
    turtle.forward(distance)
    return ""


def _execute_back(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute BACK command"""
    if not args:
        return "❌ BACK requires distance\n"
    
    distance = _evaluate_arg(interpreter, args[0])
    turtle.back(distance)
    return ""


def _execute_left(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute LEFT command"""
    if not args:
        return "❌ LEFT requires angle\n"
    
    angle = _evaluate_arg(interpreter, args[0])
    turtle.left(angle)
    return ""


def _execute_right(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute RIGHT command"""
    if not args:
        return "❌ RIGHT requires angle\n"
    
    angle = _evaluate_arg(interpreter, args[0])
    turtle.right(angle)
    return ""


def _execute_setxy(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute SETXY command"""
    if len(args) < 2:
        return "❌ SETXY requires x and y coordinates\n"
    
    x = _evaluate_arg(interpreter, args[0])
    y = _evaluate_arg(interpreter, args[1])
    turtle.goto(x, y)
    return ""


def _execute_setx(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute SETX command"""
    if not args:
        return "❌ SETX requires x coordinate\n"
    
    x = _evaluate_arg(interpreter, args[0])
    turtle.goto(x, turtle.y)
    return ""


def _execute_sety(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute SETY command"""
    if not args:
        return "❌ SETY requires y coordinate\n"
    
    y = _evaluate_arg(interpreter, args[0])
    turtle.goto(turtle.x, y)
    return ""


def _execute_setheading(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute SETHEADING command"""
    if not args:
        return "❌ SETHEADING requires angle\n"
    
    angle = _evaluate_arg(interpreter, args[0])
    turtle.setheading(angle)
    return ""


def _execute_setpencolor(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute SETPENCOLOR command"""
    if len(args) < 3:
        return "❌ SETPENCOLOR requires R G B values (0-255)\n"
    
    r = int(_evaluate_arg(interpreter, args[0]))
    g = int(_evaluate_arg(interpreter, args[1]))
    b = int(_evaluate_arg(interpreter, args[2]))
    
    turtle.setcolor(r, g, b)
    return ""


def _execute_setbgcolor(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute SETBGCOLOR command"""
    if len(args) < 3:
        return "❌ SETBGCOLOR requires R G B values (0-255)\n"
    
    r = int(_evaluate_arg(interpreter, args[0]))
    g = int(_evaluate_arg(interpreter, args[1]))
    b = int(_evaluate_arg(interpreter, args[2]))
    
    turtle.setbgcolor(r, g, b)
    return ""


def _execute_setpenwidth(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str]
) -> str:
    """Execute SETPENWIDTH command"""
    if not args:
        return "❌ SETPENWIDTH requires width\n"
    
    width = _evaluate_arg(interpreter, args[0])
    turtle.setpenwidth(width)
    return ""


def _execute_repeat(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    command: str
) -> str:
    """Execute REPEAT command"""
    # REPEAT count [ commands ]
    match = re.match(r'REPEAT\s+(\S+)\s*\[(.*?)\]', command, re.IGNORECASE)
    
    if not match:
        return "❌ REPEAT requires format: REPEAT count [ commands ]\n"
    
    count_expr = match.group(1)
    commands = match.group(2)
    
    try:
        count = int(_evaluate_arg(interpreter, count_expr))
    except Exception:
        return "❌ REPEAT count must be a number\n"
    
    # Execute commands 'count' times
    for _ in range(count):
        for cmd in commands.split('\n'):
            cmd = cmd.strip()
            if cmd:
                result = execute_logo(interpreter, cmd, turtle)
                if result and result.startswith('❌'):
                    return result
    
    return ""


def _execute_to(interpreter: 'Interpreter', command: str) -> str:
    """Execute TO (procedure definition)"""
    # TO name [parameters]
    # For now, just mark that we're in procedure definition
    # Full implementation would store procedure code
    return "ℹ️ Procedure definitions not yet fully implemented\n"


def _execute_end_procedure(interpreter: 'Interpreter') -> str:
    """Execute END (end procedure definition)"""
    return ""


def _execute_print(interpreter: 'Interpreter', text: str) -> str:
    """Execute PRINT command"""
    # Interpolate variables
    output = interpreter.interpolate_text(text)
    interpreter.output.append(output)
    return output + "\n"
