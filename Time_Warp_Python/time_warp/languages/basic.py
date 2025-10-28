"""BASIC language executor for Time Warp IDE.

BASIC (Beginner's All-purpose Symbolic Instruction Code) implementation
with support for common commands and graphics.
"""

from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from ..core.interpreter import Interpreter, ForContext
    from ..graphics.turtle_state import TurtleState


def execute_basic(
    interpreter: 'Interpreter',
    command: str,
    turtle: 'TurtleState'
) -> str:
    """Execute a BASIC command.
    
    Args:
        interpreter: Interpreter instance with variables and state
        command: BASIC command string
        turtle: Turtle state for graphics
        
    Returns:
        Output text (or empty string)
    """
    cmd = command.strip().upper()
    
    # PRINT command
    if cmd.startswith('PRINT ') or cmd == 'PRINT':
        return _execute_print(interpreter, command[6:] if len(command) > 6 else "")
    
    # LET command (variable assignment)
    if cmd.startswith('LET '):
        return _execute_let(interpreter, command[4:])
    
    # Assignment without LET keyword
    if '=' in cmd and not cmd.startswith('IF '):
        return _execute_let(interpreter, command)
    
    # INPUT command
    if cmd.startswith('INPUT '):
        return _execute_input(interpreter, command[6:])
    
    # IF/THEN command
    if cmd.startswith('IF '):
        return _execute_if(interpreter, command[3:], turtle)
    
    # GOTO command
    if cmd.startswith('GOTO '):
        return _execute_goto(interpreter, command[5:])
    
    # FOR command
    if cmd.startswith('FOR '):
        return _execute_for(interpreter, command[4:])
    
    # NEXT command
    if cmd.startswith('NEXT'):
        return _execute_next(interpreter, command[5:] if len(command) > 5 else "")
    
    # GOSUB command
    if cmd.startswith('GOSUB '):
        return _execute_gosub(interpreter, command[6:])
    
    # RETURN command
    if cmd == 'RETURN':
        return _execute_return(interpreter)
    
    # END command
    if cmd == 'END':
        interpreter.running = False
        return ""
    
    # REM command (comment)
    if cmd.startswith('REM ') or cmd == 'REM':
        return ""
    
    # CLS command (clear screen)
    if cmd == 'CLS':
        turtle.clear()
        interpreter.text_lines.clear()
        return "🎨 Screen cleared\n"
    
    # SCREEN command (set screen mode)
    if cmd.startswith('SCREEN '):
        return _execute_screen(interpreter, command[7:])
    
    # LOCATE command (position cursor)
    if cmd.startswith('LOCATE '):
        return _execute_locate(interpreter, command[7:])
    
    return f"❌ Unknown BASIC command: {command}\n"


def _execute_print(interpreter: 'Interpreter', args: str) -> str:
    """Execute PRINT command"""
    if not args.strip():
        interpreter.output.append("")
        return "\n"
    
    # Handle semicolon (no newline) and comma (tab) separators
    output_parts = []
    current = ""
    in_string = False
    
    for char in args:
        if char == '"':
            in_string = not in_string
        elif char == ';' and not in_string:
            # Semicolon: concatenate without space
            if current.strip():
                output_parts.append(_evaluate_print_item(interpreter, current))
            current = ""
            continue
        elif char == ',' and not in_string:
            # Comma: tab separation
            if current.strip():
                output_parts.append(_evaluate_print_item(interpreter, current))
            output_parts.append("\t")
            current = ""
            continue
        current += char
    
    if current.strip():
        output_parts.append(_evaluate_print_item(interpreter, current))
    
    result = ''.join(output_parts)
    interpreter.output.append(result)
    return result + "\n"


def _evaluate_print_item(interpreter: 'Interpreter', item: str) -> str:
    """Evaluate a single PRINT item (string or expression)"""
    item = item.strip()
    
    # String literal
    if item.startswith('"') and item.endswith('"'):
        return item[1:-1]
    
    # Variable or expression
    try:
        result = interpreter.evaluate_expression(item)
        return str(result)
    except Exception:
        # Try as string variable
        if item in interpreter.string_variables:
            return interpreter.string_variables[item]
        return str(interpreter.variables.get(item, 0))


def _execute_let(interpreter: 'Interpreter', args: str) -> str:
    """Execute LET or assignment"""
    if '=' not in args:
        return "❌ LET requires format: variable = expression\n"
    
    parts = args.split('=', 1)
    var_name = parts[0].strip().upper()
    expr = parts[1].strip()
    
    if not var_name:
        return "❌ LET requires variable name\n"
    
    # String variable (ends with $)
    if var_name.endswith('$'):
        # String assignment
        if expr.startswith('"') and expr.endswith('"'):
            interpreter.string_variables[var_name] = expr[1:-1]
        else:
            interpreter.string_variables[var_name] = str(expr)
        return ""
    
    # Numeric variable
    try:
        result = interpreter.evaluate_expression(expr)
        interpreter.variables[var_name] = result
    except Exception as e:
        return f"❌ Error in LET: {e}\n"
    
    return ""


def _execute_input(interpreter: 'Interpreter', args: str) -> str:
    """Execute INPUT command"""
    # Parse INPUT "prompt"; var or INPUT var
    var_name = args.strip().upper()
    prompt = "? "
    
    if '"' in args:
        # Extract prompt
        match = re.match(r'"([^"]*)"[;,]?\s*(.+)', args)
        if match:
            prompt = match.group(1) + " "
            var_name = match.group(2).strip().upper()
    
    if not var_name:
        return "❌ INPUT requires variable name\n"
    
    # Request input (synchronous or async depending on callback)
    interpreter.start_input_request(prompt, var_name, not var_name.endswith('$'))
    return ""


