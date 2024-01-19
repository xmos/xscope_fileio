from pathlib import Path
import xscope_fileio
import shutil

firmware_xe = (Path(__file__).parent / "bin" / "xscope_fileio_close.xe").absolute()
output_folder = (Path(__file__).parent / "output").absolute()

# renew the folder
shutil.rmtree(output_folder, ignore_errors=True)
output_folder.mkdir(parents=False, exist_ok=True)

# run the program
# enter your xtag id here. Use xrun -l to find out what it is
adapter_id = "EHV92U6D"

print("Adapter ID: ", adapter_id)
print("Firmware: ", firmware_xe)
print("Output folder: ", output_folder)

xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)
