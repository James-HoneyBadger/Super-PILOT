"""
TempleCode IDE - Windows Application Setup
Build configuration for creating Windows executable and installer
"""

import sys
from pathlib import Path
from setuptools import setup, find_packages

# Read version from VERSION file
version_file = Path(__file__).parent / "VERSION"
if version_file.exists():
    version = version_file.read_text().strip()
else:
    version = "1.0.0"

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")
else:
    long_description = "TempleCode IDE - Educational Programming Environment"

# Windows-specific requirements
install_requires = [
    "Pillow>=8.0.0",
    # Windows audio support is built-in via winsound
]

# Additional Windows dependencies for building
extras_require = {
    "build": [
        "pyinstaller>=4.10",
        "auto-py-to-exe>=2.0.0",
        "cx-freeze>=6.0",
    ],
    "dev": [
        "pytest>=6.0",
        "pytest-cov>=2.0",
        "black>=21.0",
        "isort>=5.0",
        "flake8>=3.8",
    ],
}

# Console and GUI entry points
entry_points = {
    "console_scripts": [
        "templecode-cli=templecode_app:main",
    ],
    "gui_scripts": [
        "templecode=templecode_app:main",
        "TempleCode=templecode_app:main",
    ],
}

setup(
    name="TempleCode-IDE",
    version=version,
    description="Educational Programming Environment for Windows 11",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TempleCode Team",
    author_email="support@templecode.edu",
    url="https://github.com/James-HoneyBadger/Super-PILOT",
    packages=find_packages(),
    py_modules=["Super_PILOT", "templecode", "templecode_app"],
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.spt", "*.pil", "*.ico", "*.png"],
        "assets": ["*"],
        "examples": ["*"],
        "sample_programs": ["**/*"],
        "docs": ["**/*"],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points=entry_points,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: User Interfaces",
    ],
    keywords="education programming basic logo pilot ide windows",
    project_urls={
        "Documentation": "https://github.com/James-HoneyBadger/Super-PILOT/docs",
        "Source": "https://github.com/James-HoneyBadger/Super-PILOT",
        "Tracker": "https://github.com/James-HoneyBadger/Super-PILOT/issues",
    },
    zip_safe=False,  # Important for PyInstaller compatibility
)
