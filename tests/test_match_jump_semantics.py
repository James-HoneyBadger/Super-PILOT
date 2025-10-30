from Super_PILOT import TempleCodeInterpreter


class Out:
    def __init__(self):
        self.lines = []
    def insert(self, pos, text):
        self.lines.append(text.rstrip('\n'))
    def see(self, *a):
        pass


def run(prog):
    interp = TempleCodeInterpreter()
    out = Out()
    interp.output_widget = out
    interp.run_program(prog)
    return '\n'.join(out.lines), interp


def test_conditional_T_consumes_sentinel():
    prog = '''Y:1==1
T:Shown
T:Always
END'''
    out, _ = run(prog)
    assert 'Shown' in out
    assert 'Always' in out


def test_conditional_J_consumes_sentinel():
    prog = '''U:X=0
Y:*X* > 0
J:SKIP
T:Shown
L:SKIP
T:Skipped
END'''
    out, _ = run(prog)
    assert 'Shown' in out
    # J: was conditional and did not jump (match was false), so execution
    # falls through to the SKIP label and 'Skipped' should appear.
    assert 'Skipped' in out


def test_M_uses_match_flag_but_not_consume():
    prog = '''Y:1==1
M:SKIP
T:WillNotShow
J:END
L:SKIP
T:Skipped
END'''
    out, _ = run(prog)
    # M: jumps but does not consume sentinel; subsequent J:END will see sentinel consumed
    assert 'Skipped' in out