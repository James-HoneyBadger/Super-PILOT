Tutorials
=========

Welcome to the Time Warp IDE interactive tutorials! These step-by-step guides will help you learn programming with PILOT, BASIC, and Logo languages.

PILOT Tutorials
===============

Tutorial 1: Hello World
-----------------------

**Objective:** Create your first PILOT program that displays text.

**Steps:**

1. Start Time Warp IDE
2. Create a new file (Ctrl+N)
3. Select PILOT as the language
4. Type the following program:

   .. code-block:: none

      T:Hello, World!
      T:Welcome to PILOT programming!
      T:This is your first program.
      END

5. Click Run (F5) to execute
6. Observe the output in the Output tab

**What you learned:**

* ``T:`` command displays text
* ``END`` terminates the program
* Programs execute sequentially

Tutorial 2: Variables and Input
-------------------------------

**Objective:** Learn to use variables and accept user input.

**Steps:**

1. Create a new PILOT program
2. Type this interactive program:

   .. code-block:: none

      T:What's your name?
      A:NAME
      T:Hello, *NAME*! Welcome to Time Warp IDE.
      T:
      T:How old are you?
      A:AGE
      T:You are *AGE* years old. That's great!
      END

3. Run the program
4. Enter your name and age when prompted

**What you learned:**

* ``A:`` command accepts input into variables
* ``*VARIABLE*`` syntax displays variable values
* Variables store user input for later use

Tutorial 3: Simple Math
-----------------------

**Objective:** Perform calculations and display results.

**Steps:**

1. Create this calculation program:

   .. code-block:: none

      T:Simple Math Calculator
      T:
      U:A=15
      U:B=25
      U:SUM=*A*+*B*
      U:PRODUCT=*A***B*
      T:A = *A*, B = *B*
      T:Sum = *SUM*
      T:Product = *PRODUCT*
      END

2. Run and observe the mathematical operations

**What you learned:**

* ``U:`` command assigns values to variables
* Mathematical operators: ``+``, ``*``
* Variable interpolation in text output

BASIC Tutorials
===============

Tutorial 1: Number Crunching
----------------------------

**Objective:** Learn BASIC variable assignment and arithmetic.

**Steps:**

1. Create a new BASIC program:

   .. code-block:: basic

      10 REM Simple Calculator
      20 LET A = 10
      30 LET B = 20
      40 LET SUM = A + B
      50 LET PRODUCT = A * B
      60 PRINT "A = "; A; ", B = "; B
      70 PRINT "Sum = "; SUM
      80 PRINT "Product = "; PRODUCT
      90 END

2. Run the program and see the calculations

**What you learned:**

* Line numbers organize BASIC programs
* ``LET`` assigns values to variables
* ``PRINT`` displays output
* ``REM`` creates comments

Tutorial 2: User Input
----------------------

**Objective:** Get input from the user and process it.

**Steps:**

1. Create an interactive BASIC program:

   .. code-block:: basic

      10 PRINT "Temperature Converter"
      20 PRINT "Enter temperature in Celsius:"
      30 INPUT C
      40 LET F = C * 9 / 5 + 32
      50 PRINT C; " Celsius = "; F; " Fahrenheit"
      60 PRINT "Convert another? (Y/N):"
      70 INPUT CHOICE$
      80 IF CHOICE$ = "Y" THEN GOTO 20
      90 PRINT "Goodbye!"
      100 END

2. Run and test with different temperatures

**What you learned:**

* ``INPUT`` gets user input
* Mathematical calculations
* ``IF...THEN`` conditional execution
* ``GOTO`` for program flow control

Tutorial 3: Looping
-------------------

**Objective:** Use FOR loops to repeat actions.

**Steps:**

1. Create a counting program:

   .. code-block:: basic

      10 PRINT "Counting Program"
      20 FOR I = 1 TO 10
      30 PRINT "Count: "; I
      40 NEXT I
      50 PRINT "All done!"
      60 END

2. Run and observe the loop execution

**What you learned:**

* ``FOR...NEXT`` creates loops
* Loop variables increment automatically
* Code between FOR and NEXT repeats

Logo Tutorials
==============

Tutorial 1: First Steps
-----------------------

**Objective:** Learn basic turtle movement commands.

**Steps:**

