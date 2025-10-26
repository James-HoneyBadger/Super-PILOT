Language Reference
==================

This section provides comprehensive reference documentation for each programming language supported by Time Warp IDE.

PILOT Language
==============

PILOT (Programmed Instruction, Learning, Or Teaching) is an educational programming language designed for computer-assisted instruction.

Command Reference
-----------------

Core Commands
~~~~~~~~~~~~~

T: (Type)
^^^^^^^^^

Display text to the user. Supports variable interpolation using asterisks.

**Syntax:** ``T:text``

**Examples:**

.. code-block:: none

   T:Hello, World!
   T:Welcome to PILOT programming!
   T:The answer is *RESULT*

A: (Accept)
^^^^^^^^^^

Accept user input and store it in a variable.

**Syntax:** ``A:variable``

**Examples:**

.. code-block:: none

   A:NAME
   T:Hello, *NAME*! How are you today?

Y: (Yes)
^^^^^^^^

Set the match flag if the condition is true. Used with conditional jumps.

**Syntax:** ``Y:condition``

**Examples:**

.. code-block:: none

   Y:*AGE*>18
   J:ADULT

N: (No)
^^^^^^^

Alternative conditional test - set match flag if condition is false.

**Syntax:** ``N:condition``

**Examples:**

.. code-block:: none

   N:*SCORE*<70
   J:FAILED

J: (Jump)
^^^^^^^^^

Jump to a label. Can be conditional based on previous Y:/N: command.

**Syntax:** ``J:label``

**Examples:**

.. code-block:: none

   J:START
   Y:*CHOICE*=1
   J:MENU1

M: (Match)
^^^^^^^^^^

Jump to label if the match flag is set (from Y:/N: commands).

**Syntax:** ``M:label``

**Examples:**

.. code-block:: none

   Y:*ANSWER*=CORRECT
   M:RIGHT_ANSWER

R: (Routine)
^^^^^^^^^^^^

Call a subroutine (gosub).

**Syntax:** ``R:label``

**Examples:**

.. code-block:: none

   R:CALCULATE_SUM

C: (Continue)
^^^^^^^^^^^^^

Return from subroutine.

**Syntax:** ``C:``

**Examples:**

.. code-block:: none

   C:

L: (Label)
^^^^^^^^^^

Define a label for jumps and subroutine calls.

**Syntax:** ``L:label``

**Examples:**

.. code-block:: none

   L:START
   L:MAIN_LOOP

U: (Update)
^^^^^^^^^^^

Update/assign a variable with an expression.

**Syntax:** ``U:variable=expression``

**Examples:**

.. code-block:: none

   U:SUM=10+20
   U:COUNT=*COUNT*+1

END
^^^

End program execution.

**Syntax:** ``END``

BASIC Language
==============

BASIC provides classic structured programming with line numbers and familiar constructs.

Command Reference
-----------------

LET
^^^

Assign a value to a variable.

**Syntax:** ``LET variable = expression``

**Examples:**

.. code-block:: basic

   LET A = 10
   LET NAME$ = "John"
   LET RESULT = A * 2 + 5

PRINT
^^^^^

Display text or variable values.

**Syntax:** ``PRINT expression [; expression...]``

**Examples:**

.. code-block:: basic

   PRINT "Hello, World!"
   PRINT "The answer is: "; RESULT
   PRINT A; B; C

INPUT
^^^^^

Get user input and store in a variable.

**Syntax:** ``INPUT ["prompt";] variable``

**Examples:**

.. code-block:: basic

   INPUT NAME$
   INPUT "Enter your age: "; AGE
   INPUT A, B, C

GOTO
^^^^

Jump to a specific line number.

**Syntax:** ``GOTO line_number``

**Examples:**

.. code-block:: basic

   10 PRINT "Looping..."
   20 GOTO 10

IF...THEN
^^^^^^^^^

Conditional execution.

**Syntax:** ``IF condition THEN command``

**Examples:**

.. code-block:: basic

   IF A > 10 THEN PRINT "Large number"
   IF SCORE >= 90 THEN GRADE$ = "A"

FOR...NEXT
^^^^^^^^^^^

Loop construct.

**Syntax:** ``FOR variable = start TO end [STEP step]``

**Examples:**

.. code-block:: basic

   FOR I = 1 TO 10
   PRINT I
   NEXT I

   FOR X = 0 TO 100 STEP 10
   PRINT X
   NEXT X

GOSUB...RETURN
^^^^^^^^^^^^^^^

Subroutine calls.

**Syntax:** ``GOSUB line_number`` and ``RETURN``

**Examples:**

