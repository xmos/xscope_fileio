# Copyright 2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import argparse
from pathlib import Path
from multiprocessing import Process

import xscope_fileio

test_path = Path(__file__).parent
firmware_xe = test_path / "simple" / "bin" / "test_simple.xe"


def fn_simple(adapter_id: str = None):
    print("Firmware: ", firmware_xe)
    use_xsim = True if adapter_id is None else False
    rtrn_code = xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=use_xsim)
    assert rtrn_code == 0, "xscope_fileio.run_on_target() failed"


def test_simple(adapter_id: str = None):
    """
    This function is just a wrapper to control
    time of execution of the close files test in case of hang
    """
    pr = Process(target=fn_simple, args=(adapter_id,))
    pr.start()
    pr.join(timeout=30)
    return_code = pr.exitcode
    pr.terminate()
    assert return_code == 0, "ERROR: test_close_files failed"
    assert not pr.is_alive(), "ERROR: xscope_fileio process did not quit"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
    parser.add_argument("--adapter-id", help="adapter_id to use", default=None)
    args = parser.parse_args()
    fn_simple(args.adapter_id)
