#coding:utf-8

import requests
import string
import json

def poc(url):
    ''' 
    usage:
        python POC-T.py -s rancher-unauth -aF "header=rancher"

        >>> type(r.content)
        <type 'str'>
        >>> type(r.text)
        <type 'unicode'>
    '''
    
    
    url = "http://" + url if "//" not in url else url
    
    try:
        r = requests.get(url=url,timeout=8,verify=False)
        js = json.loads(r.content)

        #not rancher
        if "v" not in r.headers["X-Rancher-Version"].lower():
            return False
            
        elif r.headers["X-Api-Account-Kind"] == 'admin':
            return url
        else:
            return False
    
        
        
        
    except:
        return False
