#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import os
import pytest
import tempfile
import argparse
import numpy as np
from pathlib import Path
from multiprocessing import Process
from compare_bins import analyse_error_rate
import subprocess
import xscope_fileio
import xtagctl

file_dir = Path(__file__).parent.absolute()
root_dir = Path(__file__).parent.parent.absolute()

test_sizes_hw1 = [64]
test_sizes_hw2 = [5, 10, 7] # in MB

def fn_run_throughput(size_mb, adapter_id: str = None):
    # run xrun -l to see adapters
    subprocess.run(["xrun", "-l"], check=True)
    
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

def run_throughput(test_size=10, timeout=30):
    print(f"Running throughput test with {test_size} MB")
    pr = Process(target=fn_run_throughput, args=(test_size,))
    pr.start()
    pr.join(timeout=timeout)
    return_code = pr.exitcode
    pr.terminate()
    assert return_code == 0, "ERROR: xscope_fileio process failed"
    assert not pr.is_alive(), "ERROR: xscope_fileio process did not quit"

@pytest.mark.parametrize("test_size", test_sizes_hw1)
def test_throughput_1(test_size):
    run_throughput(test_size, timeout=60)

@pytest.mark.parametrize("test_size", test_sizes_hw2)
def test_throughput_2(test_size):
    run_throughput(test_size)
    
if __name__ == "__main__":
    """This test uses the throughput_c example to test the throughput of the fileio library.
    It can be used passing an adapter id or run by pytest so xtagctl will acquire() one. 
    """
    parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
    parser.add_argument("--adapter-id", help="adapter_id to use", default=None)
    args = parser.parse_args()
    fn_run_throughput(3, args.adapter_id)
