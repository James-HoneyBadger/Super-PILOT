# Time Warp IDE

A modern educational programming environment written in Rust.

Time Warp IDE is a unified implementation supporting PILOT, BASIC, and Logo languages with integrated turtle graphics, safe expression evaluation, and modern UI powered by egui.

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

- **PILOT**: Full implementation (text, variables, conditionals, jumps)
- **BASIC**: Core commands (PRINT, LET, INPUT, INKEY$, IF...THEN, FOR/NEXT, GOTO, GOSUB, RETURN, LINE, CIRCLE)
- **Logo**: Turtle graphics with REPEAT, procedures (TO/END), PENWIDTH, named/hex colors, PNG export
- Safe expression evaluator (no eval())
- Async execution with tokio
- Expression caching (10-50x speedup)
- Security limits and timeouts
- Modern egui UI with 8 themes
- Unified Screen: single canvas for text and graphics output (text/graphics modes)
- Input prompts: interactive 📝 dialog for BASIC INPUT and PILOT A:
- Real-time keyboard detection: INKEY$ for game loops and interactive programs

## Example Programs

**PILOT:**

```pilot
T:What is your name?
A:NAME
T:Hello *NAME*!
```

**BASIC:**

```basic
10 LET A = 5
20 PRINT "Value:", A
30 IF A > 3 THEN PRINT "Greater"
```

**23 example programs** organized by difficulty in `examples/`:

- **Beginner**: `pilot_quiz.pilot`, `basic_guess.bas`, `logo_star.logo`
- **Intermediate**: `basic_rock_paper_scissors.bas`, `logo_flower.logo`
- **Advanced**: `pilot_dragon_adventure.pilot`, `logo_koch_snowflake.logo`

PNG export: use View → "Save Canvas as PNG…" in the UI.

## Learning Resources

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

**See also**: [Examples README](examples/README.md) for learning paths and all 23 programs.

## Testing

- 22 integration tests (100% pass)
- 5 doc tests
- Zero warnings

See [TEST_RESULTS.md](TEST_RESULTS.md) for details.

## License

See [LICENSE](LICENSE) file for details.
