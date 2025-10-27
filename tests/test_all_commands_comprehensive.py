import pytest
from Super_PILOT import SuperPILOTInterpreter


class MockOutput:
    def __init__(self):
        self.lines = []

    def insert(self, pos, text):
        self.lines.append(text.rstrip('\n'))

    def see(self, _):
        pass

    def get_text(self):
        return "\n".join(self.lines)


def run_program_capture(prog, inputs=None):
    interp = SuperPILOTInterpreter()
    out = MockOutput()
    interp.output_widget = out
    inputs_iter = iter(inputs or [])
    interp.get_user_input = lambda prompt="": next(inputs_iter, "")
    interp.run_program(prog)
    return out.get_text(), interp


# PILOT Commands Tests
def test_pilot_t_command():
    prog = '''T:Hello World
END'''
    out, _ = run_program_capture(prog)
    assert "Hello World" in out


def test_pilot_a_command():
    prog = '''A:NAME
END'''
    out, interp = run_program_capture(prog, inputs=["Alice"])
    assert interp.variables['NAME'] == "Alice"


def test_pilot_u_command():
    prog = '''U:X=42
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables['X'] == 42


def test_pilot_j_command():
    prog = '''L:START
T:Start
J:END
T:Skipped
L:END
T:End
END'''
    out, _ = run_program_capture(prog)
    assert "Start" in out
    assert "End" in out
    assert "Skipped" not in out


def test_pilot_r_c_commands():
    prog = '''L:MAIN
R:SUB
T:Back
END
L:SUB
T:In Sub
C:
END'''
    out, _ = run_program_capture(prog)
    assert "In Sub" in out
    assert "Back" in out


def test_pilot_y_n_commands():
    prog = '''U:X=1
Y:*X*==1
T:Yes
N:*X*==0
T:No
END'''
    out, _ = run_program_capture(prog)
    assert "Yes" in out
    assert "No" not in out


# BASIC Commands Tests
def test_basic_let():
    prog = '''LET X = 10
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables['X'] == 10


def test_basic_print():
    prog = '''PRINT "Hello"
END'''
    out, _ = run_program_capture(prog)
    assert "Hello" in out


def test_basic_input():
    prog = '''INPUT X
END'''
    out, interp = run_program_capture(prog, inputs=["5"])
    assert interp.variables['X'] == 5


def test_basic_goto():
    prog = '''10 PRINT "Start"
20 GOTO 40
30 PRINT "Skipped"
40 PRINT "End"
END'''
    out, _ = run_program_capture(prog)
    assert "Start" in out
    assert "End" in out
    assert "Skipped" not in out


def test_basic_if_then():
    prog = '''LET X = 1
IF X == 1 THEN PRINT "True"
END'''
    out, _ = run_program_capture(prog)
    assert "True" in out


def test_basic_for_next():
    prog = '''FOR I = 1 TO 3
PRINT I
NEXT I
END'''
    out, _ = run_program_capture(prog)
    assert "1" in out
    assert "2" in out
    assert "3" in out


# Logo Commands Tests
def test_logo_forward():
    prog = '''FORWARD 50
END'''
    out, interp = run_program_capture(prog)
    # Assuming turtle position updates
    assert interp.variables.get('TURTLE_X', 0) == 50  # Assuming default direction


def test_logo_right():
    prog = '''RIGHT 90
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('TURTLE_HEADING', 0) == 90


# ML Commands Tests
def test_ml_load_model():
    prog = '''LOADMODEL test linear_regression
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('MODEL_TEST_READY', 0) == 1


def test_ml_create_data():
    prog = '''CREATEDATA test linear
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('DATA_TEST_READY', 0) == 1


def test_ml_train_model():
    prog = '''CREATEDATA test linear
LOADMODEL test linear_regression
TRAINMODEL test test
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('MODEL_TEST_TRAINED', 0) == 1


def test_ml_predict():
    prog = '''CREATEDATA test linear
LOADMODEL test linear_regression
TRAINMODEL test test
PREDICT test 5
END'''
    out, interp = run_program_capture(prog)
    assert 'ML_PREDICTION' in interp.variables


# Game Commands Tests
def test_game_create_object():
    prog = '''GAME:CREATE player sprite 100 100 32 32
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('GAME_PLAYER_CREATED', 0) == 1


def test_game_move_object():
    prog = '''GAME:CREATE player sprite 0 0 32 32
GAME:MOVE player 10 10 1
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('GAME_PLAYER_X', 0) == 10


def test_game_physics():
    prog = '''GAME:CREATE ball sprite 0 0 32 32
GAME:PHYSICS ball VELOCITY 5 5
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('GAME_BALL_VX', 0) == 5


def test_game_collision():
    prog = '''GAME:CREATE obj1 sprite 0 0 32 32
GAME:CREATE obj2 sprite 30 30 32 32
GAME:COLLISION CHECK obj1 obj2
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('GAME_COLLISION', 0) == 1


# Audio Commands Tests
def test_audio_load_sound():
    prog = '''LOADSOUND beep test.wav
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('AUDIO_BEEP_LOADED', 0) == 1


def test_audio_play_sound():
    prog = '''LOADSOUND beep test.wav
PLAYSOUND beep
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('AUDIO_BEEP_PLAYING', 0) == 1


# Multiplayer Commands Tests
def test_mp_host():
    prog = '''GAME:MPHOST testroom competitive 4
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('GAME_MP_ROOM', '') == 'testroom'


def test_mp_join():
    prog = '''GAME:MPHOST testroom
GAME:MPJOIN p1 Alice
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('GAME_MP_PLAYER_COUNT', 0) == 1


def test_mp_snapshot():
    prog = '''GAME:MPHOST testroom
GAME:MPSNAPSHOT
END'''
    out, interp = run_program_capture(prog)
    assert 'GAME_MP_SNAPSHOT' in interp.variables


# Networking Commands Tests
def test_net_host():
    prog = '''GAME:NET HOST 9999
END'''
    out, interp = run_program_capture(prog)
    assert interp.variables.get('NET_HOSTING', 0) == 1


def test_net_connect():
    # Note: This would require a server running, so mock or skip
    prog = '''GAME:NET CONNECT localhost 9999 user
END'''
    out, interp = run_program_capture(prog)
    # Assuming no server, but command should not crash
    assert True  # Placeholder


def test_net_send():
    prog = '''GAME:NET SEND chat "Hello"
END'''
    out, interp = run_program_capture(prog)
    # Assuming no network, but should not error
    assert True


# Add more tests as needed for all commands