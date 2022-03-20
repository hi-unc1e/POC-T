#coding:utf-8
'''
python POC-T.py -s proxy-capture-1w -aF "app=HAProxy"
'''
import requests
import json

def poc(url):
    URL = "http://baidu.com"
    CONTENT = "baidu"
    PROXY = {"http":"sock4://%s"%(url),
    "https":"sock4://%s"%(url)
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
    # 可访问
    #print url
    try:
        r = requests.get(url=URL, headers=headers, proxies=PROXY, timeout=3, verify=False)
        if CONTENT in r.text:
            #print(r.content)
            #print url
            return PROXY

        else:    
            return False    
    except:
        return False
        
#print(poc("proxy.lfk.qianxin-inc.cn:3128"))


