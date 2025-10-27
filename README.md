# Time Warp IDE

[![Rust CI](https://github.com/James-HoneyBadger/Time_Warp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/James-HoneyBadger/Time_Warp/actions/workflows/ci.yml)
[![Python CI](https://github.com/James-HoneyBadger/Time_Warp/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/James-HoneyBadger/Time_Warp/actions/workflows/python-tests.yml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Retromodern educational IDE with multi-language support (PILOT, BASIC, Logo) and turtle graphics. Includes both a modern Python IDE and an egui-based Rust IDE.

## 🚀 Quick Start

Choose your preferred IDE flavor.

### Python IDE (Modern, PySide6)

```bash
python Time_Warp_IDE.py
```

### Python IDE (Classic, Tkinter)

```bash
python Time_Warp.py
```

### Rust IDE (Retromodern, egui)

```bash
cd Time_Warp_Rust
cargo run
```

## ✨ Features

- Project explorer and tabbed multi-file editing
- Turtle graphics and educational language executors (PILOT, BASIC, Logo)
- Retromodern UI themes (green/amber/white phosphor)
- Cross-platform file I/O and examples library
- Python and Rust implementations side-by-side

Roadmap (in progress): variable inspector, debugger, command palette, integrated terminal.

## 📦 Install

Python 3.11+ recommended. Optional Rust toolchain for the Rust IDE.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-dev.txt
```

## 🧪 Tests

Run the Python test suite:

```bash
pytest -q
```

Rust build and tests:

```bash
cd Time_Warp_Rust
cargo build && cargo test
```

## 📚 Documentation

See `USER_GUIDE.md` for usage and `DEVELOPMENT.md` for contributing and local setup. Sphinx docs live in `docs/`.

## 🤝 Contributing

See `CONTRIBUTING.md` and our `CODE_OF_CONDUCT.md`.

## 🔐 Security

Please report vulnerabilities privately. See `SECURITY.md`.

## 📝 License

MIT — see `LICENSE`.

## 🔧 Troubleshooting

### "Illegal instruction" or "Illegal instruction (core dumped)" Error

Some environments (older VMs) may lack CPU instructions PySide6/Qt expects (SSSE3/SSE4.*/POPCNT).

Solutions:
1. Run on physical hardware or a newer VM
2. Try a different Linux distro or updated QEMU/KVM
3. Use a cloud instance with a modern CPU

Verify CPU flags:

```bash
cat /proc/cpuinfo | grep -E "(flags|model name)" | head -5
```

Required: `ssse3`, `sse4_1`, `sse4_2`, `popcnt`.