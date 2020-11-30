# Copyright (c) 2020, XMOS Ltd, All rights reserved
import contextlib
import os
from pathlib import Path
import socket
import sys
import time

import sh

# How long in seconds we would expect xrun to open a port for the host app
# The firmware will have already been loaded so 5s is more than enough
# as long as the host CPU is not too busy. This can be quite long (10s+)
# for a busy CPU
XRUN_TIMEOUT = 20


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def print_output(x, verbose):
    if verbose:
        print(x, end="")
    else:
        print(".", end="", flush=True)


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def test_port_is_open(port):
    port_open = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("", port))
    except OSError:
        port_open = False
    s.close()
    return port_open


class xrun_exit_handler:
    def __init__(self, adapter_id, test_wav_exe):
        self.adapter_id = adapter_id
        self.test_wav_exe = test_wav_exe
        self.host_process = None

    def set_host_process(self, host_process):
        self.host_process = host_process

    def xcore_done(self, cmd, success, exit_code):
        if not success:
            # xrun_cmd = f"--dump-state --adapter-id {self.adapter_id} {self.test_wav_exe}"
            # dump = sh.xrun(xrun_cmd.split(), _out=print_output)
            # sys.stderr.write(dump.stdout.decode())
            self.host_process.terminate()


def run_on_target(adapter_id, test_wav_exe, host_exe, use_xsim=False):
    port = get_open_port()
    xrun_cmd = (
        f"--xscope-port localhost:{port} --adapter-id {adapter_id} {test_wav_exe}"
    )
    xsim_cmd = ["--xscope", f"-realtime localhost:{port}", test_wav_exe]

    sh_print = lambda x: print_output(x, True)

    # Start and run in background
    exit_handler = xrun_exit_handler(adapter_id, test_wav_exe)
    if use_xsim:
        print(xsim_cmd)
        xrun_proc = sh.xsim(xsim_cmd, _bg=True)
    else:
        print(xrun_cmd)
        xrun_proc = sh.xrun(
            xrun_cmd.split(),
            _bg=True,
            _bg_exc=False,
            _out=sh_print,
            _done=exit_handler.xcore_done,
            _err=sys.stderr,
        )

    print("Waiting for xrun", end="")
    timeout = time.time() + XRUN_TIMEOUT
    while test_port_is_open(port):
        print(".", end="", flush=True)
        time.sleep(0.1)
        if time.time() > timeout:
            xrun_proc.kill_group()
            assert 0, f"xrun timed out - took more than {XRUN_TIMEOUT} seconds to start"

    print()

    print("Starting host app...", end="\n")

    host_args = f"{port}"
    host_proc = sh.Command(host_exe)(host_args.split(), _bg=True, _out=sh_print)
    exit_handler.set_host_process(host_proc)
    host_proc.wait()

    print("Running on target finished")

