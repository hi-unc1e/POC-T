#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import sys
from lib.core.settings import IS_WIN, UNICODE_ENCODING


def singleTimeWarnMessage(message):  # Cross-linked function
    sys.stdout.write(message)
    sys.stdout.write("\n")
    sys.stdout.flush()

def stdoutDecode(data):
    """
    decode to str
    """
    retVal = data
    if isinstance(data, str):
        return retVal
    else:
        try:
            retVal = data.decode(sys.stdout.encoding)
        except Exception:
            retVal = data.decode(UNICODE_ENCODING) if isinstance(data, bytes) else data
    return retVal

def stdoutencode(data):
    """
    Encodes unicode data to stdout encoding
    input: str/unicode
    output: bytes
    """
    retVal = None

    try:
        data = data or ""

        # Reference: http://bugs.python.org/issue1602
        if IS_WIN:
            output = data.encode(sys.stdout.encoding, "replace")

            if '?' in output and '?' not in data:
                warnMsg = "cannot properly display Unicode characters "
                warnMsg += "inside Windows OS command prompt "
                warnMsg += "(http://bugs.python.org/issue1602). All "
                warnMsg += "unhandled occurances will result in "
                warnMsg += "replacement with '?' character. Please, find "
                warnMsg += "proper character representation inside "
                warnMsg += "corresponding output files. "
                singleTimeWarnMessage(warnMsg)

            retVal = output
        else:
            retVal = data.encode() if isinstance(data, str) else data
    except UnicodeError:
        retVal = data.encode(UNICODE_ENCODING, "replace") if isinstance(data, str) else data
    return retVal
