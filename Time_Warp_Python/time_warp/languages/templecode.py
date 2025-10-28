"""
TempleCode unified executor.
Combines BASIC, PILOT, and Logo command handling behind a single entry point.

This module fully inlines BASIC, PILOT, and Logo implementations so the
IDE exposes a single TempleCode language. Internal helpers mirror the
original command handlers, but are private to this module.
"""
from typing import TYPE_CHECKING, List
import re

if TYPE_CHECKING:
    from ..core.interpreter import Interpreter
    from ..graphics.turtle_state import TurtleState


def execute_templecode(
    interpreter: 'Interpreter',
    command: str,
    turtle: 'TurtleState',
) -> str:
    """
    Execute a single TempleCode command.
    Delegates to existing handlers based on syntax,
    but exposes only one language.
    """
    cmd = command.strip()
    if not cmd:
        return ""

    up = cmd.upper()

    # PILOT: commands start with letter followed by colon (T:, A:, J:, etc.)
    if len(up) > 1 and up[1] == ':':
        return _execute_pilot(interpreter, command, turtle)

    # Check Logo procedures first (user-defined takes precedence)
    first_word = up.split()[0] if up.split() else ""
    if first_word in interpreter.logo_procedures:
        return _execute_logo(interpreter, command, turtle)

    # Logo keywords (excluding PRINT which BASIC owns in TempleCode)
    logo_keywords = {
        "FORWARD", "FD", "BACK", "BK", "LEFT", "LT", "RIGHT", "RT",
        "PENUP", "PU", "PENDOWN", "PD", "CLEARSCREEN", "CS", "HOME",
        "SETXY", "SETX", "SETY", "REPEAT", "TO",
        "SETHEADING", "SETH",
        "SETCOLOR", "SETPENCOLOR", "SETPC", "PENWIDTH", "SETPENSIZE",
        "SETPENWIDTH", "SETPW", "SETBGCOLOR", "SETBG",
        "HIDETURTLE", "HT", "SHOWTURTLE", "ST"
    }
    if first_word in logo_keywords:
        return _execute_logo(interpreter, command, turtle)

    # BASIC keywords and patterns
    basic_keywords = {
        "LET", "PRINT", "INPUT", "GOTO", "IF", "THEN", "FOR", "NEXT",
        "GOSUB", "RETURN", "REM", "DIM", "DATA", "READ", "LINE", "CIRCLE",
        "SCREEN", "CLS", "LOCATE", "END"
    }
    if first_word in basic_keywords:
        return _execute_basic(interpreter, command, turtle)

    # BASIC assignments without LET (X = 5)
    if '=' in up and first_word not in {"IF", "FOR"}:
        left = up.split('=', 1)[0].strip()
        if left and not left.startswith(':'):
            return _execute_basic(interpreter, command, turtle)

    # Default to PILOT semantics (TempleCode fallback)
    return _execute_pilot(interpreter, command, turtle)


# =========================
# Inlined PILOT (private)
# =========================
def _execute_pilot(
    interpreter: 'Interpreter',
    command: str,
    turtle: 'TurtleState',
) -> str:
    cmd = command.strip()
    if not cmd or len(cmd) < 2:
        return ""

    cmd_type = cmd[0].upper()
    if len(cmd) < 2 or cmd[1] != ':':
        return f"❌ Invalid PILOT command: {command}\n"

    rest = cmd[2:].strip()

    if cmd_type == 'T':
        text = interpreter.interpolate_text(rest)
        interpreter.output.append(text)
        return text + "\n"
    elif cmd_type == 'A':
        var_name = rest.strip()
        if not var_name:
            return "❌ A: requires variable name\n"
        # Start async input request
        interpreter.start_input_request("? ", var_name, is_numeric=False)
        return ""
    elif cmd_type == 'M':
        pattern = rest.strip()
        if not pattern:
            interpreter.last_match_succeeded = False
            return ""
        last_input = interpreter.last_input
        regex_pattern = '^' + pattern.replace('*', '.*') + '$'
        try:
            interpreter.last_match_succeeded = bool(
                re.match(regex_pattern, str(last_input), re.IGNORECASE)
            )
        except re.error:
            interpreter.last_match_succeeded = False
        return ""
    elif cmd_type == 'Y':
        if interpreter.last_match_succeeded:
            label = rest.strip()
            if label:
                interpreter.jump_to_label(label)
        return ""
    elif cmd_type == 'N':
        if not interpreter.last_match_succeeded:
            label = rest.strip()
            if label:
                interpreter.jump_to_label(label)
        return ""
    elif cmd_type == 'C':
        if '=' not in rest:
            return "❌ C: requires format: var = expression\n"
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
        var_name = rest.strip()
        if not var_name:
            return "❌ U: requires variable name\n"
        value = interpreter.variables.get(var_name, '')
        text = str(value)
        interpreter.output.append(text)
        return text + "\n"
    elif cmd_type == 'J':
        label = rest.strip()
        if label:
            interpreter.jump_to_label(label)
        return ""
    elif cmd_type == 'L':
        return ""
    elif cmd_type == 'E':
        interpreter.running = False
        return ""
    elif cmd_type == 'R':
        return ""
    else:
        return f"❌ Unknown PILOT command: {cmd_type}:\n"


