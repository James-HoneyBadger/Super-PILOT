# SuperPILOT Project Structure

This document describes the organization of the SuperPILOT project.

## Directory Layout

```
Super-PILOT/
├── Super_PILOT.py              # Main application entry point
├── templecode.py               # Animation and effects engine
├── conftest.py                 # Pytest configuration
├── pytest.ini                  # Pytest settings
├── test_runner.py              # Custom test runner
├── README.md                   # Project homepage
├── CHANGELOG.md                # Version history
├── TESTING.md                  # Testing documentation
├── VERSION                     # Current version number
├── requirements-dev.txt        # Python dependencies
│
├── docs/                       # 📚 Complete documentation suite
│   ├── README.md               # Documentation hub
│   ├── STUDENT_GUIDE.md        # Learning tutorial (16 lessons)
│   ├── TEACHER_GUIDE.md        # Teaching curriculum (16 weeks)
│   ├── TECHNICAL_REFERENCE.md  # API documentation
│   ├── DEVELOPER_HANDBOOK.md   # Contributing guide
│   └── DOCUMENTATION_SUMMARY.md # Documentation overview
│
├── superpilot/                 # 📦 Core package (modular)
│   ├── __init__.py             # Package initialization
│   ├── core/                   # Core interpreter (planned)
│   ├── ide/                    # IDE components
│   │   └── settings.py         # Settings management
│   └── runtime/                # Runtime systems
│       ├── templecode.py       # Animation (Tween, Timer, Particle)
│       ├── hardware.py         # Hardware controllers
│       └── audio.py            # Audio playback
│
├── tests/                      # 🧪 Comprehensive test suite
│   ├── test_interpreter.py     # Core interpreter tests
│   ├── test_interpreter_comprehensive.py # Full integration tests
│   ├── test_event_callbacks.py # Observer pattern tests
│   ├── test_threading.py       # Concurrency tests
│   ├── test_ide_smoke.py       # IDE smoke tests
│   ├── test_*_commands*.py     # Command-specific tests
│   ├── test_hardware_integration.py # Hardware mocking tests
│   ├── test_templecode_integration.py # Animation tests
│   ├── test_security.py        # Security constraint tests
│   └── test_performance.py     # Performance benchmarks
│
├── sample_programs/            # 📝 Example programs (organized)
│   ├── README.md               # Sample programs guide
│   ├── pilot/                  # PILOT language examples
│   ├── basic/                  # BASIC language examples
│   ├── logo/                   # Logo graphics examples
│   ├── games/                  # Game development demos
│   │   ├── game_pong_demo.spt
│   │   ├── game_platformer_demo.spt
│   │   ├── game_physics_demo.spt
│   │   ├── game_basic_demo.bas
│   │   └── game_logo_demo.logo
│   ├── ml/                     # Machine learning demos
│   │   ├── ml_linear_regression.spt
│   │   ├── ml_classification.spt
│   │   ├── ml_clustering.spt
│   │   ├── ml_basic_demo.spt
│   │   └── ml_logo_demo.spt
│   └── hardware/               # Hardware integration demos
│       ├── hardware_demo.spt
│       └── iot_robotics_demo.spt
│
├── examples/                   # 🎯 Quick start examples (kept for compatibility)
│   ├── pilot_example.spt       # Basic PILOT program
│   ├── basic_example.spt       # Basic BASIC program
│   ├── logo_example.spt        # Basic Logo program
│   ├── logo_graphics_demo.spt  # Logo graphics demo
│   └── Logo.spt                # Advanced Logo example
│
├── Demos/                      # 🎨 Complete demonstration programs
│   ├── README.md               # Demo documentation
│   └── complete_demo.spt       # Full-featured demo
│
├── tools/                      # 🔧 Development utilities
│   ├── bench_commands.py       # Performance benchmarking
│   ├── code_library.py         # Code snippets library
│   ├── icon_factory.py         # Icon generation
│   └── theme.py                # Theme utilities
│
├── assets/                     # 🎨 Application assets
│   └── generate_icons.py       # Icon generator script
│
├── archive/                    # 📦 Legacy and archived files
│   ├── old_docs/               # Superseded documentation
│   │   ├── ADVANCED_IDE_SUMMARY.md
│   │   ├── AI_ML_INTEGRATION_GUIDE.md
│   │   ├── GAME_DEVELOPMENT_GUIDE.md
│   │   ├── IOT_ROBOTICS_GUIDE.md
│   │   ├── TESTING_SUMMARY.md
│   │   └── USER_GUIDE.md
│   ├── SuperPILOT.py           # Old implementation
│   ├── SuperPILOT.archive      # Archived code
│   └── pilot.py.bak            # Backup file
│
├── GW-BASIC/                   # 📖 BASIC language reference
│   ├── technical.txt           # Technical documentation
│   ├── GW-BASIC-master/        # GW-BASIC source code
│   └── *.pdf                   # Reference manuals
│
└── .github/                    # ⚙️ GitHub configuration
    └── workflows/              # CI/CD pipelines
```

## Key Files

### Entry Points

| File | Purpose |
|------|---------|
| `Super_PILOT.py` | Main application - launches the IDE |
| `templecode.py` | Standalone animation engine |
| `test_runner.py` | Run all tests with reporting |

### Configuration

| File | Purpose |
|------|---------|
| `requirements-dev.txt` | Python dependencies |
| `pytest.ini` | Test framework configuration |
| `conftest.py` | Pytest fixtures and setup |
| `.gitignore` | Git ignore patterns |
| `VERSION` | Current version string |

### Documentation

