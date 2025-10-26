Examples
========

This section showcases comprehensive example programs that demonstrate Time Warp IDE's capabilities. Each example includes the complete source code and explanations.

PILOT Examples
==============

Hello World Program
-------------------

A simple introduction to PILOT programming.

.. code-block:: none

   L:START
   T:********************************
   T:*   Welcome to Time Warp IDE   *
   T:*     PILOT Programming        *
   T:********************************
   T:
   T:This is your first PILOT program!
   T:Programs are made of commands that start with letters.
   T:
   T:T: means "Type" - display text
   T:L: means "Label" - mark a location
   T:END means "End" - stop the program
   END

**Features demonstrated:**

* Text output with ``T:`` command
* Program structure with labels
* Simple sequential execution

Interactive Quiz
----------------

An interactive quiz program that demonstrates input and conditional logic.

.. code-block:: none

   L:QUIZ_START
   T:Welcome to the PILOT Quiz!
   T:Let's test your knowledge.
   T:
   T:Question 1: What does PILOT stand for?
   T:A) Programmed Instruction, Learning, Or Teaching
   T:B) Personal Interactive Learning Online Tool
   T:C) Programming In Logical Order Theory
   T:
   A:ANSWER1
   Y:*ANSWER1*=A
   M:CORRECT1
   T:Sorry, that's not correct. The answer is A.
   J:QUESTION2
   L:CORRECT1
   T:Correct! PILOT stands for Programmed Instruction, Learning, Or Teaching.
   T:
   L:QUESTION2
   T:Question 2: Which command displays text in PILOT?
   T:A) D:text
   T:B) T:text
   T:C) S:text
   T:
   A:ANSWER2
   Y:*ANSWER2*=B
   M:CORRECT2
   T:Incorrect. The correct answer is B.
   J:END_QUIZ
   L:CORRECT2
   T:Excellent! T: is the command for displaying text.
   T:
   L:END_QUIZ
   T:Quiz complete! Thank you for playing.
   END

**Features demonstrated:**

* User input with ``A:`` command
* Conditional testing with ``Y:`` and ``N:``
* Program flow control with ``J:`` and ``M:``
* Labels for organizing program sections

Math Calculator
---------------

A calculator program showing mathematical operations and variable usage.

