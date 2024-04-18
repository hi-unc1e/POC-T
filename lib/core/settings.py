#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me


import os
import platform

VERSION = '2.0.6'
PROJECT = "POC-T"
AUTHOR = 'cdxy'
MAIL = 'i@cdxy.me'
PLATFORM = os.name
LICENSE = 'GPLv2'
IS_WIN = platform.system() == 'Windows' # 3:_mswindows

# essential methods/functions in custom scripts/PoC (such as function poc())
ESSENTIAL_MODULE_METHODS = ['poc']
# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"
# String representation for NULL value
NULL = "NULL"
# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\x%02x"

ISSUES_PAGE = "https://github.com/Xyntax/POC-T/issues"
GIT_REPOSITORY = "git://github.com/Xyntax/POC-T.git"
GIT_PAGE = "https://github.com/Xyntax/POC-T"

BANNER = """\033[01;34m
                                             \033[01;31m__/\033[01;34m
    ____     ____     _____           ______\033[01;33m/ \033[01;31m__/\033[01;34m
   / __ \   / __ \   / ___/   ____   /__  __/\033[01;33m_/\033[01;34m
  / /_/ /  / /_/ /  / /___   /___/     / /
 / /___/   \____/   \____/            / /
/_/                                  /_/
    \033[01;37m{\033[01;m Version %s by %s mail:%s \033[01;37m}\033[0m
\n""" % (VERSION, AUTHOR, MAIL)
