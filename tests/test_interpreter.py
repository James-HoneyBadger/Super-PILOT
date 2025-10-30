import unittest
from Super_PILOT import TempleCodeInterpreter, create_demo_program


class InterpreterTests(unittest.TestCase):
    def test_assignments_and_interpolation(self):
        prog = '''U:X=10
U:Y=20
U:SUM=*X*+*Y*
END'''
        interp = TempleCodeInterpreter()
        interp.output_widget = None
        interp.run_program(prog)
        self.assertEqual(interp.variables.get('X'), 10)
        self.assertEqual(interp.variables.get('Y'), 20)
        self.assertEqual(interp.variables.get('SUM'), 30)

    def test_demo_program_runs(self):
        interp = TempleCodeInterpreter()
        interp.output_widget = None
        ok = interp.run_program(create_demo_program())
        self.assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
