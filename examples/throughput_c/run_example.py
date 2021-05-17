#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import numpy as np
import xscope_fileio
import os


firmware_xe = os.path.dirname(os.path.realpath(__file__)) + "/fileio_test.xe"
adapter_id = "L4Ss6YfM" #enter your xtag id here. Use xrun -l to find out what it is

ref = np.random.randint(256, size=(30 * 1024 * 1024)).astype(np.uint8)
ref.tofile("throughput_ref.bin")

xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

dut = np.fromfile("throughput_dut.bin", dtype=np.uint8)

assert np.array_equal(ref, dut)

print("PASS")