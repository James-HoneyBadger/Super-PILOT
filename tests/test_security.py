"""
Security and safety tests for SuperPILOT
Tests for code injection, eval security, and safe execution
"""

import pytest
import os
import tempfile
from conftest import TestCase
from Super_PILOT import SuperPILOTInterpreter


class TestSecuritySafety(TestCase):
    """Security and safety test suite"""

    @pytest.mark.security
    def test_eval_security_basic(self, interpreter):
        """Test that eval() is properly secured"""
        # Try to execute potentially dangerous code
        dangerous_program = """U:DANGER=__import__('os').system('echo "DANGER"')
T:Danger result: *DANGER*
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, dangerous_program
        )

        # Should not execute system commands
        assert "DANGER" not in output or result == False

    @pytest.mark.security
    def test_file_system_access_prevention(self, interpreter):
        """Test that file system access is prevented"""
        # Try to access files through eval
        file_access_program = """U:SECRET=open('/etc/passwd', 'r').read()
T:Secret: *SECRET*
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, file_access_program
        )

        # Should not be able to read system files
        assert "root:" not in output

    @pytest.mark.security
    def test_import_restrictions(self, interpreter):
        """Test that dangerous imports are restricted"""
        import_program = """U:SYS=__import__('sys')
U:OS=__import__('os')
U:SUBPROCESS=__import__('subprocess')
T:Imports: *SYS* *OS* *SUBPROCESS*
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, import_program
        )

        # Should not successfully import dangerous modules
        assert "module" not in output.lower()

    @pytest.mark.security
    def test_code_injection_prevention(self, interpreter):
        """Test prevention of code injection attacks"""
        # Try to inject Python code through variable names
        injection_program = """U:exec("print('INJECTED')")=42
T:Variable value: *exec("print('INJECTED')")*
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, injection_program
        )

        # Should not execute injected code
        assert "INJECTED" not in output

    @pytest.mark.security
    def test_recursion_limit_protection(self, interpreter):
        """Test protection against stack overflow from recursion"""
        # Create deeply recursive program
        recursive_program = """R:RECURSIVE
END
L:RECURSIVE
T:Recursion level
R:RECURSIVE
RETURN"""

        # Should not crash with stack overflow
        result = interpreter.run_program(recursive_program)

        # May succeed or fail, but should not crash the process
        assert result in [True, False]

    @pytest.mark.security
    def test_infinite_loop_protection(self, interpreter):
        """Test protection against infinite loops"""
        # Set low iteration limit for testing
        original_limit = interpreter.max_iterations
        interpreter.max_iterations = 1000

        try:
            infinite_program = """L:INFINITE
T:This loops forever
J:INFINITE
END"""

            result = interpreter.run_program(infinite_program)

            # Should terminate due to iteration limit
            assert result == False
        finally:
            interpreter.max_iterations = original_limit

    @pytest.mark.security
    def test_memory_exhaustion_protection(self, interpreter):
        """Test protection against memory exhaustion"""
        # Try to create very large variables
        memory_program = """U:HUGE_STRING="A" * 10000000
T:String length: *len(HUGE_STRING)*
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, memory_program
        )

        # Should handle large strings safely
        # (may succeed or fail, but shouldn't crash)
        assert result in [True, False]

    @pytest.mark.security
    def test_variable_name_sanitization(self, interpreter):
        """Test that variable names are properly sanitized"""
        # Try special characters and Python keywords
        special_names = [
            "__import__",
            "__builtins__",
            "exec",
            "eval",
            "globals",
            "locals",
        ]

        for name in special_names:
            program = f"""U:{name}=42
T:Value: *{name}*
END"""

            result, output = self.run_program_and_capture_output(interpreter, program)

            # Should either work safely or be rejected
            if result:
                assert "42" in output  # If accepted, should work normally

    @pytest.mark.security
    def test_expression_parsing_safety(self, interpreter):
        """Test that expression parsing is safe from injection"""
        # Try to inject code through mathematical expressions
        injection_expressions = [
            '__import__("os").system("echo test")',
            "exec(\"print('HACKED')\")",
            'eval("1+1")',
            'open("/etc/passwd").read()',
        ]

        for expr in injection_expressions:
            program = f"""U:RESULT={expr}
T:Expression result: *RESULT*
END"""

            result, output = self.run_program_and_capture_output(interpreter, program)

            # Should not execute dangerous operations
            assert "HACKED" not in output
            assert "test" not in output or result == False

    @pytest.mark.security
    def test_safe_function_whitelist(self, interpreter):
        """Test that only safe functions are available in expressions"""
        # Test allowed math functions
        safe_program = """U:A=10
