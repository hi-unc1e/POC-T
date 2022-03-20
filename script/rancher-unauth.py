#coding:utf-8

import requests
import string
import json

def poc(url):
    ''' 
    usage:
        python POC-T.py -s rancher-unauth -aF "header=rancher"
    dork:
        X-Api-Account-Kind: admin

        >>> type(r.content)
        <type 'str'>
        >>> type(r.text)
        <type 'unicode'>
    '''
    
    
    url = "https://" + url if "//" not in url else url
    # url = url.replace("http", "https") if ('443' in url) else url
    
    try:
        r = requests.get(url=url, timeout=8, verify=False)
        if r.headers["X-Api-Account-Kind"] == 'admin':
            return url
        else:
            return False
    except:
        return False