# =========================
# Inlined BASIC (private)
# =========================
def _execute_basic(
    interpreter: 'Interpreter',
    command: str,
    turtle: 'TurtleState',
) -> str:
    cmd = command.strip().upper()
    if cmd.startswith('PRINT ') or cmd == 'PRINT':
        args = command[6:] if len(command) > 6 else ""
        return _basic_print(interpreter, args)
    if cmd.startswith('LET '):
        return _basic_let(interpreter, command[4:])
    if cmd.startswith('FOR '):
        return _basic_for(interpreter, command[4:])
    if '=' in cmd and not cmd.startswith('IF ') and not cmd.startswith('FOR '):
        return _basic_let(interpreter, command)
    if cmd.startswith('INPUT '):
        return _basic_input(interpreter, command[6:])
    if cmd.startswith('IF '):
        return _basic_if(interpreter, command[3:], turtle)
    if cmd.startswith('GOTO '):
        return _basic_goto(interpreter, command[5:])
    if cmd.startswith('NEXT'):
        args = command[5:] if len(command) > 5 else ""
        return _basic_next(interpreter, args)
    if cmd.startswith('GOSUB '):
        return _basic_gosub(interpreter, command[6:])
    if cmd == 'RETURN':
        return _basic_return(interpreter)
    if cmd == 'END':
        interpreter.running = False
        return ""
    if cmd.startswith('REM ') or cmd == 'REM':
        return ""
    if cmd == 'CLS':
        turtle.clear()
        interpreter.text_lines.clear()
        return "🎨 Screen cleared\n"
    if cmd.startswith('SCREEN '):
        return _basic_screen(interpreter, command[7:])
    if cmd.startswith('LOCATE '):
        return _basic_locate(interpreter, command[7:])
    return f"❌ Unknown BASIC command: {command}\n"


def _basic_print(interpreter: 'Interpreter', args: str) -> str:
    if not args.strip():
        interpreter.output.append("")
        return "\n"
    parts: List[str] = []
    current = ""
    in_quotes = False
    for ch in args:
        if ch == '"':
            in_quotes = not in_quotes
            current += ch
        elif ch == ',' and not in_quotes:
            if current.strip():
                parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())
    if not parts:
        interpreter.output.append("")
        return "\n"
    out_items: List[str] = []
    for item in parts:
        item_trim = item.strip()
        if (
            item_trim.startswith('"')
            and item_trim.endswith('"')
            and len(item_trim) >= 2
        ):
            out_items.append(item_trim[1:-1])
        elif item_trim.upper() == "INKEY$":
            out_items.append("")
        else:
            try:
                value = interpreter.evaluate_expression(item_trim)
                out_items.append(str(value))
            except Exception:
                if item_trim in interpreter.string_variables:
                    out_items.append(interpreter.string_variables[item_trim])
                elif item_trim in interpreter.variables:
                    out_items.append(str(interpreter.variables[item_trim]))
                else:
                    out_items.append(interpreter.interpolate_text(item_trim))
    result = ' '.join(out_items)
    interpreter.output.append(result)
    return result + "\n"


