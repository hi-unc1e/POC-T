#coding:utf-8
import requests
import json

def poc(url):
    URL = "http://ipwhois.cnnic.net.cn/"
    CONTENT = "CSTNET"

    URL_BAIDU = "http://google.com.hk/"
    CONTENT_BAIDU = "googlelogo"
    PROXY = {#"sock4":"%s"%(url),
    "sock5":"%s"%(url)
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
    # 可访问
    try:
        r = requests.get(url=URL, headers=headers, proxies=PROXY, timeout=3, verify=False)
        rr = requests.get(url=URL_BAIDU, headers=headers, proxies=PROXY, timeout=3, verify=False)
        if CONTENT in r.text and CONTENT_BAIDU in rr.text:
            #print(r.content)
            return url

        else:    
            return False    
    except:
        return False
        
#print(poc("proxy.lfk.qianxin-inc.cn:3128"))


