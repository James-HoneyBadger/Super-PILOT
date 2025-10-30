# TempleCode Student Guide

**Learning to Program with TempleCode**

---

## Welcome to Programming! 🚀

TempleCode is your friendly environment for learning three different programming languages. This guide will take you from complete beginner to confident programmer.

---

## Getting Started

### What You'll Learn

- **PILOT**: Simple text and input/output programs
- **BASIC**: Classic programming with numbers and logic
- **Logo**: Drawing pictures with turtle graphics

### Opening TempleCode

1. Double-click `TempleCode.py` or run from terminal:
   ```bash
   python3 TempleCode.py
   ```

2. You'll see three areas:
   - **Editor** (top): Where you write programs
   - **Output** (bottom-left): Where results appear
   - **Graphics** (bottom-right): Where turtle draws

---

## Part 1: PILOT Language - Your First Programs

### Lesson 1: Hello World

Let's make the computer say hello!

```pilot
T:Hello, World!
T:Welcome to programming!
```

**Try it:**
1. Type this in the editor
2. Click ▶ **Run** (or press F5)
3. See the output!

**What happened?**
- `T:` means "Type" or "Tell" - it shows text on screen
- Each line is a separate instruction

**Exercise:** Make it say your name:
```pilot
T:My name is [Your Name]
T:I am learning to program!
```

### Lesson 2: Getting Input

Now let's make programs interactive:

```pilot
T:What is your name?
A:NAME
T:Hello, *NAME*!
T:Nice to meet you!
```

**New commands:**
- `A:NAME` - Ask the user, store answer in NAME
- `*NAME*` - Show the value stored in NAME

**Exercise:** Ask for age too:
```pilot
T:What is your name?
A:NAME
T:How old are you?
A:AGE
T:Hello, *NAME*! You are *AGE* years old.
```

### Lesson 3: Variables (Storing Information)

Variables are like boxes that hold information:

```pilot
U:SCORE=0
T:Your score is *SCORE*

U:SCORE=10
T:Now your score is *SCORE*

U:SCORE=100
T:Great! Your score is *SCORE*
```

**What's happening?**
- `U:SCORE=0` - Use (set) SCORE to 0
- Variables remember their value
- We can change them anytime

**Exercise:** Make a counter:
```pilot
U:COUNT=1
T:Count: *COUNT*

U:COUNT=2
T:Count: *COUNT*

U:COUNT=3
T:Count: *COUNT*
```

### Lesson 4: Making Decisions

Programs can make choices:

```pilot
T:What is your favorite color?
A:COLOR

Y:COLOR == blue
T:Blue is a cool color!

Y:COLOR == red
T:Red is an exciting color!

Y:COLOR == green
T:Green is a nature color!
```

**New command:**
- `Y:condition` - Yes, if condition is true, the next `T:` runs
- `==` means "equals"

**Exercise:** Make a number guesser:
```pilot
U:SECRET=7
T:Guess a number between 1 and 10:
A:GUESS

Y:GUESS == SECRET
T:Correct! You got it!

Y:GUESS != SECRET
T:Sorry, try again!
```

### Lesson 5: Loops with Labels

Make programs repeat:

```pilot
U:COUNT=0
L:LOOP

T:Count is *COUNT*
U:COUNT=COUNT+1

Y:COUNT < 5
J:LOOP

T:Done counting!
```

**New commands:**
- `L:LOOP` - Label (marks a spot)
- `J:LOOP` - Jump to label
- Combine with `Y:` to make loops!

**Exercise:** Countdown from 10:
```pilot
U:NUMBER=10
L:START

T:*NUMBER*
U:NUMBER=NUMBER-1

Y:NUMBER > 0
J:START

T:Blast off!
```

---

## Part 2: BASIC Language - Math and Logic

### Lesson 6: Your First BASIC Program

BASIC uses line numbers:

```basic
10 PRINT "Hello from BASIC!"
20 PRINT "2 + 2 = "; 2 + 2
30 END
```

**Key differences:**
- Lines start with numbers (10, 20, 30...)
- `PRINT` instead of `T:`
- Semicolon `;` combines text and numbers

**Exercise:** Make a calculator:
```basic
10 PRINT "Simple Calculator"
20 LET A = 5
30 LET B = 3
40 PRINT "A + B = "; A + B
50 PRINT "A * B = "; A * B
60 END
```

### Lesson 7: Variables in BASIC

```basic
10 LET NAME = "Alice"
20 LET AGE = 12
30 LET SCORE = 95
40 PRINT NAME; " is "; AGE; " years old"
50 PRINT "Score: "; SCORE
60 END
```

**Try these operators:**
- `+` addition
- `-` subtraction
- `*` multiplication
- `/` division

**Exercise:** Temperature converter:
```basic
10 PRINT "Fahrenheit to Celsius"
20 LET FAHR = 72
30 LET CELSIUS = (FAHR - 32) * 5 / 9
40 PRINT FAHR; "F = "; CELSIUS; "C"
50 END
```

### Lesson 8: IF Statements

