#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
字典
'''

from lib.core.common import setPaths, paths

setPaths()


def _read_dict(path):
    with open(path, "r") as fs:
        ds = fs.readlines()
        # strip
        ds = [d.strip() for d in ds]
    if ds:
        return ds


class Wordlist:
    top_10_pass = [
        "admin",
        "a123456",
        "123456",
        "admin123",
        "Admin123",
        "000000",
        "12345678",
        "1qaz2wsx",
        "admin!@#",
    ]
    top_100_pass = _read_dict(paths.WEAK_PASS_100)
    top_1000_pass = _read_dict(paths.WEAK_PASS_1000)
