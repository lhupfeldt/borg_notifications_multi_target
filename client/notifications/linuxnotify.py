# Copyright (c) 2015 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.

import sys
import os
import enum

from .interface import STOCK_DIALOG_INFO, STOCK_DIALOG_ERROR
from .dbus import set_dbus

_ignore_errors = False
_notification = None
_gtk = None
_notify = None


def init(program_name, ignore_errors=False):
    global _gtk, _notify, _ignore_errors  # pylint: disable=W0603
    _ignore_errors = ignore_errors

    try:
        set_dbus()
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('Notify', '0.7')
        from gi.repository import Gtk, Notify  # pylint: disable=E0611
        _gtk = Gtk
        _notify = Notify

        Notify.init(program_name)
    except Exception as ex:
        if not _ignore_errors:
            raise
        print(ex, file=sys.stderr)
        _gtk = None
        _notify = None


def notify(summary, body, msg_type, expire_timeout=-1):
    global _notification, _ignore_errors  # pylint: disable=W0603

    if _gtk is None:
        return

    if msg_type == STOCK_DIALOG_INFO:
        icon = _gtk.STOCK_DIALOG_INFO
    elif msg_type == STOCK_DIALOG_ERROR:
        icon = _gtk.STOCK_DIALOG_ERROR
    else:
        raise Exception("'msg_type' must be one of " + (STOCK_DIALOG_INFO, STOCK_DIALOG_ERROR))

    try:
        if _notification:
            _notification.update(summary, body, icon)
        elif _notify:
            _notification = _notify.Notification.new(summary, body, icon)
        if _notification:
            _notification.expire_timeout = expire_timeout
            _notification.show()
    except Exception as ex:
        if not _ignore_errors:
            raise
        print(ex, file=sys.stderr)


def clear():
    if _gtk is None:
        return

    try:
        _notification.close()
    except Exception as ex:
        if not _ignore_errors:
            raise
        print(ex, file=sys.stderr)
