# Xscope FileIO

This library allows the user to read/write files on the host machine via xscope.

Source and header files for device code are found in `src_xcore`

The host-side interface is written in Python. To run an xe with access to xscope fileIO,
use:
```
xscope_fileio.run_on_target(adapter_id, firmware_xe, use_xsim=False)
```

This call will run the binary on the connected target specified by `adapter_id` using
xrun, and simultaneously launch a host application to communicate xscope data to/from 
the xrun process via sockets. The host application responds to `xscope_fileio` API calls
in the firmware code, reading/writing to the host file system.

The call to `run_on_target` returns when the firmware exits.

## Installation

`pip install -e .`
or
`pip install .`

To compile firmware code, add `src_xcore` to your source dirs and include dirs. Ensure
you use the `config.xscope` included in `src_xcore`.
