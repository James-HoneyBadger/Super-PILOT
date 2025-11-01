# Time Warp Web Edition

A comprehensive web-based IDE for educational programming languages including PILOT, BASIC, and Logo.

## Features

- **Multi-Language Support**: 
  - PILOT (Programmed Inquiry, Learning, Or Teaching)
  - BASIC (Beginner's All-purpose Symbolic Instruction Code)
  - Logo (turtle graphics programming)
  
- **Professional IDE Features**:
  - Syntax highlighting and line numbers
  - Interactive debugging with breakpoints
  - Variable inspection and watches
  - Performance monitoring and metrics
  - Execution timeline tracking
  - Code snippets library
  - Comprehensive help system

- **Graphics Engine**:
  - Full turtle graphics implementation
  - HTML5 Canvas-based rendering
  - Interactive graphics with export capabilities
  - Grid overlay and coordinate system

- **Modern Web Technologies**:
  - Responsive design for desktop and mobile
  - Local storage for program persistence
  - Professional UI with tabbed interface
  - Error handling and user feedback

## Getting Started

### Running Locally

1. Clone or download the Time Warp project
2. Navigate to the `Time_Warp_Web` directory
3. Open `index.html` in a modern web browser
4. Start programming!

### Online Deployment

Simply upload all files to any web server or hosting platform. The IDE runs entirely in the browser with no server-side requirements.

## Usage

1. **Choose Language Mode**: Select PILOT, BASIC, Logo, or Auto-Detect from the dropdown
2. **Write Your Program**: Use the code editor with line numbers and syntax support
3. **Run or Debug**: Click Run for normal execution or Debug for step-by-step
4. **Explore Tabs**: 
   - Output: Program messages and results
   - Variables: Live variable values and watches
   - Graphics: Turtle drawing canvas
   - Performance: Execution metrics and timing
   - Timeline: Step-by-step execution history
   - Snippets: Pre-built code examples
   - Help: Language reference and examples

## Example Programs

### PILOT Example
```
T:Welcome to PILOT!
A:name
T:Hello *name*!
R:5 * 10 -> result
T:5 times 10 equals *result*
E:
```

### BASIC Example
```
10 PRINT "Counting to 10"
20 FOR I = 1 TO 10
30   PRINT "Count: "; I
40 NEXT I
50 END
```

### Logo Example
```
CLEARSCREEN
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

## File Structure

```
Time_Warp_Web/
├── index.html          # Main IDE interface
├── styles.css          # Professional styling
├── js/
│   ├── interpreter.js  # Multi-language interpreter
│   ├── graphics.js     # Turtle graphics engine
│   ├── ui.js          # User interface controller
│   └── app.js         # Application initialization
└── README.md          # This file
```

## Browser Compatibility

- **Recommended**: Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- **Requirements**: ES6 support, HTML5 Canvas, Local Storage
- **Mobile**: Responsive design supports tablets and smartphones

## Educational Use

Time Warp Web is designed for:
- Programming education at all levels
- Computer science classrooms
- Self-directed learning
- Historical programming language exploration
- Turtle graphics and computational thinking

## Technical Details

### Architecture
- Pure client-side application (no server required)
- Modular JavaScript ES6+ with classes
- HTML5 Canvas for graphics rendering
- CSS3 with responsive design principles

### Performance
- Efficient interpreter with configurable execution limits
- Real-time performance monitoring
- Memory usage tracking
- Execution timeline for debugging

### Features
- Complete PILOT, BASIC, and Logo language implementations
- Variable interpolation and expression evaluation
- Debugging with breakpoints and step execution
- Professional code editor with line numbers
- Interactive turtle graphics with export
- Comprehensive help system and examples

## Development

The code is well-structured for educational purposes and further development:

- `interpreter.js`: Contains the core language interpreters
- `graphics.js`: Turtle graphics implementation
- `ui.js`: User interface management and interactions
- `app.js`: Application lifecycle and initialization

## License

Part of the Time Warp educational programming suite.

## Version History

- **2.1.0 Web**: Complete web-based IDE with all desktop features
- **2.0.x**: Desktop versions with native implementations
- **1.x**: Original PILOT interpreter versions

---

Start programming and explore the fascinating world of educational programming languages with Time Warp Web Edition!