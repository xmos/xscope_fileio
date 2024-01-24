example: fileio_feature_close
=============================

This example show how to use open and close files with xscope_fileio. 
 
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

  python tests/test_close_files.py --adapter-id "your-adapter-id"


Output
------

The output will be several files in the current directory inside the output folder. 
