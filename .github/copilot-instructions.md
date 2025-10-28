# SuperPILOT — Copilot instructions

This file contains concise, actionable guidance for an AI coding agent working on the SuperPILOT codebase.

1) Big picture (what to know first)
- **Single entrypoint**: `SuperPILOT.py` is the main IDE with embedded interpreter. `pilot.py` has been archived.
- **Core interpreter**: `SuperPILOTInterpreter` class (lines 376-2750) in `SuperPILOT.py` loads program text into `program_lines` and executes by index. Labels collect during `load_program()`.
- **Three languages**: PILOT (`T:`, `A:`, `U:`), BASIC (`LET`, `PRINT`, `GOTO`), Logo (`FORWARD`, `RIGHT`). Language detection in `determine_command_type()`.
- **Advanced features**: Full templecode integration (particles, tweens, timers), hardware integration (Arduino/RPi/sensors), turtle graphics with macros.
- **Phase 1-5 complete**: Professional IDE with breakpoints, watches, performance monitoring, syntax highlighting, minimap, and auto-save. See `COMPLETE_PHASES_1_5.md`.

2) Key files & symbols to reference
- `SuperPILOT.py` — SuperPILOTInterpreter, SuperPILOTII IDE (5785 lines), hardware controllers, templecode systems, Phase 1-5 features
- `templecode.py` — Original templecode engine (fully integrated into SuperPILOT.py)
- `hardware_demo.spt` — Example program showing hardware integration
- `tests/test_interpreter.py` — Core interpreter tests (278 tests, all passing)
- `Square.pil` — Numbered BASIC/Logo example program
- `COMPLETE_PHASES_1_5.md` — Master documentation for all IDE enhancements
- `phase5_demo.spt` — Demo of minimap and auto-save features

3) Project-specific conventions and gotchas (use these when changing behavior)
- **Variable interpolation**: Use `*VAR*` in text output. `interpolate_text()` replaces with values from `interpreter.variables`.
- **Labels vs line numbers**: PILOT labels (`L:NAME`) map to 0-based line indices. BASIC line numbers (`10 PRINT ...`) stored as `(line_num, command)` tuples.
- **Conditional jumps**: `Y:` and `N:` set `match_flag` and `_last_match_set` sentinel. Following `T:` or `J:` consume the sentinel for conditional behavior.
- **Expression evaluation**: `evaluate_expression()` uses constrained eval with allowed functions (`RND`, `INT`, `MID`, etc). Naive string replacement before eval - avoid substring collisions.
- **Hardware integration**: All hardware classes have simulation modes. Use try-except for optional imports (RPi.GPIO, pyserial).
- **Max iterations**: `run_program()` stops at 10000 iterations. Hardware/templecode systems update each iteration with delta time.
- **Cross-platform compatibility**: Hardware modules (RPi.GPIO) use importlib.util.find_spec() with error handling for graceful fallbacks.

4) How to run & quick developer workflows
- **Run SuperPILOT IDE**: `python3 SuperPILOT.py` (requires Pillow: `pip install pillow`)
- **Run tests**: `python -m pytest tests/` (or `pytest` from project root)
- **Headless interpreter**: 
  ```python
  from SuperPILOT import SuperPILOTInterpreter, create_demo_program
  interp = SuperPILOTInterpreter()
  interp.run_program(create_demo_program())
  ```
- **Install dependencies**: `pip install -r requirements-dev.txt`
- **Hardware testing**: Use `hardware_demo.spt` to test Arduino/RPi integration with simulation fallbacks

5) When editing behavior, update these hotspots
- **Changing parsing rules**: update `parse_line()` and verify `GOTO` search and label mapping (`load_program()`).
- **Adding expression functions**: update `evaluate_expression()` allowed_names and ensure safe_dict remains restrictive.
- **Adding new PILOT commands**: modify `execute_pilot_command()` and update the IDE help text in `get_help_text()` inside `SuperPILOTII` (in `SuperPILOT.py`).
- **Changing UI debugger behavior**: sync `SuperPILOT.py`'s `AdvancedDebugger` with `SuperPILOTInterpreter` if you intend breakpoints to actually pause interpreter execution.
- **Hardware integration**: Add new hardware classes following the simulation pattern (see `ArduinoController`, `RPiController`).
- **Phase 5 IDE features**: Minimap (lines 3683-3697, 5530-5595), Auto-save (lines 3487-3497, 5597-5685). All UI updates via `root.after()` for thread safety.

6) Examples to cite in patches
- **PILOT output with variable interpolation**: `T:Sum of X and Y is *SUM*` (see `create_demo_program()` in `SuperPILOT.py`).
- **Label / jump pattern**: `L:LOOP` then `J:LOOP` uses `labels['LOOP']` which stores the zero-based program index (see `load_program()` and label collection loop).
- **Numbered BASIC example**: `Square.pil` uses `10 LET X = 100` and `30 FORWARD X` — `parse_line()` expects numeric prefix when present.
- **Hardware integration**: `R: ARDUINO CONNECT /dev/ttyUSB0 9600` and `R: RPI PIN 18 OUTPUT` (see `hardware_demo.spt`).

7) Tests & safety checks an AI should add when changing code
- **Unit test idea**: import `SuperPILOTInterpreter`, run a short program that uses `U:, T:, J:, M:` and assert expected `variables` and captured output.
- **Remember to test**: variable name collisions in expression replacement, label resolution for both labeled and numbered programs, and max_iterations behavior for loops.

8) Quick triage checklist for PRs
- **Run both GUIs** (`pilot.py` and `SuperPILOT.py`) to ensure no UI imports break the process.
- **`pip3 install pillow`** and have `tk` available in CI runners for UI smoke tests, or mock GUI parts when running headless tests.
- **If you change eval behaviour**, add tests that exercise `RND()`, `INT()`, `MID()` and a string interpolation case.

If anything above is unclear or you want more detail (example unit tests, a helper test runner, or synchronization of the two debugger implementations), tell me which area you want expanded and I'll iterate.
