# Copyright 2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import os
import tempfile
from pathlib import Path

import xscope_fileio

file_dir = Path(__file__).parent.absolute()
root_dir = Path(__file__).parent.parent.absolute()
ref_text = b"Evolution is change in the heritable characteristics of biological populations over successive generations.\x00"
ref_mod_text = ref_text[0:10] + b"IS" + ref_text[12:]

def test_run_features():
    tmpdir = Path(tempfile.mkdtemp(prefix='tmp_throughput_', dir=file_dir))
    os.chdir(tmpdir) # so that the firmware can find the files

    with open(tmpdir/"features_ref.bin", "wb") as ref_file:
        ref_file.write(ref_text)

    firmware_xe = root_dir/"examples"/"fileio_features_xc"/"bin"/"fileio_features_xc.xe"
    print(f"Firmware: {firmware_xe}")
    print(f"Adapter_id: None")

    xscope_fileio.run_on_target(None, firmware_xe, use_xsim=True)
    with open(tmpdir/"features_dut.bin", "rb") as dut_file:
        dut_text = dut_file.read()
    with open(tmpdir/"features_dut_mod.bin", "rb") as dut_mod_file:
        dut_mod_text = dut_mod_file.read()

    assert dut_text == ref_text, "ERROR: features test failed (dut_text)"
    assert dut_mod_text == ref_mod_text, "ERROR: features test failed (dut_mod_text)"
    print("features test OK")


if __name__ == "__main__":
    test_run_features()
