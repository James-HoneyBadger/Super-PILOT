"""
Performance and benchmark tests for Time Warp
Tests execution speed, memory usage, and scalability
"""

import pytest
import time
import psutil
import os
from conftest import TestCase
from Time_Warp import TimeWarpInterpreter


class TestPerformanceBenchmarks(TestCase):
    """Performance benchmark tests"""

    @pytest.mark.performance
    @pytest.mark.benchmark(group="interpreter")
    def test_interpreter_startup_time(self, benchmark):
        """Benchmark interpreter initialization time"""

        def setup_interpreter():
            interp = TimeWarpInterpreter()
            interp.output_widget = None
            return interp

        result = benchmark(setup_interpreter)
        assert result is not None

    @pytest.mark.performance
    @pytest.mark.benchmark(group="execution")
    def test_simple_program_execution(self, benchmark, interpreter):
        """Benchmark simple program execution"""
        program = """U:X=10
U:Y=20
U:SUM=*X*+*Y*
T:Result: *SUM*
END"""

        def run_program():
            return interpreter.run_program(program)

        result = benchmark(run_program)
        assert result == True

    @pytest.mark.performance
    @pytest.mark.benchmark(group="execution")
    def test_complex_mathematical_operations(self, benchmark, interpreter):
        """Benchmark complex mathematical computations"""
        program = """U:RESULT=0
U:I=1
L:LOOP
U:RESULT=*RESULT*+(*I**I*)
U:I=*I*+1
C:*I*<=100
Y:J:LOOP
T:Final result: *RESULT*
END"""

        def run_math_program():
            return interpreter.run_program(program)

        result = benchmark(run_math_program)
        assert result == True

    @pytest.mark.performance
    @pytest.mark.benchmark(group="graphics")
    def test_turtle_graphics_performance(self, benchmark, interpreter):
        """Benchmark turtle graphics operations"""
        program = """REPEAT 100 [
    FORWARD 10
    RIGHT 3.6
]
END"""

        def run_graphics():
            return interpreter.run_program(program)

        result = benchmark(run_graphics)
        assert result == True

    @pytest.mark.performance
    @pytest.mark.benchmark(group="variables")
    def test_large_variable_set(self, benchmark, interpreter):
        """Benchmark handling of large variable sets"""

        def create_many_variables():
            program_lines = []
            for i in range(1000):
                program_lines.append(f"U:VAR{i}={i}")
            program_lines.append("END")
            return interpreter.run_program("\n".join(program_lines))

        result = benchmark(create_many_variables)
        assert result == True
        assert len(interpreter.variables) >= 1000

    @pytest.mark.performance
    @pytest.mark.benchmark(group="subroutines")
    def test_deep_subroutine_calls(self, benchmark, interpreter):
        """Benchmark deep nested subroutine calls"""
        program = """R:LEVEL1
T:Completed deep calls
END
L:LEVEL1
R:LEVEL2
RETURN
L:LEVEL2
R:LEVEL3
RETURN
L:LEVEL3
R:LEVEL4
RETURN
L:LEVEL4
R:LEVEL5
RETURN
L:LEVEL5
T:Deep level reached
RETURN"""

        def run_deep_calls():
            return interpreter.run_program(program)

        result = benchmark(run_deep_calls)
        assert result == True

    @pytest.mark.performance
    @pytest.mark.slow
    def test_memory_usage_large_program(self, interpreter):
        """Test memory usage with large programs"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create a large program
        large_program = []
        for i in range(10000):
            large_program.append(f"T:Line {i} with some text content")
        large_program.append("END")

        program_text = "\n".join(large_program)

        # Run the program
        result = interpreter.run_program(program_text)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        assert result == True
        assert memory_increase < 100  # Should not use more than 100MB additional

    @pytest.mark.performance
    @pytest.mark.benchmark(group="parsing")
    def test_program_parsing_speed(self, benchmark, interpreter):
        """Benchmark program parsing performance"""
        # Create a moderately complex program
        program = """T:Starting complex program
U:COUNTER=0
U:TOTAL=0
L:MAIN_LOOP
    U:COUNTER=*COUNTER*+1
    U:TEMP=*COUNTER**COUNTER*
    U:TOTAL=*TOTAL*+*TEMP*
    C:*COUNTER*<50
    Y:J:MAIN_LOOP
