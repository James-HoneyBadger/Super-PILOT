"""Languages package for Time Warp IDE."""

from .pilot import execute_pilot
from .basic import execute_basic
from .logo import execute_logo

__all__ = [
    'execute_pilot',
    'execute_basic',
    'execute_logo',
]
