
import re
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Super_PILOT import TempleCodeInterpreter


def run_program_and_get_output(program, input_values=None):
    interp = TempleCodeInterpreter()
    interp.output_widget = None
    # Provide canned inputs if requested (for A: and INPUT)
    inputs = list(input_values or [])
    interp.get_user_input = lambda prompt="": (inputs.pop(0) if inputs else "")
    interp.run_program(program)
    # capture the printed output from interpreter via pytest's capsys in callers
    return interp


def test_pilot_T_and_U_and_interpolation(capsys):
    prog = '''U:X=5
T:Value is *X*
END'''
    interp = run_program_and_get_output(prog)
    out = capsys.readouterr().out
    assert 'Value is 5' in out
    assert interp.variables['X'] == 5


def test_pilot_A_sets_variable_and_input_conversion(capsys):
    prog = '''A:NAME
T:Hello *NAME*
END'''
    interp = TempleCodeInterpreter()
    interp.output_widget = None
    interp.get_user_input = lambda prompt="": 'Alice'
    interp.run_program(prog)
    out = capsys.readouterr().out
    assert 'Hello Alice' in out
    assert interp.variables['NAME'] == 'Alice'


def test_pilot_Y_N_M_J_and_labels(capsys):
    prog = '''L:START
U:X=1
Y:*X* == 1
M:SKIP
T:NoJump
J:END
L:SKIP
T:Jumped
END'''
    interp = run_program_and_get_output(prog)
    out = capsys.readouterr().out
    assert 'Jumped' in out


def test_pilot_R_and_C_gosub_return(capsys):
    prog = '''L:MAIN
R:SUB
T:AfterSub
END
L:SUB
T:InSub
C:
END'''
    interp = run_program_and_get_output(prog)
    out = capsys.readouterr().out
    assert 'InSub' in out
    assert 'AfterSub' in out


def test_basic_LET_PRINT_INPUT_GOTO_IF_REM(capsys):
    prog = '''10 LET A = 4
20 PRINT A
30 INPUT B
40 IF B == 7 THEN PRINT "OK"
50 REM this is a comment
60 GOTO 80
70 PRINT "NO"
80 PRINT "END"
END'''
    interp = TempleCodeInterpreter()
    interp.output_widget = None
    interp.get_user_input = lambda prompt="": '7'
    interp.run_program(prog)
    out = capsys.readouterr().out
    # Should print '4' from line 20, 'OK' from IF, and 'END'
    assert re.search(r'\b4\b', out)
    assert 'OK' in out
    assert 'END' in out


def test_logo_commands_and_misc(capsys):
    prog = '''FORWARD 100
RIGHT 90
SETXY 10 20
PENUP
PENDOWN
CLEARSCREEN
HOME
END'''
    interp = run_program_and_get_output(prog)
    out = capsys.readouterr().out
    # Look for at least one of the logo log messages
    assert 'Logo command executed' in out or 'Turtle moved to position' in out


def test_expression_functions_direct():
    interp = TempleCodeInterpreter()
    # RND
    r = interp.evaluate_expression('RND()')
    assert isinstance(r, float)
    assert 0.0 <= r <= 1.0
    # INT
    assert interp.evaluate_expression('INT(3.7)') == 3
    # VAL
    assert interp.evaluate_expression('VAL("12")') == 12
    # UPPER/LOWER
    assert interp.evaluate_expression('UPPER("ab")') == 'AB'
    assert interp.evaluate_expression('LOWER("AB")') == 'ab'
    # MID
    assert interp.evaluate_expression('MID("hello",2,2)') == 'el'
