# Copyright (c) 2016 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.


import os
import getpass
import psutil


class NoSessionError(Exception):
    pass


def set_dbus():
    """Make sure DBUS_SESSION_BUS_ADDRESS and DISPLAY, which are needed for sending desktop notifications, are set."""

    if os.environ.get('DBUS_SESSION_BUS_ADDRESS'):
        return

    username = getpass.getuser()

    for proc in psutil.process_iter():
        try:
            if proc.username() != username:
                continue

            proc_name = proc.name()
            if '-session' in proc_name:
                dbus = proc.environ().get('DBUS_SESSION_BUS_ADDRESS')
                if dbus:
                    os.environ['DBUS_SESSION_BUS_ADDRESS'] = dbus
                    os.environ['DISPLAY'] = proc.environ().get('DISPLAY') or ':0.0'
                    return

        except (psutil.ZombieProcess, PermissionError, psutil.AccessDenied, IndexError):
            continue

    raise NoSessionError("Could not find var 'DBUS_SESSION_BUS_ADDRESS' in environment or /proc in a process named '*-session*', for user '{username}'.".format(
        username=username))