U:B=RND(100)
U:C=INT(*A*/3)
U:D=ABS(-5)
T:Safe functions: *A* *B* *C* *D*
END"""

        result, output = self.run_program_and_capture_output(interpreter, safe_program)
        assert result == True

        # Test that dangerous functions are not available
        dangerous_program = """U:DANGER=exec("print('BAD')")
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, dangerous_program
        )
        assert "BAD" not in output

    @pytest.mark.security
    def test_input_validation(self, interpreter):
        """Test input validation and sanitization"""
        # Test various potentially dangerous inputs
        dangerous_inputs = [
            "'; DROP TABLE users; --",
            "<script>alert('XSS')</script>",
            "$(rm -rf /)",
            "| cat /etc/passwd",
            "&& shutdown -h now",
        ]

        for dangerous_input in dangerous_inputs:
            # Simulate user input in a program
            program = f"""T:Enter value:
U:INPUT={dangerous_input}
T:You entered: *INPUT*
END"""

            result, output = self.run_program_and_capture_output(interpreter, program)

            # Should handle dangerous input safely
            assert result == True
            # Input should be escaped or sanitized in output
            assert dangerous_input in output  # Should display safely

    @pytest.mark.security
    def test_resource_limit_enforcement(self, interpreter):
        """Test that resource limits are enforced"""
        # Test program execution time limits
        long_program = """U:I=0
L:LONG_LOOP
U:I=*I*+1
C:*I*<100000
Y:J:LONG_LOOP
T:Completed long operation
END"""

        import time

        start_time = time.time()
        result = interpreter.run_program(long_program)
        end_time = time.time()

        execution_time = end_time - start_time

        # Should complete within reasonable time or be terminated
        assert execution_time < 30.0  # Max 30 seconds

    @pytest.mark.security
    def test_environment_isolation(self, interpreter):
        """Test that interpreter runs in isolated environment"""
        # Try to access global environment variables
        env_program = """U:PATH=__import__('os').environ.get('PATH', 'NOT_FOUND')
T:PATH: *PATH*
END"""

        result, output = self.run_program_and_capture_output(interpreter, env_program)

        # Should not be able to access environment variables
        assert "NOT_FOUND" in output or "/bin" not in output

    @pytest.mark.security
    def test_network_access_prevention(self, interpreter):
        """Test that network access is prevented"""
        network_program = """U:RESPONSE=__import__('urllib.request').urlopen('http://example.com').read()
T:Response: *RESPONSE*
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, network_program
        )

        # Should not be able to make network requests
        assert "Example Domain" not in output

    @pytest.mark.security
    def test_safe_error_handling(self, interpreter):
        """Test that errors don't leak sensitive information"""
        # Create program with intentional error
        error_program = """U:RESULT=1/0
T:Result: *RESULT*
END"""

        result, output = self.run_program_and_capture_output(interpreter, error_program)

        # Should handle division by zero gracefully
        # Error messages should not contain sensitive paths or info
        if "Error" in output or "Exception" in output:
            assert "/home/" not in output  # No file paths
            assert "password" not in output.lower()  # No sensitive keywords

    @pytest.mark.security
    def test_hardware_command_safety(self, interpreter):
        """Test that hardware commands are safe in simulation mode"""
        # All hardware should be in simulation mode by default
        hardware_program = """R:ARDUINO CONNECT /dev/ttyUSB0 9600
R:RPI PIN 18 OUTPUT
R:RPI PIN 18 HIGH
R:SENSOR COLLECT temperature
T:Hardware operations complete
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, hardware_program
        )

        # Should complete successfully in simulation mode
        assert result == True
        assert "Hardware operations complete" in output

        # Verify simulation mode is active
        assert interpreter.arduino_controller.simulation_mode == True
        assert interpreter.rpi_controller.simulation_mode == True

    @pytest.mark.security
    def test_data_sanitization(self, interpreter):
        """Test that data is properly sanitized before processing"""
        # Test with various control characters and special sequences
        special_data = [
            "\x00\x01\x02",  # Control characters
            "\n\r\t",  # Whitespace
            "\\x41\\x42",  # Escape sequences
            "\u0000\u001f",  # Unicode control characters
        ]

        for data in special_data:
            program = f"""U:DATA={repr(data)}
T:Data: *DATA*
END"""

            result, output = self.run_program_and_capture_output(interpreter, program)

            # Should handle special data safely
            assert result == True

    @pytest.mark.security
    def test_template_injection_prevention(self, interpreter):
        """Test prevention of template injection attacks"""
        # Try to inject code through variable interpolation
        injection_program = """U:NAME={{7*7}}
T:Hello *NAME*!
END"""

        result, output = self.run_program_and_capture_output(
            interpreter, injection_program
        )

        # Should not evaluate template expressions
        assert result == True
        assert "49" not in output  # Should not calculate 7*7
        assert "{{7*7}}" in output  # Should display literally
