#We assume that the Xscope FileIO Python library has been installed via pip beforehand and is available to import. Please see readme for instuctions.
import xscope_fileio
import xtagctl
from pathlib import Path

# For timing out on fn call
from multiprocessing import Process
import time

def read_non_existsing_file():
    with xtagctl.acquire("XCORE-AI-EXPLORER", timeout=10) as adapter_id:
        firmware_xe = Path(__file__).parent / "no_hang/no_hang.xe"
        print(f"Found adapter_id: {adapter_id}")
        xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)


if __name__ == '__main__':
    my_test = Process(target=read_non_existsing_file)
    my_test.start()
    my_test.join(timeout=10) # 10s enough time to launch and complete if working, even with empty XTAG firmware

    print("Checking to see if xscope_fileio process hung..")

    my_test_was_alive = my_test.is_alive()
    my_test.terminate()

    assert not my_test_was_alive, "ERROR: xscope_fileio process did not quit"

    print("***TEST PASS***")