def _basic_let(interpreter: 'Interpreter', args: str) -> str:
    if '=' not in args:
        return "❌ LET requires format: variable = expression\n"
    parts = args.split('=', 1)
    var_name = parts[0].strip().upper()
    expr = parts[1].strip()
    if not var_name:
        return "❌ LET requires variable name\n"
    if var_name.endswith('$'):
        if expr.startswith('"') and expr.endswith('"'):
            interpreter.string_variables[var_name] = expr[1:-1]
        else:
            interpreter.string_variables[var_name] = str(expr)
        return ""
    try:
        result = interpreter.evaluate_expression(expr)
        interpreter.variables[var_name] = result
    except Exception as e:
        return f"❌ Error in LET: {e}\n"
    return ""


def _basic_input(interpreter: 'Interpreter', args: str) -> str:
    var_name = args.strip().upper()
    prompt = "? "
    if '"' in args:
        match = re.match(r'"([^"]*)"[;,]?\s*(.+)', args)
        if match:
            prompt = match.group(1) + " "
            var_name = match.group(2).strip().upper()
    if not var_name:
        return "❌ INPUT requires variable name\n"
    interpreter.start_input_request(
        prompt, var_name, not var_name.endswith('$')
    )
    return ""


def _basic_if(
    interpreter: 'Interpreter',
    args: str,
    turtle: 'TurtleState',
) -> str:
    args_upper = args.upper()
    if ' THEN ' not in args_upper:
        return "❌ IF requires THEN keyword\n"
    then_pos = args_upper.find(' THEN ')
    condition = args[:then_pos].strip()
    then_part = args[then_pos + 6:].strip()
    try:
        result = interpreter.evaluate_expression(condition)
        condition_true = abs(result) > 0.0001
    except Exception as e:
        return f"❌ Error in IF condition: {e}\n"
    if condition_true and then_part:
        if then_part.isdigit():
            return _basic_goto(interpreter, then_part)
        else:
            return _execute_basic(interpreter, then_part, turtle)
    return ""


def _basic_goto(interpreter: 'Interpreter', args: str) -> str:
    target = args.strip()
    if not target:
        return "❌ GOTO requires line number\n"
    try:
        line_num = int(target)
        if line_num not in interpreter.line_number_map:
            return f"❌ GOTO {line_num} failed: line not found\n"
        target_idx = interpreter.line_number_map[line_num]
        interpreter.current_line = target_idx - 1
    except ValueError:
        return f"❌ Invalid line number: {target}\n"
    except Exception as e:
        return f"❌ Error in GOTO: {e}\n"
    return ""


