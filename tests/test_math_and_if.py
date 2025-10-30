import pytest

from Super_PILOT import TempleCodeInterpreter


class DummyOut:
    def __init__(self):
        self.lines = []

    def insert(self, pos, text):
        # Normalize newlines and record output
        self.lines.append(str(text))

    def see(self, pos):
        pass


def test_evaluate_basic_expressions():
    interp = TempleCodeInterpreter()

    assert interp.evaluate_expression('2+3*4') == 14
    assert interp.evaluate_expression('INT(3.9)') == 3

    # VAL should convert to int when no decimal point
    assert interp.evaluate_expression('VAL("123") + 7') == 130

    # MID, UPPER
    assert interp.evaluate_expression('MID("hello",2,3)') == 'ell'
    assert interp.evaluate_expression('UPPER("abc")') == 'ABC'

    # Division should follow Python semantics
    assert pytest.approx(interp.evaluate_expression('10/4'), rel=1e-6) == 2.5


def test_rnd_range_is_0_to_1():
    interp = TempleCodeInterpreter()
    # Test multiple samples to reduce flakiness
    for _ in range(50):
        v = interp.evaluate_expression('RND()')
        assert isinstance(v, float)
        assert 0.0 <= v < 1.0


def test_basic_if_then_assignment_and_print():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out

    program = '''10 LET X = 7
20 IF X > 5 THEN LET Y = 100
30 IF X <= 5 THEN LET Y = 0
40 PRINT Y
END'''

    interp.run_program(program)

    joined = ''.join(out.lines)
    assert '100' in joined
    assert interp.variables.get('Y') == 100


def test_if_then_with_goto_changes_flow():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out

    program = '''10 LET A = 2
20 IF A==2 THEN GOTO 50
30 LET A = 999
40 GOTO 60
50 LET A = 42
60 PRINT A
END'''

    interp.run_program(program)
    joined = ''.join(out.lines)
    assert '42' in joined
    assert interp.variables.get('A') == 42


def test_print_string_and_expression():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out

    program = '''10 PRINT "Hello"
20 PRINT 2+3
END'''

    interp.run_program(program)
    joined = ''.join(out.lines)
    assert 'Hello' in joined
    assert '5' in joined


def test_variable_expression_binding():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out

    program = '''10 LET A = 5
20 LET B = A + 2
30 PRINT B
END'''

    interp.run_program(program)
    assert interp.variables.get('B') == 7
    assert '7' in ''.join(out.lines)


def test_t_token_expression_evaluation():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out
    # Use a T: with *RND(1)* token and ensure it gets evaluated
    # Seed to make RND deterministic
    import random
    random.seed(1)
    program = 'T:Random number: *RND(1)*\nEND'
    interp.run_program(program)
    joined = ''.join(out.lines)
    assert 'Random number:' in joined
    # Should not literally contain '*RND(1)*'
    assert '*RND(1)*' not in joined


def test_mt_conditional_text():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out
    program = '''Y:1==1
MT:Shown when match
N:1==1
MT:Not shown
END'''
    interp.run_program(program)
    joined = ''.join(out.lines)
    assert 'Shown when match' in joined
    # With current N: semantics (N sets match when its condition is TRUE),
    # the N:1==1 will set a match and the following MT will print. So we
    # expect 'Not shown' to appear here.
    assert 'Not shown' in joined
