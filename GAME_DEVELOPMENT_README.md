# Time Warp IDE - Game Development

This directory contains game development examples and demos for the Time Warp IDE, showcasing the GAME command system for creating 2D games using PILOT language.

## GAME Commands Overview

The Time Warp IDE includes a comprehensive set of GAME commands for 2D game development:

### Core Commands
- `GAME:CREATE name type x y width height` - Create a game object
- `GAME:MOVE name dx dy speed` - Move an object by relative coordinates
- `GAME:DELETE name` - Remove an object from the game
- `GAME:LIST` - List all active game objects (stored in GAME_OBJECT_LIST variable)
- `GAME:CLEAR` - Remove all game objects
- `GAME:INFO name [variable]` - Get detailed information about an object

### Physics & Collision
- `GAME:PHYSICS command parameters` - Set physics properties (gravity, etc.)
- `GAME:COLLISION CHECK obj1 obj2 result_var` - Check collision between two objects
- `GAME:UPDATE delta_time` - Update physics simulation

### Rendering & Display
- `GAME:RENDER` - Render the current game scene
- `GAME:DEMO type` - Run built-in game demonstrations

## Game Examples

### Galaga Demo (`galaga_demo.pilot`)

A simplified version of the classic arcade game demonstrating:
- Player ship movement (A/D keys)
- Enemy ship creation and movement
- Bullet firing (SPACE key)
- Basic collision detection
- Score tracking

**To run:**
```bash
python3 run_program.py galaga_demo.pilot
```

**Controls:**
- `A` - Move player left
- `D` - Move player right
- `SPACE` - Fire bullet
- Enter any input to continue the game loop

### Full Galaga Game (`galaga_game.pilot`)

A complete implementation with:
- Multiple enemy waves
- Complex enemy AI patterns
- Player lives system
- Level progression
- Sound effects (when available)
- High score tracking

## Running Games

### Method 1: Command Line (Recommended for testing)
```bash
python3 run_program.py galaga_demo.pilot
```

### Method 2: GUI Application
1. Start Time Warp IDE: `python3 Time_Warp.py`
2. Load the game file from the File menu
3. Select PILOT language
4. Click Run to execute

## Game Development Tutorial

### 1. Basic Object Creation
```
GAME:CLEAR
GAME:CREATE player ship 200 300 32 24
GAME:CREATE enemy alien 100 100 24 16
```

### 2. Movement and Animation
```
GAME:MOVE player 5 0 1    * Move right
GAME:MOVE enemy 0 2 0.5  * Move down slowly
```

### 3. Collision Detection
```
GAME:COLLISION CHECK player enemy HIT
Y:HIT=1
T:COLLISION DETECTED!
```

### 4. Game Loop Structure
```
*GAME_LOOP
* Handle input
* Update object positions
* Check collisions
* Render scene
*J:GAME_LOOP
```

## Technical Details

### Variable System
- Game state is stored in interpreter variables
- `GAME_OBJECT_COUNT` - Number of active objects
- `GAME_OBJECT_LIST` - Comma-separated list of object names
- Object-specific variables: `GAME_OBJECT_{id}_X`, `GAME_OBJECT_{id}_Y`, etc.

### Coordinate System
- Origin (0,0) is top-left
- X increases right, Y increases down
- Canvas size: 400x400 pixels (configurable)

### Performance
- Designed for educational purposes
- Suitable for simple 2D games
- Not optimized for high-performance gaming

## Future Enhancements

- Sprite graphics support
- Sound effect integration
- Multiplayer capabilities
- Advanced physics (rotation, momentum)
- Level editor integration

## Requirements

- Python 3.6+
- Tkinter (usually included with Python)
- PIL/Pillow (for image support, optional)

## Troubleshooting

**Game doesn't start:**
- Ensure you're using `python3`, not `python`
- Check that all GAME commands are implemented (run tests first)

**Objects not moving:**
- Verify object names match exactly
- Check coordinate values are numeric

**Collisions not detected:**
- Ensure objects have proper width/height
- Check that collision result variable is being read correctly

## Contributing

To add new games or improve existing ones:
1. Use the GAME command API
2. Follow PILOT language conventions
3. Include clear comments and documentation
4. Test with both command-line and GUI execution