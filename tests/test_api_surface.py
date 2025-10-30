import os
import pytest

from Super_PILOT import TempleCodeInterpreter


def test_determine_command_type_samples():
    interp = TempleCodeInterpreter()
    assert interp.determine_command_type('T:Hello') == 'pilot'
    assert interp.determine_command_type('FORWARD 10') == 'logo'
    assert interp.determine_command_type('LET X = 5') == 'basic'
    assert interp.determine_command_type('10 PRINT "X"') == 'pilot' or interp.determine_command_type('10 PRINT "X"') == 'basic'


def test_parse_line_edge_cases():
    interp = TempleCodeInterpreter()
    assert interp.parse_line('') == (None, '')
    assert interp.parse_line('   ') == (None, '')
    assert interp.parse_line('10 PRINT X') == (10, 'PRINT X')


def test_toggle_breakpoint_and_debug_flags():
    interp = TempleCodeInterpreter()
    assert interp.debug_mode is False
    interp.set_debug_mode(True)
    assert interp.debug_mode is True
    interp.toggle_breakpoint(5)
    assert 5 in interp.breakpoints
    interp.toggle_breakpoint(5)
    assert 5 not in interp.breakpoints


def test_stop_program_and_step_on_empty():
    interp = TempleCodeInterpreter()
    interp.stop_program()
    # step on empty program should not raise
    interp.step()


@pytest.mark.skipif('DISPLAY' not in os.environ, reason='Requires DISPLAY for Tk GUI')
def test_gui_smoke_methods(monkeypatch):
    import tkinter as tk
    from Super_PILOT import TempleCodeII as TempleCodeIDE

    root = tk.Tk()
    # don't show window
    root.withdraw()

    # monkeypatch theme helpers to avoid file IO
    try:
        import tools.theme as theme_mod
        monkeypatch.setattr(theme_mod, 'load_config', lambda: {})
        monkeypatch.setattr(theme_mod, 'save_config', lambda cfg: None)
    except Exception:
        pass

    app = TempleCodeIDE(root)
    # exercise methods that don't require dialogs
    app.setup_theme()
    app.create_menu()
    txt = app.get_help_text()
    assert 'TEMPLECODE' in txt.upper()
    app.load_demo()
    app.load_hello_world()
    app.load_math_demo()
    app.load_quiz_game()
    app.new_file()
    # toggle dark mode back and forth
    app.toggle_dark_mode()
    app.toggle_dark_mode()

    # cleanup
    try:
        root.destroy()
    except Exception:
        pass
