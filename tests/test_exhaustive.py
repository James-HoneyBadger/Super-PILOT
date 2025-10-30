import pytest
import random

from Super_PILOT import TempleCodeInterpreter


class DummyOut:
    def __init__(self):
        self.lines = []

    def insert(self, pos, text):
        self.lines.append(str(text))

    def see(self, pos):
        pass


def run_capture(program, inputs=None, seed=None):
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out
    # simulate inputs if provided
    inputs = inputs or {}
    def fake_input(prompt=''):
        for k, v in inputs.items():
            if k in prompt:
                return v
        # fallback: return empty
        return ''
    interp.get_user_input = fake_input
    if seed is not None:
        random.seed(seed)
    interp.run_program(program)
    return interp, ''.join(out.lines)


def test_parse_line_and_labels():
    interp = TempleCodeInterpreter()
    # parse_line via load_program and labels collection
    program = 'L:FOO\n10 PRINT "X"\nL:BAR\n'
    interp.load_program(program)
    # labels should be set to indices
    assert 'FOO' in interp.labels and 'BAR' in interp.labels


def test_pilot_commands_basic():
    # T:, A:, U:, Y:, N:, J:, M:, R:, C:
    prog = '''L:START
A:NAME
T:Hello *NAME*
U:X=5
Y:*X* > 0
M:ENDLBL
T:Nope
L:ENDLBL
T:Bye
END'''
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out
    # simulate A:NAME input
    interp.get_user_input = lambda p='': 'Tester' if 'NAME' in p else ''
    interp.run_program(prog)
    joined = ''.join(out.lines)
    assert 'Hello Tester' in joined
    assert 'Bye' in joined


def test_basic_commands_and_if():
    prog = '''10 LET A = 2
20 IF A == 2 THEN LET B = 3
30 IF A == 3 THEN LET B = 999
40 PRINT B
END'''
    interp, out = run_capture(prog)
    assert '3' in out
    assert interp.variables.get('B') == 3


def test_logo_commands_do_not_crash():
    prog = 'FORWARD 10\nLEFT 90\nT:Done\nEND'
    interp, out = run_capture(prog)
    assert 'Done' in out


def test_for_next_nested_and_errors():
    # nested loops
    prog = '''10 FOR I = 1 TO 2
20 FOR J = 1 TO 2
30 PRINT I
40 NEXT J
50 NEXT I
60 END'''
    interp, out = run_capture(prog)
    assert '1' in out
    # NEXT without FOR should not throw, test graceful handling
    interp2 = TempleCodeInterpreter()
    out2 = DummyOut()
    interp2.output_widget = out2
    interp2.run_program('10 NEXT\nEND')
    assert 'Program execution completed' in ''.join(out2.lines)


def test_goto_and_gosub_return():
    prog = '''10 GOTO 30
20 T:ShouldNotSee
30 T:Seen
40 R:SUB
50 T:AfterGosub
60 END
L:SUB
T:InSub
C:
'''
    interp, out = run_capture(prog)
    assert 'Seen' in out


def test_variable_name_collision():
    interp = TempleCodeInterpreter()
    # A and AB variable collision test
    interp.variables['A'] = 1
    interp.variables['AB'] = 2
    # ensure replacing *A* does not accidentally replace AB
    text = 'A:*A* AB:*AB*'
    # simulate T: handling
    interp.output_widget = DummyOut()
    interp.execute_pilot_command('T:' + text)
    joined = ''.join(interp.output_widget.lines)
    assert 'A:1' in joined and 'AB:2' in joined


def test_evaluate_expression_edge_cases():
    interp = TempleCodeInterpreter()
    # division by zero should be handled gracefully (via evaluate_expression catching errors)
    val = interp.evaluate_expression('1/0')
    # if error, interpreter's evaluate_expression returns 0 per implementation
    assert val == 0 or val == float('inf') or isinstance(val, float)


def test_max_iterations_guard():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out
    # infinite loop via GOTO to self
    interp.run_program('10 GOTO 10\nEND')
    # max iterations message should appear
    joined = ''.join(out.lines)
    assert 'Maximum iterations reached' in joined or 'Program execution completed' in joined


def test_debugger_step_and_breakpoints():
    interp = TempleCodeInterpreter()
    out = DummyOut()
    interp.output_widget = out
    # program with multiple lines
    prog = '10 T:One\n20 T:Two\n30 T:Three\nEND'
    interp.load_program(prog)
    interp.set_debug_mode(True)
    interp.breakpoints.add(1)  # breakpoint at line index 1 (line 20)
    interp.continue_running()
    # after continue, execution should pause at breakpoint (line 1)
    # step should execute that line
    interp.step()
    assert 'Two' in ''.join(out.lines)
