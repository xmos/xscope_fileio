Example: fileio_features_c
==========================

This example shows the basics functionality of xscope fileio using ``C`` as the programming language. 

Build example (using xcommon_cmake)
-----------------------------------

.. warning::

  Make sure ``xscope_fileio`` python package and host application are installed.

Run the following command from the current directory: 

.. code-block:: console

  cmake -G "Unix Makefiles" -B build
  xmake -C build

Running example
---------------
  
Run the following command from top-level directory:

.. code-block:: console

  python run_example.py

This will xrun the code from the device with id=0 (default). 

Output
------

The example writes and reads files on the host computer and measures the KBPS throughput. Once finished, the measurements are displayed on the console.
