import platform
import sysconfig
import subprocess
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from pathlib import Path


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # Build the endpoint and set the tag
        self.build_host_app()
        build_data["tag"] = self.get_tag()

    def build_host_app(self):
        """Builds the host application

        Raises:
            NotImplementedError: If the platform is not supported
        """
        HOST_PATH = Path(self.root) / "host"
        print("Building xscope fileio host application for: ", platform.system())
        print("HOST_PATH: ", HOST_PATH)

        if platform.system() in ["Darwin", "Linux"]:
            cmd_cmake = ["cmake", "--fresh", "-B", "build"]
            cmd_make = ["make", "-C", "build"]
            subprocess.run(cmd_cmake, check=True, cwd=HOST_PATH)
            subprocess.run(cmd_make, check=True, cwd=HOST_PATH)
        elif platform.system() == "Windows":
            try:
                cmd_cmake = ["cmake", "--fresh", "-B", "build", "-G", "Ninja"]
                cmd_make = ["ninja", "-C", "build"]
                subprocess.run(cmd_cmake, check=True, cwd=HOST_PATH)
                subprocess.run(cmd_make, check=True, cwd=HOST_PATH)
            except subprocess.CalledProcessError:
                print("Error: Build failed")
        else:
            raise NotImplementedError(f"Unsupported platform: {platform.system()}")


    def get_tag(self):
        python_tag = "py3"  # Python 3+ only
        abi_tag = "none"  # Common ABI for Python 3+
        platform = sysconfig.get_platform().replace(".", "_").replace("-", "_")
        tag = f"{python_tag}-{abi_tag}-{platform}"
        return tag


#
