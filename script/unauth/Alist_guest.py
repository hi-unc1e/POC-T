#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
GlassFish directory traversal vulnerability PoC

version <= 4.1.0

Usage:
  python POC-T.py -s Alist_guest -aF "body=\"jsd.nn.ci/gh/alist-org/logo@main/logo.png\""

HTTP:
    GET /api/me

    err         {"code":401,"message":"Guest user is disabled, login please","data":null}

"""


from lib.utils.http import (
    request_ex,
    urljoin_ex
)


def poc(url):
    me_url = urljoin_ex(url, "/api/me")
    resp = request_ex("GET", me_url, timeout=8)
    if resp:
        if "401" not in resp.text:
            return True

    return False
