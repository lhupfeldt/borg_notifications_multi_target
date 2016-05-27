#!/bin/python3

# Copyright (c) 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.

# Lazy-import pyobjc to work around a conflict with pytest-xdist
# looponfail on Python 3.3
objc = None

# Swizzle [NSBundle bundleIdentifier] to make NSUserNotifications work.
#
# To post NSUserNotifications OS X requires the binary to be packaged
# as an application bundle. To circumvent this restriction, we modify
# `bundleIdentifier` to return a fake bundle identifier.
#
# Original idea for this approach by Norio Numura: https://github.com/norio-nomura/usernotification
# patches from https://github.com/dbader/pytest-osxnotify


def _swizzle(cls, SEL, func):
    old_IMP = getattr(cls, SEL, None)
    if old_IMP is None:
        # This will work on OS X <= 10.9
        old_IMP = cls.instanceMethodForSelector_(SEL)

    def wrapper(self, *args, **kwargs):
        return func(self, old_IMP, *args, **kwargs)

    new_IMP = objc.selector(
        wrapper,
        selector=old_IMP.selector,
        signature=old_IMP.signature
    )
    objc.classAddMethod(cls, SEL.encode(), new_IMP)


def _swizzled_bundleIdentifier(self, original):  # pylint: disable=W0613
    return 'com.apple.terminal'

_notification_center = None
_NSUserNotification = None


def init(app_name):  # pylint: disable=W0613
    global _NSUserNotification, _notification_center  # pylint: disable=W0603

    global objc
    if not objc:
        objc = __import__("objc")
        _swizzle(objc.lookUpClass('NSBundle'), 'bundleIdentifier', _swizzled_bundleIdentifier)

    _NSUserNotification = objc.lookUpClass('NSUserNotification')
    _NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    if not _NSUserNotification or not _NSUserNotificationCenter:
        print('NSUserNotifcation is not supported by your version of Mac OS X')
        return

    _notification_center = _NSUserNotificationCenter.defaultUserNotificationCenter()


def notify(title, subtitle, icon, expire_timeout=-1):  # pylint: disable=W0613
    """Display a NSUserNotification on Mac OS X >= 10.8"""
    notification = _NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    if subtitle:
        notification.setSubtitle_(str(subtitle))

    _notification_center.deliverNotification_(notification)


def clear():
    """Clear any displayed alerts we have posted. Requires Mavericks."""
    _notification_center.removeAllDeliveredNotifications()
