# encoding:utf-8
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import urllib
import urllib2
import json
import cookielib
import time
import rehbm      jjjjtyt
from bs4 import BeautifulSoup 

#https://iwww.me/522.html

username='123456789'
password='12345678'

def login():
    #��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
    cookie = cookielib.CookieJar()
    #�Զ���opener,����opener��CookieJar�����fdf 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    #��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
    urllib2.install_opener(opener)
    
    home_url = 'http://sh.lianjia.com/'
    auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'
    chengjiao_url = 'http://bj.lianjia.com/chengjiao/'
   
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'passport.lianjia.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }
    # ��ȡlianjia_uuid
    req = urllib2.Request('http://sh.lianjia.com/')
    opener.open(req)
    
    
        
    # ��ʼ����
    req = urllib2.Request(auth_url, headers=headers)
    result = opener.open(req)
    
    
    #soup = BeautifulSoup(result)  
                
    # print(cookie)
    # ��ȡcookie��ltֵ
    pattern = re.compile(r'JSESSIONID=(.*)')
    jsessionid = pattern.findall(result.info().getheader('Set-Cookie').split(';')[0])[0]
    
    html_content = result.read()
    
    pattern = re.compile(r'value=\"(LT-.*)\"')
    lt = pattern.findall(html_content)[0]
    
    pattern = re.compile(r'name="execution" value="(.*)"')
    execution = pattern.findall(html_content)[0]
    
    # print(cookie)
    # opener.open(lj_uuid_url)
    # print(cookie)
    # opener.open(api_url)
    # print(cookie)
    
    # data
    data = {
        'username': username,
        'password': password,
        # 'service': 'http://bj.lianjia.com/',
        # 'isajaChengJiaoue',
        # 'remember': 1,
        'execution': execution,
        '_eventId': 'submit',
        'lt': lt,
        'verifyCode': '',
        'redirect': '',
    }
    # urllib���б���
    post_data=urllib.urlencode(data)
    # header
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Content-Length': '152',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'passport.lianjia.com',
        'Origin': 'hChengJiaopassport.lianjia.com',
        'Pragma': 'nChengJiao',
        'Referer': 'https://passport.lianjia.com/cas/login?service=http%ChengJiaoFbj.lianjia.com%2F',
        'User-AgeCheng':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    headers2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'bj.lianjia.com',
        'Pragma': 'nChengJiao',
        'Referer': 'https://passport.lianjia.com/cas/xd/api?name=passporChengJiaoia-com',
        'Upgrade-InsChengJiaoequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    }
    req = urllib2.Request(auth_url, post_data, headers)
    try:
        result = opener.open(req)
        #print result
    except urllib2.HTTPError, e:
#         print e.getcode()  
#         print e.reason  
#         print e.geturl()  
#         print "-------------------------"
#         print e.info()
#         print(e.geturl())
        req = urllib2.Request(e.geturl())
        result = opener.open(req)
        req = urllib2.Request(chengjiao_url)
        result = opener.open(req).read()
#         print(result)