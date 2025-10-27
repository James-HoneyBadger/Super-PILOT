# SuperPILOT Sample Programs

This directory contains example programs demonstrating SuperPILOT's capabilities across different domains.

## Directory Structure

```
sample_programs/
├── pilot/          Basic PILOT language examples and test programs
├── basic/          BASIC language examples (coming soon)
├── logo/           Logo turtle graphics examples (coming soon)
├── games/          Game development examples
├── ml/             Machine learning integration examples
└── hardware/       Hardware integration (Arduino, Raspberry Pi, IoT)
```

## Categories

### PILOT Programs (`pilot/`)
Basic examples demonstrating PILOT language features:
- Text input/output
- Variables and conditionals
- Loops and control flow
- Test programs for debugging

### Games (`games/`)
Interactive game examples:
- `game_pong_demo.spt` - Classic Pong game
- `game_platformer_demo.spt` - Platform game mechanics
- `game_physics_demo.spt` - Physics simulation
- `game_basic_demo.bas` - BASIC game example
- `game_logo_demo.logo` - Logo graphics game

### Machine Learning (`ml/`)
ML algorithm demonstrations:
- `ml_linear_regression.spt` - Linear regression example
- `ml_classification.spt` - Classification algorithms
- `ml_clustering.spt` - Clustering techniques
- `ml_basic_demo.spt` - Basic ML concepts
- `ml_logo_demo.spt` - ML visualization with Logo

### Hardware Integration (`hardware/`)
Hardware control examples:
- `hardware_demo.spt` - Arduino and RPi GPIO control
- `iot_robotics_demo.spt` - IoT and robotics applications

## Running Examples

### From IDE
1. Open SuperPILOT: `python3 Super_PILOT.py`
2. File → Open
3. Navigate to desired sample program
4. Press F5 to run

### From Command Line
```bash
python3 Super_PILOT.py sample_programs/games/game_pong_demo.spt
```

## Contributing Examples

Want to add your own examples? Great!

1. Choose the appropriate category
2. Add descriptive comments in your code
3. Test thoroughly
4. Submit a pull request

## Learning Path

**Beginners**: Start with `pilot/` examples
**Intermediate**: Try `games/` examples
**Advanced**: Explore `ml/` and `hardware/` examples

For detailed tutorials, see the [Student Guide](../docs/STUDENT_GUIDE.md).
