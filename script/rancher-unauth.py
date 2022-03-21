# coding:utf-8

import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
import string
import json
import warnings
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)



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
        s = requests.session()
        s.keep_alive = False
        r = s.head(url=url, timeout=8, verify=False)
        if r.headers["X-Api-Account-Kind"] == 'admin':
            return url
        else:
            return False

    except Exception as e:
        return False

    finally:
        s.close()
