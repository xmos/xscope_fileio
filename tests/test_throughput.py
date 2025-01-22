# Copyright 2021-2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
"""
This test uses the throughput_c example to test the throughput of the fileio library.
It can be used passing an adapter id or run by pytest so xtagctl will acquire() one. 

We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. 
Please see readme for instuctions.
"""
import os
import time
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

# Test sizes for each hardware
# Hw1 will run a single big file
# Hw2 will run multiple small files
test_sizes_hw1 = [64]        # in MB
test_sizes_hw2 = [5, 10, 7]  # in MB


def run_throughput(size_mb, adapter_id: str = None):
    # run xrun -l to see adapters
    subprocess.run(["xrun", "-l"], check=True)

    # create tmp folder and random file
    tmpdir = Path(tempfile.mkdtemp(prefix="tmp_throughput_", dir=file_dir))
    ref = np.random.randint(256, size=(size_mb * 1024 * 1024)).astype(np.uint8)
    ref.tofile(tmpdir / "throughput_ref.bin")

    # get adapter id if none is passed
    if adapter_id is None:
        with xtagctl.acquire("XCORE-AI-EXPLORER", timeout=10) as xtag_id:
            adapter_id = xtag_id

    # run the firmware
    os.chdir(tmpdir)
    firmware_xe = root_dir / "examples" / "throughput_c" / "bin" / "fileio_test.xe"
    print(f"Firmware: {firmware_xe}")
    print(f"Adapter_id: {adapter_id}")
    xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

    # compare the results
    dut = np.fromfile(tmpdir / "throughput_dut.bin", dtype=np.uint8)
    equal = np.array_equal(ref, dut)
    if not equal:
        analyse_error_rate(ref, dut)
        raise ValueError("ERROR: throughput test failed")


def run_throughput_for_sizes(test_sizes: list = [3]):
    # Run the throughput test for each size, sequentially
    for size in test_sizes:
        run_throughput(size)
        time.sleep(1)  # give time to the target to reconnect


def join_all_processes(proc_list, timeout=120):
    for proc in proc_list:
        proc.join(timeout=timeout)
        assert not proc.is_alive(), f"ERROR: process {proc.name} is still running"
        assert (proc.exitcode == 0), f"ERROR: process {proc.name} failed, exit code {proc.exitcode}"


def test_throughput_parallel():
    # Create the processes in parallel
    pr1 = Process(target=run_throughput_for_sizes, args=(test_sizes_hw1,), name="hw1")
    pr2 = Process(target=run_throughput_for_sizes, args=(test_sizes_hw2,), name="hw2")

    # Start the processes
    pr1.start()
    pr2.start()

    # Wait for the processes to finish
    join_all_processes([pr1, pr2])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
    parser.add_argument("--adapter-id", help="adapter_id to use", required=True)
    args = parser.parse_args()
    run_throughput(64, args.adapter_id)
