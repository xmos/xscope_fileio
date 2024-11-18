Xscope FileIO
=============

This library allows a program on the xCore to access binary files on the host machine
via xscope. 

Features:

#. Read and write binary files on the host machine from the xCore.
#. “wb” or “rb” file access mode only
#. 6-8MBytes/s Device to Host speed (compared to 2kBytes/s for standard fielio).
#. Up to 1MBytes/s Host to Device speed.

Installation
************

Xscope fileio module consist of two parts: 

#. A python module: launches the device application and simultaneously launches the host application to communicate xscope data to/from.
#. A host application: an executable that runs on the host machine and communicates with the device application.

To install the xscope fileio python module, simply run:

.. code-block:: console
    
    pip install .

For Linux and Mac, the host application is installed alongside the python module. 
For Windows, you will have to build the host application yourself. 
For more information for building the host app in windows see 
`host/README <./host/README.rst>`_.


Host side API
-------------

The host-side interface is written in Python. To run an xcore binary with access to
xscope fileIO,
use:

.. code-block:: python

    import xscope_fileio

.. code-block:: python

    xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

This can be combined with xtagctl e.g.:

.. code-block:: python

    with xtagctl.acquire("XCORE-AI-EXPLORER") as adapter_id:
        xscope_fileio.run_on_target(adapter_id, device_xe)


Device side API
---------------

Source and header files for device code are found in the ``xscope_fileio`` directory.

The device side application requires a multi-tile main since it uses the xscope_host_data(xscope_chan); service
to communicate with the host, which requires this. See examples for XC and C applications for how to do this.

You will also need a copy of ``config.xscope`` in your firmware directory. This
enables xscope in the tools and sets up the xscope probes used by fileio for communicating with the host app. You
can find a copy in ``xscope_fileio/config.xscope xscope_fileio/config.xscope.txt`` which you should rename to ``config.xscope``.

.. note::

    Note currently missing from fileio api: ``fprintf`` ,  ``fscanf``

System Architecture
-------------------

The ``run_on_target`` function calls ``xrun --xscope-port`` with the binary and specified target adapter,
and simultaneously launches a host application to communicate xscope data to/from
the xrun process via sockets. The host application responds to ``xscope_fileio`` API calls
in the firmware code, reading/writing to the host file system.

The call to ``run_on_target`` returns when the firmware exits.

.. image:: doc/imgs/arch.png
    :alt: System Architecture
