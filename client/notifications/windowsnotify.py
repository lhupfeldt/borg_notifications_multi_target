# Copyright (c) 2016 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.


from .interface import STOCK_DIALOG_INFO, STOCK_DIALOG_ERROR

_ignore_errors = False
_notification = None
_notify = None


def init(program_name, ignore_errors=False):
    # TODO
    pass

def notify(summary, body, msg_type, expire_timeout=-1):
    # TODO
    return


def clear():
    # TODO
    return