T:Processing complete
R:CALCULATE_AVERAGE
T:Final total: *TOTAL*
T:Average: *AVERAGE*
END
L:CALCULATE_AVERAGE
U:AVERAGE=*TOTAL*/50
RETURN"""

        def parse_and_run():
            return interpreter.run_program(program)

        result = benchmark(parse_and_run)
        assert result == True

    @pytest.mark.performance
    @pytest.mark.stress
    def test_stress_many_iterations(self, interpreter):
        """Stress test with many loop iterations"""
        program = """U:COUNT=0
L:STRESS_LOOP
U:COUNT=*COUNT*+1
C:*COUNT*<5000
Y:J:STRESS_LOOP
T:Completed *COUNT* iterations
END"""

        # Increase max_iterations for this stress test
        original_max = interpreter.max_iterations
        interpreter.max_iterations = 50000
        try:
            start_time = time.time()
            result = interpreter.run_program(program)
            end_time = time.time()

            execution_time = end_time - start_time

            assert result == True
            assert interpreter.variables.get("COUNT") == 5000
            assert execution_time < 10.0  # Should complete within 10 seconds
        finally:
            interpreter.max_iterations = original_max

    @pytest.mark.performance
    @pytest.mark.benchmark(group="iot")
    def test_iot_operations_performance(self, benchmark, interpreter):
        """Benchmark IoT operations performance"""
        program = """R:IOT DISCOVER
R:SENSOR COLLECT temperature
R:SENSOR COLLECT humidity
R:IOT DEVICE light_1 ON
R:SMARTHOME RULE "temp > 25" "ac_on"
T:IoT operations complete
END"""

        def run_iot_ops():
            return interpreter.run_program(program)

        result = benchmark(run_iot_ops)
        assert result == True

    @pytest.mark.performance
    @pytest.mark.benchmark(group="robotics")
    def test_robotics_performance(self, benchmark, interpreter):
        """Benchmark robotics operations"""
        program = """R:ROBOT PLAN "complex_path"
R:ROBOT NAVIGATE 100 200
R:ROBOT ARM EXTEND 75
R:ROBOT GRIPPER CLOSE
R:ROBOT VISION DETECT objects
T:Robotics sequence complete
END"""

        def run_robotics():
            return interpreter.run_program(program)

        result = benchmark(run_robotics)
        assert result == True

    @pytest.mark.performance
    @pytest.mark.slow
    def test_concurrent_execution_simulation(self, interpreter):
        """Simulate concurrent program execution"""
        programs = [
            "REPEAT 100 [FORWARD 5\nRIGHT 3.6]\nEND",
            "U:SUM=0\nU:I=1\nL:LOOP\nU:SUM=*SUM*+*I*\nU:I=*I*+1\nC:*I*<=100\nY:J:LOOP\nEND",
            'R:IOT DISCOVER\nR:SENSOR COLLECT temperature\nR:ROBOT PLAN "task"\nEND',
        ]

        start_time = time.time()

        # Run programs sequentially (simulating concurrent load)
        results = []
        for program in programs:
            # Create fresh interpreter for each program
            interp = TimeWarpInterpreter()
            interp.output_widget = None
            result = interp.run_program(program)
            results.append(result)

        end_time = time.time()
        total_time = end_time - start_time

        assert all(results)
        assert total_time < 5.0  # All programs should complete within 5 seconds

    @pytest.mark.performance
    def test_memory_leak_detection(self):
        """Test for memory leaks in repeated interpreter creation"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create and destroy many interpreter instances
        for i in range(100):
            interp = TimeWarpInterpreter()
            interp.output_widget = None
            interp.run_program("T:Test\nEND")
            del interp

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Should not increase memory significantly
        assert memory_increase < 50  # Less than 50MB increase

    @pytest.mark.performance
    @pytest.mark.benchmark(group="evaluation")
    def test_expression_evaluation_performance(self, benchmark, interpreter):
        """Benchmark mathematical expression evaluation"""
        program = """U:A=10
U:B=20
U:C=30
U:RESULT=((*A*+*B*)*(*C*-5)+((*A* * *B*)/(*C*/3)))*2
T:Complex result: *RESULT*
END"""

        def evaluate_expressions():
            return interpreter.run_program(program)

        result = benchmark(evaluate_expressions)
        assert result == True

        # Verify the calculation is correct
        # ((10+20)*(30-5)+((10*20)/(30/3)))*2 = (30*25+(200/10))*2 = (750+20)*2 = 1540
        expected = 1540
        actual = interpreter.variables.get("RESULT")
        assert abs(actual - expected) < 0.001
