# Copyright (c) 2016 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.


from notifications import init, notify, clear, STOCK_DIALOG_INFO, STOCK_DIALOG_ERROR


def test_notification():
    init("Bakup")
    notify("Hi", "Hello", STOCK_DIALOG_INFO)
    notify("Hi2", "Hello2", STOCK_DIALOG_ERROR)
    clear()


def test_notification_ignore_errors():
    init("Bakup", ignore_errors=True)
    notify("Not Important", "Hello", STOCK_DIALOG_INFO)
    notify("Not Important", "I will let you know by other means!", STOCK_DIALOG_ERROR)
    clear()
