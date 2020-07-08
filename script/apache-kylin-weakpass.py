# -*- coding: UTF-8 -*-
import requests

'''Aapche_kylin_weakpass.py
Aapche_kylin_WEB:
访问主机: http://hostname:7070
    使用用户名登陆：ADMIN
    使用密码登陆：KYLIN
 the default account and passsword "ADMIN-KYLIN".
    e.g:    http://47.99.80.48:7070/kylin/login
	fofa dork: 
	    port=7070 && "kylin" 
	    title==Kylin
	Usage: 
		python2 POC-T.py -s apache-kylin-weakpass -aF   "title==Kylin"

'''


def poc(url):
    TIMEOUT = 5
    next_url = url if "http" in url else "http://" + url





