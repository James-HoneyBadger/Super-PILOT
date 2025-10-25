# 🎮 Time Warp Game Development Framework

## Overview

Time Warp now includes a comprehensive game development framework with advanced physics simulation, collision detection, and interactive graphics. This guide covers all aspects of creating games in Time Warp across all three supported languages: PILOT, BASIC, and Logo.

## Quick Start

### Basic Game Creation (PILOT)
```pilot
T:Creating my first game
GAME:CREATE player rectangle 100 100 32 48
GAME:CREATE enemy rectangle 200 150 24 24
GAME:PHYSICS GRAVITY 9.8
GAME:UPDATE 0.016
GAME:RENDER
```

### Basic Game Creation (BASIC)
```basic
10 PRINT "Creating my first game"
20 GAMECREATE player rectangle 100 100 32 48
30 GAMECREATE enemy rectangle 200 150 24 24
40 GAMEPHYSICS GRAVITY 9.8
50 GAMEUPDATE 0.016
60 GAMERENDER
```

### Basic Game Creation (Logo)
```logo
PRINT [Creating my first game]
CREATEOBJECT player rectangle 100 100 32 48
CREATEOBJECT enemy rectangle 200 150 24 24
SETGRAVITY 9.8
UPDATEGAME 0.016
RENDERGAME
```

## Game Framework Architecture

### Core Components

1. **Vector2D**: Mathematical foundation for 2D physics
2. **GameObject**: Represents all game entities with physics properties
3. **PhysicsEngine**: Handles gravity, velocity, acceleration, and collisions
4. **GameRenderer**: Renders objects to canvas (when available)
5. **GameManager**: Orchestrates all game systems

### Physics System

The physics engine supports:
- **Gravity**: Global downward acceleration (default: 9.8 m/s²)
- **Velocity**: Object movement speed and direction
- **Acceleration**: Changes in velocity over time
- **Mass**: Affects how forces impact objects
- **Collision Detection**: AABB (Axis-Aligned Bounding Box) collision detection

## Command Reference

### PILOT Game Commands

| Command | Description | Example |
|---------|-------------|---------|
| `GAME:CREATE` | Create game object | `GAME:CREATE player rectangle 100 100 32 48` |
| `GAME:MOVE` | Move object relatively | `GAME:MOVE player 10 0 5` |
| `GAME:PHYSICS` | Set physics properties | `GAME:PHYSICS GRAVITY 9.8` |
| `GAME:COLLISION` | Check collision | `GAME:COLLISION CHECK player enemy HIT` |
| `GAME:RENDER` | Render scene | `GAME:RENDER` |
| `GAME:UPDATE` | Update physics | `GAME:UPDATE 0.016` |
| `GAME:DELETE` | Delete object | `GAME:DELETE enemy1` |
| `GAME:LIST` | List all objects | `GAME:LIST` |
| `GAME:CLEAR` | Clear all objects | `GAME:CLEAR` |
| `GAME:INFO` | Get object info | `GAME:INFO player` |
| `GAME:DEMO` | Run demo | `GAME:DEMO pong` |

### BASIC Game Commands

| Command | Description | Example |
|---------|-------------|---------|
| `GAMECREATE` | Create game object | `GAMECREATE player rectangle 100 100 32 48` |
| `GAMEMOVE` | Move object | `GAMEMOVE player 10 0 5` |
| `GAMEPHYSICS` | Set physics | `GAMEPHYSICS GRAVITY 9.8` |
| `GAMECOLLISION` | Check collision | `GAMECOLLISION player enemy HIT` |
| `GAMERENDER` | Render scene | `GAMERENDER` |
| `GAMEUPDATE` | Update physics | `GAMEUPDATE 0.016` |
| `GAMEDEMO` | Run demo | `GAMEDEMO pong` |

### Logo Game Commands

| Command | Description | Example |
|---------|-------------|---------|
| `CREATEOBJECT` | Create game object | `CREATEOBJECT player rectangle 100 100 32 48` |
| `MOVEOBJECT` | Move object | `MOVEOBJECT player 10 0 5` |
| `SETGRAVITY` | Set gravity | `SETGRAVITY 9.8` |
| `SETVELOCITY` | Set velocity | `SETVELOCITY player 10 -5` |
| `CHECKCOLLISION` | Check collision | `CHECKCOLLISION player enemy` |
| `RENDERGAME` | Render scene | `RENDERGAME` |
| `UPDATEGAME` | Update physics | `UPDATEGAME 0.016` |
| `GAMEOBJECTS` | List objects | `GAMEOBJECTS` |
| `CLEARGAME` | Clear objects | `CLEARGAME` |
| `GAMEDEMO` | Run demo | `GAMEDEMO pong` |

