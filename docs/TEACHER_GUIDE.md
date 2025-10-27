# SuperPILOT Teacher Guide

**Teaching Programming with SuperPILOT**

---

## Overview

This guide helps educators effectively teach programming using SuperPILOT's multi-language environment. It includes curriculum suggestions, assessment strategies, and classroom management tips.

---

## Table of Contents

1. [Curriculum Planning](#curriculum-planning)
2. [Teaching Strategies](#teaching-strategies)
3. [Assessment & Grading](#assessment--grading)
4. [Classroom Management](#classroom-management)
5. [Differentiation](#differentiation)
6. [Project Ideas](#project-ideas)
7. [Troubleshooting](#troubleshooting)

---

## 1. Curriculum Planning

### Suggested Course Structure

#### **Unit 1: Introduction to PILOT (3-4 weeks)**

**Week 1: Text Output & Input**
- Learning Goals:
  - Understand program structure (line-by-line execution)
  - Use T: and A: commands
  - Store and display variables
- Activities:
  - "Hello World" variations
  - Mad Libs program
  - Simple questionnaire
- Assessment: Create personalized greeting program

**Week 2: Variables & Math**
- Learning Goals:
  - Use U: to set variables
  - Understand variable interpolation (*VAR*)
  - Basic arithmetic in expressions
- Activities:
  - Calculator programs
  - Unit converter (temperature, distance)
  - Shopping cart total
- Assessment: Multi-step calculation program

**Week 3: Conditionals**
- Learning Goals:
  - Use Y: for conditional execution
  - Understand comparison operators
  - Make branching decisions
- Activities:
  - Number guessing game
  - Quiz program
  - Choose-your-own-adventure
- Assessment: Interactive story with 3+ branches

**Week 4: Labels & Loops**
- Learning Goals:
  - Create labels with L:
  - Jump with J:
  - Build loops with Y: and J:
- Activities:
  - Countdown program
  - Menu system
  - Repetitive task automation
- Assessment: Multi-level game or interactive menu

#### **Unit 2: BASIC Programming (4-5 weeks)**

**Week 5: BASIC Fundamentals**
- Learning Goals:
  - Understand line numbers
  - Use PRINT, LET, INPUT
  - Compare PILOT vs BASIC syntax
- Activities:
  - Port PILOT programs to BASIC
  - Simple I/O programs
  - Variable manipulation
- Assessment: Create BASIC version of previous PILOT project

**Week 6: Control Structures**
- Learning Goals:
  - IF...THEN statements
  - Logical operators (AND, OR, NOT)
  - GOTO for control flow
- Activities:
  - Grade calculator
  - Number classifier (even/odd, prime)
  - Decision tree program
- Assessment: Complex decision-making program

**Week 7: Loops & Iteration**
- Learning Goals:
  - FOR...NEXT loops
  - STEP parameter
  - Nested loops
- Activities:
  - Times tables
  - Pattern generators
  - Animation loops
- Assessment: Generate multiplication table 1-12

**Week 8: Functions & Randomness**
- Learning Goals:
  - Built-in functions (RND, INT, ABS, etc.)
  - String functions (LEFT, RIGHT, MID)
  - Math operations
- Activities:
  - Dice rolling simulator
  - Random name generator
  - Simple games (dice, coin flip)
- Assessment: Complete game with random elements

**Week 9: Arrays & Data (Advanced)**
- Learning Goals:
  - DIM arrays
  - DATA, READ, RESTORE
  - GOSUB/RETURN for subroutines
- Activities:
  - Student grade tracker
  - Inventory system
  - Quiz with multiple questions
- Assessment: Data-driven application

#### **Unit 3: Logo Graphics (3-4 weeks)**

**Week 10: Turtle Basics**
- Learning Goals:
  - Understand coordinate system
  - Use FORWARD, BACK, LEFT, RIGHT
  - Pen control (UP/DOWN)
- Activities:
  - Draw basic shapes
  - Create initials
  - Geometric patterns
- Assessment: Draw house or robot

**Week 11: Loops in Logo**
- Learning Goals:
  - REPEAT command
  - Pattern creation
  - Nested loops
- Activities:
  - Polygon generator
  - Spirals and circles
  - Flower patterns
- Assessment: Complex symmetrical design

**Week 12: Procedures**
- Learning Goals:
  - TO...END definitions
  - Parameters with :VAR
  - Procedure reuse
- Activities:
  - Shape library
  - Modular scene creation
  - Recursive patterns
- Assessment: Scene with 5+ custom procedures

**Week 13: Creative Project**
- Learning Goals:
  - Combine all Logo skills
  - Plan complex graphics
  - Debug and iterate
- Activities:
  - Student choice project
  - Gallery walk
  - Peer feedback
- Assessment: Final Logo masterpiece with documentation

#### **Unit 4: Integration & Advanced Topics (2-3 weeks)**

**Week 14: Multi-Language Programs**
- Learning Goals:
  - When to use each language
  - Combine PILOT, BASIC, Logo in one program
  - Design patterns
- Activities:
  - Interactive graphics programs
  - Games with text and graphics
  - Educational simulations
- Assessment: Program using all three languages

**Week 15: Hardware Integration (Optional)**
- Learning Goals:
  - R: runtime commands
  - Arduino/Raspberry Pi basics
  - Sensors and actuators
- Activities:
  - LED control
  - Button input
  - Temperature monitoring
- Assessment: Simple IoT project

**Week 16: Final Project**
- Student-designed capstone project
- Presentation and demonstration
- Written reflection

---

## 2. Teaching Strategies

### Pedagogical Approaches

#### **1. Scaffolded Learning**

**Start Simple:**
```pilot
T:Hello
```

**Add Complexity Gradually:**
```pilot
T:Hello, what is your name?
A:NAME
T:Nice to meet you, *NAME*!
```

**Then More Features:**
```pilot
T:What is your name?
A:NAME
T:How old are you?
A:AGE
Y:AGE < 18
T:You are young, *NAME*!
Y:AGE >= 18
T:You are an adult, *NAME*!
```

#### **2. Pair Programming**

**Roles:**
- **Driver**: Types code, operates computer
- **Navigator**: Reads instructions, suggests solutions, spots errors

**Benefits:**
- Peer learning
- Reduced frustration
- Communication skills
- Collaborative problem-solving

**Tips:**
- Switch roles every 10-15 minutes
- Use timer for role swaps
- Both students submit the same code
- Encourage discussion, not just commands

#### **3. Live Coding**

**Techniques:**
- Think aloud while coding
- Make intentional mistakes and fix them
- Ask students to predict output
- Invite students to suggest next steps

**Example Session:**
```
Teacher: "Let's make a program that asks your age and tells you 
          how many years until you're 100."
          
Teacher: "What should we do first?"
Student: "Ask for their age!"
Teacher: "Good! In PILOT, how do we ask questions?"
Student: "Use A:"
Teacher: [Types] "A:AGE"
Teacher: "Now what?"
```

#### **4. Debugging as Learning**

**Intentional Bugs:**

Buggy Program:
```pilot
T:What is your name
A:NAME
T:Hello, *NAMES*!
```

**Ask students to:**
1. Run the program
2. Observe the error
3. Hypothesize the cause
4. Test their fix
5. Explain what was wrong

**Common bugs to teach:**
- Missing colon in PILOT
- Typo in variable name
- Wrong bracket count
- Infinite loops
- Off-by-one errors

#### **5. Project-Based Learning**

**Structure:**
1. **Hook**: Present engaging problem/challenge
2. **Explore**: Students research and experiment
3. **Plan**: Pseudocode or flowchart
4. **Implement**: Code incrementally
5. **Test**: Debug and refine
6. **Present**: Demo and explain

**Example Project: Virtual Pet**
- Students create interactive pet program
- Pet has hunger, happiness, energy
- Commands: feed, play, sleep
- Stats change over time
- Use any language(s)

---

## 3. Assessment & Grading

### Formative Assessment Strategies

#### **1. Code Reviews**

Walk around during lab time:
- Ask: "What does this line do?"
- Ask: "What would happen if we changed X to Y?"
- Have student explain their logic
- Check for understanding, not just working code

#### **2. Exit Tickets**

End-of-class quick checks:
- "Write a PILOT command that stores 10 in variable X"
- "What's wrong with this code: `REPEAT 4 FORWARD 50`"
- "How would you make a triangle in Logo?"

#### **3. Code Tracing**

Give students code, ask for output:
```basic
10 LET X = 5
20 LET Y = 3
30 LET Z = X + Y
40 PRINT Z
50 LET X = 10
60 PRINT Z
```
"What will this print? Why?"

#### **4. Self-Assessment Rubrics**

Students rate themselves:
- [ ] My program runs without errors
- [ ] My program meets all requirements
- [ ] My code is easy to read
- [ ] I used comments to explain tricky parts
- [ ] I tested edge cases

### Summative Assessment

#### **Project Rubric Template**

| Criteria | Beginning (1) | Developing (2) | Proficient (3) | Advanced (4) |
|----------|---------------|----------------|----------------|--------------|
| **Functionality** | Program doesn't run | Runs with major issues | Meets all requirements | Exceeds requirements |
| **Code Quality** | Hard to read, no structure | Some organization | Clear and organized | Excellent style, modular |
| **Problem Solving** | Minimal logic | Basic logic | Good problem decomposition | Creative, efficient solutions |
| **Debugging** | Cannot fix errors | Fixes with heavy help | Debugs independently | Anticipates and prevents bugs |
| **Documentation** | No comments | Minimal comments | Good explanations | Professional documentation |

#### **Sample Grading Weights**

**For Programming Projects:**
- Functionality: 40%
- Code Quality: 20%
- Problem Solving: 20%
- Documentation: 10%
- Presentation/Demo: 10%

**For Written Assignments:**
- Understanding: 50%
- Accuracy: 30%
- Clarity: 20%

### Portfolio Assessment

Students maintain portfolios with:
- 3-5 best programs
- Written reflections
- Screenshots of graphics
- Code documentation
- Growth narrative

---

## 4. Classroom Management

### Lab Setup

#### **Recommended Configuration**

**Small Class (<15 students):**
- One computer per student
- Teacher station with projector
- Student screens visible to teacher

**Large Class (15-30 students):**
- Pair programming (2 students per computer)
- Teacher station
- Consider lab monitors/helpers

**Remote Learning:**
- Share screen during demos
- Breakout rooms for pair programming
- Use chat for quick questions

### Time Management

#### **Typical Class Structure (50 minutes)**

```
0-5 min:    Do Now / Warm-up
5-15 min:   Mini-lesson / Demo
15-40 min:  Lab Time / Practice
40-45 min:  Share Out / Examples
45-50 min:  Exit Ticket / Cleanup
```

#### **Lab Time Tips**

- Set clear timer for transitions
- Use "Ask 3 Before Me" rule (ask 3 peers before teacher)
- Circulate constantly
- Use popsicle sticks for random selection
- Have extension challenges ready

### Behavior Management

#### **Computer Lab Rules**

1. **No typing during instruction**
2. **Follow along when demonstrated**
3. **Save work frequently**
4. **Help neighbors (but no doing their work)**
5. **Stay on task - programming only**

#### **Intervention Strategies**

**Off-task behavior:**
- Give specific redirection
- Move closer to student
- Assign specific mini-goal
- Partner with on-task student

**Frustration:**
- Acknowledge the difficulty
- Break problem into smaller steps
- Celebrate small wins
- Remind them everyone struggles

---

## 5. Differentiation

### For Struggling Students

#### **Strategies:**

1. **Provide starter code**
```pilot
REM Fill in the blanks:
T:What is your name?
A:_____
T:Hello, *_____*!
```

2. **Use visual aids**
- Flowcharts
- Command reference cards
- Annotated examples

3. **Break tasks down**
Instead of "Make a calculator":
- Step 1: Get two numbers
- Step 2: Add them
- Step 3: Show result
- Step 4: Add other operations

4. **Peer tutoring**
- Partner with advanced student
- Assign specific helper role
- Structured collaboration

5. **Simplified requirements**
- Reduce feature count
- Accept working program in any language
- Focus on core concepts only

### For Advanced Students

#### **Extension Activities:**

1. **Optimization Challenges**
"Make your solution shorter/faster/more efficient"

2. **Feature Addition**
"Add these extra features to your program"

3. **Code Golf**
"Write the shortest program that does X"

4. **Teaching Others**
"Create a tutorial for this concept"

5. **Open-ended Projects**
"Design and build anything you want"

#### **Advanced Topics:**

- **Recursion** in Logo procedures
- **Data structures** with BASIC arrays
- **Algorithm efficiency** (bubble sort, etc.)
- **Hardware integration** with Arduino/RPi
- **Multi-threading** concepts
- **File I/O** operations

### Universal Design for Learning (UDL)

#### **Multiple Means of Representation:**
- Text instructions + video demos
- Code + flowcharts
- Visual + auditory explanations

#### **Multiple Means of Engagement:**
- Choice of project topics
- Game-based vs. practical applications
- Individual vs. collaborative work

#### **Multiple Means of Expression:**
- Written code + verbal explanation
- Presentation + documentation
- Video demo + live coding

---

## 6. Project Ideas

### Beginner Projects (PILOT)

1. **Mad Libs Generator**
   - Ask for nouns, verbs, adjectives
   - Insert into story template
   - Display funny result

2. **Choose Your Own Adventure**
   - Multi-path story
   - User decisions change outcome
   - At least 3 different endings

3. **Simple Quiz**
   - 5-10 questions
   - Track score
   - Give feedback

4. **Chatbot**
   - Respond to keywords
   - Simulate conversation
   - Personalized responses

### Intermediate Projects (BASIC)

1. **Number Guessing Game**
   - Computer picks random number
   - Player guesses
   - Hints (higher/lower)
   - Count attempts

2. **Grade Calculator**
   - Input multiple test scores
   - Calculate average
   - Assign letter grade
   - Show statistics

3. **Simple Encryption**
   - Caesar cipher
   - Encode/decode messages
   - User-chosen shift value

4. **Statistics Program**
   - Input dataset
   - Calculate mean, median, mode
   - Find min/max
   - Display results

### Advanced Projects (Logo)

1. **Geometric Art Generator**
   - User parameters (size, color, complexity)
   - Procedural generation
   - Save designs

2. **Animated Scene**
   - Multi-object scene
   - Simple animation
   - Interactive elements

3. **Fractal Explorer**
   - Recursive procedures
   - Koch snowflake, Sierpinski triangle
   - Parameterized depth

4. **Interactive Game**
   - Maze navigation
   - Collision detection
   - Score keeping

### Multi-Language Integration

1. **Educational Simulation**
   - PILOT: Menu and instructions
   - BASIC: Calculations and logic
   - Logo: Visual representation

2. **Data Visualization Tool**
   - PILOT: Data entry
   - BASIC: Statistical analysis
   - Logo: Chart/graph display

3. **Interactive Story with Graphics**
   - PILOT: Narrative and choices
   - Logo: Scene illustrations
   - BASIC: Game logic

### Real-World Applications

1. **Unit Converter**
   - Temperature, distance, weight
   - Multiple units
   - Bidirectional conversion

2. **Budget Tracker**
   - Income and expenses
   - Category tracking
   - Balance calculation

3. **Study Timer**
   - Pomodoro technique
   - Break reminders
   - Session tracking

4. **Password Generator**
   - Random character selection
   - Length customization
   - Strength indicator

---

## 7. Troubleshooting

### Common Student Issues

#### **Issue: "It doesn't work!"**

**Debugging Protocol:**
1. "What were you trying to do?"
2. "What happened instead?"
3. "What line do you think has the problem?"
4. "Let's run it step-by-step" (use debugger)

#### **Issue: Infinite Loops**

**Symptoms:**
- Program hangs
- No output
- Stop button needed

**Teaching Moment:**
```pilot
U:COUNT=0
L:LOOP
T:*COUNT*
J:LOOP          REM Always jumps - never ends!
```

**Fix:**
```pilot
U:COUNT=0
L:LOOP
T:*COUNT*
U:COUNT=COUNT+1
Y:COUNT < 10    REM Condition to continue
J:LOOP
```

#### **Issue: Variable Not Found**

**Common Cause:**
```pilot
A:NAME          REM Stored as NAME
T:Hello, *NAMES*!    REM Looking for NAMES (typo)
```

**Strategy:**
- Check spelling carefully
- Use variables panel in debugger
- Show all defined variables

#### **Issue: Graphics Not Appearing**

**Checklist:**
- Did you use Logo commands?
- Is pen down? (PENDOWN)
- Is canvas cleared? (CS at start)
- Are values reasonable? (FORWARD 1000000 goes off screen)

### Technical Issues

#### **SuperPILOT Won't Start**

**Checks:**
1. Python version: `python3 --version` (need 3.8+)
2. Tkinter installed: `python3 -c "import tkinter"`
3. File permissions: Check Super_PILOT.py is readable
4. Dependencies: `pip install -r requirements-dev.txt`

#### **Slow Performance**

**Causes:**
- Very large programs (1000+ lines)
- Complex graphics (1000+ turtle moves)
- Infinite loops
- Too many callbacks

**Solutions:**
- Break into smaller programs
- Optimize graphics (use filled shapes)
- Add loop counters
- Remove unnecessary print statements

#### **Save/Load Issues**

**Checks:**
- File permissions in directory
- Disk space available
- Valid file path
- Proper file extension (.spt, .pil, .bas, .logo)

---

## Assessment Bank

### Quick Checks (5 minutes)

**1. PILOT Variables**
```
What is the output?
U:X=5
T:The value is *X*
U:X=10
T:Now it is *X*
```

**2. BASIC Loop**
```
What numbers does this print?
10 FOR I = 2 TO 10 STEP 2
20   PRINT I
30 NEXT I
```

**3. Logo Angles**
```
What shape does this make?
REPEAT 6 [FORWARD 50 RIGHT 60]
```

### Longer Assessments (15-30 minutes)

**1. Debug This Code**
```pilot
T:Guess a number
A:GUES
U:SECRET=7
Y:GUESS = SECRET
T:Correct
```

**2. Fill in the Blanks**
```basic
10 PRINT "Fahrenheit to Celsius"
20 INPUT FAHR
30 LET CELSIUS = (FAHR - ____) * ____ / ____
40 PRINT FAHR; "F = "; CELSIUS; "C"
```

**3. Design Challenge**
"Write pseudocode for a program that:
- Asks for 3 test scores
- Calculates the average
- Prints letter grade (A/B/C/D/F)"

---

## Resources

### Supplementary Materials

**Student Handouts:**
- Command reference cards (one per language)
- Debugging checklist
- Project planning worksheet
- Code review guide

**Example Programs:**
- Annotated sample code
- Common patterns library
- Bug fix examples
- Style guide

**Visual Aids:**
- Flowchart symbols poster
- Coordinate system diagram (Logo)
- Operator precedence chart
- Color code reference (Logo)

### Extension Resources

**Books:**
- "Logo Programming for the Beginner"
- "BASIC Computer Games" (David Ahl)
- "Turtle Geometry" (Abelson & diSessa)

**Websites:**
- Computer Science Unplugged activities
- Hour of Code challenges
- Logo Foundation resources
- Scratch to text-based transition guides

**Integration:**
- Math: Geometry, algebra, statistics
- Science: Simulations, data analysis
- Art: Generative art, fractals
- English: Interactive fiction, storytelling

---

## Frequently Asked Questions

### Pedagogical Questions

**Q: Should I start with PILOT, BASIC, or Logo?**

A: PILOT is recommended for absolute beginners due to simple syntax. Logo works well for visual learners. BASIC is good for students with some programming experience.

**Q: How much time should students spend on each language?**

A: Suggested: 4 weeks PILOT, 5 weeks BASIC, 4 weeks Logo, 2-3 weeks integration. Adjust based on student pace.

**Q: Should I allow students to use only one language?**

A: Encourage trying all three, but allow specialization for final projects. Each language teaches different concepts.

**Q: How do I grade partial credit?**

A: Use rubric with multiple criteria. A program with bugs can still show good problem-solving and effort.

### Technical Questions

**Q: Can students work on this at home?**

A: Yes, SuperPILOT runs on Windows, Mac, Linux, and Raspberry Pi. Share Super_PILOT.py or have students clone from GitHub.

**Q: How do I prevent students from accessing solutions online?**

A: Create unique project requirements, require documentation of process, check understanding through verbal explanation.

**Q: What if a student's program is too long?**

A: Introduce procedures/functions, teach modular design, encourage breaking into multiple files.

**Q: Can SuperPILOT connect to real hardware?**

A: Yes! It supports Arduino and Raspberry Pi GPIO with simulation mode for testing without hardware.

---

## Conclusion

SuperPILOT provides a rich, multi-paradigm environment for teaching programming fundamentals. Its three languages offer different entry points and teaching opportunities:

- **PILOT**: Simplicity, text processing, decision making
- **BASIC**: Classic programming, numerical computation, algorithms
- **Logo**: Visual feedback, geometry, creative expression

By scaffolding carefully, differentiating instruction, and providing engaging projects, you can help all students develop computational thinking skills and programming confidence.

**Remember:**
- Start simple, build gradually
- Make it relevant to student interests
- Celebrate mistakes as learning opportunities
- Code together, learn together

**Good luck, and happy teaching!** 🎓💻