.. code-block:: none

   L:CALCULATOR
   T:*******************************
   T:*    PILOT Math Calculator    *
   T:*******************************
   T:
   T:Enter first number:
   A:NUM1
   T:Enter second number:
   A:NUM2
   T:
   U:SUM=*NUM1*+*NUM2*
   U:DIFFERENCE=*NUM1*-*NUM2*
   U:PRODUCT=*NUM1***NUM2*
   U:QUOTIENT=*NUM1*/*NUM2*
   T:
   T:Results:
   T:*NUM1* + *NUM2* = *SUM*
   T:*NUM1* - *NUM2* = *DIFFERENCE*
   T:*NUM1* × *NUM2* = *PRODUCT*
   T:*NUM1* ÷ *NUM2* = *QUOTIENT*
   T:
   T:Thank you for using the calculator!
   END

**Features demonstrated:**

* Mathematical operations in expressions
* Variable assignment with ``U:``
* Complex text output with variable interpolation
* Calculator-style program structure

BASIC Examples
==============

Number Guessing Game
--------------------

An interactive game demonstrating loops, conditionals, and random numbers.

.. code-block:: basic

   10 REM Number Guessing Game
   20 PRINT "Welcome to the Number Guessing Game!"
   30 PRINT "I'm thinking of a number between 1 and 100."
   40 LET SECRET = INT(RND() * 100) + 1
   50 LET GUESSES = 0
   60 PRINT "Take a guess:"
   70 INPUT GUESS
   80 LET GUESSES = GUESSES + 1
   90 IF GUESS = SECRET THEN GOTO 130
   100 IF GUESS < SECRET THEN PRINT "Too low! Try again:"
   110 IF GUESS > SECRET THEN PRINT "Too high! Try again:"
   120 GOTO 70
   130 PRINT "Congratulations! You got it in"; GUESSES; "guesses."
   140 PRINT "Play again? (Y/N):"
   150 INPUT CHOICE$
   160 IF CHOICE$ = "Y" THEN GOTO 20
   170 PRINT "Thanks for playing!"
   180 END

**Features demonstrated:**

* Random number generation with ``RND()``
* Loop structures with ``GOTO``
* Conditional logic with ``IF...THEN``
* User input and output
* Game-like program flow

Temperature Converter
---------------------

A utility program for temperature conversions with a table display.

.. code-block:: basic

   10 REM Temperature Conversion Program
   20 PRINT "Temperature Conversion Table"
   30 PRINT "Celsius    Fahrenheit"
   40 PRINT "--------   ----------"
   50 FOR C = 0 TO 100 STEP 10
   60 LET F = C * 9 / 5 + 32
   70 PRINT C; "         "; F
   80 NEXT C
   90 PRINT
   100 PRINT "Interactive Conversion"
   110 PRINT "Enter temperature in Celsius:"
   120 INPUT CELSIUS
   130 LET FAHRENHEIT = CELSIUS * 9 / 5 + 32
   140 PRINT CELSIUS; "°C = "; FAHRENHEIT; "°F"
   150 PRINT "Convert another? (Y/N):"
   160 INPUT AGAIN$
   170 IF AGAIN$ = "Y" THEN GOTO 110
   180 PRINT "Goodbye!"
   190 END

**Features demonstrated:**

* ``FOR...NEXT`` loops for iteration
* Mathematical calculations
* Formatted output with spacing
* Interactive user interface
* Program flow control

Simple Database
---------------

A basic data storage and retrieval system.

.. code-block:: basic

   10 REM Simple Student Database
   20 DIM NAMES$(100)
   30 DIM SCORES(100)
   40 LET COUNT = 0
   50 PRINT "Student Database System"
   60 PRINT "1. Add Student"
   70 PRINT "2. List Students"
   80 PRINT "3. Search Student"
   90 PRINT "4. Exit"
   100 PRINT "Choose option:"
   110 INPUT CHOICE
   120 IF CHOICE = 1 THEN GOTO 200
   130 IF CHOICE = 2 THEN GOTO 300
   140 IF CHOICE = 3 THEN GOTO 400
   150 IF CHOICE = 4 THEN GOTO 500
   160 PRINT "Invalid choice. Try again."
   170 GOTO 50
   200 REM Add Student
   210 PRINT "Enter student name:"
   220 INPUT NAME$
   230 PRINT "Enter score:"
   240 INPUT SCORE
   250 LET COUNT = COUNT + 1
   260 LET NAMES$(COUNT) = NAME$
   270 LET SCORES(COUNT) = SCORE
   280 PRINT "Student added!"
   290 GOTO 50
   300 REM List Students
   310 IF COUNT = 0 THEN PRINT "No students in database."
   320 FOR I = 1 TO COUNT
   330 PRINT NAMES$(I); ": "; SCORES(I)
   340 NEXT I
   350 GOTO 50
   400 REM Search Student
   410 PRINT "Enter name to search:"
   420 INPUT SEARCH$
   430 LET FOUND = 0
   440 FOR I = 1 TO COUNT
   450 IF NAMES$(I) = SEARCH$ THEN LET FOUND = I
   460 NEXT I
   470 IF FOUND = 0 THEN PRINT "Student not found."
   480 IF FOUND > 0 THEN PRINT NAMES$(FOUND); ": "; SCORES(FOUND)
   490 GOTO 50
   500 PRINT "Goodbye!"
   510 END

**Features demonstrated:**

* Arrays for data storage (``DIM``)
* Menu-driven interface
* Data search and retrieval
* Multiple program sections
* Complex conditional logic

Logo Examples
=============

Geometric Shapes
----------------

Programs that draw various geometric shapes using turtle graphics.

Square
~~~~~~

.. code-block:: none

   CLEARSCREEN
   PENDOWN
   FORWARD 100
   RIGHT 90
   FORWARD 100
   RIGHT 90
   FORWARD 100
   RIGHT 90
   FORWARD 100
   RIGHT 90
   PENUP
   HOME

Triangle
~~~~~~~~

.. code-block:: none

   CLEARSCREEN
   PENDOWN
   FORWARD 100
   RIGHT 120
   FORWARD 100
   RIGHT 120
   FORWARD 100
   RIGHT 120
   PENUP
   HOME

Circle
~~~~~~

.. code-block:: none

   CLEARSCREEN
   PENDOWN
   FOR I = 1 TO 36
   FORWARD 8.7
   RIGHT 10
   NEXT I
   PENUP
   HOME

Star
~~~~

.. code-block:: none

   CLEARSCREEN
   PENDOWN
   FOR I = 1 TO 5
   FORWARD 100
   RIGHT 144
   NEXT I
   PENUP
   HOME

Complex Patterns
----------------

Spiral
~~~~~~

.. code-block:: none

   CLEARSCREEN
   PENDOWN
   FOR I = 1 TO 100
   FORWARD I * 2
   RIGHT 15
   NEXT I
   PENUP
   HOME

Flower
~~~~~~

.. code-block:: none

   CLEARSCREEN
   FOR PETAL = 1 TO 6
   PENDOWN
   FOR I = 1 TO 30
   FORWARD I * 0.5
   RIGHT 6
   NEXT I
   PENUP
   RIGHT 60
   NEXT PETAL
   HOME

Artistic Patterns
~~~~~~~~~~~~~~~~~

.. code-block:: none

   CLEARSCREEN
   FOR PATTERN = 1 TO 3
   PENDOWN
   FOR I = 1 TO 50
   FORWARD I
   RIGHT 91
   NEXT I
   PENUP
   RIGHT 120
   NEXT PATTERN
   HOME

Mixed Language Examples
=======================

Graphics Calculator
-------------------

Combines BASIC calculations with Logo graphics to visualize functions.

.. code-block:: none

   REM Graphics Calculator - Plot y = x^2
   LET SCALE = 10
   PRINT "Plotting y = x^2"
   PRINT "Scale factor:"; SCALE

   CLEARSCREEN
   PENUP
   SETXY -200 0
   PENDOWN
   FORWARD 400  ' Draw x-axis
   PENUP
   SETXY 0 -200
   PENDOWN
   RIGHT 90
   FORWARD 400  ' Draw y-axis
   RIGHT 90

   REM Plot the function
   PENUP
   FOR X = -20 TO 20
   LET Y = X * X
   SETXY X * SCALE Y * SCALE / 10
   IF X = -20 THEN PENDOWN
   NEXT X

   PENUP
   HOME
   END

Interactive Drawing Program
---------------------------

A program that lets users create drawings interactively.

.. code-block:: none

   REM Interactive Drawing Program
   PRINT "Interactive Drawing Program"
   PRINT "Commands: F=forward, B=back, L=left, R=right, C=clear, Q=quit"

   CLEARSCREEN
   PENDOWN

   L:MAIN_LOOP
   PRINT "Enter command (F/B/L/R number or C or Q):"
   INPUT CMD$

   Y:*CMD*=Q
   J:QUIT

   Y:*CMD*=C
   M:CLEAR_CMD

   REM Parse movement commands
   LET DIR = MID(CMD$, 1, 1)
   LET DIST = VAL(MID(CMD$, 2, LEN(CMD$) - 1))

   Y:*DIR*=F
   M:FORWARD_CMD

   Y:*DIR*=B
   M:BACK_CMD

   Y:*DIR*=L
   M:LEFT_CMD

   Y:*DIR*=R
   M:RIGHT_CMD

   T:Invalid command. Try again.
   J:MAIN_LOOP

   L:FORWARD_CMD
   FORWARD DIST
   J:MAIN_LOOP

   L:BACK_CMD
   BACK DIST
   J:MAIN_LOOP

   L:LEFT_CMD
   LEFT DIST
   J:MAIN_LOOP

   L:RIGHT_CMD
   RIGHT DIST
   J:MAIN_LOOP

   L:CLEAR_CMD
   CLEARSCREEN
   PENDOWN
   J:MAIN_LOOP

   L:QUIT
   PRINT "Thanks for drawing!"
   END

Educational Examples
====================

Multiplication Quiz
-------------------

An educational program that teaches multiplication tables.

.. code-block:: none

   REM Multiplication Quiz
   LET SCORE = 0
   LET QUESTIONS = 0

   PRINT "Multiplication Quiz!"
   PRINT "Answer as many as you can. Enter 0 to quit."
   PRINT

   L:QUIZ_LOOP
   LET A = INT(RND() * 12) + 1
   LET B = INT(RND() * 12) + 1
   LET ANSWER = A * B

   PRINT A; "×"; B; "= ?";
   INPUT GUESS

   IF GUESS = 0 THEN GOTO 200

   LET QUESTIONS = QUESTIONS + 1

   IF GUESS = ANSWER THEN GOTO 150
   PRINT "Incorrect. The answer is"; ANSWER
   GOTO 160

   150 PRINT "Correct!"
   155 LET SCORE = SCORE + 1

   160 PRINT "Score:"; SCORE; "/"; QUESTIONS
   170 PRINT
   180 GOTO 100

   200 PRINT "Quiz complete!"
   210 PRINT "Final score:"; SCORE; "/"; QUESTIONS
   220 LET PERCENT = INT(SCORE / QUESTIONS * 100)
   230 PRINT "Percentage:"; PERCENT; "%"
   240 END

Math Visualization
------------------

Uses Logo graphics to visualize mathematical concepts.

.. code-block:: none

   REM Math Visualization - Number Patterns
   PRINT "Mathematical Pattern Visualization"

   CLEARSCREEN
   FOR ROW = 1 TO 10
   FOR COL = 1 TO 10
   LET PRODUCT = ROW * COL
   PENUP
   SETXY (COL - 5) * 20 (ROW - 5) * 20
   PENDOWN
   IF PRODUCT < 25 THEN FORWARD 5
   IF PRODUCT >= 25 AND PRODUCT < 50 THEN FORWARD 10
   IF PRODUCT >= 50 AND PRODUCT < 75 THEN FORWARD 15
   IF PRODUCT >= 75 THEN FORWARD 20
   PENUP
   NEXT COL
   NEXT ROW

   HOME
   END

Running the Examples
====================

To run any of these examples:

1. Start Time Warp IDE
2. Create a new file (Ctrl+N)
3. Copy and paste the example code
4. Select the appropriate language if prompted
5. Click Run (F5) or use the debugger (F6)

The examples are also available in the ``examples/`` directory of your Time Warp IDE installation.

Modifying Examples
==================

Feel free to modify these examples to:

* Change colors and sizes
* Add more features
* Combine multiple examples
* Create your own variations

Use the debugger to understand how the programs work and experiment with different values.

Next Steps
==========

After exploring these examples, you can:

* Create your own programs using similar techniques
* Combine elements from different examples
* Check the :doc:`tutorials` for step-by-step learning
* Refer to the :doc:`language_reference` for detailed command information
* Explore the :doc:`api_reference` for advanced programming