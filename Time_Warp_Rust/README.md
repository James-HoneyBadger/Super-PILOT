# Time Warp IDE (TempleCode)

A modern educational programming environment written in Rust.

Time Warp IDE implements TempleCode — a unified language that combines the best of BASIC, PILOT, and Logo — with integrated turtle graphics, safe expression evaluation, and a modern egui UI. You can freely mix commands (PRINT / T: / FORWARD, etc.) in a single program.

## Quick Start

```bash
# Build and run
cargo run

# Run tests
cargo test

# Build release
cargo build --release
./target/release/time-warp
```

## Features

- TempleCode language: All BASIC, PILOT, and Logo commands in one language
  - Text commands: PRINT, LET, INPUT, INKEY$, IF...THEN, FOR/NEXT, GOTO, GOSUB, RETURN
  - PILOT-style: T:, A:, labels (L:), jumps (J:)
  - Logo turtle graphics: FORWARD/FD, LEFT/LT, RIGHT/RT, REPEAT, TO/END procedures, PENWIDTH, colors, PNG export
- Safe expression evaluator (no eval())
- Async execution with tokio
- Expression caching (10-50x speedup)
- Security limits and timeouts
- Modern egui UI with 8 themes
- Unified Screen: single canvas for text and graphics output (text/graphics modes)
- Text screen controls: CLS, LOCATE; GW-BASIC–style SCREEN command
- Input prompts: interactive 📝 dialog for BASIC INPUT and PILOT A:
- Real-time keyboard detection: INKEY$ for game loops and interactive programs

## Example Programs

**PILOT:**

```pilot
T:What is your name?
A:NAME
T:Hello *NAME*!
```

**TempleCode (BASIC-style):**

```basic
10 LET A = 5
20 PRINT "Value:", A
30 IF A > 3 THEN PRINT "Greater"
```

**33 example programs** organized by difficulty in `examples/`:

- **Beginner**: `pilot_quiz.pilot`, `basic_guess.bas`, `logo_star.logo`
- **Intermediate**: `basic_rock_paper_scissors.bas`, `logo_flower.logo`
- **Advanced**: `pilot_dragon_adventure.pilot`, `logo_koch_snowflake.logo`

PNG export: use View → "Save Canvas as PNG…" in the UI.

## Learning Resources

- [User Guide (Unified)](../USER_GUIDE.md) — Covers both Rust and Python versions

**Getting Started**:

- [Getting Started Guide](docs/GETTING_STARTED.md) — Your first 5 minutes with Time Warp
- [Quick Reference](docs/QUICK_REFERENCE.md) — Complete command reference for all languages
- [Student Guide](docs/STUDENT_GUIDE.md) — Language cheatsheets and challenges

**For Teachers**:

- [Lesson Plans](docs/LESSON_PLANS.md) — Complete 8-week curriculum for middle school
- [Teacher Guide](docs/TEACHER_GUIDE.md) — Session outlines and assessment ideas
- [Programming Challenges](docs/PROGRAMMING_CHALLENGES.md) — 12 challenges with solutions

**For Developers**:

- [Developer Reference](docs/DEVELOPER_REFERENCE.md) — API documentation and extension guide
- [Parsing & Language Detection](docs/PARSING_REFERENCE.md) — Command precedence, line numbers, comparisons

### TempleCode Compiler (experimental)

You can transpile TempleCode to C and build a native Linux executable.

Scope (v0):
 
- Text-mode subset: PRINT, LET, INPUT, IF ... THEN (GOTO | PRINT), GOTO, END
- PILOT: T:, A:
- Logo: currently ignored at compile-time (runtime support remains via interpreter)

Usage:

```bash
# Build and run the GUI normally
cargo run

# Compile a TempleCode source file to an executable
cargo run -- --compile my_program.tc -o my_program

# Then run it
./my_program
```

Notes:
 
- Requires a system C compiler (cc/gcc/clang) on PATH.
- Output C file is written to target/tmp internally before linking.

**See also**: [Examples README](examples/README.md) for learning paths and all 33 programs.

## Testing

- 22 integration tests (100% pass)
- 5 doc tests
- Zero warnings

See [TEST_RESULTS.md](TEST_RESULTS.md) for details.

## License

See [LICENSE](LICENSE) file for details.
