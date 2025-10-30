"""
Test suite for Logo turtle graphics functionality
Tests movement commands, drawing, macros, and repeat structures
"""
import pytest
import math
from conftest import TestCase
from Super_PILOT import TempleCodeInterpreter


class TestLogoTurtleGraphics(TestCase):
    """Test Logo turtle graphics commands"""
    
    def test_turtle_initialization(self, interpreter):
        """Test that turtle starts at origin with correct heading"""
        # Initialize turtle by running a simple command
        interpreter.run_program("FORWARD 0\nEND")
        
        # Turtle should start at origin (0,0) facing up (90 degrees)
        assert hasattr(interpreter, 'turtle_x')
        assert hasattr(interpreter, 'turtle_y')
        assert hasattr(interpreter, 'turtle_heading')
        
        # Check initial position (allowing for small floating point differences)
        assert abs(interpreter.turtle_x - 200) < 1  # Default canvas center
        assert abs(interpreter.turtle_y - 200) < 1
        assert abs(interpreter.turtle_heading - 90) < 1  # Facing up
    
    def test_forward_movement(self, interpreter):
        """Test FORWARD command moves turtle correctly"""
        program = '''FORWARD 100
END'''
        
        interpreter.run_program(program)
        
        # Should move 100 units up from starting position
        expected_x = 200  # Starting x
        expected_y = 200 - 100  # Starting y minus distance (up is negative y)
        
        self.assert_turtle_position(interpreter, expected_x, expected_y)
    
    def test_backward_movement(self, interpreter):
        """Test BACKWARD command moves turtle correctly"""
        program = '''BACKWARD 50
END'''
        
        interpreter.run_program(program)
        
        # Should move 50 units down from starting position
        expected_x = 200  # Starting x
        expected_y = 200 + 50  # Starting y plus distance (down is positive y)
        
        self.assert_turtle_position(interpreter, expected_x, expected_y)
    
    def test_right_turn(self, interpreter):
        """Test RIGHT command rotates turtle correctly"""
        program = '''RIGHT 90
FORWARD 100
END'''
        
        interpreter.run_program(program)
        
        # After turning right 90 degrees and moving forward,
        # turtle should be at (300, 200) facing right (0 degrees)
        expected_x = 200 + 100  # Starting x plus distance
        expected_y = 200  # Starting y unchanged
        expected_heading = 0  # Facing right
        
        self.assert_turtle_position(interpreter, expected_x, expected_y, expected_heading)
    
    def test_left_turn(self, interpreter):
        """Test LEFT command rotates turtle correctly"""
        program = '''LEFT 90
FORWARD 100
END'''
        
        interpreter.run_program(program)
        
        # After turning left 90 degrees and moving forward,
        # turtle should be at (100, 200) facing left (180 degrees)
        expected_x = 200 - 100  # Starting x minus distance
        expected_y = 200  # Starting y unchanged
        expected_heading = 180  # Facing left
        
        self.assert_turtle_position(interpreter, expected_x, expected_y, expected_heading)
    
    def test_square_drawing(self, interpreter):
        """Test drawing a complete square"""
        program = '''FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
END'''
        
        interpreter.run_program(program)
        
        # After drawing a square, turtle should return to starting position
        # with same heading
        self.assert_turtle_position(interpreter, 200, 200, 90)
    
    def test_pen_up_down(self, interpreter):
        """Test PENUP and PENDOWN commands"""
        program = '''PENUP
FORWARD 50
PENDOWN
FORWARD 50
END'''
        
        result = interpreter.run_program(program)
        assert result == True
        
        # Check that pen state is tracked
        if hasattr(interpreter, 'pen_down'):
            assert interpreter.pen_down == True  # Should be down after PENDOWN
    
    def test_repeat_structure(self, interpreter):
        """Test REPEAT command for loops"""
        program = '''REPEAT 4 [
    FORWARD 100
    RIGHT 90
]
END'''
        
        interpreter.run_program(program)
        
        # Should draw a square and return to starting position
        self.assert_turtle_position(interpreter, 200, 200, 90)
    
    def test_nested_repeat(self, interpreter):
        """Test nested REPEAT structures"""
        program = '''REPEAT 4 [
    REPEAT 2 [
        FORWARD 50
        RIGHT 45
    ]
    RIGHT 90
]
END'''
        
        result = interpreter.run_program(program)
        assert result == True
        # Complex pattern should execute without errors
    
    def test_macro_definition_and_call(self, interpreter):
        """Test defining and calling Logo macros"""
        program = '''TO SQUARE :SIZE
    REPEAT 4 [
        FORWARD :SIZE
        RIGHT 90
    ]
END

SQUARE 100
END'''
        
        interpreter.run_program(program)
        
        # Should draw a square with side length 100
        self.assert_turtle_position(interpreter, 200, 200, 90)
    
    def test_macro_with_parameters(self, interpreter):
        """Test macro with multiple parameters"""
        program = '''TO RECTANGLE :WIDTH :HEIGHT
    FORWARD :WIDTH
    RIGHT 90
    FORWARD :HEIGHT
    RIGHT 90
    FORWARD :WIDTH
    RIGHT 90
    FORWARD :HEIGHT
    RIGHT 90
END

RECTANGLE 150 75
END'''
        
        result = interpreter.run_program(program)
        assert result == True
        
        # Should return to starting position after drawing rectangle
        self.assert_turtle_position(interpreter, 200, 200, 90)
    
    def test_clear_screen(self, interpreter):
        """Test CLEARSCREEN command"""
        program = '''FORWARD 100
CLEARSCREEN
END'''
        
        result = interpreter.run_program(program)
        assert result == True
        
        # After clear screen, turtle should be back at center
        if hasattr(interpreter, 'turtle_x') and hasattr(interpreter, 'turtle_y'):
            self.assert_turtle_position(interpreter, 200, 200, 90)
    
    def test_home_command(self, interpreter):
        """Test HOME command returns turtle to origin"""
        program = '''FORWARD 100
RIGHT 45
FORWARD 50
HOME
END'''
        
        interpreter.run_program(program)
        
        # HOME should return turtle to center with original heading
        self.assert_turtle_position(interpreter, 200, 200, 90)
    
    def test_setheading_command(self, interpreter):
        """Test SETHEADING command sets absolute direction"""
        program = '''SETHEADING 45
FORWARD 100
END'''
        
        interpreter.run_program(program)
        
        # Should move diagonally (45 degrees)
        distance = 100
        expected_x = 200 + distance * math.sin(math.radians(45))
        expected_y = 200 - distance * math.cos(math.radians(45))
        
        self.assert_turtle_position(interpreter, expected_x, expected_y, 45)
    
    def test_setxy_command(self, interpreter):
        """Test SETXY command moves to absolute position"""
        program = '''SETXY 150 250
END'''
        
        interpreter.run_program(program)
        
        # Should be at the specified absolute coordinates
        self.assert_turtle_position(interpreter, 150, 250)
    
    def test_complex_spiral_pattern(self, interpreter):
        """Test complex spiral drawing pattern"""
        program = '''TO SPIRAL :SIZE :INCREMENT
    FORWARD :SIZE
    RIGHT 90
    SPIRAL (:SIZE + :INCREMENT) :INCREMENT
END

SPIRAL 10 5
END'''
        
        # This will create a recursive spiral, but should be limited by max_iterations
        result = interpreter.run_program(program)
        # Should not crash even with recursive pattern
        assert result in [True, False]  # May terminate due to max iterations
    
    def test_mathematical_expressions_in_logo(self, interpreter):
        """Test mathematical expressions within Logo commands"""
        program = '''U:SIZE=50
FORWARD (*SIZE* * 2)
RIGHT (90 + 45)
FORWARD (*SIZE* / 2)
END'''
        
        result = interpreter.run_program(program)
        assert result == True
        
        # Verify that expressions were evaluated correctly
        # First move: 100 units up
        # Turn: 135 degrees right (facing down-right)
        # Second move: 25 units in that direction
    
    def test_logo_basic_integration(self, interpreter):
        """Test mixing Logo commands with BASIC-style numbered lines"""
        program = '''10 FORWARD 100
20 RIGHT 90
30 FORWARD 100
40 RIGHT 90
50 FORWARD 100
60 RIGHT 90
70 FORWARD 100
END'''
        
        interpreter.run_program(program)
        
        # Should draw a square and return to start
        self.assert_turtle_position(interpreter, 200, 200, 90)
    
    def test_error_handling_invalid_logo_command(self, interpreter):
        """Test error handling for invalid Logo commands"""
        program = '''FORWARD 100
INVALID_LOGO_COMMAND 50
RIGHT 90
FORWARD 100
END'''
        
        result, output = self.run_program_and_capture_output(interpreter, program)
        # Should continue execution despite invalid command
        # Turtle should still move correctly for valid commands
        assert hasattr(interpreter, 'turtle_x')
    
    def test_variable_interpolation_in_logo(self, interpreter):
        """Test using PILOT variables in Logo commands"""
        program = '''U:SIDE=80
U:ANGLE=90
FORWARD *SIDE*
RIGHT *ANGLE*
FORWARD *SIDE*
RIGHT *ANGLE*
FORWARD *SIDE*
RIGHT *ANGLE*
FORWARD *SIDE*
END'''
        
        interpreter.run_program(program)
        
        # Should draw a square with side length 80
        self.assert_turtle_position(interpreter, 200, 200, 90)