# Copyright 2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import platform
import subprocess
from pathlib import Path

CWD = Path(__file__).parent.absolute()

def build_host_app():
    """Builds the host application

    Raises:
        NotImplementedError: If the platform is not supported
    """
    print("Building xscope fileio host application for: ", platform.system())
    if platform.system() in ["Darwin", "Linux"]:
        cmd_cmake = "cmake --fresh -B build"
        cmd_make = "make -C build"
        subprocess.run(cmd_cmake, shell=True, check=True, cwd=CWD)
        subprocess.run(cmd_make, shell=True, check=True, cwd=CWD)
    elif platform.system() == "Windows":
        try:
            cmd_cmake = "cmake --fresh -B build -G Ninja"
            cmd_make = "ninja -C build"
            subprocess.run(cmd_cmake, shell=True, check=True, cwd=CWD)
            subprocess.run(cmd_make, shell=True, check=True, cwd=CWD)
        except subprocess.CalledProcessError:
            print("Error: Build failed")
    else:
        raise NotImplementedError(f"Unsupported platform: {platform.system()}")
    print("Build complete")


if __name__ == "__main__":
    build_host_app()
