Getting Started
===============

Welcome to Time Warp IDE! This guide will help you get up and running quickly.

Installation
------------

Prerequisites
~~~~~~~~~~~~~

* Python 3.8 or higher
* tkinter (usually included with Python)
* pip for package management

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/your-repo/Time_Warp.git
   cd Time_Warp

   # Install development dependencies
   pip install -r requirements-dev.txt

   # For documentation generation
   pip install sphinx sphinx-rtd-theme

First Run
---------

Launch the IDE:

.. code-block:: bash

   python Time_Warp.py

You should see the main Time Warp IDE window with:

* Code editor on the left
* Turtle graphics canvas on the right
* Menu bar with File, Edit, View, and Help options
* Status bar showing current language and cursor position

Your First Program
------------------

Let's create a simple PILOT program:

1. Click "New File" in the File menu
2. Select "PILOT" as the language
3. Type this program:

   .. code-block:: none

      T:Hello World!
      T:This is my first PILOT program.
      T:
      T:Let's draw a square with turtle graphics.
      T:
      FORWARD 100
      RIGHT 90
      FORWARD 100
      RIGHT 90
      FORWARD 100
      RIGHT 90
      FORWARD 100
      RIGHT 90

4. Click the "Run" button or press F5
5. Watch your program execute and draw a square!

Language Selection
------------------

Time Warp IDE supports three programming languages:

**PILOT**
   Teaching-oriented language with simple commands:

   * ``T:`` - Type text
   * ``A:`` - Accept input
   * ``J:`` - Jump to label
   * ``Y:`` - Yes branch
   * ``N:`` - No branch

**BASIC**
   Classic line-numbered programming:

   * ``PRINT`` - Display text
   * ``INPUT`` - Get user input
   * ``LET`` - Assign variables
   * ``GOTO`` - Jump to line
   * ``IF...THEN`` - Conditional execution

**Logo**
   Turtle graphics programming:

   * ``FORWARD`` - Move turtle forward
   * ``BACK`` - Move turtle backward
   * ``LEFT`` - Turn turtle left
   * ``RIGHT`` - Turn turtle right
   * ``PENUP`` - Lift pen
   * ``PENDOWN`` - Lower pen

Next Steps
----------

* Explore the ``examples/`` directory for more sample programs
* Read the :doc:`user_guide` for detailed usage instructions
* Check out the :doc:`tutorials` for step-by-step learning
* Visit the :doc:`api_reference` for developer documentation