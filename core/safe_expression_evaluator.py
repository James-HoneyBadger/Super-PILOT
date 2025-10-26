"""
Safe Expression Evaluator for Time Warp IDE

This module provides secure expression evaluation using AST parsing
instead of eval(). It supports mathematical operations, function calls,
and variable access while preventing code injection and other security
vulnerabilities.
"""

import ast
import math
import random
from typing import Any


class SafeExpressionEvaluator:
    """
    Secure expression evaluator using AST parsing.

    Supports:
    - Basic arithmetic operations (+, -, *, /, //, %, **)
    - Comparison operations (==, !=, <, <=, >, >=)
    - Logical operations (and, or, not)
    - Function calls with whitelisted functions
    - Variable access (variables must be pre-substituted)
    - String operations and literals
    - Numeric literals (int, float)
    """

    # Whitelisted functions and their implementations
    ALLOWED_FUNCTIONS = {
        # Basic functions
        "abs": abs,
        "round": round,
        "int": int,
        "float": float,
        "max": max,
        "min": min,
        "len": len,
        "str": str,
        # BASIC-style functions
        "RND": lambda *a: random.random(),
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
        "SIN": math.sin,
        "COS": math.cos,
        "TAN": math.tan,
        "LOG": math.log,
        "SQR": math.sqrt,
        "EXP": math.exp,
        "ATN": math.atan,
        "SGN": lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
        "ABS": abs,
    }

    # Allowed AST node types
    ALLOWED_NODES = {
        # Literals
        ast.Constant,  # Python 3.8+
        # Variables and names
        ast.Name,
        # Operations
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,  # and, or operations
        ast.Compare,
        # Function calls
        ast.Call,
        # Expression containers
        ast.Expression,
        ast.Module,
        # Context nodes
        ast.Load,
        ast.Store,
        ast.Del,
    }

    # Allowed operators
    ALLOWED_BINOP_OPERATORS = {
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
    }

    ALLOWED_UNARYOP_OPERATORS = {
        ast.UAdd,
        ast.USub,
        ast.Not,
    }

    ALLOWED_COMPARE_OPERATORS = {
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
    }

    ALLOWED_BOOLOP_OPERATORS = {
        ast.And,
        ast.Or,
    }

    def __init__(self):
        """Initialize the evaluator with allowed functions."""
        self.functions = self.ALLOWED_FUNCTIONS.copy()

    def evaluate(self, expression: str) -> Any:
        """
        Safely evaluate an expression.

        Args:
            expression: The expression string to evaluate

        Returns:
            The result of the evaluation

        Raises:
            ValueError: If the expression contains forbidden operations
            SyntaxError: If the expression has invalid syntax
        """
        if not isinstance(expression, str):
            return expression

        expression = expression.strip()
        if not expression:
            raise ValueError("Empty expression")

        try:
            # Parse the expression into an AST
            tree = ast.parse(expression, mode="eval")

            # Validate the AST for security
            self._validate_ast(tree)

            # Evaluate the expression
            return self._evaluate_ast(tree.body)

        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in expression '{expression}': {e}")
        except Exception as e:
            raise ValueError(f"Expression evaluation error: {e}")

    def _validate_ast(self, node: ast.AST) -> None:
        """
        Validate that the AST contains only allowed operations.

        Args:
            node: The AST node to validate

        Raises:
            ValueError: If forbidden operations are found
        """
        for child in ast.walk(node):
            # Skip operator objects - they are validated in their parent nodes
            if isinstance(child, (ast.operator, ast.unaryop, ast.cmpop, ast.boolop)):
                continue

            if isinstance(child, ast.AST) and type(child) not in self.ALLOWED_NODES:
                raise ValueError(f"Forbidden operation: {type(child).__name__}")

            # Additional validation for specific node types
            if isinstance(child, ast.Call):
                self._validate_call(child)
            elif isinstance(child, ast.BinOp):
                if type(child.op) not in self.ALLOWED_BINOP_OPERATORS:
                    raise ValueError(
                        f"Forbidden binary operator: {type(child.op).__name__}"
                    )
            elif isinstance(child, ast.UnaryOp):
                if type(child.op) not in self.ALLOWED_UNARYOP_OPERATORS:
                    raise ValueError(
                        f"Forbidden unary operator: {type(child.op).__name__}"
                    )
            elif isinstance(child, ast.BoolOp):
                if type(child.op) not in self.ALLOWED_BOOLOP_OPERATORS:
                    raise ValueError(
                        f"Forbidden boolean operator: {type(child.op).__name__}"
                    )
            elif isinstance(child, ast.Compare):
                for op in child.ops:
                    if type(op) not in self.ALLOWED_COMPARE_OPERATORS:
                        raise ValueError(
                            f"Forbidden comparison operator: {type(op).__name__}"
                        )

    def _validate_call(self, node: ast.Call) -> None:
        """
        Validate function calls.

        Args:
            node: The Call AST node

        Raises:
            ValueError: If the function is not allowed
        """
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")

        func_name = node.func.id
        if func_name not in self.functions:
            raise ValueError(f"Forbidden function: {func_name}")

    def _evaluate_ast(self, node: ast.AST) -> Any:
        """
        Evaluate an AST node.

        Args:
            node: The AST node to evaluate

        Returns:
            The result of evaluation
        """
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Name):
            # Variables should have been substituted by the caller
            raise ValueError(f"Undefined variable: {node.id}")
        elif isinstance(node, ast.BinOp):
            left = self._evaluate_ast(node.left)
            right = self._evaluate_ast(node.right)
            return self._apply_binop(node.op, left, right)
        elif isinstance(node, ast.BoolOp):
            values = [self._evaluate_ast(value) for value in node.values]
            return self._apply_boolop(node.op, values)
        elif isinstance(node, ast.UnaryOp):
            operand = self._evaluate_ast(node.operand)
            return self._apply_unaryop(node.op, operand)
        elif isinstance(node, ast.Compare):
            left = self._evaluate_ast(node.left)
            comparators = [self._evaluate_ast(comp) for comp in node.comparators]
            return self._apply_compare(left, node.ops, comparators)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function names are allowed")
            func_name = node.func.id
            args = [self._evaluate_ast(arg) for arg in node.args]
            kwargs = {kw.arg: self._evaluate_ast(kw.value) for kw in node.keywords}
            return self._call_function(func_name, args, kwargs)
        else:
            raise ValueError(f"Unsupported AST node: {type(node).__name__}")

    def _apply_binop(self, op: ast.operator, left: Any, right: Any) -> Any:
        """Apply a binary operation."""
        match op:
            case ast.Add():
                return left + right
            case ast.Sub():
                return left - right
            case ast.Mult():
                return left * right
            case ast.Div():
                return left / right
            case ast.FloorDiv():
                return left // right
            case ast.Mod():
                return left % right
            case ast.Pow():
                return left**right
            case _:
                raise ValueError(f"Unsupported binop: {type(op).__name__}")

    def _apply_boolop(self, op: ast.boolop, values: list) -> bool:
        """Apply a boolean operation."""
        if isinstance(op, ast.And):
            # All values must be truthy
            return all(values)
        elif isinstance(op, ast.Or):
            # At least one value must be truthy
            return any(values)
        else:
            raise ValueError(f"Unsupported boolean operator: {type(op).__name__}")

    def _apply_unaryop(self, op: ast.unaryop, operand: Any) -> Any:
        """Apply a unary operation."""
        if isinstance(op, ast.UAdd):
            return +operand
        elif isinstance(op, ast.USub):
            return -operand
        elif isinstance(op, ast.Not):
            return not operand
        else:
            raise ValueError(f"Unsupported unary operator: {type(op).__name__}")

    def _apply_compare(self, left: Any, ops: list, comparators: list) -> bool:
        """Apply comparison operations."""
        result = True
        current_left = left

        for op, right in zip(ops, comparators):
            if isinstance(op, ast.Eq):
                result = result and (current_left == right)
            elif isinstance(op, ast.NotEq):
                result = result and (current_left != right)
            elif isinstance(op, ast.Lt):
                result = result and (current_left < right)
            elif isinstance(op, ast.LtE):
                result = result and (current_left <= right)
            elif isinstance(op, ast.Gt):
                result = result and (current_left > right)
            elif isinstance(op, ast.GtE):
                result = result and (current_left >= right)
            else:
                raise ValueError(
                    f"Unsupported comparison operator: {type(op).__name__}"
                )
            current_left = right

        return result

    def _call_function(self, func_name: str, args: list, kwargs: dict) -> Any:
        """Call a whitelisted function."""
        if func_name not in self.functions:
            raise ValueError(f"Unknown function: {func_name}")

        func = self.functions[func_name]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Function {func_name} error: {e}")


# Global evaluator instance
_evaluator = SafeExpressionEvaluator()


def safe_eval(expression: str, globals_dict: dict[str, Any] | None = None) -> Any:
    """
    Safely evaluate an expression using AST parsing.

    This is a convenience function that uses a global evaluator instance.

    Args:
        expression: The expression string to evaluate
        globals_dict: Optional dictionary of additional allowed globals

    Returns:
        The result of the evaluation

    Raises:
        ValueError: If the expression contains forbidden operations
        SyntaxError: If the expression has invalid syntax
    """
    if globals_dict:
        # Create a temporary evaluator with additional globals
        temp_evaluator = SafeExpressionEvaluator()
        temp_evaluator.functions.update(globals_dict)
        return temp_evaluator.evaluate(expression)
    else:
        return _evaluator.evaluate(expression)
