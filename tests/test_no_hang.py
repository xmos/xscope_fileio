# Copyright 2023-2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import pytest
import argparse

import xscope_fileio
import xtagctl

from pathlib import Path
from multiprocessing import Process


def read_non_existsing_file(adapter_id: str = None):
    firmware_xe = (Path(__file__).parent / "no_hang" / "bin" / "no_hang.xe").absolute()
    if adapter_id is None:
        with xtagctl.acquire("XCORE-AI-EXPLORER", timeout=10) as xtag_id:
            adapter_id = xtag_id

    print(f"Firmware: {firmware_xe}")
    print(f"Adapter_id: {adapter_id}")
    try:
        xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)
    except AssertionError:
        print("Expected error, exisitng app...")
        exit(0) # expeted error
    
def test_non_existsing_file(adapter_id: str = None):
    """
    This function is just a wrapper to control to use with pytest
    time of execution of the close files test in case of hang
    """
    pr = Process(target=read_non_existsing_file, args=(adapter_id,))
    pr.start()
    pr.join(timeout=30)
    pr.terminate()
    assert not pr.is_alive(), "ERROR: xscope_fileio process did not quit"

if __name__ == '__main__':
    """
    This test intentionally tries to open an invalid read file which used to cause
    a hang in run_on_target(). This is now fixed but the test remains in case of 
    a regression. 
    
    It can be used passing an adapter id or with xtagctl.acquire() to get one
    """
    parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
    parser.add_argument("--adapter-id", help="adapter_id to use", required=True)
    args = parser.parse_args()
    test_non_existsing_file(args.adapter_id)