def _execute_if(interpreter: 'Interpreter', args: str, turtle: 'TurtleState') -> str:
    """Execute IF/THEN command"""
    if ' THEN ' not in args.upper():
        return "❌ IF requires THEN keyword\n"
    
    parts = args.upper().split(' THEN ', 1)
    condition = parts[0].strip()
    then_part = parts[1].strip() if len(parts) > 1 else ""
    
    # Evaluate condition
    try:
        result = interpreter.evaluate_expression(condition)
        condition_true = abs(result) > 0.0001  # True if non-zero
    except Exception as e:
        return f"❌ Error in IF condition: {e}\n"
    
    if condition_true and then_part:
        # Execute THEN part
        # Could be line number (GOTO) or command
        if then_part.isdigit():
            # Jump to line number
            return _execute_goto(interpreter, then_part)
        else:
            # Execute command
            return execute_basic(interpreter, then_part, turtle)
    
    return ""


def _execute_goto(interpreter: 'Interpreter', args: str) -> str:
    """Execute GOTO command"""
    target = args.strip()
    
    if not target:
        return "❌ GOTO requires line number\n"
    
    try:
        line_num = int(target)
        interpreter.jump_to_line_number(line_num)
    except ValueError:
        return f"❌ Invalid line number: {target}\n"
    except Exception as e:
        return f"❌ Error in GOTO: {e}\n"
    
    return ""


def _execute_for(interpreter: 'Interpreter', args: str) -> str:
    """Execute FOR command"""
    # FOR var = start TO end [STEP step]
    match = re.match(
        r'(\w+)\s*=\s*(.+?)\s+TO\s+(.+?)(?:\s+STEP\s+(.+))?$',
        args.upper()
    )
    
    if not match:
        return "❌ FOR requires format: var = start TO end [STEP step]\n"
    
    var_name = match.group(1)
    start_expr = match.group(2)
    end_expr = match.group(3)
    step_expr = match.group(4) if match.group(4) else "1"
    
    try:
        start_val = interpreter.evaluate_expression(start_expr)
        end_val = interpreter.evaluate_expression(end_expr)
        step_val = interpreter.evaluate_expression(step_expr)
        
        # Set loop variable
        interpreter.variables[var_name] = start_val
        
        # Push FOR context to stack
        from ..core.interpreter import ForContext
        context = ForContext(
            var_name=var_name,
            end_value=end_val,
            step=step_val,
            for_line=interpreter.current_line
        )
        interpreter.for_stack.append(context)
        
    except Exception as e:
        return f"❌ Error in FOR: {e}\n"
    
    return ""


def _execute_next(interpreter: 'Interpreter', args: str) -> str:
    """Execute NEXT command"""
    if not interpreter.for_stack:
        return "❌ NEXT without FOR\n"
    
    context = interpreter.for_stack[-1]
    
    # Increment loop variable
    current_val = interpreter.variables.get(context.var_name, 0)
    new_val = current_val + context.step
    interpreter.variables[context.var_name] = new_val
    
    # Check if loop should continue
    if context.step > 0:
        should_continue = new_val <= context.end_value
    else:
        should_continue = new_val >= context.end_value
    
    if should_continue:
        # Jump back to FOR line
        interpreter.current_line = context.for_line
    else:
        # Exit loop
        interpreter.for_stack.pop()
    
    return ""


def _execute_gosub(interpreter: 'Interpreter', args: str) -> str:
    """Execute GOSUB command"""
    target = args.strip()
    
    if not target:
        return "❌ GOSUB requires line number\n"
    
    try:
        line_num = int(target)
        
        # Push current line to stack
        interpreter.gosub_stack.append(interpreter.current_line)
        
        # Jump to subroutine
        interpreter.jump_to_line_number(line_num)
        
    except ValueError:
        return f"❌ Invalid line number: {target}\n"
    except Exception as e:
        return f"❌ Error in GOSUB: {e}\n"
    
    return ""


def _execute_return(interpreter: 'Interpreter') -> str:
    """Execute RETURN command"""
    if not interpreter.gosub_stack:
        return "❌ RETURN without GOSUB\n"
    
    return_line = interpreter.gosub_stack.pop()
    interpreter.current_line = return_line + 1
    
    return ""


def _execute_screen(interpreter: 'Interpreter', args: str) -> str:
    """Execute SCREEN command"""
    mode_str = args.strip()
    
    try:
        mode = int(mode_str)
        from ..core.interpreter import ScreenMode
        
        if mode == 0:
            interpreter.screen_mode = ScreenMode.TEXT
            return "🎨 Text mode activated\n"
        elif mode == 1:
            interpreter.screen_mode = ScreenMode.GRAPHICS
            return "🎨 Graphics mode activated\n"
        else:
            return f"❌ Unknown screen mode: {mode}\n"
    except ValueError:
        return f"❌ Invalid screen mode: {mode_str}\n"


def _execute_locate(interpreter: 'Interpreter', args: str) -> str:
    """Execute LOCATE command"""
    parts = args.split(',')
    
    if len(parts) < 2:
        return "❌ LOCATE requires row, col\n"
    
    try:
        row = int(parts[0].strip())
        col = int(parts[1].strip())
        
        interpreter.cursor_row = max(0, min(24, row - 1))  # 0-24
        interpreter.cursor_col = max(0, min(79, col - 1))  # 0-79
        
    except ValueError:
        return "❌ LOCATE requires numeric row and column\n"
    
    return ""
