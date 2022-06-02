#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File    :   f5-bigip.py
@Datetime:   2022/5/10 16:06
@Contact :   lihanwei@zhiqiansec.com
@Descriptions
    -
'''

"""
fofa dork
    title="BIG-IP&reg;-+Redirect"
"""

import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


#
def format_url(xstr):
    xstr = str(xstr)
    if "//" not in xstr:
        xstr = "https://" + xstr

    return xstr.rstrip('/')

def poc(url):
    url = format_url(url)

    burp0_url = "%s/mgmt/shared/authn/login" % url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        }
    try:
        r = requests.get(burp0_url, headers=headers, verify=False, timeout=8)
        if r.status_code == 401 and "resterrorresponse" in r.text and "message" in r.text :
            return burp0_url
        else:
            return False
    except Exception as e:
        print(e)
        return False