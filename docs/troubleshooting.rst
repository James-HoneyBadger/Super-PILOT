Troubleshooting
===============

This guide helps you resolve common issues with Time Warp IDE. If you can't find a solution here, check the :doc:`user_guide` or contact support.

Installation Issues
===================

Python Not Found
----------------

**Problem**: ``python: command not found`` or ``python3: command not found``

**Solutions**:

1. **Install Python**:

   * **Ubuntu/Debian**: ``sudo apt install python3 python3-tk``
   * **CentOS/RHEL**: ``sudo yum install python3 python3-tkinter``
   * **macOS**: Install from python.org or use Homebrew: ``brew install python3``
   * **Windows**: Download from python.org

2. **Check PATH**:

   .. code-block:: bash

      which python3
      python3 --version

3. **Use full path** if needed:

   .. code-block:: bash

      /usr/bin/python3 Time_Warp.py

tkinter Not Available
---------------------

**Problem**: ``ModuleNotFoundError: No module named 'tkinter'``

**Solutions**:

1. **Install tkinter**:

   * **Ubuntu/Debian**: ``sudo apt install python3-tk``
   * **CentOS/RHEL**: ``sudo yum install python3-tkinter``
   * **macOS**: Usually included with Python from python.org
   * **Windows**: Usually included with Python installer

2. **Verify installation**:

   .. code-block:: python

      python3 -c "import tkinter; print('tkinter available')"

Missing Dependencies
--------------------

**Problem**: Import errors for Pillow, numpy, or other libraries

**Solution**:

.. code-block:: bash

   # Install all dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

   # Or install individually
   pip install pillow numpy

Permission Errors
-----------------

**Problem**: Permission denied when installing or running

**Solutions**:

1. **Use virtual environment**:

   .. code-block:: bash

      python3 -m venv time_warp_env
      source time_warp_env/bin/activate  # Linux/Mac
      # time_warp_env\Scripts\activate  # Windows
      pip install -r requirements.txt

2. **Install with user permissions**:

   .. code-block:: bash

      pip install --user -r requirements.txt

3. **Use sudo** (not recommended):

   .. code-block:: bash

      sudo pip install -r requirements.txt

Runtime Issues
==============

Program Won't Start
-------------------

**Problem**: Time Warp IDE fails to launch

**Check these**:

1. **Python version**:

   .. code-block:: bash

      python3 --version  # Should be 3.8 or higher

2. **Dependencies**:

   .. code-block:: bash

      python3 -c "import tkinter, pillow; print('OK')"

3. **File permissions**:

   .. code-block:: bash

      ls -la Time_Warp.py

4. **Run with verbose output**:

   .. code-block:: bash

      python3 Time_Warp.py --verbose

Display Issues
--------------

**Problem**: GUI doesn't appear or looks wrong

**Solutions**:

1. **X11 forwarding** (remote systems):

   .. code-block:: bash

      export DISPLAY=:0.0
      xhost +

2. **Wayland issues** (Linux):

   .. code-block:: bash

      export GDK_BACKEND=x11
      python3 Time_Warp.py

3. **High DPI displays**:

   Add to your ``~/.Xresources``:

   .. code-block:: text

      Xft.dpi: 96

4. **Theme issues**:

   Reset theme in config:

   .. code-block:: python

      # Edit ~/.Time_Warp/config.json
      {"theme": "default"}

Program Execution Issues
========================

Syntax Errors
-------------

**Problem**: Program fails with syntax errors

**Common causes**:

1. **Wrong language selected**:

   * Ensure correct language is selected for your code
   * PILOT commands start with letters: ``T:``, ``A:``, ``J:``
   * BASIC uses line numbers: ``10 PRINT "Hello"``
   * Logo uses turtle commands: ``FORWARD 100``

2. **Missing semicolons** in BASIC:

   .. code-block:: basic

      PRINT "Hello"; NAME$  ' Correct
      PRINT "Hello" NAME$   ' Wrong - missing ;

3. **Incorrect PILOT commands**:

   .. code-block:: none

      T:Hello World  ' Correct
      Type Hello     ' Wrong - not PILOT syntax

4. **Logo command case**:

   .. code-block:: none

      forward 100   ' Correct (case insensitive)
      FORWARD 100   ' Also correct

Runtime Errors
--------------

**Problem**: Program starts but fails during execution

**Common issues**:

1. **Division by zero**:

   .. code-block:: basic

      LET RESULT = 10 / 0  ' Error!

   **Fix**: Add checks:

   .. code-block:: basic

      IF DENOMINATOR <> 0 THEN LET RESULT = 10 / DENOMINATOR

2. **Undefined variables**:

   .. code-block:: basic

      PRINT X  ' Error if X not defined!

   **Fix**: Initialize variables:

   .. code-block:: basic

      LET X = 0
      PRINT X

3. **Array bounds errors**:

   .. code-block:: basic

      DIM A(10)
      LET A(11) = 5  ' Error - array only has indices 0-10!

