"""Deprecated module: Logo is inlined into TempleCode.

This file remains to avoid import errors. All functionality is provided by
TempleCode's unified executor. Please import and use TempleCode only.
"""

from warnings import warn

# Re-export for compatibility with legacy imports
from .templecode import execute_templecode as execute_logo  # noqa: F401

__all__ = ["execute_logo"]

warn(
    (
        "time_warp.languages.logo is deprecated. TempleCode is unified. "
        "Import from time_warp.languages.templecode instead."
    ),
    DeprecationWarning,
    stacklevel=2,
)