1. Create a simple Logo program:

   .. code-block:: none

      FORWARD 100
      RIGHT 90
      FORWARD 100
      RIGHT 90
      FORWARD 100
      RIGHT 90
      FORWARD 100

2. Run and watch the turtle draw a square

**What you learned:**

* ``FORWARD`` moves the turtle
* ``RIGHT`` turns the turtle
* Turtle graphics are visual and immediate

Tutorial 2: Pen Control
-----------------------

**Objective:** Learn to control when the turtle draws.

**Steps:**

1. Create a program with pen control:

   .. code-block:: none

      CLEARSCREEN
      PENUP
      FORWARD 50
      PENDOWN
      FORWARD 100
      PENUP
      RIGHT 90
      FORWARD 50
      PENDOWN
      FORWARD 100

2. Run and see the dashed line effect

**What you learned:**

* ``PENUP`` stops drawing
* ``PENDOWN`` starts drawing
* ``CLEARSCREEN`` resets the canvas

Tutorial 3: Shapes and Patterns
-------------------------------

**Objective:** Create more complex geometric patterns.

**Steps:**

1. Create a star pattern:

   .. code-block:: none

      CLEARSCREEN
      FOR I = 1 TO 5
      FORWARD 100
      RIGHT 144
      NEXT I

2. Run and observe the star shape

**What you learned:**

* Nested loops create complex patterns
* Angles determine shape characteristics
* Repetition creates geometric figures

Advanced Tutorials
==================

Mixed Language Programming
--------------------------

**Objective:** Combine PILOT, BASIC, and Logo in one program.

**Steps:**

1. Create a comprehensive program:

   .. code-block:: none

      REM BASIC section for calculations
      LET RADIUS = 50
      LET CIRCUMFERENCE = 2 * 3.14159 * RADIUS

      L:PILOT_GREETING
      T:Welcome to Mixed Language Demo!
      T:We'll draw a circle with radius *RADIUS*
      T:Circumference = *CIRCUMFERENCE*

      REM Logo section for drawing
      CLEARSCREEN
      PENUP
      FORWARD RADIUS
      LEFT 90
      PENDOWN

      REM Draw circle approximation
      FOR I = 1 TO 36
      FORWARD 8.7
      RIGHT 10
      NEXT I

      HOME
      END

2. Run and see all languages working together

**What you learned:**

* Languages can be mixed in one file
* Each language handles different tasks
* Seamless integration between languages

Debugging Tutorial
------------------

**Objective:** Learn to use the debugging tools.

**Steps:**

1. Create a program with intentional issues:

   .. code-block:: basic

      10 LET A = 10
      20 LET B = 0
      30 LET C = A / B  ' This will cause an error
      40 PRINT "Result: "; C
      50 END

2. Run with debugger (F6)
3. Set breakpoint on line 30
4. Step through execution
5. Observe variable values in Watch tab

**What you learned:**

* Debugger helps find program errors
* Breakpoints pause execution
* Variable watching shows program state
* Step execution reveals logic flow

Exercises
=========

Beginner Exercises
------------------

1. **Greeting Program**
   Write a PILOT program that asks for the user's name and favorite color, then displays a personalized message.

2. **Simple Calculator**
   Create a BASIC program that asks for two numbers and displays their sum, difference, product, and quotient.

3. **Square Drawer**
   Write a Logo program that draws a square of any size specified by the user.

Intermediate Exercises
----------------------

1. **Temperature Table**
   Create a BASIC program that displays a table of Celsius to Fahrenheit conversions from 0°C to 100°C.

2. **Shape Chooser**
   Write a Logo program that asks the user to choose a shape (triangle, square, pentagon) and draws it.

3. **Quiz Program**
   Create a PILOT program that asks multiple choice questions and keeps score.

Advanced Exercises
------------------

1. **Graphics Calculator**
   Build a program that combines BASIC calculations with Logo graphics to visualize mathematical functions.

2. **Adventure Game**
   Create an interactive text adventure using PILOT commands with Logo graphics for scenes.

3. **Educational Tool**
   Develop a program that teaches multiplication tables with interactive quizzes and progress tracking.

Next Steps
==========

After completing these tutorials, you should:

* Understand the basics of each language
* Know how to combine languages effectively
* Be able to debug your programs
* Create your own educational programs

For more advanced topics, check the :doc:`api_reference` and explore the example programs in the ``examples/`` directory.