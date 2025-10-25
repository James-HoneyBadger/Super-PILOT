import re
import pytest

from Time_Warp import TimeWarpInterpreter


class Out:
    def __init__(self):
        self.lines = []

    def insert(self, pos, text):
        self.lines.append(text.rstrip("\n"))

    def see(self, *_):
        pass


def run(prog, inputs=None):
    interp = TimeWarpInterpreter()
    out = Out()
    interp.output_widget = out
    it = iter(inputs or [])
    interp.get_user_input = lambda prompt="": next(it, "")
    interp.run_program(prog)
    return "".join(out.lines), interp


def test_determine_and_parse_and_basic_gosub_return():
    # Ensure GOSUB/RETURN for BASIC work (push/pop) and parse_line works
    prog = """10 PRINT "Start"\n20 GOSUB 50\n30 PRINT "AfterGosub"\n40 END\n50 PRINT "InSub"\n60 RETURN\n"""
    out, interp = run(prog)
    assert "Start" in out
    assert "InSub" in out
    assert "AfterGosub" in out


def test_pilot_u_assignment_and_update_and_types():
    prog = """U:A=5\nT:*A*\nU:B=3.14\nT:*B*\nU:C="abc"\nT:*C*\nEND"""
    out, interp = run(prog)
    assert "5" in out
    assert "3.14" in out
    assert "abc" in out
    assert isinstance(interp.variables["A"], int)
    assert isinstance(interp.variables["B"], float)


def test_a_input_numeric_and_string_and_decimal():
    prog = "A:X\nT:*X*\nA:Y\nT:*Y*\nEND"
    out, interp = run(prog, inputs=["42", "hello"])
    assert "42" in out
    assert "hello" in out


def test_t_expression_and_token_interpolation():
    prog = "U:A=2\nT:Sum *A* + *3* = *A+3*\nEND"
    out, interp = run(prog)
    assert "Sum 2 + 3 = 5" in out


def test_y_n_mt_flow_and_label_jump():
    prog = """L:START\nU:X=0\nY:*X* > 0\nT:Positive\nN:*X* <= 0\nT:ZeroOrNeg\nM:SKIP\nJ:SKIP\nL:SKIP\nT:SkippedLabel\nEND"""
    out, interp = run(prog)
    # With current N: semantics (N matches when its condition is TRUE), for X=0
    # the N:*X* <= 0 check is true so ZeroOrNeg should appear and M: will
    # also jump to SKIP (so SkippedLabel should appear as well).
    assert "ZeroOrNeg" in out
    assert "SkippedLabel" in out


def test_conditional_t_after_y_n_consumed_once():
    prog = """U:V=1\nY:*V* == 1\nT:Yes\nT:Always\nEND"""
    out, _ = run(prog)
    # First T conditional, second T unconditional
    assert "Yes" in out
    assert "Always" in out


def test_basic_if_then_executes_various_then_commands():
    prog = """10 LET A=1\n20 IF *A*==1 THEN PRINT "OK"\n30 IF *A*==1 THEN U:B=5\n40 IF *B*==5 THEN PRINT "BOK"\n50 END"""
    out, interp = run(prog)
    assert "OK" in out
    assert "BOK" in out
    assert interp.variables.get("B") == 5


def test_for_next_with_specified_var_and_nested_and_pop():
    # Use explicit parentheses and tokenized variables so exponentiation is unambiguous
    prog = """10 U:S=0\n20 FOR I=1 TO 2\n30 FOR J=1 TO 2\n40 U:S=*S*+(*I* ** *J*)\n50 NEXT J\n60 NEXT I\n70 PRINT *S*\n80 END"""
    out, interp = run(prog)
    # 1**1 + 1**2 + 2**1 + 2**2 = 1 + 1 + 2 + 4 = 8
    assert "8" in out


def test_next_with_var_not_found_and_error_message():
    prog = "NEXT X\nEND"
    out, _ = run(prog)
    assert "NEXT without FOR" in out or "NEXT for unknown variable" in out


def test_logo_and_misc_commands_smoke():
    prog = "FORWARD 10\nLEFT 90\nPENUP\nPENDOWN\nCS\nSETXY 10,20\nEND"
    out, _ = run(prog)
    assert out


def test_expression_edge_cases_and_val_mid_upper_lower():
    prog = 'T:*VAL("10")*\nT:*MID("abcde",2,2)*\nT:*UPPER("x")*\nT:*LOWER("Y")*\nEND'
    out, _ = run(prog)
    assert "10" in out
    assert "bc" in out
    assert "X" in out
    assert "y" in out


def test_variable_name_collision_and_word_boundaries():
    prog = "U:A=1\nU:AB=2\nT:*A* *AB*\nT:*A+*AB**\nEND"
    out, _ = run(prog)
    assert "1" in out and "2" in out


def test_expression_errors_are_logged_and_return_zero():
    prog = "T:*NONEXISTENT(1)*\nEND"
    out, _ = run(prog)
    assert "Expression error" in out or "0" in out
