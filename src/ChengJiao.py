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
from utility import strip_space,strips
from ChengJiaoDbHelper import InsertChenJiao

denglu.login()
time.clock()  

def get_file_list(path):
    return os.listdir(path)

def get_date(date):
    d=date.split('-')
    l=[]
    l.append(int(d[0]))
    l.append(int(d[1]))
    l.append(int(d[2]))
    return l

def date_cmp(date1,date2):
    if date1[0] > date2[0]:
        return 1
    elif date1[0] < date2[0]:
        return -1    
    
    if date1[1]>date2[1]:
        return 1
    elif date1[1]<date2[1]:
        return -1  
       
    if date1[2]>date2[2]:
        return 1
    elif date1[2]<date2[2]:
        return -1
    else :
        return 0
    
def get_last_update_date(path):
    f=get_file_list(path)
    last_date=[2014,9,12]
    for entry in f:
        entry=entry.strip('.xls')
        print entry
        entry=get_date(entry)
        if last_date is None:
            last_date=entry
        elif date_cmp(entry, last_date)>=0:
            last_date=entry            
        
    return last_date

def get_last_date(cur_date):
    cur_date=get_date(cur_date)
    d=datetime.date(cur_date[0],cur_date[1],cur_date[2])
    d=d+datetime.timedelta(days =15)
    l=[]
    l.append(d.year)
    l.append(d.month)
    l.append(d.day)
    return d

def get_pre_date(d):   
    d=datetime.date(d[0],d[1],d[2])
    d=d-datetime.timedelta(days =1)
    l=[]
    l.append(d.year)
    l.append(d.month)
    l.append(d.day)
    return l

begindate=""
enddate=""
#output = open(r'F:\source_code\workspace\lianjia\src\record.txt', 'a')
last_date=get_last_update_date('shanghai')
total_page=200
row=1
over=False
def get_total_page():
    url = 'http://sh.lianjia.com/chengjiao/pudongxinqu/'  
    page = urllib2.urlopen(url)  
    soup = BeautifulSoup(page)  
    
    div=soup.find_all('div',"page-box house-lst-page-box")
    for d in div:
        page_a=d.find_all('a')
        total_page=page_a[7].string
        print total_page
        
def main():
    global begindate
    global enddate
    global row
    global output       
    global last_date
    global total_page
    global over
    global work_book
    global sheet

    print last_date
    
    print total_page

    for i in range((int)(total_page)):                   
            
            url = 'http://sh.lianjia.com/chengjiao/pudongxinqu/'
            url = 'http://sh.lianjia.com/chengjiao/'             
             
            url+='d'
            url+=str(i+1)
            print url
            page = urllib2.urlopen(url)  
            soup = BeautifulSoup(page)  
        
            time.sleep(2)
            content=soup.find_all('div','m-list cj-list')
            
            content=content[0]
            for info in content.find_all('div','info'): 
                recordstr=u"" 
                splitter='$'
                infotable=info.find('div','info-table')
                inforowlist=infotable.find_all('div','info-row')
                
                inforowone=inforowlist[0]                
                link=inforowone.a
                key=link['key']
                basic=(strips(link.get_text()))
               # print key,basic
                recordstr+=key
                recordstr+=splitter
                
                recordstr+=basic
                recordstr+=splitter
                
                
                
                inforowtwo=inforowlist[1]
                row1_text=strip_space(strips(inforowtwo.find('div','row1-text').get_text()))
                #print row1_text
                recordstr+=row1_text
                recordstr+=splitter
                
                info_col_price_item_main_strong_num=inforowtwo.find('div','info-col deal-item main strong-num')
                info_col_price_item_main_strong_num_txt=(info_col_price_item_main_strong_num.get_text())
                strips(info_col_price_item_main_strong_num_txt)
                # print info_col_price_item_main_strong_num_txt
                recordstr+=info_col_price_item_main_strong_num_txt
                recordstr+=splitter
                
                info_col_price_item_main=inforowtwo.find('div','info-col price-item main')
                info_col_price_item_main_txt=strip_space(strips(info_col_price_item_main.get_text()))
                # print info_col_price_item_main_txt
                recordstr+=info_col_price_item_main_txt
                recordstr+=splitter
                
                inforowthree=inforowlist[2]
                
                span=inforowthree.span
                span_txt=strip_space(strips(span.get_text()))
                # print span_txt
                recordstr+=span_txt
                recordstr+=splitter
                
                info_col_price_item_minor=inforowthree.find('div','info-col price-item minor')
                info_col_price_item_minor_txt=strip_space(strips(info_col_price_item_minor.get_text()))
                # print info_col_price_item_minor_txt
                recordstr+=info_col_price_item_minor_txt
                recordstr+=splitter
                
                property_tag_container=info.find('div','property-tag-container')
                property_tag_container_txt=(strips(property_tag_container.get_text()))
                # print property_tag_container_txt
                recordstr+=property_tag_container_txt
                recordstr+=splitter
                #  print recordstr
                InsertChenJiao(recordstr)                              
                row+=1
                print total_page," :complete ",i
                        
            if over:
                break
    
    #pre_day=get_pre_date(last_date);
    str_pre_day=str(last_date[0])+"-"+str(last_date[1])+"-"+str(last_date[2])+'.xlsx'   
    #output.close()    
    print "complete num" ,row-1 ,"pre update day ",  \
            get_last_date(str(last_date[0])+"-"+str(last_date[1])+"-"+str(last_date[2]))
    print "saved data to ", begindate       
       
main()
