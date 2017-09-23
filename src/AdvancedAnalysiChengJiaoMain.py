# -*- coding: utf-8 -*-

'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
               （4）成交数据，需要提供修改账户密码，请查找 admin 或者password 修改
'''

import sqlite3
import os
from ErShouFangDbHelper import GetXiaoquNianDai 
from ErShouFangDbHelper import GetCountFromSummary
from ChengJiaoDbHelper import  GetMaxRiQi
from AdvancedAnalysisErShouFangMain import GetPriceFromDbList
import time
import datetime

def GetXiaoquData(dbname):
    xiaoqulist={}
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=u'select DISTINCT xiaoqu  from chengjiao '    
   
    cursor=conn.execute(sqlstring)
 
    for row in cursor:  
        xiaoqulist[row[0]]={}
        xiaoqulist[row[0]]['qu']=''
        xiaoqulist[row[0]]['zhen']='' 
        xiaoqulist[row[0]]['min']=None
        xiaoqulist[row[0]]['max']=None
        xiaoqulist[row[0]]['range']=0.0         
        
    conn.close()        
    return xiaoqulist    
        
def Analysis(dbname):
    '''key $ xiaoqu $ fangxing $ mianji $ qu $ zhen $ zongjia $ danjia $ manji $ riqi'''    
    
    conn = sqlite3.connect("database/"+dbname+".db")
    sqlstring='select qu,zhen,sum(zongjia),sum(mianji) from chengjiao group by zhen order by qu'
    cursor=conn.execute(sqlstring)
    totalprice=0.0
    totalmianji=0.0
    
    for row in cursor:   
        qu=row[0]
        zhen=row[1]
        totalprice=row[2] 
        totalmianji=row[3]
        if(totalmianji!=0):
            print qu,zhen,totalprice,totalmianji,totalprice/totalmianji        
    conn.close()   
    
def TrendShanghaiMonth(dbname):
    '''key $ xiaoqu $ fangxing $ mianji $ qu $ zhen $ zongjia $ danjia $ manji $ riqi'''    
    
    conn = sqlite3.connect("database/"+dbname+".db")
    sqlstring='select qu,zhen,sum(zongjia),sum(mianji) from chengjiao group by zhen order by qu'
    cursor=conn.execute(sqlstring)
    totalprice=0.0
    totalmianji=0.0
    
    for row in cursor:   
        qu=row[0]
        zhen=row[1]
        totalprice=row[2] 
        totalmianji=row[3]
        if(totalmianji!=0):
            print qu,zhen,totalprice,totalmianji,totalprice/totalmianji        
    conn.close()   
    
def TrendZhenMonth(dbname):
    
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=u'select qu,zhen,count(key),sum(zongjia),sum(mianji),strftime(\'%Y%m\',riqi) \
    from chengjiao group by zhen,strftime(\'%Y%m\',riqi)  '    
    
    cursor=conn.execute(sqlstring)
    totalprice=0.0
    totalmianji=0.0
    zhenlist=[]
    for row in cursor:   
        
        qu=row[0]
        zhen=row[1]
        count=row[2]
        totalprice=row[3] 
        totalmianji=row[4]
        average=totalprice/totalmianji
        riqi=row[5]
        zhenlist.append([qu,zhen,count,totalprice,totalmianji,average,riqi])
        
    conn.close() 
    zhendata={}
    for zhen in zhenlist:
        key=zhen[1]
        zhendata[key]={}
        zhendata[key]['qu']=''
        zhendata[key]['zhen']='' 
        zhendata[key]['min']=None
        zhendata[key]['max']=None
        zhendata[key]['range']=0.0  
        zhendata[key]['count']=0
        show=[u'张江',u'唐镇',u'三林',u'川沙',u'北蔡',u'祝桥 ']
        if key.strip() in show:
            print zhen[0],zhen[1],zhen[2],zhen[5],zhen[6]
        
            
    
    for zhen in zhenlist:   
        key=zhen[1]    
        zhendata[key]['qu']=zhen[0];
        zhendata[key]['zhen']=zhen[1]
        junjia=zhen[5]
        if zhendata[key]['min']==None or \
           zhendata[key]['max']==None:
            zhendata[key]['min']=junjia
            zhendata[key]['max']=junjia         
     
           
            
        if junjia<zhendata[key]['min']:
            zhendata[key]['min']=junjia
            zhendata[key]['range']=zhendata[key]['max']-zhendata[key]['min']
        elif junjia>zhendata[key]['max']:
            
            zhendata[key]['max']=junjia
            zhendata[key]['range']=zhendata[key]['max']-zhendata[key]['min']
        zhendata[key]['count']+=zhen[2]
                    
   
    f=open('report\\chenjiao\\chengjiaoTrendZhen.txt','w')
    f.write('qu$zhen$shuliang$min$max$range\n')
    for key in zhendata:
        txt=('%s $ %s $ %s $ %s $ %s $ %s\n')%(zhendata[key]['qu'],zhendata[key]['zhen'],\
            zhendata[key]['count'],zhendata[key]['min'],zhendata[key]['max'],zhendata[key]['range'])
        f.write(txt.encode('utf-8'))  
    f.close()

def TrendXiaoQuMonth(dbname,xiaoqudata):
    
    xiaoqulist=GetXiaoquNianDai('20170107')
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=u'select qu,zhen,xiaoqu,count(key),sum(zongjia),sum(mianji),strftime(\'%m\',riqi) \
    from chengjiao group by xiaoqu,strftime(\'%m\',riqi)  '
    
    
    cursor=conn.execute(sqlstring)
    totalprice=0.0
    totalmianji=0.0
    
    for row in cursor:   
        qu=row[0]
        zhen=row[1]
        xiaoqu=row[2]
        count=row[3]
        totalprice=row[4] 
        totalmianji=row[5]
        riqi=row[6] 
        niandai=''
        junjia=totalprice/totalmianji
        if xiaoqulist.has_key(xiaoqu):
            niandai=xiaoqulist[xiaoqu]
        
        print xiaoqu,niandai
        xiaoqudata[xiaoqu]['niandai']=niandai
        xiaoqudata[xiaoqu]['qu']=qu;
        xiaoqudata[xiaoqu]['zhen']=zhen
        if xiaoqudata[xiaoqu]['min']==None or \
           xiaoqudata[xiaoqu]['max']==None:
            xiaoqudata[xiaoqu]['min']=junjia
            xiaoqudata[xiaoqu]['max']=junjia
            
        
        if junjia<xiaoqudata[xiaoqu]['min']:
            xiaoqudata[xiaoqu]['min']=junjia
            xiaoqudata[xiaoqu]['range']=xiaoqudata[xiaoqu]['max']-xiaoqudata[xiaoqu]['min']
        elif junjia>xiaoqudata[xiaoqu]['max']:
            xiaoqudata[xiaoqu]['max']=junjia
            xiaoqudata[xiaoqu]['range']=xiaoqudata[xiaoqu]['max']-xiaoqudata[xiaoqu]['min']
 
    conn.close() 
     
    f=open('report\\chenjiao\\chengjiaoTrendXiaoqu.txt','w')
    f.write('qu$zhen$xiaoqu$niandai$min$max$range\n')
    for key in xiaoqudata:
        txt=('%s$%s$%s$%s$%s$%s$%s\n')%(xiaoqudata[key]['qu'],xiaoqudata[key]['zhen'],\
                key,xiaoqudata[key]['niandai'],xiaoqudata[key]['min'],\
                xiaoqudata[key]['max'],xiaoqudata[key]['range'])
        f.write(txt.encode('utf-8'))
    f.close()
    
def ChenJiaoShangHaiPerMonth(dbname='chengjiao'):
    print '月份         均价        套数'
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=u'select count(key),sum(zongjia),sum(mianji),strftime(\'%Y%m\',riqi) \
    from chengjiao group by strftime(\'%Y%m\',riqi)  '#%d
    
    
    cursor=conn.execute(sqlstring)
    totalprice=0.0
    totalmianji=0.0
    count=0
    t=''
    
    for row in cursor:  
        count=row[0] 
        totalprice=row[1]
        totalmianji=row[2]
        t=row[3]
        print ('%s %-11.4f %s')%(t,totalprice/totalmianji,count)
    
    
def get_latest_90_count(date,dbname='chengjiao'):
    date = time.strptime(date,"%Y-%m-%d")
    date=datetime.datetime(date[0],date[1],date[2])
    
    lastdate= date + datetime.timedelta(days = -90)
    print date,'九十天前日期；',lastdate
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=(u'select count(key)  from chengjiao where riqi>=\'%s\'')%(lastdate)   
   
    cursor=conn.execute(sqlstring)
    c=0
    for row in cursor:  
        c=row[0]      
    conn.close()       
    return c 

def get_chengjiao_count(where,dbname='chengjiao'):
    
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=(u'select count(key)  from chengjiao where %s')%(where)   
   
    cursor=conn.execute(sqlstring)
    c=0
    for row in cursor:  
        c=row[0]      
    conn.close()       
    return c 
def get_90_count(date,dbname='chengjiao'):
    date = time.strptime(date,"%Y-%m-%d")
    date=datetime.datetime(date[0],date[1],date[2])
    
    lastdate= date + datetime.timedelta(days = -90)
    lastdate=lastdate.strftime("%Y-%m-%d")
    #print "90 day before",date,lastdate
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=(u'select count(key)  from chengjiao where riqi=\'%s\'')%(lastdate)   
   
    cursor=conn.execute(sqlstring)
    c=0
    for row in cursor:  
        c=row[0]      
    conn.close()       
    return c 

def get_latest_15_count():
    date=time.strftime('%Y-%m-%d',time.localtime()) 
    datetime=time.strftime('%Y%m%d',time.localtime())
    count= GetCountFromSummary(datetime)
    count90= get_latest_90_count(date)
    print '最近90天成交套数 ，统计到：',GetMaxRiQi(),count90
    delta=count-count90
    countbetween=get_chengjiao_count(' riqi>=\'2017-02-01\' and riqi <= \'2017-01-08\'')
    
    print delta+countbetween

def get_day_count(date=None):
    if date==None:
        date=time.strftime('%Y-%m-%d',time.localtime())
    date = time.strptime(date,"%Y-%m-%d")
    date=datetime.datetime(date[0],date[1],date[2])
    
    predate= date + datetime.timedelta(days = -1)
    day=date.strftime("%Y%m%d")
    preday=predate.strftime("%Y%m%d")
    preday2=predate.strftime("%Y-%m-%d")
    countday=GetCountFromSummary(day)    
    countpreday=GetCountFromSummary(preday)
    coutpreday90=get_90_count(preday2)
    #print countday,countpreday,coutpreday90
    print preday2,"chenjiao",countday-(countpreday-coutpreday90)

def GetChengJiaoPreviousData(dbname='chengjiao'):
    conn = sqlite3.connect("database/"+dbname+".db")
    
    sqlstring=(u'select * from chengjiao order by riqi desc')
    
    cursor=conn.execute(sqlstring)
    chengjiao=[]
    count=1
    with open('report/chengjiaoPreviousJiaGe.txt','w+') as chenjiaofile:
        for row in cursor:  
            chen=[]
            chen.append(row[0]) #key 
            chen.append(row[6])  #zongjia
            chen.append(row[1]) #xiaoqu 
            chen.append(row[2])  #fang
            chen.append(row[3])  #mianji
            chen.append(row[4]) #qu
            chen.append(row[5]) #zhen
            
            if row[5] == u'北3蔡':
                continue
           
            chen.append(row[7])  #danjia
            chen.append(row[8]) 
            chen.append(row[9])  #riqi
            chen.append(GetPriceFromDbList(row[0])) 
            chengjiao.append(chen) 
            print chen[0],chen[1],chen[2],chen[3],chen[4],chen[5],chen[6],chen[7],chen[8],chen[9],chen[10]
            count+=1
            lastprice=0
            change=0
            daikan=0
            if len(chen[10])>0:
                lastprice=int(chen[10][1])
                daikan=int(chen[10][0])
                change=int(chen[1])-lastprice
            txt=('%s $ %s $ %s $ %s $ %s $ %s $ %s $ %s $ %s $ %s $ %s $ %s $ %s $ %s\n')%(chen[0],chen[2],chen[1],lastprice,change,daikan,chen[3],\
                    chen[4],chen[5],chen[6],chen[7],chen[8],chen[9],chen[10])#chen[10] pricelist latest to oldest
            chenjiaofile.write(txt)
            chenjiaofile.flush()
 
def GetChenJiaoPerDay():
    #显示的数据晚一天
    date=time.strftime('%Y-%m-%d',time.localtime())
    get_day_count(date)
    date = time.strptime(date,"%Y-%m-%d")
    
    while(True): 
        
        date=datetime.datetime(date[0],date[1],date[2]) 
               
        predate= date + datetime.timedelta(days = -1)        
        predate=predate.strftime("%Y-%m-%d") 
         
        date=predate
        date = time.strptime(date,"%Y-%m-%d")
        
        if(predate=='2017-02-23'):
            break      
        get_day_count(predate)     
       
    
if __name__ == "__main__":
    if 1:
        #Analysis('chengjiao')
        
        #TrendXiaoQuMonth('chengjiao',GetXiaoquData('chengjiao'))
        GetChengJiaoPreviousData()
        pass
    else:
        pass
        GetChengJiaoPreviousData()
        ChenJiaoShangHaiPerMonth()
        get_latest_15_count()
        GetChenJiaoPerDay()
        

        TrendZhenMonth('chengjiao')
        TrendXiaoQuMonth('chengjiao',GetXiaoquData('chengjiao'))     
        TrendShanghaiMonth('chengjiao')
    
    