Installing xscope_fileio host tools
-----------------------------------

To install ``xscope_fileio`` host tool, please follow the steps below:

1. Make sure you have a C compiler  installed. If you are developing on Windows, we recomend using VS tools with a ``cl`` compiler.

2. Open a terminal or command prompt.

3. Install the xscope_fileio package. From the current directory, run the following command:

.. tab:: Linux and Mac

  .. code-block:: console

    >> Linux and Mac
    pip install -e ../.

.. tab:: Windows

  .. code-block:: console

    >> Windows
    pip install -e ../.
    cmake -G Ninja .
    ninja
  
Your ``xscope_fileio`` host app is now ready to use.
