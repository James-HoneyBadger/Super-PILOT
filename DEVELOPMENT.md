# Development Guide

## Repos and Layout

- Python IDE entrypoints: `Time_Warp_IDE.py` (modern), `Time_Warp.py` (classic)
- Core Python engine: `core/` and `tools/`
- Rust retromodern IDE: `Time_Warp_Rust/`
- Docs: `docs/`
- Tests: `tests/`

## Prerequisites

- Python 3.11+
- Rust stable toolchain (rustup)
- Node not required

## Python Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-dev.txt
pytest -q
```

## Rust Setup

```bash
cd Time_Warp_Rust
cargo fmt --all
cargo clippy -- -D warnings || true
cargo build
```

## Code Style

- Python: black, isort, ruff (see ruff.toml). Use pre-commit hooks.
- Rust: rustfmt and clippy. See rustfmt.toml.

## Running

- Python IDE (modern): `python Time_Warp_IDE.py`
- Python IDE (classic): `python Time_Warp.py`
- Rust IDE: `cargo run` in `Time_Warp_Rust/`

## Tests

- Python: `pytest`
- Rust: `cargo test`

## Docs

Sphinx docs live under `docs/`. Build locally with:

```bash
cd docs
make html
```