```basic
10 LET SCORE = 85
20 IF SCORE >= 90 THEN PRINT "Grade: A"
30 IF SCORE >= 80 AND SCORE < 90 THEN PRINT "Grade: B"
40 IF SCORE >= 70 AND SCORE < 80 THEN PRINT "Grade: C"
50 IF SCORE < 70 THEN PRINT "Grade: F"
60 END
```

**Comparison operators:**
- `=` equals
- `<>` not equal
- `<` less than
- `>` greater than
- `<=` less than or equal
- `>=` greater than or equal

### Lesson 9: FOR Loops

Count automatically:

```basic
10 PRINT "Counting to 10:"
20 FOR I = 1 TO 10
30   PRINT I
40 NEXT I
50 PRINT "Done!"
60 END
```

**Loop variations:**
```basic
10 REM Count by 2s
20 FOR I = 0 TO 20 STEP 2
30   PRINT I
40 NEXT I

50 REM Count backwards
60 FOR I = 10 TO 1 STEP -1
70   PRINT I
80 NEXT I
90 END
```

**Exercise:** Times table:
```basic
10 PRINT "5 Times Table"
20 FOR I = 1 TO 10
30   LET RESULT = 5 * I
40   PRINT "5 x "; I; " = "; RESULT
50 NEXT I
60 END
```

### Lesson 10: Random Numbers

```basic
10 PRINT "Dice Roller"
20 LET DICE = INT(RND(6)) + 1
30 PRINT "You rolled: "; DICE
40 END
```

**Exercise:** Number guessing game:
```basic
10 LET SECRET = INT(RND(10)) + 1
20 PRINT "Guess a number (1-10):"
30 INPUT GUESS
40 IF GUESS = SECRET THEN GOTO 70
50 PRINT "Wrong! Try again."
60 GOTO 20
70 PRINT "Correct! The number was "; SECRET
80 END
```

---

## Part 3: Logo Language - Turtle Graphics

### Lesson 11: Drawing Your First Shape

Logo uses a "turtle" that draws as it moves:

```logo
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
```

**Turtle commands:**
- `FORWARD 100` - Move forward 100 pixels
- `RIGHT 90` - Turn right 90 degrees
- Watch the turtle draw!

**What shape did it make?** (Almost a square!)

### Lesson 12: Complete Square

```logo
CS
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
```

**New command:**
- `CS` - Clear Screen (start fresh)

**Exercise:** Try different sizes:
```logo
CS
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
FORWARD 50
RIGHT 90
```

### Lesson 13: Using REPEAT

Make loops easier:

```logo
CS
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

**Much shorter!** One square in just 4 lines.

**Exercise:** Triangle:
```logo
CS
REPEAT 3 [
  FORWARD 100
  RIGHT 120
]
```

**Why 120 degrees?** (360 ÷ 3 = 120)

### Lesson 14: Cool Patterns

```logo
CS
REPEAT 36 [
  FORWARD 100
  RIGHT 10
]
```

**Exercise:** Flower pattern:
```logo
CS
REPEAT 12 [
  REPEAT 4 [
    FORWARD 50
    RIGHT 90
  ]
  RIGHT 30
]
```

### Lesson 15: Colors and Pen Control

```logo
CS
SETCOLOR 1
PENSIZE 3
FORWARD 100

PENUP
FORWARD 20
PENDOWN

SETCOLOR 2
FORWARD 100
```

**New commands:**
- `SETCOLOR n` - Change pen color (0-9)
- `PENSIZE n` - Change line thickness
- `PENUP` - Stop drawing (lift pen)
- `PENDOWN` - Start drawing

**Exercise:** Rainbow line:
```logo
CS
SETCOLOR 1
FORWARD 50
SETCOLOR 2
FORWARD 50
SETCOLOR 3
FORWARD 50
SETCOLOR 4
FORWARD 50
```

### Lesson 16: Creating Procedures

Make your own commands:

```logo
TO SQUARE :SIZE
  REPEAT 4 [
    FORWARD :SIZE
    RIGHT 90
  ]
END

CS
SQUARE 50
PENUP
FORWARD 70
PENDOWN
SQUARE 30
```

**What's happening?**
- `TO SQUARE :SIZE` - Define procedure with parameter
- `:SIZE` - Use the parameter value
- `END` - Finish the procedure
- `SQUARE 50` - Call it with size 50

**Exercise:** Make a house:
```logo
TO HOUSE :SIZE
  REM Draw square
  REPEAT 4 [
    FORWARD :SIZE
    RIGHT 90
  ]
  REM Draw roof
  FORWARD :SIZE
  RIGHT 30
  FORWARD :SIZE
  RIGHT 120
  FORWARD :SIZE
END

CS
HOUSE 100
```

---

## Part 4: Practice Projects

### Project 1: About Me Program (PILOT)

```pilot
T:=============================
T:      ABOUT ME
T:=============================

T:What is your name?
A:NAME

T:How old are you?
A:AGE

T:What is your favorite hobby?
A:HOBBY

