from distutils.command.build import build
import os
import setuptools
import subprocess
import contextlib


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


class CustomBuildCommand(build):
    """Customized setuptools install command - prints a friendly greeting."""

    def run(self):
        # Make the host binary
        with pushd("xscope_fileio/host/"):
            subprocess.run("make")

        build.run(self)


setuptools.setup(
    name="xscope_fileio",
    version="0.1.0",
    cmdclass={"build": CustomBuildCommand,},
    # Note for anyone trying to copy this pattern:
    # package_data keys are NAMES OF PACKAGES, not dirs
    # So it's "xscope_fileio" not "xscope_fileio/"
    package_data={
        "xscope_fileio": [
            "host/Makefile",
            "host/xscope_io_host.c",
            "host/xscope_host_endpoint",
        ]
    },
    packages=setuptools.find_packages(),
)
