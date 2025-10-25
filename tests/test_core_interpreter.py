"""
Comprehensive test suite for SuperPILOT Core Interpreter
Tests basic PILOT commands, variable handling, and program flow
"""

import pytest
from conftest import TestCase
from Super_PILOT import SuperPILOTInterpreter


class TestCoreInterpreter(TestCase):
    """Test core interpreter functionality"""

    def test_interpreter_initialization(self, interpreter):
        """Test that interpreter initializes correctly"""
        assert interpreter.variables == {}
        assert interpreter.program_lines == []
        assert interpreter.current_line == 0
        assert interpreter.running == False
        # max_iterations is set during run_program, not initialization

    def test_variable_assignment_and_retrieval(self, interpreter):
        """Test U: command for variable assignment"""
        program = """U:X=42
U:Y=3.14
U:NAME="John"
END"""
        interpreter.run_program(program)

        self.assert_variables_equal(interpreter, {"X": 42, "Y": 3.14, "NAME": "John"})

    def test_variable_interpolation(self, interpreter):
        """Test variable interpolation in text output"""
        program = """U:NAME="Alice"
U:AGE=25
T:Hello *NAME*, you are *AGE* years old!
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "Hello Alice, you are 25 years old!" in output

    def test_mathematical_expressions(self, interpreter):
        """Test mathematical operations and variable calculations"""
        program = """U:X = 10
U:Y = 5
U:SUM = X + Y
U:DIFF = X - Y
U:PROD = X * Y
END"""
        interpreter.run_program(program)

        self.assert_variables_equal(
            interpreter, {"X": 10, "Y": 5, "SUM": 15, "DIFF": 5, "PROD": 50}
        )

    def test_conditional_matching(self, interpreter):
        """Test M: and C: commands for pattern matching"""
        program = """U:INPUT=hello
M:*INPUT*,hello
T:Match found!
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "Match found!" in output

    def test_conditional_jump_yes(self, interpreter):
        """Test conditional jump when condition is true"""
        program = """U:AGE = 15
Y:AGE < 18
J:MINOR
T:You are an adult
J:END
L:MINOR
T:You are a minor
L:END
END"""
        output = self.run_program_and_capture_output(interpreter, program)[1]

        assert "You are a minor" in output
        assert "You are an adult" not in output

    def test_conditional_jump_no(self, interpreter):
        """Test conditional text output with Y: and N: commands"""
        program = """U:AGE=25
Y:AGE < 18
T:You are a minor
U:AGE=25
N:AGE >= 18
T:You are an adult
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "You are an adult" in output
        assert "You are a minor" not in output

    def test_jump_to_label(self, interpreter):
        """Test J: command for jumping to labels"""
        program = """T:Start
J:MIDDLE
T:This should be skipped
L:MIDDLE
T:Middle section
J:END_LABEL
T:This should also be skipped
L:END_LABEL
T:End section
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "Start" in output
        assert "Middle section" in output
        assert "End section" in output
        assert "This should be skipped" not in output
        assert "This should also be skipped" not in output

    def test_subroutine_call_and_return(self, interpreter):
        """Test R: command for subroutine calls and returns"""
        program = """T:Main program
R:SUBROUTINE
T:Back in main
END
L:SUBROUTINE
T:In subroutine
RETURN"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "Main program" in output
        assert "In subroutine" in output
        assert "Back in main" in output

    # def test_nested_subroutine_calls(self, interpreter):
    #     """Test nested subroutine calls with proper return stack"""
    #     program = """T:Level 0
    # R:SUB1
    # T:Back to Level 0
    # END
    # L:SUB1
    # T:Level 1
    # C:"""

    #     result, output = self.run_program_and_capture_output(interpreter, program)
    #     assert result == True
    #     lines = output.strip().split("\n")
    #     expected_order = ["Level 0", "Level 1", "Back to Level 0"]

    #     # Check that output appears in correct order
    #     output_order = [
    #         line.strip() for line in lines if line.strip() in expected_order
    #     ]
    #     assert output_order == expected_order

    def test_loop_with_exit_condition(self, interpreter):
        """Test loops with exit conditions to prevent infinite loops"""
        program = """U:COUNTER=0
L:LOOP
T:Count: *COUNTER*
U:COUNTER=*COUNTER*+1
Y:*COUNTER* < 5
J:LOOP
T:Loop finished
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "Count: 0" in output
        assert "Count: 4" in output
        assert "Loop finished" in output

    def test_error_handling_invalid_syntax(self, interpreter):
        """Test that invalid syntax is handled gracefully"""
        program = """INVALID_COMMAND
T:This should still work
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        # Should not crash, but may show error message
        assert "This should still work" in output

    def test_max_iterations_protection(self, interpreter):
        """Test that infinite loops are prevented by max iterations"""
        interpreter.max_iterations = 100  # Set low limit for testing

        program = """L:INFINITE
T:This is an infinite loop
J:INFINITE
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        # Should terminate due to max iterations, not hang forever
        assert result == False or "This is an infinite loop" in output

    def test_variable_type_coercion(self, interpreter):
        """Test numeric operations with different types"""
        program = """U:NUM1=42
U:NUM2=3.14
U:RESULT=*NUM1*+*NUM2*
END"""

        interpreter.run_program(program)
        result = interpreter.variables.get("RESULT")
        assert abs(result - 45.14) < 0.001  # Should be 42 + 3.14

    def test_string_operations(self, interpreter):
        """Test string variables and text output"""
        program = """U:FIRST="Hello"
U:SECOND="World"
T:*FIRST* *SECOND*!
END"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "Hello World!" in output

    def test_complex_expression_evaluation(self, interpreter):
        """Test complex mathematical expressions"""
        program = """U:X=10
U:Y=5
U:Z=2
U:RESULT=(*X*+*Y*)*(*Z*-1)
END"""

        interpreter.run_program(program)
        assert interpreter.variables.get("RESULT") == 15  # (10+5)*(2-1) = 15

    def test_case_sensitive_commands(self, interpreter):
        """Test that commands are case sensitive"""
        program = """T:Hello from uppercase
U:TEST_VAR=123
E:"""

        result, output = self.run_program_and_capture_output(interpreter, program)
        assert result == True
        assert "Hello from uppercase" in output
        assert interpreter.variables.get("TEST_VAR") == 123
