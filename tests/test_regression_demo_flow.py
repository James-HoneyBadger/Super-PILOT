import pytest

from Super_PILOT import SuperPILOTInterpreter, create_demo_program


class DummyOut:
    """Simple output collector compatible with the interpreter's output_widget API."""
    def __init__(self):
        self.lines = []

    def insert(self, _index, text):
        # store lines without trailing newline so assertions are easier
        self.lines.append(text.rstrip('\n'))

    def see(self, *a):
        return None

    def get_text(self):
        return '\n'.join(self.lines)


@pytest.fixture
def run_demo():
    """Return a helper that runs the demo with the provided user input value."""

    def _run(value):
        interp = SuperPILOTInterpreter()
        out = DummyOut()
        interp.output_widget = out
        interp.get_user_input = lambda prompt='': str(value)
        interp.run_program(create_demo_program())
        return out.get_text(), interp

    return _run


@pytest.mark.parametrize(
    "value, expected_present, expected_absent, expected_var",
    [
        (54, "Great choice!", "Zero or negative", 54),
        (0, "Zero or negative", "Great choice!", 0),
    ],
)
def test_demo_fav_number(run_demo, value, expected_present, expected_absent, expected_var):
    """Regression test for the demo favorite-number branch selection.

    Verifies that positive numbers take the positive branch and zero/negative
    numbers take the alternate branch, and that the `FAV_NUM` variable is set
    to the numeric value provided.
    """

    out_text, interp = run_demo(value)

    assert expected_present in out_text
    assert expected_absent not in out_text
    assert interp.variables.get('FAV_NUM') == expected_var
