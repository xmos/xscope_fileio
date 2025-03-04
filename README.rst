:orphan:

.. |xtc_tools_version_| replace:: 15.3.0
.. |python_version_|    replace:: 3.10
.. |cmake_version_|     replace:: 3.23

xscope_fileio: FileIO over Xscope
#################################

:vendor: XMOS
:version: 1.3.1
:scope: General Use
:description: FileIO library over xscope
:category: Filesystem
:keywords: stdio, fileio, xscope, xscope_fileio
:devices: xcore.ai, xcore-200

*******
Summary
*******

Provides a fast method for reading and writing files between an ``xcore.ai`` device and a host computer. 
It uses ``xscope`` to communicate between the two devices.

********
Features
********

  * Device and host FileIO library over xscope. 
  * Python module for seamless integration and execution of firmware.
  * 6MB/s Device to Host speed (vs 2KB/s for stdio).
  * 1MB/s Host to Device speed (vs 1KB/s for stdio).
  * Application for loopback testing on Simulator or Hardware.

************
Known issues
************

  * Missing the following stdio functions: ``fprintf`` , ``fscanf``. 
  * Byte only access: ``wb`` or ``rb`` file access mode only.

****************
Development repo
****************

  * `xscope_fileio Repository <https://www.github.com/xmos/xscope_fileio>`_.

*************
Documentation
*************

 * XMOS Libraries : `XMOS Website <https://www.xmos.com/libraries>`_.
 * Documentation source : `xscope_fileio Doc Source <https://github.com/xmos/xscope_fileio/tree/master/doc>`_.

**************
Required tools
**************

- XTC tools: |xtc_tools_version_| `XTC tools`_.
- Python: |python_version_| or later Python_.
- CMake: |cmake_version_| or later CMake_.


*********************************
Required libraries (dependencies)
*********************************

  * None

*************************
Related application notes
*************************

  * None

*******
Support
*******

This package is supported by XMOS Ltd. Issues can be raised against the software at: http://www.xmos.com/support
