#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import os
import pytest
import tempfile
import argparse
import numpy as np
import xscope_fileio
import xtagctl
from pathlib import Path
from multiprocessing import Process
from compare_bins import analyse_error_rate

file_dir = Path(__file__).parent.absolute()
root_dir = Path(__file__).parent.parent.absolute()

def run_throughput(size_mb, adapter_id: str = None):
    
    # create tmp folder and random file
    tmpdir = Path(tempfile.mkdtemp(prefix='tmp_throughput_', dir=file_dir))
    ref = np.random.randint(256, size=(size_mb * 1024 * 1024)).astype(np.uint8)
    ref.tofile(tmpdir/"throughput_ref.bin")
    
    # get adapter id if none is passed
    if adapter_id is None:
        with xtagctl.acquire("XCORE-AI-EXPLORER", timeout=10) as xtag_id:
            adapter_id = xtag_id

    # run the firmware
    os.chdir(tmpdir)
    firmware_xe = root_dir/"examples"/"throughput_c"/"bin"/"fileio_test.xe"
    print(f"Firmware: {firmware_xe}")
    print(f"Adapter_id: {adapter_id}")
    xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

    # compare the results
    dut = np.fromfile(tmpdir/"throughput_dut.bin", dtype=np.uint8)
    equal = np.array_equal(ref, dut)
    if not equal:
        analyse_error_rate(ref, dut)
        assert 0, "ERROR: throughput test failed"

def test_run_throughput(test_size=10):
    print(f"Running throughput test with {test_size} MB")
    pr = Process(target=run_throughput, args=(test_size,))
    pr.start()
    pr.join(timeout=30)
    pr.terminate()
    assert not pr.is_alive(), "ERROR: xscope_fileio process did not quit"

    
if __name__ == "__main__":
    """This test uses the throughput_c example to test the throughput of the fileio library.
    It can be used passing an adapter id or run by pytest so xtagctl will acquire() one. 
    """
    parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
    parser.add_argument("--adapter-id", help="adapter_id to use", default=None)
    args = parser.parse_args()
    run_throughput(3, args.adapter_id)
