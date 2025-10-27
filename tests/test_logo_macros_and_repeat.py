import pytest
from Super_PILOT import SuperPILOTInterpreter

class DummyOut:
    def __init__(self):
        self.lines = []
    def insert(self, where, text):
        self.lines.append(str(text))
    def see(self, where):
        pass

def run(prog):
    interp = SuperPILOTInterpreter()
    interp.output_widget = DummyOut()
    interp.run_program(prog)
    return interp

def test_nested_repeat_counts():
    # Expect 3 * 2 = 6 forward moves; we infer by line metadata length
    prog = """REPEAT 3 [ REPEAT 2 [ FORWARD 10 ] ]\nEND"""
    interp = run(prog)
    meta = interp.turtle_graphics.get('line_meta', []) if interp.turtle_graphics else []
    assert len(meta) == 6

def test_macro_define_and_call():
    prog = """DEFINE BOX [ REPEAT 4 [ FORWARD 20 RIGHT 90 ] ]\nCALL BOX\nEND"""
    interp = run(prog)
    meta = interp.turtle_graphics.get('line_meta', [])
    # A box: 4 sides
    assert len(meta) == 4

def test_macro_nested_repeat_combo():
    prog = """DEFINE EDGE [ FORWARD 5 RIGHT 90 ]\nREPEAT 3 [ CALL EDGE CALL EDGE ]\nEND"""
    interp = run(prog)
    meta = interp.turtle_graphics.get('line_meta', [])
    # Each CALL EDGE draws 1 line; 2 per outer iteration * 3 = 6
    assert len(meta) == 6


def test_profile_report_collects_logo():
    prog = """PROFILE ON\nREPEAT 2 [ FORWARD 10 RIGHT 90 ]\nPROFILE REPORT\nEND"""
    interp = run(prog)
    # Profile stats should include FORWARD and RIGHT
    keys = set(interp.profile_stats.keys())
    assert 'FORWARD' in keys and 'RIGHT' in keys
    # Counts should match loop expansion (2 forward, 2 right)
    assert interp.profile_stats['FORWARD']['count'] == 2
    assert interp.profile_stats['RIGHT']['count'] == 2


def test_penstyle_affects_metadata():
    prog = """PENSTYLE dotted\nFORWARD 15\nPENSTYLE dashed\nFORWARD 10\nEND"""
    interp = run(prog)
    meta = interp.turtle_graphics.get('line_meta', [])
    assert len(meta) == 2
    styles = {m['style'] for m in meta}
    assert 'dotted' in styles and 'dashed' in styles


def test_debuglines_command_does_not_crash():
    prog = """FORWARD 5\nDEBUGLINES\nEND"""
    interp = run(prog)
    # Ensure command executed; metadata present
    meta = interp.turtle_graphics.get('line_meta', [])
    assert len(meta) == 1
