import re
import pytest
from Time_Warp import TimeWarpInterpreter


def run_program(program, inputs=None):
    interp = TimeWarpInterpreter()
    interp.output_widget = None
    inputs = list(inputs or [])
    interp.get_user_input = lambda prompt="": (inputs.pop(0) if inputs else "")
    interp.run_program(program)
    return interp


def test_pilot_basic_commands_and_interpolation(capsys):
    prog = """L:START
A:NAME
T:Hello *NAME*
U:X=2
U:Y=3
U:SUM=*X*+*Y*
T:Sum is *SUM*
END"""
    interp = run_program(prog, inputs=["Tester"])
    out = capsys.readouterr().out
    assert "Hello Tester" in out
    assert interp.variables["SUM"] == 5


def test_pilot_jumps_and_gosub(capsys):
    prog = """L:MAIN
R:SUB
T:AfterSub
END
L:SUB
T:InSub
C:
END"""
    interp = run_program(prog)
    out = capsys.readouterr().out
    assert "InSub" in out and "AfterSub" in out


def test_basic_for_next_simple(capsys):
    prog = """10 FOR I = 1 TO 3
20 PRINT I
30 NEXT I
END"""
    interp = run_program(prog)
    out = capsys.readouterr().out
    assert re.findall(r"\b1\b|\b2\b|\b3\b", out)


def test_basic_for_next_step_and_negative(capsys):
    prog = """FOR I = 5 TO 1 STEP -2
T:*I*
NEXT I
END"""
    interp = run_program(prog)
    out = capsys.readouterr().out
    # Expect 5 then 3 then 1
    assert "5" in out and "3" in out and "1" in out


def test_nested_for_next(capsys):
    prog = """FOR I = 1 TO 2
FOR J = 1 TO 2
T:*I*,*J*
NEXT J
NEXT I
END"""
    interp = run_program(prog)
    out = capsys.readouterr().out
    assert out.count("\n") >= 4


def test_basic_let_print_if_goto(capsys):
    prog = """10 LET A = 4
20 PRINT A
30 INPUT B
40 IF B == 7 THEN PRINT "OK"
50 REM this is a comment
60 GOTO 80
70 PRINT "NO"
80 PRINT "END"
END"""
    interp = TimeWarpInterpreter()
    interp.output_widget = None
    interp.get_user_input = lambda prompt="": "7"
    interp.run_program(prog)
    out = capsys.readouterr().out
    assert re.search(r"\b4\b", out)
    assert "OK" in out and "END" in out


def test_logo_commands():
    prog = """FORWARD 100
RIGHT 90
SETXY 10 20
PENUP
PENDOWN
CLEARSCREEN
HOME
END"""
    interp = run_program(prog)
    # After all commands, HOME should bring turtle back to 0,0
    assert interp.turtle_x == 0
    assert interp.turtle_y == 0
    # Heading should be 90 from the RIGHT 90 command
    assert interp.turtle_heading == 90


def test_expression_functions_direct():
    interp = TimeWarpInterpreter()
    r = interp.evaluate_expression("RND()")
    assert isinstance(r, float) and 0.0 <= r <= 1.0
    assert interp.evaluate_expression("INT(3.7)") == 3
    assert interp.evaluate_expression('VAL("12")') == 12
    assert interp.evaluate_expression('UPPER("ab")') == "AB"
    assert interp.evaluate_expression('LOWER("AB")') == "ab"
    assert interp.evaluate_expression('MID("hello",2,2)') == "el"


def test_error_next_without_for(capsys):
    prog = "NEXT I\nEND"
    run_program(prog)
    out = capsys.readouterr().out
    assert "NEXT without FOR" in out
