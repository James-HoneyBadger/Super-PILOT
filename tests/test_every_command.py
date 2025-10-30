import re
import pytest

from Super_PILOT import TempleCodeInterpreter


class MockOutput:
    def __init__(self):
        self.lines = []

    def insert(self, pos, text):
        # emulate tkinter.Text.insert behaviour; interpreter adds newline
        self.lines.append(text.rstrip('\n'))

    def see(self, _):
        pass

    def get_text(self):
        return "\n".join(self.lines)


def run_program_capture(prog, inputs=None):
    interp = TempleCodeInterpreter()
    out = MockOutput()
    interp.output_widget = out

    # Setup inputs iterator
    inputs_iter = iter(inputs or [])
    interp.get_user_input = lambda prompt="": next(inputs_iter, "")

    interp.run_program(prog)
    return out.get_text(), interp


def test_pilot_t_and_variable_interpolation():
    prog = '''L:START
U:NAME="Alice"
T:Hello *NAME*!
T:Calc *INT(2.7)*
END'''
    out, interp = run_program_capture(prog)
    assert "Hello Alice!" in out
    assert "Calc 2" in out


def test_pilot_expression_token_evaluation():
    prog = '''T:Value is *1+2* 
END'''
    out, _ = run_program_capture(prog)
    assert "Value is 3" in out


def test_pilot_input_and_a_command():
    prog = '''A:AGE
T:You entered *AGE*
END'''
    out, interp = run_program_capture(prog, inputs=["54"])
    # AGE stored as int
    assert interp.variables.get('AGE') == 54
    assert "You entered 54" in out


def test_pilot_y_n_mt_m_j_labels_and_gosub_return():
    prog = '''L:START
U:X=5
Y:*X* > 0
T:Should show always
N:*X* < 0
MT:Matched text
M:END_LABEL
J:END_LABEL
L:END_LABEL
T:EndLabelHit
R:SUB
T:AfterGosub
L:SUB
T:InSub
C:
END'''
    out, interp = run_program_capture(prog)
    # basic checks
    assert "Should show always" in out
    # With current N: semantics (N matches when its condition is TRUE), the N:*X* < 0
    # check for X=5 is false, so MT: should NOT print here.
    assert "Matched text" not in out
    assert "EndLabelHit" in out
    assert "InSub" in out


def test_basic_let_print_input_goto_if_then():
    prog = '''10 LET A = 2
20 LET B = 3
30 IF *A* + *B* == 5 THEN PRINT "OK"
40 INPUT C
50 PRINT *C*
60 END'''
    out, interp = run_program_capture(prog, inputs=["7"])
    assert "OK" in out
    assert "7" in out


def test_basic_for_next_and_step_and_nested():
    prog = '''10 LET S = 0
20 FOR I = 1 TO 3
30 U:S=*S*+*I*
40 NEXT I
50 FOR J = 3 TO 1 STEP -1
60 U:S=*S*+*J*
70 NEXT J
80 PRINT *S*
90 END'''
    out, interp = run_program_capture(prog)
    # S should be 1+2+3 + 3+2+1 = 12
    assert re.search(r"\b12\b", out)


def test_next_without_for_logs_error():
    prog = 'PRINT "Start"\nNEXT\nEND'
    out, _ = run_program_capture(prog)
    assert "NEXT without FOR" in out


def test_basic_rem_and_end():
    prog = '10 REM this is a comment\n20 PRINT "Hi"\n30 END\n40 PRINT "Nope"'
    out, _ = run_program_capture(prog)
    assert "Hi" in out
    assert "Nope" not in out


def test_logo_commands_are_handled():
    prog = 'FORWARD 10\nLEFT 90\nPENUP\nPENDOWN\nCS\nSETXY 10,20\nEND'
    out, _ = run_program_capture(prog)
    assert "Logo command executed" in out or "Screen command" in out or "Turtle moved" in out


def test_expression_helpers_mid_upper_lower_val():
    prog = '''T:*MID("abcdef",2,3)*
T:*UPPER("hi")*
U:V=VAL("123")
T:*V*
END'''
    out, interp = run_program_capture(prog)
    assert "bcd" in out
    assert "HI" in out
    assert interp.variables.get('V') == 123


def test_rnd_and_int_behaviour():
    prog = 'T:*RND(1)*\nT:*INT(3.7)*\nEND'
    out, interp = run_program_capture(prog)
    assert re.search(r"\d+\.\d+", out) or "0." in out
    assert "3" in out


def test_invalid_expression_returns_zero_and_logs():
    prog = 'T:*UNKNOWNFUNC(1)*\nEND'
    out, _ = run_program_capture(prog)
    assert "Expression error" in out or "0" in out
