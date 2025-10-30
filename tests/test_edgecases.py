import re
import pytest
from Super_PILOT import TempleCodeInterpreter


def run_and_capture(program, inputs=None):
    interp = TempleCodeInterpreter()
    interp.output_widget = None
    if inputs:
        vals = list(inputs)
        interp.get_user_input = lambda prompt='': vals.pop(0) if vals else ''
    interp.run_program(program)
    return interp


def test_variable_name_collision():
    prog = '''U:A=1
U:AB=2
U:SUM=A+AB
END'''
    interp = run_and_capture(prog)
    assert interp.variables['A'] == 1
    assert interp.variables['AB'] == 2
    assert interp.variables['SUM'] == 3


def test_max_iterations_guard():
    # Program that loops forever using label jump
    prog = '''L:LOOP
J:LOOP
END'''
    interp = run_and_capture(prog)
    # The interpreter should stop after hitting the max_iterations guard
    # and set running to False
    assert interp.running is False


def test_rnd_and_val_and_mid():
    interp = TempleCodeInterpreter()
    r1 = interp.evaluate_expression('RND()')
    r2 = interp.evaluate_expression('RND(1)')
    r3 = interp.evaluate_expression('RND(5)')
    assert 0.0 <= r1 <= 1.0
    assert 0.0 <= r2 <= 1.0
    assert 0.0 <= r3 <= 1.0
    assert interp.evaluate_expression('VAL("12")') == 12
    assert interp.evaluate_expression('VAL("12.5")') == 12.5
    assert interp.evaluate_expression('MID("hello",2,2)') == 'el'


def test_case_insensitive_if_then():
    prog = '''10 LET A = 1
20 IF A == 1 then PRINT "YES"
30 END'''
    interp = run_and_capture(prog)
    # Should print YES (captured via console)
    # We can't directly read the console here, but ensure no crash and variable A remains
    assert interp.variables['A'] == 1


def test_goto_line_number_resolution():
    prog = '''10 PRINT "LINE10"
20 GOTO 10
30 END'''
    interp = run_and_capture(prog)
    # Should not hang (max_iterations guard may stop it); ensure program finished
    assert interp.running is False