.. code-block:: basic

   10 GOSUB 100
   20 PRINT "Back from subroutine"
   30 END
   100 PRINT "In subroutine"
   110 RETURN

REM
^^^

Comments (remark).

**Syntax:** ``REM comment_text``

**Examples:**

.. code-block:: basic

   REM This is a comment
   10 REM Calculate sum
   20 LET SUM = A + B

END
^^^

End program.

**Syntax:** ``END``

Logo Language
=============

Logo is designed for turtle graphics programming with an emphasis on educational use.

Command Reference
-----------------

Movement Commands
~~~~~~~~~~~~~~~~~

FORWARD / FD
^^^^^^^^^^^^

Move the turtle forward by the specified number of units.

**Syntax:** ``FORWARD distance`` or ``FD distance``

**Examples:**

.. code-block:: none

   FORWARD 100
   FD 50

BACK / BK
^^^^^^^^^

Move the turtle backward by the specified number of units.

**Syntax:** ``BACK distance`` or ``BK distance``

**Examples:**

.. code-block:: none

   BACK 50
   BK 25

LEFT / LT
^^^^^^^^^

Turn the turtle left by the specified angle in degrees.

**Syntax:** ``LEFT angle`` or ``LT angle``

**Examples:**

.. code-block:: none

   LEFT 90
   LT 45

RIGHT / RT
^^^^^^^^^^

Turn the turtle right by the specified angle in degrees.

**Syntax:** ``RIGHT angle`` or ``RT angle``

**Examples:**

.. code-block:: none

   RIGHT 90
   RT 180

Pen Control
~~~~~~~~~~~

PENUP / PU
^^^^^^^^^^

Lift the pen so the turtle doesn't draw while moving.

**Syntax:** ``PENUP`` or ``PU``

PENDOWN / PD
^^^^^^^^^^^^

Lower the pen so the turtle draws while moving.

**Syntax:** ``PENDOWN`` or ``PD``

Screen Control
~~~~~~~~~~~~~~

CLEARSCREEN / CS
^^^^^^^^^^^^^^^^

Clear the screen and return turtle to home position.

**Syntax:** ``CLEARSCREEN`` or ``CS``

HOME
^^^^

Return turtle to center of screen facing north.

**Syntax:** ``HOME``

SETXY
^^^^^

Set the turtle's position to specific coordinates.

**Syntax:** ``SETXY x y``

**Examples:**

.. code-block:: none

   SETXY 100 50
   SETXY -50 -25

Built-in Functions
==================

Mathematical Functions
----------------------

RND()
^^^^^

Generate a random number between 0 and 1.

**Syntax:** ``RND()``

**Examples:**

.. code-block:: none

   LET X = RND() * 100
   U:RANDOM=*RND*

INT()
^^^^^

Convert a number to an integer (truncate decimal part).

**Syntax:** ``INT(number)``

**Examples:**

.. code-block:: none

   PRINT INT(3.14)    ' Prints 3
   LET A = INT(7.9)   ' A = 7

VAL()
^^^^

Convert a string to a number.

**Syntax:** ``VAL(string)``

**Examples:**

.. code-block:: none

   LET NUM = VAL("123")
   PRINT VAL(INPUT_STR)

String Functions
----------------

UPPER()
^^^^^^^

Convert a string to uppercase.

**Syntax:** ``UPPER(string)``

**Examples:**

.. code-block:: none

   PRINT UPPER("hello")    ' Prints "HELLO"
   LET NAME = UPPER(INPUT_NAME)

LOWER()
^^^^^^^

Convert a string to lowercase.

**Syntax:** ``LOWER(string)``

**Examples:**

.. code-block:: none

   PRINT LOWER("HELLO")    ' Prints "hello"
   LET TEXT = LOWER(INPUT_TEXT)

MID()
^^^^^

Extract a substring from a string.

**Syntax:** ``MID(string, start, length)``

**Examples:**

.. code-block:: none

   PRINT MID("HELLO", 2, 3)    ' Prints "ELL"
   LET PART = MID(FULL_NAME, 1, 5)

Operators
=========

Arithmetic Operators
--------------------

* ``+`` - Addition
* ``-`` - Subtraction
* ``*`` - Multiplication
* ``/`` - Division
* ``^`` - Exponentiation

Comparison Operators
--------------------

* ``=`` - Equal to
* ``<>`` or ``!=`` - Not equal to
* ``<`` - Less than
* ``>`` - Greater than
* ``<=`` - Less than or equal to
* ``>=`` - Greater than or equal to

Logical Operators
-----------------

* ``AND`` - Logical AND
* ``OR`` - Logical OR
* ``NOT`` - Logical NOT

String Operators
----------------

* ``&`` or ``+`` - String concatenation