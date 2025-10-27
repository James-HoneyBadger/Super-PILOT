# Time Warp IDE

**A modern educational programming environment written in Rust**

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
- **BASIC**: Core commands (PRINT, LET, IF...THEN, GOTO, GOSUB, RETURN)
- **Logo**: Turtle graphics (in progress)
- Safe expression evaluator (no eval())
- Async execution with tokio
- Expression caching (10-50x speedup)
- Security limits and timeouts
- Modern egui UI with 8 themes

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

## Testing

- 18 unit tests (100% pass)
- 5 doc tests
- Zero warnings

See [TEST_RESULTS.md](TEST_RESULTS.md) for details.

## License

See [LICENSE](LICENSE) file for details.
