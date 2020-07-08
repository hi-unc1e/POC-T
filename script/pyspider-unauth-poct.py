#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author unc1e


"""
pyspider-unauth POC in framework POC-T
Usage:
  python POC-T.py -s pyspider-unauth-poct -aF "pyspider"
  python POC-T.py -s pyspider-unauth-poct -aF "title=\"Dashboard - pyspider\""
    
  python POC-T.py -s pyspider-unauth-poct -iS http://39.105.5.125:5000
"""

import re
import urllib2
import requests

TIMEOUT = 8

def poc(url):

    #formatten url
    url = url if '://' in url else 'http://' + url
    url = url.replace("http://","https://") if "443" in url else url    #为了使返回url符合格式, 此条不去除 
    
    try:
        res = requests.get(url, timeout=TIMEOUT, verify=False)
        if "pyspider dashboard" in res.text:
            return url
    except:
        pass

    return False
    
    
#print(poc("http://88.17.240.245:5000/"))
