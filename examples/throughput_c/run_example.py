#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import numpy as np
import xscope_fileio

firmware_xe = "fileio_test.xe"
adapter_id = "L4Ss6YfM"

ref = np.random.randint(256, size=(30 * 1024 * 1024)).astype(np.uint8)
ref.tofile("ref.bin")

xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

dut = np.fromfile("dut.bin", dtype=np.uint8)

assert np.array_equal(ref, dut)

print("PASS")