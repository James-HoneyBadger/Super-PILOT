# Changelog

All notable changes to this project will be documented in this file.

## [3.0.2] - 2025-10-28

### New Features

- **Added Logo TO...END procedure definitions**: Full support for Logo-style procedures with parameters
  - Syntax: `TO SQUARE SIZE ... END` defines procedure with parameters
  - Parameters are passed by position: `SQUARE 100` calls with SIZE=100
  - Variables set during procedure execution are scoped and restored after
  - Complements existing DEFINE/CALL syntax with more traditional Logo syntax

### Bug Fixes & Improvements

- **Fixed SETCOLOR command**: Added missing handler for SETCOLOR Logo command
  - Previously only PENCOLOR was recognized, SETCOLOR was ignored despite being in command list
  - Both SETCOLOR and PENCOLOR now work correctly to change pen color
  - Color changes now apply immediately to subsequent drawing operations
- **Fixed turtle graphics coordinate system**: Turtle now starts at logical (0,0) which maps to canvas center
  - Previously turtle started at (200, 200) causing drawings to appear off-screen
  - Graphics now display correctly in the visible canvas area
- **Made Tkinter import optional**: Module now imports successfully in headless environments (fixes `ImportError: libtk8.6.so` on import)
  - Added `TK_AVAILABLE` flag to check GUI availability programmatically
  - GUI components raise clear error messages when Tk is unavailable
  - Headless interpreter usage fully supported without system Tk libraries
- **Enhanced installation documentation**:
  - Added Linux prerequisites section with distro-specific Tk installation commands
  - Documented Arch Linux (ARM64/aarch64) package installation via pacman
  - Added verification steps and headless/CI guidance with Xvfb
- **Improved CLI experience**:
  - Running `Super_PILOT.py` without Tk now shows helpful installation instructions
  - Clear error messages guide users to install system packages
- **Updated requirements.txt**: Added comprehensive comments explaining Tk system dependency

### Developer Experience

- Exported `TK_AVAILABLE` in `__all__` for programmatic Tk availability checks
- Tests and headless automation no longer require Tk installation
- Better separation between GUI and core interpreter functionality

## [3.0.1] - 2025-10-28

### Bug Fixes & Maintenance

- **Fixed version inconsistency**: Synchronized version numbers between VERSION file and package (`3.0.0`)
- **Fixed duplicate import**: Removed duplicate import statement in SuperPILOT.py compatibility shim
- **Fixed test coverage**: Updated test runner to use correct module name (`Super_PILOT`) for coverage reporting
- **Cleaned up TODO comments**: Updated module extraction comments to reflect current architecture
- **Added basic requirements.txt**: Added minimal requirements file for end users (separate from dev requirements)
- **Updated installation instructions**: README now shows correct installation steps with both basic and dev requirements
- **Enhanced documentation**: Added descriptive comments to core package placeholders

### Project Structure Improvements

- Constants (`MIN_DELTA_TIME_MS`, `MAX_DELTA_TIME_MS`) properly centralized in templecode module
- Core and languages package directories documented for future modular architecture
- .gitignore already comprehensive for Python projects

## [3.0.0] - 2025-10-06

### Interpreter & Language Core

- Conditional jump semantics stabilized: `J:` consumes sentinel after `Y:` / `N:`.
- Extended compute command: `C:VAR=EXPR` assigns evaluated expression.
- Safer variable interpolation (word-boundary + `*VAR*`).
- Nested `REPEAT` implementation with guarded expansion.
- Macro system: `DEFINE NAME [ ... ]` + `CALL NAME` (recursion protection & depth limit).
- Performance profiling (`PROFILE ON|OFF|RESET|REPORT`).

### Turtle / Logo Enhancements

- Centered canvas coordinate system with auto-pan & scroll expansion.
- Auto color cycling per new drawn shape (pen-up → pen-down transition).
- New commands: `COLOR`, `TRACE`, `KEEP_CANVAS`, `CENTER`, `PENSTYLE`, `DEBUGLINES`, `FIT`, aliases (`SETCOLOR/SETCOLOUR`, `SETPENSIZE`).
- Pen style customization (`PENSTYLE solid|dashed|dotted`).
- Start-of-shape markers for orientation.
- Line metadata capture (coords, width, color, style) accessible via `DEBUGLINES`.

### UI / IDE Improvements

- Output panel context menu: Copy / Copy All / Clear.
- Turtle menu: trace & canvas preservation toggles, manual clear.
- Theme accent & dark/light switching.
- Extended syntax highlighting & auto-complete for new Logo & profiler commands.
- Reduced duplicate completion logs.

### Debug & Diagnostics

- TRACE mode outputs movement, heading, pen state after Logo actions.
- `PROFILE REPORT` provides per-command counts, avg, max, total time.
- `DEBUGLINES` surfaces early geometry metadata for first N segments.

### Quality & Housekeeping

- Refactored turtle initialization guard to avoid accidental re-init / wiping lines mid-run.
- Added defensive background redraw (`draw_turtle_background`) to eliminate missing attribute warnings.
- Scrollregion and viewport logic reduce user confusion about off-screen shapes.

### Known Limitations / Deferred

- No polygon fill / export-to-image command (planned >3.0.0).
- Expression evaluator still uses constrained `eval` (plan hardening pass).
- No persisted user settings yet (trace, keep-canvas, theme, profiling preference).
- No ZOOM / BOUNDS commands yet (only FIT / CENTER).

## [Unreleased]

- (Reserved for upcoming patches after 3.0.0 release.)

## Previous

- Initial project files.
