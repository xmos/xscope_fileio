import sysconfig
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # Set the desired wheel tags
        python_tag = "py3"  # Python 3+ only
        abi_tag = "none"    # Common ABI for Python 3+
        platform = sysconfig.get_platform().replace(".", "_").replace("-", "_")
        build_data['tag'] = f"{python_tag}-{abi_tag}-{platform}"
        
