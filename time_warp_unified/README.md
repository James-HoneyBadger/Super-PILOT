# Time Warp Unified - Rust Implementation

Welcome to the unified Rust-based Time Warp IDE!

## Building

```bash
cargo build --release
```

## Running

```bash
cargo run --release
```

## Features

### Phase 1 (Current) - Foundation ✓
- Core interpreter architecture
- PILOT, BASIC, and Logo language support (basic commands)
- Modern egui-based UI with retromodern themes
- Tabbed file editing
- Turtle graphics with zoom/pan
- Multi-theme support (8 themes)

### Coming Soon
- Phase 2: Complete language interpreters
- Phase 3: Full turtle graphics features
- Phase 4: 2D game engine
- Phase 5: ML/AI integration
- Phase 6: IoT/Robotics simulation
- Phase 7: Audio system
- Phase 8: Plugin architecture

## Project Structure

```
src/
├── main.rs          # Entry point
├── app.rs           # Main application
├── interpreter/     # Core interpreter
├── languages/       # PILOT, BASIC, Logo
│   ├── pilot/
│   ├── basic/
│   └── logo/
├── graphics/        # Turtle graphics
├── ui/             # egui UI components
│   ├── themes.rs
│   ├── menubar.rs
│   ├── editor.rs
│   ├── output.rs
│   └── ...
├── game/           # Game engine (stub)
├── ml/             # ML/AI (stub)
├── iot/            # IoT/Robotics (stub)
├── audio/          # Audio system (stub)
└── plugins/        # Plugin system (stub)
```

## Development

This project is being built incrementally following the roadmap in `RUST_UNIFICATION_PLAN.md`.

Current status: **Phase 1 - Foundation** ✓

## License

MIT
