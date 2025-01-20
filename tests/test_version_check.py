import re
import sys
import io
import pytest
import subprocess
from pathlib import Path

test_path = Path(__file__).parent
xscope_io_common = test_path.parent / "xscope_fileio" / "xscope_io_common.h"
firmware_xe = test_path / "simple" / "bin" / "test_simple.xe"
python_path = sys.executable


# test matrix
# initial, new, return_code, msg
test_cases = [
    ("1.3.1", "1.3.1", 0, ""),  # no change
    ("1.3.1", "1.3.2", 0, ""),  # patch version change
    ("1.3.1", "1.4.0", 0, "Warning"),  # minor version change
    ("1.3.1", "2.3.0", 1, "Error"),  # major version change
]


def set_io_common_version(file_path, new_version):
    with open(file_path, "r+") as file:
        content = file.read()
        content = re.sub(
            r'#define XSCOPE_IO_VERSION\s+"[\d.]+',
            f'#define XSCOPE_IO_VERSION\t\t"{new_version}',
            content,
        )
        file.seek(0)
        file.write(content)


def reinstall_package():
    resintall_package_cmd = [python_path, "-m", "pip", "install", "-e", "."]
    subprocess.run(resintall_package_cmd, check=True, cwd=test_path.parent)


def build_run_test_simple():
    kwargs = dict(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
        cwd=test_path,
    )
    cmake_cmd = ["cmake", "--fresh", "-G", "Ninja", "-B", "build", "-S", "simple"]
    build_cmd = ["cmake", "--build", "build"]
    run_cmd = [python_path, "test_simple.py"]
    subprocess.run(cmake_cmd, **kwargs)
    subprocess.run(build_cmd, **kwargs)
    kwargs.pop("check")  # remove check=True
    proc = subprocess.run(run_cmd, **kwargs)
    return proc


@pytest.mark.parametrize("initial, new, return_code, msg", test_cases)
def test_device_version_change(initial, new, return_code, msg):
    try:
        set_io_common_version(xscope_io_common, new)
        proc = build_run_test_simple()
        assert proc.returncode == return_code
        assert msg in proc.stderr or msg in proc.stdout
    finally:
        set_io_common_version(xscope_io_common, "1.3.1")


if __name__ == "__main__":
    pytest.main(["-s", __file__])
