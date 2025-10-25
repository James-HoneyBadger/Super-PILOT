# Time Warp

CI: ![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)

Quick start

Install dev requirements:

```bash
python -m pip install -r requirements-dev.txt
```

Run tests:

```bash
python -m pytest -q
```

Run the simple IDE:

```bash
python pilot.py
```


![CI](https://github.com/James-HoneyBadger/Time_Warp/actions/workflows/ci.yml/badge.svg?branch=main)

## Recent changes and semantics

- Conditional jump semantics: `J:label` now behaves as a conditional jump when it immediately follows a `Y:` or `N:` command (it consumes the match sentinel).

  Example:

  ```text
  Y:*COUNT* > 5
  J:END_LOOP
  ```

- `T:` and `MT:` interpolation consolidated into a helper for consistent evaluation of `*VAR*` and `*expr*` tokens.

- `N:` currently acts as a conditional test that sets the match flag when its condition is TRUE (this aligns with demo programs). `Y:` and `N:` both set the `_last_match_set` sentinel which consumer commands may use.

## Version 3 Highlights (3.0.0)

Turtle / Logo Extensions:

- New commands: `COLOR`, `TRACE`, `KEEP_CANVAS`, `CENTER`, `PENSTYLE`, `DEBUGLINES`, `FIT`, aliases (`SETCOLOR/SETCOLOUR`, `SETPENSIZE`).
- Pen style customization: `PENSTYLE solid|dashed|dotted` (teaching different stroke semantics).
- Auto color cycle per shape (each PENUP→PENDOWN transition advances palette).
- Pen-down start markers (small dots) + optional tracing (movement, heading, pen state).
- Auto-pan and dynamic scrollregion (shapes no longer appear to “disappear” off canvas).
- Canvas preservation toggle via command or Turtle menu.
- Geometry inspection: `DEBUGLINES` prints first N line segments & metadata; `FIT` recenters viewport to drawing bounds.

Interpreter / Core:

- Conditional jump sentinel consumption (`Y:`/`N:` + subsequent `J:` / `T:` logic stabilized).
- Compute assignment form: `C:VAR=EXPR`.
- Nested `REPEAT` loops: `REPEAT 3 [ REPEAT 2 [ FORWARD 50 RIGHT 90 ] LEFT 45 ]`.
- Macro system: `DEFINE STAR [ REPEAT 5 [ FORWARD 80 RIGHT 144 ] ]` then `CALL STAR`.
- Performance profiling: `PROFILE ON`, run program, `PROFILE REPORT` (per-command counts, avg, max, total ms).
- Style-aware line metadata tracked for debugging & future analytics.

IDE / UX:

- Output pane context menu (Copy / Copy All / Clear).
- Dedicated Turtle menu: Trace toggle, Preserve Canvas, Clear.
- Accent theme switching + dark/light mode.
- Auto-completion & syntax highlighting extended for: `DEFINE`, `CALL`, `REPEAT` (nested), `PENSTYLE`, `DEBUGLINES`, `FIT`, `PROFILE`.

## Roadmap (Planned >3.0.0)

- Polygon fill & EXPORT (PNG/SVG) commands.
- Settings persistence (trace / keep-canvas / last theme, profiling preference).
- BOUNDS and ZOOM/ZOOMRESET viewport helpers.
- FILL mode or SHAPE capture API for teaching geometry.
- Sandboxed expression evaluator refactor (remove eval).
- Live variable watch + time-travel execution (stretch goal).

## Running tests

From project root:

```bash
PYTHONPATH=. pytest -q
```

If you want me to open a pull request for these changes, tell me the target
branch (default `main`) and whether to create a descriptive PR title and body.
