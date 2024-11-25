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

  * 48000 and 44100 ADAT receivers
  * 48000 and 44100 ADAT transmitters
  * Application for loopback testing on Simulator or hardware

************
Known issues
************

  * ADAT Rx: Requirement for 100 MHz reference clock (#18)
  * ADAT Tx: No support for 256x master clock (i.e. 48 kHz from 12.288 MHz master clock) (#17)

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