| File | Audience | Lines |
|------|----------|-------|
| `README.md` | All users | 376 |
| `docs/README.md` | Navigation hub | 375 |
| `docs/STUDENT_GUIDE.md` | Students | 670 |
| `docs/TEACHER_GUIDE.md` | Teachers | 877 |
| `docs/TECHNICAL_REFERENCE.md` | Developers | 575 |
| `docs/DEVELOPER_HANDBOOK.md` | Contributors | 1,100+ |
| `CHANGELOG.md` | All users | History |
| `TESTING.md` | Developers | Test guide |

## Module Organization

### superpilot Package

```
superpilot/
├── __init__.py              # Package exports
├── core/                    # Core interpreter (planned refactor)
│   ├── interpreter.py       # Main interpreter class
│   └── languages/           # Language-specific executors
│       ├── pilot.py         # PILOT command handler
│       ├── basic.py         # BASIC command handler
│       └── logo.py          # Logo command handler
├── ide/                     # IDE components
│   ├── settings.py          # Settings management (✅ implemented)
│   ├── editor.py            # Editor widget (planned)
│   └── debugger.py          # Debugger UI (planned)
└── runtime/                 # Runtime systems
    ├── templecode.py        # Animation engine (✅ implemented)
    ├── hardware.py          # Hardware controllers (✅ implemented)
    └── audio.py             # Audio system (✅ implemented)
```

## Test Organization

### Test Categories

| Pattern | Purpose | Count |
|---------|---------|-------|
| `test_interpreter*.py` | Core interpreter | 2 |
| `test_*_commands*.py` | Command testing | 8 |
| `test_*_integration.py` | Integration tests | 3 |
| `test_event_*.py` | Event system | 1 |
| `test_threading.py` | Concurrency | 1 |
| `test_ide_*.py` | IDE components | 1 |
| `test_security.py` | Security | 1 |
| `test_performance.py` | Performance | 1 |

### Running Tests

```bash
# All tests
pytest

# Specific category
pytest tests/test_interpreter*.py

# With coverage
pytest --cov=. --cov-report=html

# Verbose
pytest -v
```

## File Naming Conventions

### Programs

| Extension | Type | Example |
|-----------|------|---------|
| `.spt` | SuperPILOT (multi-language) | `demo.spt` |
| `.pil` | PILOT only | `quiz.pil` |
| `.bas` | BASIC only | `calculator.bas` |
| `.logo` | Logo only | `turtle.logo` |

### Python Files

| Pattern | Type | Example |
|---------|------|---------|
| `Super_PILOT.py` | Main application | Entry point |
| `test_*.py` | Unit tests | `test_interpreter.py` |
| `*_demo.py` | Demonstrations | `hardware_demo.py` |
| `conftest.py` | Test fixtures | pytest config |

### Documentation

| Pattern | Type | Example |
|---------|------|---------|
| `README.md` | Overview | Main docs |
| `*_GUIDE.md` | Tutorials | `STUDENT_GUIDE.md` |
| `*_REFERENCE.md` | Technical docs | `TECHNICAL_REFERENCE.md` |
| `CHANGELOG.md` | History | Version log |

## Clean Build

To start fresh and remove all generated files:

```bash
# Remove caches
rm -rf __pycache__ .pytest_cache .mypy_cache .benchmarks

# Remove test artifacts
rm -rf htmlcov .coverage test_reports/

# Remove config
rm -f .config.json debug_test.py

# Run tests to verify
pytest
```

## Git Ignored Files

The following are excluded from version control:

- Python cache: `__pycache__/`, `*.pyc`, `*.pyo`
- Virtual environments: `venv/`, `env/`
- IDE files: `.vscode/`, `.idea/`
- Test artifacts: `.pytest_cache/`, `htmlcov/`, `.coverage`
- Benchmarks: `.benchmarks/`
- User configs: `.config.json`
- Temporary files: `debug_test.py`, `*.log`

See `.gitignore` for complete list.

## Adding New Files

### New Feature

```
1. Add code to Super_PILOT.py or superpilot/
2. Add tests to tests/test_*.py
3. Update docs/TECHNICAL_REFERENCE.md
4. Add example to sample_programs/ or examples/
5. Update CHANGELOG.md
```

### New Example Program

```
1. Create file in sample_programs/<category>/
2. Add descriptive comments
3. Test thoroughly
4. Update sample_programs/README.md
```

### New Documentation

```
1. Create file in docs/
2. Add to docs/README.md navigation
3. Cross-reference other docs
4. Update main README.md if needed
```

## Migration Notes

### From Old Structure

The following reorganization was done:

**Sample Programs**: Scattered `.spt` files → `sample_programs/` with categories  
**Documentation**: Mixed `.md` files → `docs/` directory  
**Tests**: Mixed test files → `tests/` directory  
**Legacy Code**: Root level → `archive/` directory  
**Old Docs**: Superseded guides → `archive/old_docs/`

### Preserved Locations

- `Super_PILOT.py` - Main entry point (kept at root)
- `examples/` - Quick start examples (kept for compatibility)
- `Demos/` - Demo programs (kept as showcase)
- `GW-BASIC/` - Reference materials (educational value)

## Best Practices

1. **Keep root clean** - Only essential files at top level
2. **Organize by purpose** - Tests, docs, samples in separate dirs
3. **Use descriptive names** - Clear file naming conventions
4. **Document structure** - README in each major directory
5. **Archive old files** - Don't delete, move to archive/
6. **Test organization** - Match test files to source files
7. **Update docs** - Keep structure documentation current

## Questions?

See [Developer Handbook](docs/DEVELOPER_HANDBOOK.md) for development guidelines.