T:
T:=============================
T:*NAME*'s Profile
T:=============================
T:Age: *AGE*
T:Hobby: *HOBBY*
T:=============================
```

### Project 2: Math Quiz (BASIC)

```basic
10 PRINT "MATH QUIZ"
20 PRINT
30 LET NUM1 = INT(RND(10)) + 1
40 LET NUM2 = INT(RND(10)) + 1
50 LET ANSWER = NUM1 + NUM2
60 PRINT "What is "; NUM1; " + "; NUM2; "?"
70 INPUT GUESS
80 IF GUESS = ANSWER THEN GOTO 110
90 PRINT "Wrong! Try again."
100 GOTO 70
110 PRINT "Correct!"
120 END
```

### Project 3: House Drawing (Logo)

```logo
TO HOUSE :SIZE
  REM Square base
  REPEAT 4 [
    FORWARD :SIZE
    RIGHT 90
  ]
  
  REM Roof
  RIGHT 30
  FORWARD :SIZE
  RIGHT 120
  FORWARD :SIZE
  RIGHT 150
  
  REM Door
  FORWARD :SIZE / 4
  RIGHT 90
  FORWARD :SIZE / 3
  REPEAT 3 [
    RIGHT 90
    FORWARD :SIZE / 3
  ]
END

CS
HOUSE 100
```

### Project 4: Story Adventure (PILOT)

```pilot
L:START
T:You are in a dark forest.
T:There are two paths ahead.
T:Which way do you go? (left/right)
A:CHOICE

Y:CHOICE == left
J:LEFT_PATH

Y:CHOICE == right
J:RIGHT_PATH

T:Invalid choice!
J:START

L:LEFT_PATH
T:You find a treasure chest!
T:You win!
E:

L:RIGHT_PATH
T:You encounter a dragon!
T:Game over!
E:
```

---

## Part 5: Debugging Tips

### Common Mistakes

**Forgot the colon in PILOT:**
```pilot
T Hello     ❌ Wrong
T:Hello     ✅ Correct
```

**Wrong line number order in BASIC:**
```basic
10 PRINT "First"
30 PRINT "Second"
20 PRINT "This runs second!"  ❌ Confusing!
```

**Forgot to close brackets in Logo:**
```logo
REPEAT 4 [
  FORWARD 100    ❌ Missing ]
```

### Using the Debugger

1. Click 🐛 **Debug** to enable debug mode
2. Click next to line numbers to set breakpoints (red dots)
3. Click ➡ **Step** to run one line at a time
4. Watch variables in the right panel
5. See which line is running (highlighted)

### Getting Help

**In TempleCode:**
- Press `F1` for help menu
- Check the OUTPUT panel for error messages
- Look at the VARIABLES panel to see what's stored

**Remember:**
- Start simple, then add more
- Test after each change
- Read error messages carefully
- Try examples from this guide

---

## Challenge Projects

### 🌟 Challenge 1: Temperature Converter (Your Choice!)

Make a program that converts between Fahrenheit and Celsius.
- Let user choose direction
- Show the formula
- Use any language you prefer

### 🌟 Challenge 2: Drawing Gallery (Logo)

Create a gallery of shapes:
- Circle (use REPEAT 360)
- Star (5 points)
- Spiral (increasing size)
- Your own design!

### 🌟 Challenge 3: Text Adventure (PILOT)

Make a multi-room adventure:
- At least 3 rooms
- Items to collect
- Choices that matter
- Win condition

### 🌟 Challenge 4: Calculator (BASIC)

Build a full calculator:
- Menu of operations (+, -, *, /)
- Input two numbers
- Show result
- Let user try again

---

## Next Steps

### You've learned:
✅ Three programming languages  
✅ Variables and math  
✅ Decisions and loops  
✅ Procedures and functions  
✅ Graphics and animation  
✅ Debugging skills

### Keep learning:
- Try mixing languages in one program!
- Study the example programs in `/examples`
- Read the Teacher Guide for advanced topics
- Experiment and have fun!

---

## Quick Reference Card

### PILOT Commands
```
T:text          Output text
A:var           Get input
U:var=value     Set variable
Y:condition     If true, run next
J:label         Jump to label
L:label         Define label
E:              End program
```

### BASIC Commands
```
PRINT           Output
LET var = val   Assign
INPUT var       Get input
IF...THEN       Conditional
FOR...NEXT      Loop
GOTO linenum    Jump
END             End program
```

### Logo Commands
```
FORWARD n       Move forward
BACK n          Move back
RIGHT n         Turn right
LEFT n          Turn left
REPEAT n [...]  Loop
CS              Clear screen
PENUP/PENDOWN   Stop/start drawing
```

### Keyboard Shortcuts
```
F5              Run program
F8              Debug mode
F10             Step (debug)
Ctrl+S          Save file
Ctrl+O          Open file
Ctrl+N          New file
```

---

**Happy Programming!** 💻✨

Remember: Every programmer started exactly where you are. Keep practicing, stay curious, and don't be afraid to make mistakes - that's how we learn!
