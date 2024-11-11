# Copyright 2020-2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import os
import setuptools
import subprocess
import platform

from pathlib import Path
from distutils.command.build import build
from setuptools.command.develop import develop

CWD = Path(__file__).parent.absolute()
HOST_PATH = CWD / "host"
CMD_CMAKE = "cmake -B build"
CMD_MAKE = "make -C build"
LIB_VERSION = "1.2.0"

class CustomBuildCommand(build):
    """Customized distutils build command """

    def run(self):
        # Can't assume a specific build command for Windows, so just build for Linux and Mac
        if platform.system() in ['Darwin', 'Linux']:
            # Make the host binary
            subprocess.run(CMD_CMAKE, shell=True, check=True, cwd=HOST_PATH)
            subprocess.run(CMD_MAKE, shell=True, check=True, cwd=HOST_PATH)
        
        build.run(self)

class CustomDevelopCommand(develop):
    """Customized setuptools develop command """

    def run(self):
        # Can't assume a specific build command for Windows, so just build for Linux and Mac
        if platform.system() in ['Darwin', 'Linux']:
            # Make the host binary
            subprocess.run(CMD_CMAKE, shell=True, check=True, cwd=HOST_PATH)
            subprocess.run(CMD_MAKE, shell=True, check=True, cwd=HOST_PATH)
        
        develop.run(self)


setuptools.setup(
    name="xscope_fileio",
    version=LIB_VERSION,
    cmdclass={"build": CustomBuildCommand, "develop": CustomDevelopCommand,},
    package_data={
        "xscope_fileio": [
            "../host/Makefile",
            "../host/xscope_io_host.c",
            "../host/xscope_host_endpoint",
        ]
    },
    packages=setuptools.find_packages(),
)

# Note:
# package_data keys are NAMES OF PACKAGES, not dirs
# So it's "xscope_fileio" not "xscope_fileio/"