4. **PILOT variable interpolation**:

   .. code-block:: none

      U:NAME=John
      T:Hello *NAME*  ' Correct
      T:Hello NAME    ' Wrong - missing asterisks

Turtle Graphics Issues
----------------------

**Problem**: Graphics don't appear or behave incorrectly

**Solutions**:

1. **Canvas not visible**:

   * Ensure turtle graphics tab is selected
   * Check that canvas is initialized

2. **Wrong coordinates**:

   .. code-block:: none

      SETXY 100 100  ' Correct
      SETXY 100,100  ' Wrong - no comma in Logo

3. **Pen state issues**:

   .. code-block:: none

      PENUP
      FORWARD 100  ' Won't draw
      PENDOWN
      FORWARD 100  ' Will draw

4. **Screen clearing**:

   .. code-block:: none

      CLEARSCREEN  ' Resets turtle to home position

File I/O Issues
---------------

**Problem**: Can't load or save files

**Solutions**:

1. **File permissions**:

   .. code-block:: bash

      chmod 644 myprogram.spt

2. **File paths**:

   * Use absolute paths or relative to current directory
   * Avoid special characters in filenames

3. **File formats**:

   * ``.spt`` - Time Warp program files
   * ``.txt`` - Plain text
   * ``.pil`` - PILOT files
   * ``.bas`` - BASIC files
   * ``.logo`` - Logo files

4. **Encoding issues**:

   Save files as UTF-8 encoding.

Plugin Issues
=============

Plugin Not Loading
------------------

**Problem**: Custom plugins don't appear

**Check**:

1. **Plugin structure**:

   .. code-block:: text

      plugins/my_plugin/
      ├── __init__.py
      └── plugin.json

2. **Plugin class**:

   .. code-block:: python

      class MyPlugin:
          def initialize(self):
              pass

3. **Plugin registration**:

   Plugins are auto-discovered from ``plugins/`` directory.

4. **Import errors**:

   Check console output for plugin loading errors.

Plugin Conflicts
----------------

**Problem**: Plugins interfere with each other

**Solutions**:

1. **Disable conflicting plugins**:

   Move plugin folder out of ``plugins/`` directory.

2. **Check plugin metadata**:

   Ensure ``plugin.json`` has correct information.

3. **Update plugins**:

   Check for updated versions compatible with current IDE version.

Performance Issues
==================

Slow Program Execution
----------------------

**Problem**: Programs run slowly

**Optimizations**:

1. **Reduce loop iterations**:

   .. code-block:: basic

      FOR I = 1 TO 1000  ' Might be slow
      FOR I = 1 TO 100   ' Faster

2. **Use efficient algorithms**:

   Avoid nested loops when possible.

3. **Minimize graphics updates**:

   .. code-block:: none

      PENUP
      FOR I = 1 TO 100
      SETXY I*2 I*2  ' Multiple position changes
      NEXT I
      PENDOWN

4. **Profile code**:

   Use Python's ``cProfile`` to identify bottlenecks.

Memory Issues
-------------

**Problem**: Program uses too much memory

**Solutions**:

1. **Clear variables**:

   .. code-block:: basic

      LET LARGE_ARRAY = 0  ' Free memory

2. **Use smaller data types**:

   .. code-block:: basic

      DIM SMALL(100)  ' Instead of DIM BIG(10000)

3. **Clean up graphics**:

   .. code-block:: none

      CLEARSCREEN  ' Free graphics memory

High CPU Usage
--------------

**Problem**: IDE consumes excessive CPU

**Check**:

1. **Infinite loops**:

   .. code-block:: basic

      10 PRINT "Loop"
      20 GOTO 10  ' Infinite loop!

2. **Busy waiting**:

   Avoid empty loops waiting for input.

3. **Graphics rendering**:

   Complex graphics can be CPU intensive.

Debugging Issues
================

Debugger Not Working
--------------------

**Problem**: Can't set breakpoints or step through code

**Solutions**:

1. **Enable debugging**:

   Use F6 (Run with Debugger) instead of F5.

2. **Breakpoint placement**:

   Click in the line number area to set breakpoints.

3. **Variable watching**:

   Use the Watch Variables tab to monitor values.

4. **Step execution**:

   * F10: Step over
   * F11: Step into
   * F8: Stop execution

Watch Variables Empty
---------------------

**Problem**: Variable values don't appear in watch tab

**Check**:

1. **Variable scope**:

   Variables must be in current execution context.

2. **Variable naming**:

   Ensure correct variable names (case sensitive in some contexts).

3. **Execution state**:

   Variables only show values during execution.

Error Messages
--------------

**Problem**: Unclear error messages

**Common errors**:

1. **"Syntax error"**: Check command syntax
2. **"Undefined variable"**: Ensure variable is declared
3. **"Type mismatch"**: Check data types
4. **"Division by zero"**: Add division checks

Getting Help
============

If these solutions don't work:

1. **Check logs**:

   Look for error messages in console output.

