:orphan:

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

Provides a fast method for reading and writing files between an |xcore| device and a host computer. 
It uses |xscope| to communicate between the two devices.

********
Features
********

  * Device and host FileIO library over xscope. 
  * Python module for seamless integration and execution of firmware.
  * 6MB/s Device to Host speed (vs 2KB/s for stdio).
  * 1MB/s Host to Device speed (vs 1KB/s for stdio).
  * Application for loopback testing on Simulator or hardware

************
Known issues
************

  * Missing the following stdio functions: ``fprintf`` , ``fscanf``. 
  * Byte only access: ``wb`` or ``rb`` file access mode only.

****************
Development repo
****************

  * `lib_adat <https://www.github.com/xmos/lib_adat>`_

**************
Required tools
**************

  * XMOS XTC Tools: 15.3.0

*********************************
Required libraries (dependencies)
*********************************

  * None

*************************
Related application notes
*************************

The following application notes use this library:

  * `AN02003: SPDIF/ADAT/I²S Receive to I²S Slave Bridge with ASRC <https://www.xmos.com/file/an02003>`_

*******
Support
*******

This package is supported by XMOS Ltd. Issues can be raised against the software at: http://www.xmos.com/support
