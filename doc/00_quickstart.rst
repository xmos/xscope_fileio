Introduction
============

This section covers the principle of operation of the |xscope_fileio| library and how to use it.

The |xscope_fileio| library consists of three components:

* **Device Library**: provides functions for managing host files from an xcore.ai. The functions are similar to the ones used in the C Standard Library ``<stdio.h>``, like fopen, fread, fwrite, and fclose.

* **Host Application**: an executable that runs on the host machine and communicates with the device application.

* **Python Package**: launches the device application and simultaneously launches the host application to communicate ``xscope`` data  between them.

Architecture
------------

Xscope is a high-speed protocol between the host and the target that runs over an XMOS Link. It enables high-speed communication between the device and the host.  

The |xscope_fileio| library uses this protocol to manipulate host files and perform file operations. Certain types of messages, known as probes, are allowed depending on the type of file operation performed. These probes are stored in a file called ``config.xscope``.

This Library uses ``XCommon CMake`` as build system. ``XCommon CMake`` is a build system based on ``CMake`` for xcore applications and libraries. More information can be found in `XCommon CMake Documentation <https://www.xmos.com/documentation/XM-015090-PC/html/>`_.

Finally, the **Python Package** simplifies the communication process through Python function calls. For instance, the Python function :func:`xscope_fileio.run_on_target` runs the firmware binary on a specified device while simultaneously launching a host application to exchange xscope data.  

For more information about XMOS tools or xscope, please refer to the `XTC Tools Documentation <https://www.xmos.com/documentation/XM-014363-PC/html/>`_ and `Xscope Documentation <https://www.xmos.com/documentation/XM-014363-PC/html/tools-guide/tools-ref/xscope/index.html>`_.

The diagram of the system architecture appears in :ref:`Figure 1 <fig-system-architecture>`.

.. _fig-system-architecture:
.. figure:: ./imgs/arch.png
  :alt: System Architecture

  xscope_fileio System Architecture

.. raw:: latex

    \newpage

Requirements
------------

In order to use the |xscope_fileio| library, the following requirements must be met:

- XTC tools: |xtc_tools_version| `XTC tools`_.
- Python: |python_version| or later Python_.
- CMake: |cmake_version| or later CMake_.

.. note::

  For running the examples on Hardware the `XMOS Evaluation Board`_ is required. 

Device Installation
-------------------

The library can be obtained from the `XMOS Website`_, which provides the latest stable release, or from the `xscope_fileio Repository`_, where you can access the latest development version and contribute to its ongoing improvement.

The library can be used either as a dependency in a project or as a standalone library.

To use the **Device Library** library as dependency, the user needs to:

1. Import the library header file in the source code:

.. code-block:: c

  #include <xscope_fileio.h>

2. Add `xscope_fileio` to the project dependencies in the application ``CMakeLists.txt``:

.. code-block:: console

  set(APP_DEPENDENT_MODULES xscope_fileio)

3. Add the xscope fileio probes to your application folder: 

.. code-block:: console

  config.xscope

At CMake configuration time, the tools will automatically download the library and integrate it into the project.

.. note:: 
  
  The ``config.xscope`` file defines the probes or types of messages allowed between the host and device. The ``config.xscope`` file is located in the current library, inside the ``xscope_fileio`` folder. It is fetched by the build system when added as a dependency or can be downloaded manually from the repository at the same location. 


To use the **Device Library** as a standalone library, the easiest way is to download the library and copy it to the user directory. The library provides some examples that can be used as a starting point for developing applications that require xscope_fileio operations. More information is provided on the :ref:`quickstart` section of this document.

For more information on the device side API, please refer to the :ref:`device-reference`.

Python Package and Host Installation
------------------------------------

To install the **Python Package** and the **Host Application**, run the following command:

.. code-block:: console

  pip install xscope_fileio

This will install the **Python Package** xscope_fileio and the  **Host Application** for the appropriate Operating System.

The **Python Package** can also be installed locally. This could allow users to modify the library, the host code or device code with their own functions. To do so, run the the following command from the top-level directory of the |xscope_fileio| library:

.. code-block:: console

  pip install -e .

For more information on host side API, please refer to :ref:`host-reference`.

.. _quickstart:

Quickstart: Throughput Example 
------------------------------

The following example demonstrates how to use the |xscope_fileio| library to measure the throughput of the fileIO operations. 

This example can be used as a starting point for developing applications that require xscope_fileio operations.

For building and running the example, follow the steps below:

1. Connect the board ``XK-EVK-XU316`` to the host computer. The board connects via two micro USBs, one labeled ``DEBUG`` and the other ``USB``.

2. To build the example, run the following command from the top-level directory:

.. code-block:: console

  cd examples/throughput_c
  cmake -G "Unix Makefiles" -B build
  xmake -C build

3. Run the example by entering the following command:

.. code-block:: console

  python run_example.py

This will xrun the code from the device with ``id=0`` (default). 

Output
^^^^^^

The example writes and reads files on the host computer and measures the KBPS throughput. 
Once finished, the measurements are displayed on the console.
The Output should look something similar to the following:

.. code-block:: console

  [DEVICE] Input file size kB: 31457
  [DEVICE] Throughput KBPS Read: 1352.151489, Write: 5864.112793
  Running on target finished
  Example run successfully!

In this particular example, the throughput for reading is about *1.3MBPS*, and for writing is about *5.8MBPS*.
The throughput will depend on the host machine and the connection between the host and the device.
