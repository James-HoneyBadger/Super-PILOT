"""PILOT language executor for Time Warp IDE.

PILOT (Programmed Inquiry, Learning, Or Teaching) is a simple 
educational language using single-letter commands followed by colons.
"""

import re
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..core.interpreter import Interpreter
    from ..graphics.turtle_state import TurtleState


def execute_pilot(interpreter: 'Interpreter', command: str, turtle: 'TurtleState') -> str:
    """Execute a PILOT command.
    
    Args:
        interpreter: Interpreter instance with variables and state
        command: PILOT command string
        turtle: Turtle state for graphics
        
    Returns:
        Output text (or empty string)
    """
    # PILOT commands are single letters followed by colon
    # T: text     - Type (print) text
    # A: var      - Accept (input) to variable
    # M: pattern  - Match input against pattern
    # Y: label    - Yes (jump if last match succeeded)
    # N: label    - No (jump if last match failed)
    # C: expr     - Compute expression and store
    # U: var      - Use variable (print variable value)
    # J: label    - Jump unconditionally
    # L: label    - Label definition
    # E:          - End program
    # R: comment  - Remark (comment, ignored)
    
    cmd = command.strip()
    if not cmd or len(cmd) < 2:
        return ""
    
    # Extract command letter and rest
    cmd_type = cmd[0].upper()
    
    if len(cmd) < 2 or cmd[1] != ':':
        return f"❌ Invalid PILOT command: {command}\n"
    
    rest = cmd[2:].strip()
    
    # Handle each command type
    if cmd_type == 'T':
        # T: text - Type (print) text with variable interpolation
        text = interpreter.interpolate_text(rest)
        interpreter.output.append(text)
        return text + "\n"
    
    elif cmd_type == 'A':
        # A: var - Accept (input) to variable
        var_name = rest.strip()
        if not var_name:
            return "❌ A: requires variable name\n"
        
        # Request input through interpreter
        interpreter.request_input(f"? ", var_name, is_numeric=False)
        return ""
    
    elif cmd_type == 'M':
        # M: pattern - Match last input against pattern
        pattern = rest.strip()
        if not pattern:
            interpreter.last_match_succeeded = False
            return ""
        
        # Get last input value
        last_input = interpreter.variables.get('_LAST_INPUT', '')
        
        # Simple pattern matching (supports * as wildcard)
        # Convert pattern to regex
        regex_pattern = pattern.replace('*', '.*')
        regex_pattern = '^' + regex_pattern + '$'
        
        try:
            interpreter.last_match_succeeded = bool(
                re.match(regex_pattern, str(last_input), re.IGNORECASE)
            )
        except re.error:
            interpreter.last_match_succeeded = False
        
        return ""
    
    elif cmd_type == 'Y':
        # Y: label - Yes (jump if last match succeeded)
        if interpreter.last_match_succeeded:
            label = rest.strip()
            if label:
                interpreter.jump_to_label(label)
        return ""
    
    elif cmd_type == 'N':
        # N: label - No (jump if last match failed)
        if not interpreter.last_match_succeeded:
            label = rest.strip()
            if label:
                interpreter.jump_to_label(label)
        return ""
    
    elif cmd_type == 'C':
        # C: var = expr - Compute expression and store in variable
        if '=' not in rest:
            return f"❌ C: requires format: var = expression\n"
        
        parts = rest.split('=', 1)
        var_name = parts[0].strip()
        expr = parts[1].strip()
        
        if not var_name:
            return "❌ C: requires variable name\n"
        
        try:
            result = interpreter.evaluate_expression(expr)
            interpreter.variables[var_name] = result
        except Exception as e:
            return f"❌ Error in C: {e}\n"
        
        return ""
    
    elif cmd_type == 'U':
        # U: var - Use (print) variable value
        var_name = rest.strip()
        if not var_name:
            return "❌ U: requires variable name\n"
        
        value = interpreter.variables.get(var_name, '')
        text = str(value)
        interpreter.output.append(text)
        return text + "\n"
    
    elif cmd_type == 'J':
        # J: label - Jump unconditionally to label
        label = rest.strip()
        if label:
            interpreter.jump_to_label(label)
        return ""
    
    elif cmd_type == 'L':
        # L: label - Label definition (no-op, handled by parser)
        return ""
    
    elif cmd_type == 'E':
        # E: - End program
        interpreter.running = False
        return ""
    
    elif cmd_type == 'R':
        # R: comment - Remark (comment, ignored)
        return ""
    
    else:
        return f"❌ Unknown PILOT command: {cmd_type}:\n"
