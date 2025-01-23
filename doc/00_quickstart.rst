Introduction
============

This section covers the principle of operation of the |xscope_fileio| library and how to use it.

The |xscope_fileio| library consists of three components:

* **Device Library**: provides functions for managing files from an xcore.ai. The functions are similar to the ones used in the C Standard Library ``<stdio.>``, like fopen, fread, fwrite, and fclose.

* **Host Application**: an executable that runs on the host machine and communicates with the device application.

* **Python Module**: launches the device application and simultaneously launches the host application to communicate ``xscope`` data to/from.

Architecture
------------

The Python function ``run_on_target`` calls ``xrun --xscope-port`` with the binary and specified target adapter, and simultaneously launches a host application to communicate xscope data to/from the xrun process via ``sockets``. 
The host application responds to |xscope_fileio| API calls in the firmware code, reading/writing to the host file system. 
For doing so it uses known probes to communicate with the host app. These probes can be found in the ``config.xscope`` file. 
The user should copy this file to the firmware directory.
The call to ``run_on_target`` returns when the firmware exits.

Below is a diagram of the system architecture:

.. figure:: ./imgs/arch.png
  :alt: System Architecture

  xscope_fileio System Architecture

Device Installation
-------------------

The library can be downloaded from either the `XMOS Website <https://www.xmos.com/libraries>`_ to get the latest release or the `XMOS GitHub Repository <https://github.com/xmos/xscope_fileio>`_ for the latest development version or to contribute. 

The library can be used either as a dependency in a project or as a standalone library.

To use the To use the **Device Library** library as dependency, the user needs to:

1. Import the library header file in the source code:

.. code-block:: c

  #include <xscope_fileio.h>

2. Add `xscope_fileio` to the project dependencies:

.. code-block:: console

  set(APP_DEPENDENT_MODULES xscope_fileio)

Then at cmake configuration time, the tools will automatically download the library and add it to the project.

To use the **Device Library** as a standalone library, the easiest way is to download the library and copy it to the user directory. Thhe library provides some examples that can be used as a starting point for developing applications that require xscope_fileio operations. More information is prvoided on the Quickstart section of this document :ref:`quickstart`.

For more information on the device side API, please refer to the :ref:`device-reference`.

Host Installation
-----------------

To install the **Python Module** and the **Host Application**, run the following command:

.. code-block:: console

  pip install xscope_fileio

This will install the Python Package xscope_fileio and the  **Host Application** for the appropriate Operating System.

The Python Package can also be installed locally alongside the host app. This could allow users to modify the library or the host device code with their functions. To do so, install the package with the following command from the top-level directory:

.. code-block:: console

  pip install -e .

For more information on host side API, please refer to :ref:`host-reference`.

.. _quickstart:

Quickstart : Throughput Example 
-------------------------------

The following example demonstrates how to use the |xscope_fileio| library to read and write to a file on the host machine
and measure the throughput of the fileIO operations. 

This example can be used as a starting point for developing applications that require xscope_fileio operations.

To run on hardware the following XMOS evaluation board is required: ``XCORE-AI-EXPLORER``. 
Once the board is connected to the host machine, the example can be run. The boards connect via two micro USBs, one labeled ``DEBUG`` and the other ``USB``.

To build the example, run the following command from the top-level directory:

.. code-block:: console

  cd examples/throughput_c
  cmake -G "Unix Makefiles" -B build
  xmake -C build

Run the following command from top-level directory:

.. code-block:: console

  python run_example.py

This will xrun the code from the device with ``id=0`` (default). 

Output
------

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
