Xscope FileIO Quickstart
========================

This section covers the principle of operation of the |xscope_fileio| library and how to use it.

Introduction
------------

Xscope fileio module consist of three parts:

* An **Xcore Library** for managing files. With similar apis to stdio, like fopen, fread, fwrite, fclose.
* A **Host Application**: an executable that runs on the host machine and communicates with the device application.
* A **Python Module**: launches the device application and simultaneously launches the host application to communicate xscope data to/from.

Architecture
------------

The run_on_target function calls ``xrun --xscope-port`` with the binary and specified target adapter, and simultaneously launches a host application to communicate xscope data to/from the xrun process via ``sockets``. 
The host application responds to xscope_fileio API calls in the firmware code, reading/writing to the host file system. 
For doing so it uses known probes to communicate with the host app. This probes can be found in the ``config.xscope`` file. 
The user should copy this file to the firmware directory.
The call to run_on_target returns when the firmware exits.

.. image:: ./imgs/arch.png
    :alt: System Architecture

Device Installation
-------------------

To use the **Xcore Library**, the user needs to add `xscope_fileio` to the firmware dependencies:

.. code-block:: console

    set(APP_DEPENDENT_MODULES xscope_fileio)

For more information on setting up the device side, please refer to the :ref:`device-reference`.

Host Installation
-----------------

To install the **Python Module** on the host side, the user can use `pip <https://pypi.org/project/xscope-fileio/>`_:

.. code-block:: console

    pip install xscope_fileio

This will also install the **Host Application** for the appropriate operating system.

For more information on setting up the host side, please refer to the :ref:`host-reference`.

.. note::

    Alternatively, the user can build the **Host Application** from source. For details, see the `xscope_fileio/host <https://github.com/xalbertoisorna/xscope_fileio/tree/develop/host>`_.

Quickstart
----------

Once we have the device and host side set up, we can start using the |xscope_fileio| library. 
This section introduces some of the key tools required to build and run a simple program on a single tile. 
To run on hardware one of the following XMOS evaluation boards is required: XCORE-AI-EXPLORER. 

//TODO









#
