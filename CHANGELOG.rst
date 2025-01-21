xscope fileio change log
========================

1.3.1
-----

  * ADDED: Quickstart Guide documentation.
  * ADDED: xrun with ``--id`` option to run_on_target if ``adapter_id`` is ``int``.  
  * ADDED: Library version check between host and target.  
  * CHANGED: Update XTC tools version to ``15.3.0``.  
  * CHANGED: Replacement of setup.py with pyproject.toml using Hatch.  
  * REMOVED: Makefiles in examples and test applications.  

1.2.0
-----

  * CHANGED: Update tools version in Jenkinsfile to 15.2.1.
  * ADDED: XCommon CMake for tests and example integration.
  * FIXED: Adapter ID can now be passed to examples.
  * CHANGED: Improved documentation formatting and updates.
  * ADDED: Pytest support.
  * ADDED: xscope_fclose function for closing a single file.
  * ADDED: Support for XCommon CMake build system.
  * FIXED: Hang in run_on_target when invalid file was opened for reading.
  * FIXED: fread no longer can cause buffer overflow.
  * FIXED: fread always returns the end of the file if eof is reached.

1.1.2
-----

  * CHANGED: Update tools version in Jenkinsfile to 15.1.4
  * CHANGED: Update flake8 python linting to warn instead of error on Jenkins
  * CHANGED: Pin importlib-meta python package to 4.13.0

1.1.1
-----

  * REMOVED: xscope_fread() delay for Windows race condition
  * ADDED: checks that xscope_io_init() has completed before allowing a file to be opened
  * ADDED: adds helper function, xscope_fileio_is_initialized(), to allow application to check if the host connection has been established

1.1.0
-----

  * ADDED: ability to use alternate mutex methods
  * ADDED: 0.1 ms delay in xscope_fread() to work-around Windows race condition

1.0.0
-----

  * ADDED: support for building and running the host endpoint on Windows
  * ADDED: XMOS public V1 license
  * ADDED: support for run_on_target() to optionally redirect stdout to file
  * REMOVED:run_on_target() method returns stdout/err as list of lines
  * REMOVED: optional verbose kwarg in run_on_target()to reduce verbosity

0.4.0
-----

  * CHANGED: Python code to use subprocess instead of sh
  * REMOVED: Contextlib support for capturing stout/stderr
  * ADDED: run_on_target() method returns stdout/err as list of lines
  * ADDED: optional verbose kwarg in run_on_target()to reduce verbosity

0.3.2
-----

  * FIXED: changelog title

0.3.1
-----

  * ADDED: Jenkins stage to update view files automatically

0.3.0
-----
  * ADDED: Jenkins driven file transfer test
  * ADDED: Note in API about maximum fread of 64kB on Linux hosts
  * FIXED: Duplicate printing of [DEVICE] on long lines

0.2.0
-----

  * FIXED: setup.py now properly builds host app
  * CHANGED: config.xscope now needs to be copied to local firmware app

0.1.0
-----

  * ADDED: ftell and fseek
  * ADDED: XC and C based examples
  * CHANGED: module_build_info friendly layout of embedded source
  * CHANGED: API argument ordering so file handle comes last as per stdio

0.0.1
-----
  * ADDED: Initial version with support for fread & frwite + python helper

