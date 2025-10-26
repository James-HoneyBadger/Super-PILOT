"""
Core Time Warp Interpreter Engine

This module contains the base classes and interfaces for the Time Warp interpreter system.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any, Union
import re


class InterpreterError(Exception):
    """Base exception for interpreter errors"""

    pass


class LanguageExecutor(ABC):
    """Abstract base class for language-specific executors"""

    def __init__(self, interpreter):
        self.interpreter = interpreter

    @abstractmethod
    def can_execute(self, command: str) -> bool:
        """Check if this executor can handle the given command"""
        pass

    @abstractmethod
    def execute_command(self, command: str) -> str:
        """Execute a command and return the result"""
        pass


class VariableManager:
    """Manages variables and their evaluation"""

    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.user_functions: Dict[str, Dict] = {}

    def set_variable(self, name: str, value: Any) -> None:
        """Set a variable value"""
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """Get a variable value"""
        return self.variables.get(name)

    def has_variable(self, name: str) -> bool:
        """Check if a variable exists"""
        return name in self.variables

    def clear_variables(self) -> None:
        """Clear all variables"""
        self.variables.clear()

    def evaluate_expression(self, expr: str) -> Any:
        """Safely evaluate mathematical expressions with variables"""
        if not isinstance(expr, str):
            return expr

        expr = expr.strip()

        # Reject obviously dangerous expressions
        if any(
            char in expr
            for char in [
                "{",
                "}",
                "[",
                "]",
                "__",
                "import",
                "exec",
                "eval",
                "open",
                "file",
            ]
        ):
            raise InterpreterError("Expression contains forbidden characters")

        # Replace variables
        for var_name, var_value in self.variables.items():
            if isinstance(var_value, str):
                val_repr = f'"{var_value}"'
            else:
                val_repr = str(var_value)
            # Replace *VAR* occurrences first
            expr = expr.replace(f"*{var_name}*", val_repr)

        # Replace bare variable names
        for var_name, var_value in self.variables.items():
            if isinstance(var_value, str):
                val_repr = f'"{var_value}"'
            else:
                val_repr = str(var_value)
            try:
                expr = re.sub(rf"\b{re.escape(var_name)}\b", val_repr, expr)
            except re.error:
                expr = expr.replace(var_name, val_repr)

        try:
            # Allow basic math operations and functions
            allowed_names = {
                "abs": abs,
                "round": round,
                "int": int,
                "float": float,
                "max": max,
                "min": min,
                "len": len,
                "str": str,
                "RND": (lambda *a: __import__("random").random()),
                "INT": int,
                "VAL": lambda x: float(x) if "." in str(x) else int(x),
                "UPPER": lambda x: str(x).upper(),
                "LOWER": lambda x: str(x).lower(),
                "MID": lambda s, start, length: (
                    str(s)[int(start) - 1 : int(start) - 1 + int(length)]
                    if isinstance(s, (str, int, float))
                    else ""
                ),
                # Math functions
                "SIN": __import__("math").sin,
                "COS": __import__("math").cos,
                "TAN": __import__("math").tan,
                "LOG": __import__("math").log,
                "SQR": __import__("math").sqrt,
                "EXP": __import__("math").exp,
                "ATN": __import__("math").atan,
                "SGN": lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
                "ABS": abs,
            }

            safe_dict = {
                "str": str,
                "int": int,
                "float": float,
                "len": len,
                "abs": abs,
                "round": round,
                "max": max,
                "min": min,
            }
            safe_dict.update(allowed_names)

            result = eval(expr, safe_dict)
            return result
        except SyntaxError as e:
            raise InterpreterError(f"Syntax error in expression '{expr}': {e}")
        except Exception as e:
            raise InterpreterError(f"Expression error: {e}")


class ProgramManager:
    """Manages program loading, parsing, and execution flow"""

    def __init__(self):
        self.program_lines: List[Tuple[Optional[int], str]] = []
        self.labels: Dict[str, int] = {}
        self.procedures: Dict[str, Dict] = {}
        self.current_line: int = 0
        self.stack: List[int] = []
        self.for_stack: List[Dict] = []

    def load_program(self, program_text: str) -> bool:
        """Load and parse a program"""
        self.reset()
        lines = program_text.strip().split("\n")

        # Parse lines and collect labels
        for i, line in enumerate(lines):
            line_num, command = self.parse_line(line)
            self.program_lines.append((line_num, command))

            # Collect PILOT labels
            if command and command.startswith("L:"):
                label = command[2:].strip()
                self.labels[label] = i

        return True

    def parse_line(self, line: str) -> Tuple[Optional[int], str]:
        """Parse a program line for line number and command"""
        line = line.strip()
        match = re.match(r"^(\d+)\s+(.*)", line)
        if match:
            line_number, command = match.groups()
            return int(line_number), command.strip()
        return None, line.strip()

    def reset(self) -> None:
        """Reset program state"""
        self.program_lines.clear()
        self.labels.clear()
        self.procedures.clear()
        self.current_line = 0
        self.stack.clear()
        self.for_stack.clear()

    def get_current_command(self) -> Optional[str]:
        """Get the current command to execute"""
        if 0 <= self.current_line < len(self.program_lines):
            _, command = self.program_lines[self.current_line]
            return command
        return None

    def advance_line(self) -> None:
        """Move to the next line"""
        self.current_line += 1

    def jump_to_line(self, line_index: int) -> None:
        """Jump to a specific line index"""
        self.current_line = line_index

    def push_return_address(self, address: int) -> None:
        """Push a return address onto the stack"""
        self.stack.append(address)

    def pop_return_address(self) -> Optional[int]:
        """Pop a return address from the stack"""
        return self.stack.pop() if self.stack else None


class ExecutionContext:
    """Holds the current execution state"""

    def __init__(self):
        self.running = False
        self.debug_mode = False
        self.breakpoints = set()
        self.max_iterations = 10000
        self.match_flag = False
        self._last_match_set = False

    def reset(self):
        """Reset execution state"""
        self.running = False
        self.match_flag = False
        self._last_match_set = False
