# Copyright 2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import time
import argparse
from pathlib import Path

import xscope_fileio

test_path = Path(__file__).parent
firmware_xe = test_path / "simple" / "bin" / "test_simple.xe"


def test_simple(adapter_id: str = None):
    """
    This function runs test simple binary on the target.
    """
    use_xsim = True if adapter_id is None else False
    return_code = xscope_fileio.run_on_target(
        adapter_id, firmware_xe, use_xsim=use_xsim
    )
    assert return_code == 0, "ERROR: test_simple failed"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
    parser.add_argument("--adapter-id", help="adapter_id to use", default=None)
    args = parser.parse_args()
    test_simple(args.adapter_id)
