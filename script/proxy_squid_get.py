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
    url_US = "https://www.nsfc.gov.cn/publish/portal0/jgsz/08/default.htm#01"
    timeout = 3
    
    try:
        r1 = requests.get(url=url_US, proxies=proxies, timeout=timeout, verify=True)
        #r2 = requests.get(url=url_US, proxies=proxies, timeout=timeout, verify=False)
   
        #if "baidu" in r1.text and "google" in r2.text:
        if "青年科学基金项" in r1.text:
            return url
        else:
            return False
    except:
        return False
