#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import subprocess
import xscope_fileio
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
parser.add_argument("--adapter-id", help="adapter_id to use", required=True)
try:
    args = parser.parse_args()
    adapter_id = args.adapter_id
    print(f"Using adapter ID: {adapter_id}")
except SystemExit:
    print('Note: run "xrun -l" to see available adapters')
    exit(1)



firmware_xe = (Path(__file__).parent / "bin" / "fileio_features_xc.xe").absolute()
ref_text = b"Evolution is change in the heritable characteristics of biological populations over successive generations." + b"\x00"

with open("features_ref.bin", "wb") as ref_file:
    ref_file.write(ref_text)

xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=True)

with open("features_dut.bin", "rb") as dut_file:
    dut_text = dut_file.read()

with open("features_dut_mod.bin", "rb") as dut_mod_file:
    dut_mod_text = dut_mod_file.read()

ref_mod_text = ref_text[0:10] + b"IS" + ref_text[12:]

assert dut_text == ref_text
print(dut_mod_text, ref_mod_text)
assert dut_mod_text == ref_mod_text

print("PASS")
