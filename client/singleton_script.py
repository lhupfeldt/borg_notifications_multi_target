#!/bin/python3

# Copyright (c) 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.

import sys, os, platform
system = platform.system()
has_psutil = system != 'Windows' and not system.startswith('CYGWIN')
if has_psutil:
    import psutil


def singleton_script():
    proc_name = os.path.basename(__file__)
    my_proc = None

    if not has_psutil:
        print("Warning single instance invocation not checked on Windows, make sure you only run one backup at any time")
        return

    for proc in psutil.process_iter():
        try:
            try:
                # Handle script called as 'python <script>'
                arg_name = os.path.basename(proc.cmdline()[1]) if len(proc.cmdline()) > 1 else None
            except (psutil.ZombieProcess):
                continue
            except (PermissionError, psutil.AccessDenied, IndexError) as ex:
                arg_name = None

            if proc_name in (os.path.basename(proc.name()), arg_name):
                if my_proc:
                    print("Already running")
                    sys.exit(1)
                my_proc = proc

        except UnicodeDecodeError:
            # Workaround for broken psutils on non english installation
            # Singleton is still guaranteed if script is installed in a full path with an 'ascii' name
            pass


if __name__ == "__main__":
    import time
    singleton_script()
    print("Going to sleep for 10 seconds. Run one more of me to test!")
    time.sleep(10)
