import setuptools

setuptools.setup(
    name="xscope_fileio",
    version="0.1.0",
    # Note for anyone trying to copy this pattern:
    # package_data keys are NAMES OF PACKAGES, not dirs
    # So it's "xscope_fileio" not "xscope_fileio/"
    package_data={'xscope_fileio': ['host_src/Makefile', "host_src/xscope_io_host.c"]},
    packages=setuptools.find_packages(),
)
