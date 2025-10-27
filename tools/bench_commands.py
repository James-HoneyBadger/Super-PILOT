"""Benchmark each SuperPILOT command by calling interpreter command handlers directly.

Usage:
    python tools/bench_commands.py

Produces simple per-command timings (avg microseconds per call).
"""
import time
import contextlib
import io
from pilot import SuperPILOTInterpreter

REPEATS_FAST = 50000
REPEATS_MED = 5000
REPEATS_SLOW = 500

cases = []

# PILOT commands (use execute_pilot_command)
cases.extend([
    ("T:", "T:Hello World", REPEATS_FAST, 'pilot'),
    ("U:", "U:V=123", REPEATS_FAST, 'pilot'),
    ("Y:", "Y:1==1", REPEATS_FAST, 'pilot'),
    ("N:", "N:1==0", REPEATS_FAST, 'pilot'),
    ("J:", "J:NONEXIST", REPEATS_FAST, 'pilot'),
    ("M:", "M:NONEXIST", REPEATS_FAST, 'pilot'),
    ("R:", "R:SUB", REPEATS_FAST, 'pilot'),
    ("C:", "C:", REPEATS_FAST, 'pilot'),
    ("L:", "L:LABEL", REPEATS_FAST, 'pilot'),
    ("A:", "A:INP", REPEATS_MED, 'pilot'),
    ("END", "END", REPEATS_FAST, 'pilot'),
])

# BASIC commands
cases.extend([
    ("LET", "LET A = 123", REPEATS_FAST, 'basic'),
    ("PRINT", "PRINT A", REPEATS_FAST, 'basic'),
    ("INPUT", "INPUT B", REPEATS_MED, 'basic'),
    ("GOTO", "GOTO 10", REPEATS_FAST, 'basic'),
    ("IF", "IF 1==1 THEN PRINT \"OK\"", REPEATS_FAST, 'basic'),
    ("REM", "REM comment", REPEATS_FAST, 'basic'),
    ("FOR", "FOR I = 1 TO 2", REPEATS_SLOW, 'basic'),
    ("NEXT", "NEXT I", REPEATS_SLOW, 'basic'),
])

# LOGO commands
cases.extend([
    ("FORWARD", "FORWARD 10", REPEATS_FAST, 'logo'),
    ("LEFT", "LEFT 90", REPEATS_FAST, 'logo'),
    ("PENUP", "PENUP", REPEATS_FAST, 'logo'),
    ("PENDOWN", "PENDOWN", REPEATS_FAST, 'logo'),
    ("CLEARSCREEN", "CLEARSCREEN", REPEATS_FAST, 'logo'),
    ("SETXY", "SETXY 10 20", REPEATS_FAST, 'logo'),
])

# Expression functions
expr_cases = [
    ("RND", "RND()", REPEATS_FAST),
    ("INT", "INT(3.7)", REPEATS_FAST),
    ("VAL", "VAL(\"12\")", REPEATS_FAST),
    ("UPPER", "UPPER(\"ab\")", REPEATS_FAST),
    ("LOWER", "LOWER(\"AB\")", REPEATS_FAST),
    ("MID", "MID(\"hello\",2,2)", REPEATS_FAST),
]


def bench_case(interp, name, cmd, repeats, kind):
    # warm-up
    if kind == 'pilot':
        fn = interp.execute_pilot_command
    elif kind == 'basic':
        fn = interp.execute_basic_command
    elif kind == 'logo':
        fn = interp.execute_logo_command
    else:
        raise ValueError(kind)

    # Special-case input: avoid blocking
    interp.get_user_input = lambda prompt='': '1'

    # Time the loop (suppress stdout during the timed section so printed
    # output from commands like SETXY or FORWARD doesn't skew timing).
    with contextlib.redirect_stdout(io.StringIO()):
        t0 = time.perf_counter()
        for i in range(repeats):
            fn(cmd)
        t1 = time.perf_counter()
    total = t1 - t0
    avg_us = (total / repeats) * 1e6
    print(f"{name:10s} | repeats={repeats:6d} | total={total:.6f}s | avg={avg_us:.2f}us")


def bench_expr(interp, name, expr, repeats):
    t0 = time.perf_counter()
    for i in range(repeats):
        interp.evaluate_expression(expr)
    t1 = time.perf_counter()
    total = t1 - t0
    avg_us = (total / repeats) * 1e6
    print(f"{name:10s} | repeats={repeats:6d} | total={total:.6f}s | avg={avg_us:.2f}us")


def main():
    print("SuperPILOT command benchmark — running quick microbenchmarks")
    interp = SuperPILOTInterpreter()
    interp.output_widget = None

    print("\n-- PILOT / BASIC / LOGO commands --")
    for name, cmd, repeats, kind in cases:
        bench_case(interp, name, cmd, repeats, kind)

    print("\n-- Expression functions --")
    for name, expr, repeats in expr_cases:
        bench_expr(interp, name, expr, repeats)

    print("\nBenchmark completed")

if __name__ == '__main__':
    main()