def _basic_for(interpreter: 'Interpreter', args: str) -> str:
    match = re.match(
        r'(\w+)\s*=\s*(.+?)\s+TO\s+(.+?)(?:\s+STEP\s+(.+))?$',
        args.upper(),
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
        interpreter.variables[var_name] = start_val
        from ..core.interpreter import ForContext
        context = ForContext(
            var_name=var_name,
            end_value=end_val,
            step=step_val,
            for_line=interpreter.current_line,
        )
        interpreter.for_stack.append(context)
    except Exception as e:
        return f"❌ Error in FOR: {e}\n"
    return ""


def _basic_next(interpreter: 'Interpreter', args: str) -> str:
    if not interpreter.for_stack:
        return "❌ NEXT without FOR\n"
    context = interpreter.for_stack[-1]
    current_val = interpreter.variables.get(context.var_name, 0)
    new_val = current_val + context.step
    interpreter.variables[context.var_name] = new_val
    if context.step > 0:
        should_continue = new_val <= context.end_value
    else:
        should_continue = new_val >= context.end_value
    if should_continue:
        interpreter.current_line = context.for_line
    else:
        interpreter.for_stack.pop()
    return ""


def _basic_gosub(interpreter: 'Interpreter', args: str) -> str:
    target = args.strip()
    if not target:
        return "❌ GOSUB requires line number\n"
    try:
        line_num = int(target)
        interpreter.gosub_stack.append(interpreter.current_line)
        interpreter.jump_to_line_number(line_num)
    except ValueError:
        return f"❌ Invalid line number: {target}\n"
    except Exception as e:
        return f"❌ Error in GOSUB: {e}\n"
    return ""


def _basic_return(interpreter: 'Interpreter') -> str:
    if not interpreter.gosub_stack:
        return "❌ RETURN without GOSUB\n"
    return_line = interpreter.gosub_stack.pop()
    interpreter.current_line = return_line + 1
    return ""


def _basic_screen(interpreter: 'Interpreter', args: str) -> str:
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


def _basic_locate(interpreter: 'Interpreter', args: str) -> str:
    parts = args.split(',')
    if len(parts) < 2:
        return "❌ LOCATE requires row, col\n"
    try:
        row = int(parts[0].strip())
        col = int(parts[1].strip())
        interpreter.cursor_row = max(0, min(24, row - 1))
        interpreter.cursor_col = max(0, min(79, col - 1))
    except ValueError:
        return "❌ LOCATE requires numeric row and column\n"
    return ""


# =========================
# Inlined Logo (private)
# =========================
def _execute_logo(
    interpreter: 'Interpreter',
    command: str,
    turtle: 'TurtleState',
) -> str:
    cmd = command.strip().upper()
    words = cmd.split()
    if not words:
        return ""
    cmd_name = words[0]
    args = words[1:] if len(words) > 1 else []
    if cmd_name in ['FORWARD', 'FD']:
        return _logo_forward(interpreter, turtle, args)
    if cmd_name in ['BACK', 'BK', 'BACKWARD']:
        return _logo_back(interpreter, turtle, args)
    if cmd_name in ['LEFT', 'LT']:
        return _logo_left(interpreter, turtle, args)
    if cmd_name in ['RIGHT', 'RT']:
        return _logo_right(interpreter, turtle, args)
    if cmd_name in ['PENUP', 'PU']:
        turtle.penup()
        return ""
    if cmd_name in ['PENDOWN', 'PD']:
        turtle.pendown()
        return ""
    if cmd_name == 'HOME':
        turtle.home()
        return ""
    if cmd_name in ['CLEARSCREEN', 'CS', 'CLEAR']:
        turtle.clear()
        return ""
    if cmd_name in ['HIDETURTLE', 'HT']:
        turtle.hideturtle()
        return ""
    if cmd_name in ['SHOWTURTLE', 'ST']:
        turtle.showturtle()
        return ""
    if cmd_name == 'SETXY':
        return _logo_setxy(interpreter, turtle, args)
    if cmd_name == 'SETX':
        return _logo_setx(interpreter, turtle, args)
    if cmd_name == 'SETY':
        return _logo_sety(interpreter, turtle, args)
    if cmd_name in ['SETHEADING', 'SETH']:
        return _logo_setheading(interpreter, turtle, args)
    if cmd_name in ['SETPENCOLOR', 'SETPC']:
        return _logo_setpencolor(interpreter, turtle, args)
    if cmd_name in ['SETBGCOLOR', 'SETBG']:
        return _logo_setbgcolor(interpreter, turtle, args)
    if cmd_name in ['SETPENWIDTH', 'SETPW']:
        return _logo_setpenwidth(interpreter, turtle, args)
    if cmd_name == 'REPEAT':
        return _logo_repeat(interpreter, turtle, command)
    if cmd_name == 'TO':
        return _logo_to(interpreter, command)
    if cmd_name == 'END':
        return _logo_end_procedure(interpreter)
    if cmd_name == 'PRINT':
        return _logo_print(interpreter, ' '.join(args))
    return f"❌ Unknown Logo command: {cmd_name}\n"


def _logo_eval_arg(interpreter: 'Interpreter', arg: str) -> float:
    try:
        if arg.startswith(':'):
            var_name = arg[1:].upper()
            return interpreter.variables.get(var_name, 0)
        return interpreter.evaluate_expression(arg)
    except Exception:
        return 0.0


def _logo_forward(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str],
) -> str:
    if not args:
        return "❌ FORWARD requires distance\n"
    distance = _logo_eval_arg(interpreter, args[0])
    turtle.forward(distance)
    return ""


