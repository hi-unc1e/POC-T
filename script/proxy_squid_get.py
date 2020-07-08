#coding:utf-8

import requests
import string
import json

def poc(url):
    
    ''' 
    usage:
       python2 POC-T.py -s proxy_squid_get -aF "port=3128&&app=Squid" --limit 10000 -t 50
      python2 POC-T.py -s proxy_squid_get -aF "app=Tinyproxy"

    '''
    
    # parsing
    ip = url.split(":")[0]
    try:
        port = 80 if url.split(":")[1] == '80' else url.split(":")[1]
    except:
        return False
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
