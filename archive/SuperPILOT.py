# Compatibility shim for tests and external imports expecting `SuperPILOT`
# Re-export the main implementation from Super_PILOT.py
from Super_PILOT import *  # noqa: F401,F403

# Ensure the MIN_DELTA_TIME_MS constant is available at module scope
try:
    MIN_DELTA_TIME_MS  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    MIN_DELTA_TIME_MS = 1
