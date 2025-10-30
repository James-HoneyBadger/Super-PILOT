# A: Command Thread-Safety Fix

## Problem
The `A:` (Accept input) command was not working in the IDE because it called `simpledialog.askstring()` from a background thread. Tkinter GUI operations must run on the main thread.

## Solution
Implemented thread-safe input mechanism using the same pattern as the graphics queue:

1. **Detection**: `get_user_input()` detects when running in a background thread using `threading.current_thread()`
2. **Routing**: When in background thread with IDE attached, routes input request through `_ide_input_request` callback
3. **Synchronization**: IDE's `_request_user_input()` schedules dialog on main thread via `root.after(0, ...)` and blocks interpreter thread using `threading.Event()` until user responds
4. **Timeout**: 5-minute timeout prevents indefinite blocking

## Changes Made

### TempleCodeInterpreter (lines 883-906)
- Modified `get_user_input()` to detect threading context
- Routes GUI input requests through `_ide_input_request` callback when in background thread
- Maintains backward compatibility with console mode and main-thread execution

### TempleCodeII IDE (lines 4118-4144)
- Added `_request_user_input(prompt)` method that:
  - Creates result container and threading event
  - Schedules `simpledialog.askstring()` on main thread
  - Blocks interpreter thread until input received
  - Returns result or None
- Wired `_request_user_input` to interpreter's `_ide_input_request` callback (line 3435)

## Testing
- All 278 existing tests pass
- Created `test_a_command_fix.py` demonstrating both console and IDE modes work correctly
- Test file `test_accept_input.spt` provided for manual IDE testing

## Usage Example
```pilot
T:Welcome! What's your name?
A:NAME
T:Hello, *NAME*! How old are you?
A:AGE
T:Nice to meet you, *NAME*. You are *AGE* years old.
```

## Technical Notes
- Pattern mirrors graphics queue implementation (Phase 2)
- No changes needed to A: command syntax or semantics
- Console mode (stdin/stdout) unchanged
- Thread-safe for daemon background threads used in IDE execution
- Event-based synchronization ensures interpreter waits for user input
