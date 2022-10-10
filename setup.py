from distutils.command.build import build
from setuptools.command.develop import develop
import os
import setuptools
import subprocess
import contextlib
import platform


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


class CustomBuildCommand(build):
    """Customized distutils build command """

    def run(self):
        # Can't assume a specific build command for Windows, so just build for Linux and Mac
        if platform.system() in ['Darwin', 'Linux']:
            # Make the host binary
            with pushd("host/"):
                subprocess.check_output(["cmake", "."])
                subprocess.check_output(["make"])
        build.run(self)


class CustomDevelopCommand(develop):
    """Customized setuptools develop command """

    def run(self):
        # Can't assume a specific build command for Windows, so just build for Linux and Mac
        if platform.system() in ['Darwin', 'Linux']:
            # Make the host binary
            with pushd("host/"):
                subprocess.check_output(["cmake", "."])
                subprocess.check_output(["make"])
        develop.run(self)


setuptools.setup(
    name="xscope_fileio",
    version="1.1.2",
    cmdclass={"build": CustomBuildCommand, "develop": CustomDevelopCommand,},
    # Note for anyone trying to copy this pattern:
    # package_data keys are NAMES OF PACKAGES, not dirs
    # So it's "xscope_fileio" not "xscope_fileio/"
    package_data={
        "xscope_fileio": [
            "../host/Makefile",
            "../host/xscope_io_host.c",
            "../host/xscope_host_endpoint",
        ]
    },
    packages=setuptools.find_packages(),
)
