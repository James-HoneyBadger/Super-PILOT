# Time Warp IDE

[![CI](https://github.com/James-HoneyBadger/Time_Warp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/James-HoneyBadger/Time_Warp/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

**Official IDE:**

```bash
python Time_Warp_IDE.py
```

- The modern PySide6-based IDE is now the official version.
- The classic Tkinter IDE (`Time_Warp.py`) is archived in `archive/` for reference only.

For more details, see documentation and examples in the repo.

## 🔧 Troubleshooting

### "Illegal instruction" or "Illegal instruction (core dumped)" Error

**Symptoms:** The IDE crashes immediately with "Illegal instruction" when starting.

**Cause:** This system is running on a virtual CPU that lacks support for modern CPU instructions (SSSE3, SSE4.1, SSE4.2, POPCNT) required by PySide6/Qt and other modern libraries.

**Solutions:**
1. **Run on physical hardware** or a newer virtual environment with proper CPU instruction support
2. **Use a different Linux distribution** or container with better CPU emulation
3. **Update QEMU/KVM** to a version that supports newer CPU instructions
4. **Use cloud instances** with modern CPU architectures (AWS, GCP, Azure, etc.)

**Verification:** Check your CPU flags:
```bash
cat /proc/cpuinfo | grep -E "(flags|model name)" | head -5
```

Required CPU flags include: `ssse3`, `sse4_1`, `sse4_2`, `popcnt`

The Time Warp IDE requires a CPU with SSSE3, SSE4.1, SSE4.2, and POPCNT support.