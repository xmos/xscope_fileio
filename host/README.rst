Installing xscope_fileio Host App Manually
------------------------------------------

To install ``xscope_fileio`` host tool manually, please follow the steps below:

1. Make sure you have a C compiler  installed. If you are developing on Windows, we recomend using VS tools with a ``cl`` compiler.

2. Open a terminal or command prompt.

3. From the current directory, run the following command:

 .. code-block:: console

  # Linux and Mac
  cmake -B build
  make -C build

  # Windows
  cmake -G Ninja -B build
  ninja -C build
  
Your ``xscope_fileio`` host app is now ready to use.
