#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import logging
import sys

from lib.core.enums import CUSTOM_LOGGING

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "*")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "+")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "-")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "!")
logging.addLevelName(CUSTOM_LOGGING.DEBUG, " ")

LOGGER = logging.getLogger("TookitLogger")

LOGGER_HANDLER = None
try:
    from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    try:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
        LOGGER_HANDLER.level_map[logging.getLevelName("*")] = (None, "cyan", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("+")] = (None, "green", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("-")] = (None, "red", False)
        LOGGER_HANDLER.level_map[logging.getLevelName("!")] = (None, "yellow", False)
    except Exception:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter("\r[%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.SYSINFO)


class MY_LOGGER:
    @staticmethod
    def success(msg):
        return LOGGER.log(CUSTOM_LOGGING.SUCCESS, msg)

    @staticmethod
    def info(msg):
        return LOGGER.log(CUSTOM_LOGGING.SYSINFO, msg)

    @staticmethod
    def warning(msg):
        return LOGGER.log(CUSTOM_LOGGING.WARNING, msg)

    @staticmethod
    def error(msg):
        return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)

    @staticmethod
    def debug(msg):
        return LOGGER.log(CUSTOM_LOGGING.DEBUG, msg)
