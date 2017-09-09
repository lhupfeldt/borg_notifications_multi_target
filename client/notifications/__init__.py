# Copyright (c) 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.


import platform

from .interface import STOCK_DIALOG_INFO, STOCK_DIALOG_ERROR


# pylint: disable=unused-import
system = platform.system()
if system == "Darwin":
    from .osxnotify import init, notify, clear
elif system == 'Windows' or system.startswith('CYGWIN'):
    from .windowsnotify import init, notify, clear
else:
    from .linuxnotify import init, notify, clear
