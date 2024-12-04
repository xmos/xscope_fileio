from pathlib import Path
import xscope_fileio

adapter_id = xscope_fileio.get_adapter_id()
firmware_xe = Path(__file__).parent / "bin" / "minimal.xe"

xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)
