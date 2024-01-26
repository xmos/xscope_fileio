import argparse
import shutil
from pathlib import Path

import xtagctl
import xscope_fileio
from multiprocessing import Process

firmware_xe = (Path(__file__).parent /
"close_files" / "bin" / "xscope_fileio_close.xe").absolute()
output_folder = (Path.cwd() / "output").absolute()
# output folder will be created in the same directory as this script


def fn_close_files(adapter_id: str = None):
    """This test perform several opening and closing of files on the device.
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
        print("Acquiring adapter_id...")
        with xtagctl.acquire("XCORE-AI-EXPLORER", timeout=10) as adapter_id:
            print("Adapter ID: ", adapter_id)
            rtrn_code = xscope_fileio.run_on_target(
                adapter_id, firmware_xe, use_xsim=False
            )
    else:
        rtrn_code = xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)

    assert rtrn_code == 0, "xscope_fileio.run_on_target() failed"


def test_close_files():
    pr = Process(target=fn_close_files)
    pr.start()
    pr.join(timeout=60)
    pr.terminate()
    assert not pr.is_alive(), "ERROR: xscope_fileio process did not quit"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run xscope_fileio_close.xe")
    parser.add_argument("--adapter-id", help="adapter_id to use", default=None)
    args = parser.parse_args()
    fn_close_files(adapter_id=args.adapter_id)