## Game Object Types

### Rectangle Objects
- Standard rectangular collision boxes
- Most common for platforms, walls, characters
- Defined by x, y, width, height

### Circle Objects  
- Circular collision detection
- Good for balls, bullets, round objects
- Defined by x, y, radius (stored as width/height)

### Future Object Types
- **Sprite**: Image-based objects with animation
- **Platform**: Static objects with special collision behavior
- **Projectile**: Fast-moving objects with trail effects

## Coordinate System

- **Origin**: (0, 0) is at the screen center
- **X-Axis**: Positive right, negative left
- **Y-Axis**: Positive up, negative down (following physics convention)
- **Units**: Pixels for position, pixels/second for velocity

## Physics Properties

### Position and Movement
```pilot
GAME:CREATE ball circle 100 50 20 20
GAME:PHYSICS ball VELOCITY 10 -15  ; 10 right, 15 up
GAME:MOVE ball 5 0                  ; Move 5 pixels right
```

### Mass and Forces
```pilot
GAME:PHYSICS ball MASS 2.0         ; Heavier objects
GAME:PHYSICS GRAVITY 9.8           ; Earth-like gravity
```

### Collision Detection
```pilot
GAME:COLLISION CHECK player enemy RESULT
Y:RESULT = 1
T:Collision detected!
```

## Complete Game Examples

### 1. Pong Game
```pilot
T:🏓 Time Warp Pong Game
GAME:CREATE paddle1 rectangle 50 200 20 80
GAME:CREATE paddle2 rectangle 750 200 20 80  
GAME:CREATE ball circle 400 200 20 20
GAME:PHYSICS ball VELOCITY 5 3

L:GAMELOOP
GAME:UPDATE 0.016
GAME:COLLISION CHECK ball paddle1 HIT1
GAME:COLLISION CHECK ball paddle2 HIT2
Y:HIT1 = 1
T:Ball hit left paddle!
Y:HIT2 = 1  
T:Ball hit right paddle!
GAME:RENDER
J:GAMELOOP
```

### 2. Physics Sandbox
```pilot
T:🌍 Physics Playground
GAME:PHYSICS GRAVITY 9.8
GAME:CREATE ground rectangle 400 550 800 50
GAME:CREATE box1 rectangle 200 100 50 50
GAME:CREATE box2 rectangle 400 50 40 40
GAME:CREATE ball circle 600 100 30 30

U:STEPS=0
L:SIMULATE
U:STEPS=STEPS+1
GAME:UPDATE 0.016
T:Step *STEPS*: Ball at (*GAME_BALL_X*, *GAME_BALL_Y*)
Y:STEPS < 100
J:SIMULATE
```

### 3. Simple Platformer
```pilot
T:🏃 Platformer Demo
GAME:PHYSICS GRAVITY 9.8
GAME:CREATE player rectangle 100 400 32 48
GAME:CREATE platform1 rectangle 200 500 200 20
GAME:CREATE platform2 rectangle 500 350 150 20

; Simple jump mechanics
GAME:PHYSICS player VELOCITY 0 -15
GAME:UPDATE 0.016
GAME:COLLISION CHECK player platform1 ONPLAT
Y:ONPLAT = 1
T:Player landed on platform!
```

## Advanced Features

### Game Manager Dialog
Access the visual game development interface:
1. Go to **🎮 Game Dev** menu
2. Select **Game Manager**
3. Use tabs for:
   - **🎯 Game Objects**: Create, edit, delete objects
   - **⚡ Physics**: Control gravity and simulation
   - **🎨 Scene Preview**: Visual representation of game world
   - **🚀 Quick Demo**: Pre-built game templates

### Variable Integration
Game commands automatically create variables:
```pilot
GAME:CREATE player rectangle 100 100 32 32
T:Player X position: *GAME_PLAYER_X*
T:Player Y position: *GAME_PLAYER_Y*
T:Player velocity: (*GAME_PLAYER_VX*, *GAME_PLAYER_VY*)
```

### Physics Timing
- Use `GAME:UPDATE 0.016` for 60 FPS simulation
- Use `GAME:UPDATE 0.033` for 30 FPS simulation  
- Smaller timesteps = more accurate physics
- Larger timesteps = faster but less accurate

## Educational Concepts