2. **Run tests**:

   .. code-block:: bash

      python -m pytest tests/ -v

3. **Update IDE**:

   Ensure you have the latest version.

4. **Report issues**:

   * GitHub Issues: https://github.com/your-repo/Time_Warp/issues
   * Email: james@honey-badger.org

5. **Include information**:

   * Operating system and version
   * Python version
   * Full error message
   * Steps to reproduce
   * Sample code that causes the issue

System Information
==================

To help diagnose issues, provide this information:

.. code-block:: bash

   # Operating system
   uname -a

   # Python version
   python3 --version

   # Installed packages
   pip list

   # Tkinter version
   python3 -c "import tkinter; print(tkinter.TkVersion)"

   # Current directory
   pwd

   # File permissions
   ls -la Time_Warp.py

Configuration
=============

Reset Configuration
-------------------

**Problem**: Corrupted configuration causing issues

**Solution**:

.. code-block:: bash

   # Remove user config
   rm -rf ~/.Time_Warp/

   # Restart IDE - will create default config

Backup Configuration
--------------------

.. code-block:: bash

   # Backup settings
   cp -r ~/.Time_Warp/ ~/.Time_Warp_backup/

   # Restore if needed
   cp -r ~/.Time_Warp_backup/ ~/.Time_Warp/

Advanced Troubleshooting
========================

Debug Mode
----------

Run with debug output:

.. code-block:: bash

   python3 Time_Warp.py --debug

Verbose Logging
---------------

Enable detailed logging:

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)

Memory Profiling
----------------

Check memory usage:

.. code-block:: bash

   python3 -m memory_profiler Time_Warp.py

Performance Profiling
---------------------

Profile execution:

.. code-block:: bash

   python3 -m cProfile Time_Warp.py

Network Issues
--------------

If using network features:

1. **Check connectivity**:

   .. code-block:: bash

      ping 8.8.8.8

2. **Proxy settings**:

   Set environment variables if behind proxy:

   .. code-block:: bash

      export HTTP_PROXY=http://proxy.company.com:8080
      export HTTPS_PROXY=http://proxy.company.com:8080

3. **Firewall**:

   Ensure firewall allows Python network access.

Hardware-Specific Issues
========================

Raspberry Pi
------------

**Common issues**:

1. **Display**: Ensure X11 forwarding or console mode
2. **GPIO**: Install RPi.GPIO for hardware features
3. **Performance**: Use lighter themes

macOS
-----

**Common issues**:

1. **Gatekeeper**: Allow app to run in Security settings
2. **Tkinter**: May need to install from python.org
3. **Menu bar**: May appear differently than on other platforms

Windows
-------

**Common issues**:

1. **Antivirus**: May block execution - add exception
2. **Path length**: Keep paths under 260 characters
3. **Permissions**: Run as administrator if needed

Linux
-----

**Common issues**:

1. **Package manager**: Use correct package names for your distro
2. **Display server**: Ensure X11 or Wayland compatibility
3. **Dependencies**: Install development packages if compiling

Virtual Machines
----------------

**Common issues**:

1. **3D acceleration**: Disable for better compatibility
2. **Shared folders**: Ensure proper permissions
3. **Memory**: Allocate sufficient RAM (2GB minimum)

Cloud Instances
---------------

**Common issues**:

1. **Headless mode**: Use Xvfb for GUI testing
2. **Display**: Set DISPLAY variable correctly
3. **Network**: Ensure proper security group settings

Preventive Maintenance
======================

Regular Tasks
-------------

1. **Update dependencies**:

   .. code-block:: bash

      pip install -U -r requirements.txt

2. **Run tests**:

   .. code-block:: bash

      python -m pytest tests/

3. **Check disk space**:

   .. code-block:: bash

      df -h

4. **Backup configuration**:

   .. code-block:: bash

      cp -r ~/.Time_Warp/ ~/.Time_Warp_backup/

Best Practices
--------------

1. **Use virtual environments** to avoid conflicts
2. **Keep backups** of important programs
3. **Test programs** before sharing
4. **Update regularly** for bug fixes
5. **Monitor resources** during development
6. **Use version control** for your programs

Emergency Recovery
==================

Complete Reset
--------------

If everything fails:

.. code-block:: bash

   # Remove all user data
   rm -rf ~/.Time_Warp/

   # Reinstall from scratch
   git clone https://github.com/your-repo/Time_Warp.git
   cd Time_Warp
   pip install -r requirements.txt
   python3 Time_Warp.py

Data Recovery
-------------

Recover lost programs:

1. Check ``~/.Time_Warp/versions/`` for auto-saved versions
2. Look in system temp directories
3. Check browser cache if using web interface
4. Restore from backups

Contact Support
===============

If you still need help:

**Email**: james@honey-badger.org

**GitHub**: https://github.com/your-repo/Time_Warp/issues

**Include**:
- Full error messages
- System information
- Steps to reproduce
- Sample code
- IDE version (check VERSION file)