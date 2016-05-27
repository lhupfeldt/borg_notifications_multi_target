#!/bin/python3

# Copyright (c) 2012-2016 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.

import shutil
from pathlib import Path


def rotate_logs(log_file):
    for log_num in range(8, 0, -1):
        lf = Path(log_file, '.' + str(log_num)) if log_num else Path(log_file)
        if lf.exists():
            lf.replace(Path(log_file, '.' + str(log_num + 1)))
