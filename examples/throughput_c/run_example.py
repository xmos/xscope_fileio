#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import subprocess
import numpy as np
import xscope_fileio
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
parser.add_argument("--adapter-id", help="adapter_id to use", required=True)
try:
    args = parser.parse_args()
    adapter_id = args.adapter_id
    print(f"Using adapter ID: {adapter_id}")
except SystemExit:
    print('Note: run "xrun -l" to see available adapters')
    exit(1)

firmware_xe = (Path(__file__).parent / "bin" / "fileio_test.xe").absolute()

ref = np.random.randint(256, size=(30 * 1024 * 1024)).astype(np.uint8)
ref.tofile("throughput_ref.bin")

xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

dut = np.fromfile("throughput_dut.bin", dtype=np.uint8)

assert np.array_equal(ref, dut)
print("Example run successfully!")
