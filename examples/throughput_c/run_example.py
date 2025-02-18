# Copyright 2021-2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

# We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import subprocess
import numpy as np
import xscope_fileio
import argparse
from pathlib import Path

firmware_xe = (Path(__file__).parent / "bin" / "fileio_test.xe").absolute()
adapter_id = 0

# create reference file (random)
ref = np.random.randint(256, size=(30 * 1024 * 1024)).astype(np.uint8)
ref.tofile("throughput_ref.bin")

# run example
xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

# compare reference and output
dut = np.fromfile("throughput_dut.bin", dtype=np.uint8)
assert np.array_equal(ref, dut)

print("Example run successfully!")
