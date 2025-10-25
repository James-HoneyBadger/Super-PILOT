import random
import pytest

from Super_PILOT import SuperPILOTInterpreter


class DummyOut:
    def __init__(self):
        self.lines = []

    def insert(self, pos, text):
        self.lines.append(str(text))

    def see(self, pos):
        pass


def run_and_capture(interp, program):
    out = DummyOut()
    interp.output_widget = out
    interp.run_program(program)
    return ''.join(out.lines), interp.variables


def test_arithmetic_and_precedence():
    interp = SuperPILOTInterpreter()
    assert interp.evaluate_expression('2 + 3 * 4') == 14
    assert interp.evaluate_expression('(2 + 3) * 4') == 20
    assert interp.evaluate_expression('-5 + 10') == 5
    assert interp.evaluate_expression('2 ** 3') == 8
    assert interp.evaluate_expression('10 % 3') == 1


def test_comparisons_numeric():
    interp = SuperPILOTInterpreter()
    assert interp.evaluate_expression('5 > 3') is True
    assert interp.evaluate_expression('5 < 3') is False
    assert interp.evaluate_expression('5 >= 5') is True
    assert interp.evaluate_expression('5 <= 4') is False
    assert interp.evaluate_expression('5 == 5') is True
    assert interp.evaluate_expression('5 != 6') is True


def test_comparisons_between_numeric_and_string_using_val():
    interp = SuperPILOTInterpreter()
    # assign a string variable via U: syntax
    interp.execute_pilot_command('U:STR=\"5\"')
    # STR replaced as a string in expressions, so 'STR == 5' is false
    assert interp.evaluate_expression('STR == 5') is False
    # but VAL(STR) == 5 is True
    assert interp.evaluate_expression('VAL(STR) == 5') is True


def test_rnd_deterministic_with_seed_and_range():
    interp = SuperPILOTInterpreter()
    random.seed(12345)
    v1 = interp.evaluate_expression('RND()')
    random.seed(12345)
    v2 = interp.evaluate_expression('RND()')
    assert v1 == v2
    assert 0.0 <= v1 < 1.0


def test_basic_if_then_various_comparisons():
    interp = SuperPILOTInterpreter()
    program = '''10 LET X = 3
20 IF X < 5 THEN LET A = 1
30 IF X > 5 THEN LET A = 2
40 IF X <= 3 THEN LET B = 7
50 IF X >= 4 THEN LET B = 8
60 IF X == 3 THEN LET C = 9
70 PRINT A
80 PRINT B
90 PRINT C
END'''
    out, vars = run_and_capture(interp, program)
    # A was set by X < 5
    assert vars.get('A') == 1
    # B set by X <= 3
    assert vars.get('B') == 7
    assert vars.get('C') == 9
    assert '1' in out and '7' in out and '9' in out


def test_pilot_y_n_m_jumps():
    interp = SuperPILOTInterpreter()
    program = '''L:START
Y:2 > 1
M:SKIP
T:SHOULD NOT SEE
L:SKIP
T:JUMPED
END'''
    out, vars = run_and_capture(interp, program)
    assert 'JUMPED' in out


def test_for_next_positive_and_negative_steps():
    # Positive step
    interp = SuperPILOTInterpreter()
    prog = '''10 FOR I = 1 TO 3
20 PRINT I
30 NEXT I
40 PRINT 999
END'''
    out, vars = run_and_capture(interp, prog)
    assert '1' in out and '2' in out and '3' in out
    assert vars.get('I') == 4 or '999' in out

    # Negative step
    interp2 = SuperPILOTInterpreter()
    prog2 = '''10 FOR J = 3 TO 1 STEP -1
20 PRINT J
30 NEXT J
40 END'''
    out2, vars2 = run_and_capture(interp2, prog2)
    assert '3' in out2 and '2' in out2 and '1' in out2


def test_pilot_gosub_and_return():
    interp = SuperPILOTInterpreter()
    prog = '''L:START
R:SUB
T:AFTER
END
L:SUB
T:INSUB
C:
'''
    out, vars = run_and_capture(interp, prog)
    assert 'INSUB' in out and 'AFTER' in out
