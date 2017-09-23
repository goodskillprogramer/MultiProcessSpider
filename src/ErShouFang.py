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
import sqlite3
import ErShouFangDbHelper
from utility import strip_space,strips
import sys
import time


def get_current_row(dbname,startPage,endPage):
    filename='database\\'+dbname+'_'+str(startPage)+'_'+str(startPage+endPage-1)+'.txt'
    
    if os.path.exists(filename) == False:
        print 'file not foudn',filename
        return 0
   
    f=open(filename);
    lines= f.readlines()
    max=0
    for line in lines:
        line=line.strip()
        s=line.split('$')
        if  len(s)>0:        
            cur=int(s[0])
            if(cur>max):
                max=cur
    print 'max',max
    return max
splitter='$'
def main(startPage,total_page,cur):
    global begindate
    global enddate
    global row
    global output       
    global last_date
    
    global over
    global work_book
    global sheet 
    
    print total_page
    dbname=time.strftime('%Y%m%d',time.localtime()) 
    #dbname='20170320'
    cur=get_current_row(dbname, startPage, total_page) 
    for i in range((int)(total_page)):       
             
              
            url = 'http://sh.lianjia.com/chengjiao/pudongxinqu/'
            url = 'http://sh.lianjia.com/ershoufang/'  
            url = 'http://sh.lianjia.com/ershoufang/s7/'     
            
            if cur+1==total_page:
                break
                        
            if(i+1<cur):
                continue
            url+='d'
            url+=str(i+startPage)
            url+='s7'
            record_list=[]
            print url
            while(True):
                page = urllib2.urlopen(url)  
                soup = BeautifulSoup(page)         
           
                divcontent=soup.find_all('div','m-list')
                if divcontent:
                    divcontent=divcontent[0]
                    break
                else:                    
                    print url,'Error'
                    time.sleep(1)
                    
                    
                        
            lilist=divcontent.find_all(name='li')
            
            for li in lilist: 
                recordstr=u"" 
                a=li.a
                #sh4250530 
                key_txt=a['key']
                recordstr+=key_txt
                              
                     
                info_div=li.find(attrs={'class':'info'})   
                prop_title_div=info_div.find(attrs={'class':'prop-title'})
                #房型正气，业主诚意出售，新鲜好房，视野很好  新上
                prop_title_txt=strips(prop_title_div.get_text())
                recordstr+="$"+prop_title_txt
                                
                info_table_div=info_div.find(attrs={'class':'info-table'})
                
                info_col_row1_text_div=info_table_div.find(attrs={'class':'info-col row1-text'})    
                #1室2厅|91.26平|高区/28层|朝南北            
                info_col_row1_text_div_txt= strip_space(strips(info_col_row1_text_div.get_text())) 
                recordstr+="$"+info_col_row1_text_div_txt               
                
                info_col_price_item_main_div=info_table_div.find(attrs={'class':'info-col price-item main'})
                #950万 
                totalprice_txt= strip_space(strips(info_col_price_item_main_div.get_text()))
                recordstr+="$"+totalprice_txt 
                               
                
                info_col_row2_text_div=info_table_div.find(attrs={'class':'info-col row2-text'})
                #御翠豪庭|长宁|古北|2008年建
                info_col_row2_text_div_txt=strip_space(strips(info_col_row2_text_div.get_text()))
                recordstr+="$"+info_col_row2_text_div_txt 
                                
                info_col_price_item_minor_div=info_table_div.find(attrs={'class':'info-col price-item minor'})
                #单价104098元/平
                price_txt=strip_space(strips(info_col_price_item_minor_div.get_text()))    
                recordstr+="$"+price_txt        
                 
                property_tag_container_div=info_div.find(attrs={'class':'property-tag-container'})
                #距离10号线伊犁路站494米 满五 有钥匙
                introduce_txt=strips(property_tag_container_div.get_text())
                recordstr+="$"+introduce_txt 
                
              
                recordstr+=u'\n'             
                #output.write(recordstr.encode('gbk') ) 
                #output.flush()
                
                record_list.append(recordstr)
                
                
            print total_page," :complete ",startPage,i,total_page,'record num',len(record_list)  
            if len(record_list)==0:
                break
            ErShouFangDbHelper.InsertErShouFang(dbname,i,startPage,total_page,record_list)  


if len(sys.argv)>3:
    start=int(sys.argv[1])
    end=int(sys.argv[2])
    cur=int(sys.argv[3])
    main(start,end,cur)