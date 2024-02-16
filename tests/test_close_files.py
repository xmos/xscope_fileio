import argparse
import shutil
from pathlib import Path

import xscope_fileio
import xtagctl

from multiprocessing import Process

firmware_xe = (Path(__file__).parent /
"close_files" / "bin" / "xscope_fileio_close.xe").absolute()
output_folder = (Path.cwd() / "output").absolute()
# output folder will be created in the same directory as this script


def fn_close_files(adapter_id: str = None):
    """This test performs several openings and closings of files on the device.
    It is intended to test the robustness of the file system and 
    the xscope_fclose function.

    Args:
        adapter_id (str, optional): _description_. Defaults to None.
    """

    rtrn_code = 1
    # renew the folder
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir(parents=False, exist_ok=True)

    # print info
    print("Firmware: ", firmware_xe)
    print("Output folder: ", output_folder)

    if adapter_id is None:
        with xtagctl.acquire("XCORE-AI-EXPLORER", timeout=10) as adapter_id:
            print(f"Found adapter_id: {adapter_id}")
            rtrn_code = xscope_fileio.run_on_target(
                adapter_id, firmware_xe, use_xsim=False
            )
    else:
        rtrn_code = xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

    assert rtrn_code == 0, "xscope_fileio.run_on_target() failed"


def test_close_files(adapter_id: str = None):
    """
    This function is just a wrapper to control 
    time of execution of the close files test in case of hang
    """
    pr = Process(target=fn_close_files, args=(adapter_id,))
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

    test_close_files(args.adapter_id)
