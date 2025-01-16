Test: No Hang
=============

This test opens a file that does no exist and verifies that the program does not hang.
Host app and device app terminate with the device error.

Build example
-------------
Run the following command from the current directory: 

.. code-block:: console

  cmake -G "Unix Makefiles" -B build
  xmake -C build

Running example
---------------

.. warning::

  Make sure ``xscope_fileio`` is installed.
  

Run the following command from top-level directory:

.. code-block:: console

  python tests/test_no_hang.py --adapter-id "your-adapter-id"


Output
------

The output will show the error message and the device error code.

.. code-block:: console

  Failed to open file_doesnt_exist.txt
  ...
  ERROR: xrun exited with error code 1
