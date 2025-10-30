import os
import unittest

from Super_PILOT import TempleCodeInterpreter


class TestGWBASICCore(unittest.TestCase):
    def run_prog(self, prog):
        out = []
        interp = TempleCodeInterpreter()
        interp.output_widget = None
        interp.on_output.append(lambda s: out.append(str(s)))
        interp.run_program(prog)
        return out

    def test_dim_arrays_and_for(self):
        prog = """10 DIM A(5)
20 FOR I = 0 TO 5
30 A(I)=I*I
40 NEXT I
50 PRINT A(3)
60 END"""
        out = self.run_prog(prog)
        # Expect 9 then Program execution completed
        self.assertIn("9", out)

    def test_def_fn_and_call(self):
        prog = """10 DEF FNS(X)=X*2
20 PRINT FNS(7)
30 END"""
        out = self.run_prog(prog)
        self.assertIn("14", out)

    def test_on_goto_branch(self):
        prog = """10 ON 2 GOTO 200,300,400
90 END
200 PRINT 111: END
300 PRINT 222: END
400 PRINT 333: END"""
        out = self.run_prog(prog)
        self.assertIn("222", out)

    def test_colon_splitting(self):
        prog = """10 PRINT 111: END"""
        out = self.run_prog(prog)
        self.assertIn("111", out)

    def test_line_input_and_print_hash(self):
        import tempfile

        # Use cross-platform temporary directory
        tmp = os.path.join(tempfile.gettempdir(), "templecode_io_test.txt")
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
            prog = f"""10 OPEN \"{tmp}\" FOR OUTPUT AS #1
20 PRINT #1, \"HELLO\"
30 CLOSE #1
40 OPEN \"{tmp}\" FOR INPUT AS #1
50 LINE INPUT #1, A$
60 PRINT A$
70 CLOSE #1
80 END"""
            out = self.run_prog(prog)
            self.assertIn("HELLO", out)
        finally:
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass


if __name__ == "__main__":
    unittest.main()