### Physics Concepts Demonstrated
1. **Gravity**: Objects accelerate downward
2. **Velocity**: Speed and direction of movement
3. **Acceleration**: Change in velocity over time
4. **Collision Detection**: When objects overlap
5. **Conservation of Energy**: In bouncing balls
6. **Projectile Motion**: Parabolic trajectories

### Programming Concepts
1. **Object-Oriented Design**: Game objects with properties
2. **Event-Driven Programming**: Collision responses
3. **Game Loops**: Continuous update/render cycles
4. **State Management**: Tracking object properties
5. **Coordinate Systems**: 2D positioning
6. **Real-time Simulation**: Physics timesteps

## Performance Tips

### Optimization Strategies
1. **Limit Objects**: Don't create too many objects (< 50 recommended)
2. **Efficient Updates**: Only update active objects
3. **Collision Culling**: Only check nearby objects for collisions
4. **Render Batching**: Group similar objects for rendering
5. **Fixed Timestep**: Use consistent physics timing

### Best Practices
1. **Initialize Once**: Create objects at start, modify during gameplay
2. **Clear Unused**: Delete objects that are no longer needed
3. **Check Bounds**: Remove objects that leave the game area
4. **Validate Input**: Check collision results before using
5. **Handle Errors**: Use conditional checks for object existence

## Troubleshooting

### Common Issues

**Objects Not Moving**
```pilot
; Check if physics is being updated
GAME:UPDATE 0.016
; Check if object has velocity
GAME:PHYSICS player VELOCITY 10 0
```

**Collisions Not Detected**
```pilot
; Ensure objects exist
GAME:INFO player
GAME:INFO enemy
; Check positions are close enough
GAME:COLLISION CHECK player enemy RESULT
T:Collision result: *RESULT*
```

**Objects Falling Through Floor**
```pilot
; Create static platforms
GAME:CREATE floor rectangle 400 550 800 50
; Or check collision and stop movement
GAME:COLLISION CHECK player floor ONFLOOR
Y:ONFLOOR = 1
GAME:PHYSICS player VELOCITY *GAME_PLAYER_VX* 0
```

### Debug Information
```pilot
; Show all game objects
GAME:LIST
; Show object details
GAME:INFO player
; Show physics state
T:Gravity: *GAME_GRAVITY*
T:Objects: *GAME_OBJECT_COUNT*
```

## Integration with Other Features

### Combining with Turtle Graphics
```logo
; Draw game world with turtle
CLEARSCREEN
CREATEOBJECT player rectangle 0 0 30 30
UPDATEGAME 0.016

; Draw player position with turtle
SETXY GAME_PLAYER_X GAME_PLAYER_Y
REPEAT 4 [FORWARD 15 RIGHT 90]
```

### Using with Machine Learning
```pilot
; Train AI to play games
ML:DATA gamedata classification
; Use game state as ML input
ML:PREDICT player_ai "*GAME_PLAYER_X*,*GAME_PLAYER_Y*,*GAME_ENEMY_X*,*GAME_ENEMY_Y*" ACTION
Y:ACTION > 0.5
GAME:PHYSICS player VELOCITY 10 0
```

### Hardware Integration
```pilot
; Use sensors to control games
R:ARDUINO READ SENSOR DISTANCE
Y:DISTANCE < 20
GAME:PHYSICS player VELOCITY 0 -15  ; Jump when object is near
```

## Future Enhancements

### Planned Features
1. **Sprite System**: Image-based objects with animation
2. **Sound Integration**: Audio effects for collisions and actions
3. **Particle Systems**: Visual effects like explosions and trails
4. **Advanced Physics**: Rotation, friction, bouncing
5. **Networking**: Multiplayer games over network
6. **Save/Load**: Persistent game states
7. **Scripting**: Custom game logic with events

### Contributing
The game framework is designed to be extensible. Key areas for enhancement:
- New object types in `GameObject` class
- Additional physics features in `PhysicsEngine`
- Enhanced rendering in `GameRenderer`
- More demo games in `_run_game_demo()`

## Conclusion

The Time Warp Game Development Framework provides a powerful yet educational platform for creating interactive games while learning programming and physics concepts. The integration across all three languages (PILOT, BASIC, Logo) ensures flexibility in teaching and learning approaches.

Whether creating simple collision detection demos or complex physics simulations, the framework provides the tools needed for engaging, educational game development experiences.

---

*For more information, use the Game Manager interface or explore the sample game files provided with Time Warp.*