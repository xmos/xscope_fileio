example: fileio_features_c
===========================

This example show the basics functionality of xscope fileio using ``C`` as the programming language. 

Build example (using xcommon_cmake)
-----------------------------------

.. warning::

  Make sure ``xscope_fileio`` host application is installed.
  Make sure ``XCOMMON_CMAKE_PATH`` environment variable is set to the directory where ``xcommon_cmake`` is located.

Run the following command from the current directory: 

.. code-block:: console

  cmake -G "Unix Makefiles" -B build
  xmake -C build

Running example
---------------
  
Run the following command from top-level directory:

.. code-block:: console

  python run_example.py --adapter-id "your-adapter-id"

Output
------

The output will be several files in the current directory inside the output folder. 
