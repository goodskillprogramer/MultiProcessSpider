# -*- coding: utf-8 -*-
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import urllib2  
import time    
from bs4 import BeautifulSoup  
from __builtin__ import int
import denglu
import datetime
import os
from ctypes.wintypes import INT

def get_house_price(houseid):
    #denglu.login()
    url = 'http://sh.lianjia.com/ershoufang/'+houseid+'.html'
    page = urllib2.urlopen(url)  
    soup = BeautifulSoup(page) 
    issold=False
    price=0
    region=u'无'
    for link in soup.find_all('div','mainInfo bold'):        
        recordstr=u""         
        text=link.get_text()  
        
        issold=False
        price=text.strip(u'万')
        price=float(price)
        
        for around in soup.find_all('table','aroundInfo'):  
            trs=around.find_all('span','areaEllipsis')                          
            text=trs[0].get_text() 
            region=text.split(u' ')[1]
            
    
    for link in soup.find_all('div','soldInfo'):    
        divs=link.find_all('div','cell')
        
        p=divs[1].p
        text=p.get_text()
        issold=True
        price=text.strip(u'万')
        price=float(price)
        for around in soup.find_all('table','aroundInfo'):  
            trs=around.findAll('tr')     
            td=trs[3].td   
            
            text=td.get_text().strip('\n')            
            print text
            l=text.rfind(u'（')
            r=text.rfind(u'）')
            text=text[l+1:r]     
            region= text.split(u' ')[1]     
             
    if price==0:
        print 'can not find price info'
        print url
    return (issold,price,region)

#print get_house_price('sh4328026')   
#print get_house_price('sh4261033')