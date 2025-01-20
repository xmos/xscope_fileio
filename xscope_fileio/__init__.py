# Copyright 2020-2024 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import contextlib
import os
from pathlib import Path
import socket
import sys
import time
import platform

import subprocess
import threading, queue

from typing import Union
from importlib.resources import files

# How long in seconds we would expect xrun to open a port for the host app
# The firmware will have already been loaded so 5s is more than enough
# as long as the host CPU is not too busy. This can be quite long (10s+)
# for a busy CPU
XRUN_TIMEOUT = 20


def _get_host_exe():
    """ Returns the path the the host exe """
    package_path = files("xscope_fileio")
    host_path_wh = package_path / "host"
    host_path_ed = package_path.parent / "host"
    # check is none exists
    if not host_path_wh.exists() and not host_path_ed.exists():
        raise FileNotFoundError(f"Host not found at {host_path_wh} or {host_path_ed}")
    # if wheel is installed, use that, otherwise use the editable version
    host_path = host_path_wh if host_path_wh.exists() else host_path_ed
    endp = "xscope_host_endpoint.exe" if platform.system() == 'Windows' else "xscope_host_endpoint"
    endp = host_path / endp
    assert endp.exists(), f"Host not found at {endp}" 
    return str(endp)


def _get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def _test_port_is_open(port):
    port_open = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("localhost", port))
    except OSError:
        port_open = False
    s.close()
    return port_open


class _XrunExitHandler:
    def __init__(self, adapter_id, firmware_xe):
        self.adapter_id = adapter_id
        self.firmware_xe = firmware_xe
        self.host_process = None

    def set_host_process(self, host_process):
        self.host_process = host_process

    def xcore_done(self, cmd, success, exit_code):
        if not success:
            self.host_process.terminate()

def popenAndCall(onExit, *popenArgs, **popenKWArgs):
    """
    Asynchronously runs a subprocess and executes a callback function upon completion.

    Parameters
    ----------
    onExit : callable
        Function to execute when the subprocess completes.
    *popenArgs : 
        Positional arguments passed to subprocess.Popen.
    **popenKWArgs : 
        Keyword arguments passed to subprocess.Popen.

    Returns
    -------
    subprocess.Popen
        Object representing the subprocess, returned immediately after thread starts.
    """
    def runInThread(onExit, popenArgs, popenKWArgs, q):
        proc = subprocess.Popen(*popenArgs, **popenKWArgs)
        q.put(proc)
        proc.wait()
        onExit(proc.args, proc.returncode == 0, proc.returncode)
        assert proc.returncode == 0, f'\nERROR: xrun exited with error code {proc.returncode}\n'
        return

    q = queue.Queue()
    thread = threading.Thread(target=runInThread,
                              args=(onExit, popenArgs, popenKWArgs, q))
    thread.start()

    return q.get() # returns immediately after the thread starts



def run_on_target(
        adapter_id: Union[str, int, None],
        firmware_xe: str,
        use_xsim: bool = False,
        **kwargs: dict
    ) -> int:
    """
    Run a target application using xrun or xsim along with a host application.

    Parameters
    ----------
    adapter_id : str or int or None
        Argument for xrun. If str xrun will use --adapter-id, if int will use --id.
        Use None when using xsim.
    firmware_xe : str
        The path to the firmware executable.
    use_xsim : bool, optional
        If True, use xsim; otherwise, use xrun. Default is False.
    **kwargs
        Additional keyword arguments to be passed to subprocess.Popen.

    Returns
    -------
    int
        The return code of the host process.

    Raises
    ------
    AssertionError
        If xrun times out or if the host app exits with a non-zero return code.

    Notes
    -----
    This function starts the target application using xrun or xsim, and a host application
    to communicate with the target. The host application runs in a separate process.

    The function monitors the status of xrun to ensure it starts within a specified timeout.
    If xrun takes longer than the timeout, the function terminates the process.

    If the host application exits with a non-zero return code, the function terminates
    the xrun process and raises an AssertionError.

    Examples
    --------
    To run the target application using xrun:
    >>> run_on_target(adapter_id, 'firmware.xe')

    To run the target application using xsim:
    >>> run_on_target(None, 'firmware.xe', use_xsim=True)
    """
    
    # raise invalid argument error
    if adapter_id is None and use_xsim is False:
        raise ValueError("Invalid argument: adapter_id must be set when xsim is False")

    if isinstance(adapter_id, int):
        adapt_arg, did = "--id", f"{adapter_id}"
    elif isinstance(adapter_id, str):
        adapt_arg, did = "--adapter-id", f"{adapter_id}"
    else:
        adapt_arg, did = "", ""
    
    # get open port
    port = _get_open_port()
    
    # Start and run in background
    firmware_xe = str(Path(firmware_xe).resolve())
    exit_handler = _XrunExitHandler(adapter_id, firmware_xe)
    if use_xsim:
        xsim_cmd = ["xsim", "--xscope", f"-realtime localhost:{port}", firmware_xe]
        print(xsim_cmd)
        xrun_proc = subprocess.Popen(xsim_cmd)
    else:
        xrun_cmd = ["xrun", "--xscope-port", f"localhost:{port}", adapt_arg, did, firmware_xe]
        print(xrun_cmd)
        xrun_proc = popenAndCall(exit_handler.xcore_done, xrun_cmd, **kwargs)

    print("Waiting for xrun", end="")
    timeout = time.time() + XRUN_TIMEOUT
    while _test_port_is_open(port):
        print(".", end="", flush=True)
        time.sleep(0.1)
        if time.time() > timeout:
            xrun_proc.terminate()
            assert 0, f"xrun timed out - took more than {XRUN_TIMEOUT} seconds to start"

    print("\nStarting host app...\n")
    host_exe = _get_host_exe()
    host_args = f"{port}"
    host_proc = subprocess.Popen([host_exe] + host_args.split(), **kwargs)
    exit_handler.set_host_process(host_proc)
    host_proc.wait()
    
    # if device exited with error, terminate devide process
    if host_proc.returncode != 0:
        xrun_proc.terminate()
        assert 0, f'\nERROR: host app exited with error code {host_proc.returncode}\n'
    
    return host_proc.returncode
