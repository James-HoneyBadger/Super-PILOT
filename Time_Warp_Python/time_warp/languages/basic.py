"""Deprecated module: BASIC is inlined into TempleCode.

This file remains to avoid import errors. All functionality is provided by
TempleCode's unified executor. Please import and use TempleCode only.
"""

from warnings import warn

# Re-export for compatibility with legacy imports
from .templecode import execute_templecode as execute_basic  # noqa: F401

__all__ = ["execute_basic"]

warn(
    (
        "time_warp.languages.basic is deprecated. TempleCode is unified. "
        "Import from time_warp.languages.templecode instead."
    ),
    DeprecationWarning,
    stacklevel=2,
)