def _logo_back(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str],
) -> str:
    if not args:
        return "❌ BACK requires distance\n"
    distance = _logo_eval_arg(interpreter, args[0])
    turtle.back(distance)
    return ""


def _logo_left(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str],
) -> str:
    if not args:
        return "❌ LEFT requires angle\n"
    angle = _logo_eval_arg(interpreter, args[0])
    turtle.left(angle)
    return ""


def _logo_right(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str],
) -> str:
    if not args:
        return "❌ RIGHT requires angle\n"
    angle = _logo_eval_arg(interpreter, args[0])
    turtle.right(angle)
    return ""


def _logo_setxy(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str],
) -> str:
    if len(args) < 2:
        return "❌ SETXY requires x and y coordinates\n"
    x = _logo_eval_arg(interpreter, args[0])
    y = _logo_eval_arg(interpreter, args[1])
    turtle.goto(x, y)
    return ""


def _logo_setx(
    interpreter: 'Interpreter',
    turtle: 'TurtleState',
    args: List[str],
) -> str:
    if not args:
        return "❌ SETX requires x coordinate\n"
    x = _logo_eval_arg(interpreter, args[0])
    turtle.goto(x, turtle.y)
    return ""


def _logo_sety(interpreter: 'Interpreter', turtle: 'TurtleState', args: List[str]) -> str:
    if not args:
        return "❌ SETY requires y coordinate\n"
    y = _logo_eval_arg(interpreter, args[0])
    turtle.goto(turtle.x, y)
    return ""


def _logo_setheading(interpreter: 'Interpreter', turtle: 'TurtleState', args: List[str]) -> str:
    if not args:
        return "❌ SETHEADING requires angle\n"
    angle = _logo_eval_arg(interpreter, args[0])
    turtle.setheading(angle)
    return ""


def _logo_setpencolor(interpreter: 'Interpreter', turtle: 'TurtleState', args: List[str]) -> str:
    if len(args) < 3:
        return "❌ SETPENCOLOR requires R G B values (0-255)\n"
    r = int(_logo_eval_arg(interpreter, args[0]))
    g = int(_logo_eval_arg(interpreter, args[1]))
    b = int(_logo_eval_arg(interpreter, args[2]))
    turtle.setcolor(r, g, b)
    return ""


def _logo_setbgcolor(interpreter: 'Interpreter', turtle: 'TurtleState', args: List[str]) -> str:
    if len(args) < 3:
        return "❌ SETBGCOLOR requires R G B values (0-255)\n"
    r = int(_logo_eval_arg(interpreter, args[0]))
    g = int(_logo_eval_arg(interpreter, args[1]))
    b = int(_logo_eval_arg(interpreter, args[2]))
    turtle.setbgcolor(r, g, b)
    return ""


def _logo_setpenwidth(interpreter: 'Interpreter', turtle: 'TurtleState', args: List[str]) -> str:
    if not args:
        return "❌ SETPENWIDTH requires width\n"
    width = _logo_eval_arg(interpreter, args[0])
    turtle.setpenwidth(width)
    return ""


def _logo_repeat(interpreter: 'Interpreter', turtle: 'TurtleState', command: str) -> str:
    match = re.match(r'REPEAT\s+(\S+)\s*\[(.*?)\]', command, re.IGNORECASE)
    if not match:
        return "❌ REPEAT requires format: REPEAT count [ commands ]\n"
    count_expr = match.group(1)
    commands = match.group(2)
    try:
        count = int(_logo_eval_arg(interpreter, count_expr))
    except Exception:
        return "❌ REPEAT count must be a number\n"
    for _ in range(count):
        for cmd in commands.split('\n'):
            cmd = cmd.strip()
            if cmd:
                result = _execute_logo(interpreter, cmd, turtle)
                if result and result.startswith('❌'):
                    return result
    return ""


def _logo_to(interpreter: 'Interpreter', command: str) -> str:
    return "ℹ️ Procedure definitions not yet fully implemented\n"


def _logo_end_procedure(interpreter: 'Interpreter') -> str:
    return ""


def _logo_print(interpreter: 'Interpreter', text: str) -> str:
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    output = interpreter.interpolate_text(text)
    interpreter.output.append(output)
    return output + "\n"
