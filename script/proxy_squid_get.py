#coding:utf-8

import requests
import string
import json

def poc(url):
    
    ''' 
    usage:
        python POC-T.py -s rancher-unauth -aF "header=rancher"
    app="Squid" && after="2019-01-01" && country="US" && port="3128"

    '''
    
    # parsing
    ip = url.split(":")[0]
    port = 3128 if url.split(":")[1] == '3128' else url.split(":")[1] 
    
    proxies = {
    "http": "http://{0}:{1}".format(ip,port),
     "https": "https://{0}:{1}".format(ip,port),
}
    #print(proxies)
    # target conf
    url_CN = "http://www.baidu.com"
    #url_US = "http://www.google.com"
    timeout = 3
    
    try:
        r1 = requests.get(url=url_CN, proxies=proxies, timeout=timeout, verify=False)
        #r2 = requests.get(url=url_US, proxies=proxies, timeout=timeout, verify=False)
   
        #if "baidu" in r1.text and "google" in r2.text:
        if "baidu" in r1.content and "ERROR" not in r1.content:
            return url
        else:
            return False
    except:
        return False
