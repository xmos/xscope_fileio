#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import numpy as np
import xscope_fileio
import os, sys
import xtagctl
import contextlib
import random, string


@contextlib.contextmanager
def cd(path):
    CWD = os.getcwd()
    os.mkdir(path)
    os.chdir(path)
    yield
    os.chdir(CWD)


def run_features():
    tmpdirname = 'tmp_features_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    test_dir = os.path.dirname(os.path.realpath(__file__)) + "/" + tmpdirname
    with cd(test_dir):
        ref_text = b"Evolution is change in the heritable characteristics of biological populations over successive generations." + b"\x00";
        with open("features_ref.bin", "wb") as ref_file:
            ref_file.write(ref_text)

        firmware_xe = test_dir + "/../../examples/fileio_features_xc/bin/fileio_features_xc.xe"
        xscope_fileio.run_on_target(None, firmware_xe, use_xsim=True)


        with open("features_dut.bin", "rb") as dut_file:
            dut_text = dut_file.read()

        with open("features_dut_mod.bin", "rb") as dut_mod_file:
            dut_mod_text = dut_mod_file.read()

        ref_mod_text = ref_text[0:10] + b"IS" + ref_text[12:]

        assert dut_text == ref_text
        print(dut_mod_text, ref_mod_text)
        assert dut_mod_text == ref_mod_text
    print("PASS")

if __name__ == "__main__":
    run_features()