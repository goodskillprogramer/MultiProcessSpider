# -*- coding: utf-8 -*-
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import sqlite3
from utility import ErShouFangDbItem
from utility import get_current_time_str
from utility import WriteStringList
from utility import PrintStringList
from ErShouFangDbHelper import GetDistincZhen, GetDistincQu
from ErShouFangDbHelper import InsertZhenPrice
from ErShouFangDbHelper import InsertQuPrice
from ErShouFangDbHelper import InsertXiaoQuPrice
from ErShouFangDbHelper import GetTableEntryCount
from ErShouFangDbHelper import DisplaySummary,DisplayErShouFangXiaoquDetail,DbToTxt
import time
import datetime

import sys
import os
from operator import itemgetter
from nt import tmpfile

reload(sys)

sys.setdefaultencoding('UTF-8') 

def GetRecored(dbname,house,minkanguo=0):
    conn = sqlite3.connect("database/"+dbname+".db")
    if minkanguo>0:
        cursor=conn.execute('select * from ErShouFang kanguo>0')
    else:
        cursor=conn.execute('select * from ErShouFang')
        
    for row in cursor:
        if row[ErShouFangDbItem.key] in house:
            house[row[ErShouFangDbItem.key]][dbname]=row[ErShouFangDbItem.zongjia]
           
        else:
            house[row[ErShouFangDbItem.key]]={}
            house[row[ErShouFangDbItem.key]][dbname]=row[ErShouFangDbItem.zongjia]
            house[row[ErShouFangDbItem.key]]['basic']=[row[ErShouFangDbItem.key],
                                                       row[ErShouFangDbItem.title],
                                                       row[ErShouFangDbItem.xiaoqu],
                                                        row[ErShouFangDbItem.fangxing],
                                                        row[ErShouFangDbItem.mianji],
                                                        row[ErShouFangDbItem.qu],
                                                        row[ErShouFangDbItem.zhen],
                                                        row[ErShouFangDbItem.louceng],
                                                        row[ErShouFangDbItem.chaoxiang],
                                                        row[ErShouFangDbItem.zongjia]]
            
        
    conn.close()

def TrendHousePriceChange(dblist_change):
    
    length=len(dblist_change)
    houses={}
    zhendata={}
    qudata={}
    
    zhenlist=GetDistincZhen(dblist_change[0])
    qulist=GetDistincQu(dblist_change[0])
    
    for zhen in zhenlist:
        zhendata[zhen]={}
        zhendata[zhen]['shangtiao']=0
        zhendata[zhen]['xiajiang']=0
        zhendata[zhen]['chiping']=0
        zhendata[zhen]['qu']=""
    
    for qu in qulist:
        qudata[qu]={}
        qudata[qu]['shangtiao']=0
        qudata[qu]['xiajiang']=0
        qudata[qu]['chiping']=0
    
    
    for db in dblist_change:    
        GetRecored(db,houses)   
    
    name=''#get_current_time_str()
    name+='from_'+dblist_change[0]+'_to_'+dblist_change[length-1]
    
    f=open('report\\change\\'+name+'Change.txt','w')
    up=open('report\\change\\'+name+'Up.txt','w')
    down=open('report\\change\\'+name+'Down.txt','w')
    upcount=0
    downcount=0
    txt=''
    spliter=' $ '
    txt+='key'+spliter    
    txt+='xiaoqu'+spliter
    txt+='title'+spliter
    txt+='fangxing'+spliter
    txt+='mianji'+spliter
    txt+='qu'+spliter
    txt+='zhen'+spliter
    txt+='louceng'+spliter
    txt+='chaoxiang'+spliter
    txt+='daikan'+spliter
   
    for db in dblist_change:            
        txt+=str(db)+spliter 
    
    txt+='change'+spliter
    txt+='\n' 
    f.write(txt)
    down.write(txt)
    up.write(txt)
              
    equal=0;
    shangtiao=0
    xiajiang=0
    sumshangtiao=0
    sumxiatiao=0
    for key in houses:
        txt=''        
        basic=houses[key]['basic']
        txt+=str(basic[0])+spliter
        txt+=str(basic[2])+spliter
        txt+=str(basic[1])+spliter        
        txt+=str(basic[3])+spliter
        txt+=str(basic[4])+spliter
        qu=basic[5]
        txt+=str(basic[5])+spliter#qu
        zhen=basic[6]
        txt+=str(basic[6])+spliter #zhen
        txt+=str(basic[7])+spliter #louceng
        txt+=str(basic[8])+spliter #chaoxiang
        txt+=str(basic[9])+spliter#daikan
        
        startprice=''
        endprice=''
        for db in dblist_change:
            if db in houses[key]:
                txt+=str(houses[key][db])+spliter
                if db==dblist_change[0]:
                    startprice=str(houses[key][db])
                if db==dblist_change[length-1]:
                    endprice=str(houses[key][db])
            else:
                txt+=''+spliter
    
         
        if startprice=='' and endprice!='':           
            up.write(txt+'\n')
            upcount+=1
            continue
        
        if startprice !='' and endprice=='':           
            down.write(txt+'\n')
            downcount+=1
            continue
        zhendata[zhen]['qu']=qu
        
        if startprice==endprice:
            equal+=1
            zhendata[zhen]['chiping']+=1
            qudata[qu]['chiping']+=1
            continue
        elif endprice>startprice:
            zhendata[zhen]['shangtiao']+=1
            qudata[qu]['shangtiao']+=1
            shangtiao+=1
            sumshangtiao+=(int(endprice)-int(startprice))
        else:
            xiajiang+=1
            zhendata[zhen]['xiajiang']+=1
            qudata[qu]['xiajiang']+=1
            sumxiatiao+=(int(startprice)-int(endprice))
            
        txt+=str(int(endprice)-int(startprice))+spliter
        txt+='\n'
        f.write(txt)
        
    total=xiajiang+equal+shangtiao
    print ('From %s to %s')%(dblist_change[0],dblist_change[length-1]) 
    print ('xiajia %s shangjia %s\n')%(downcount,upcount)
    print ('%s:%s')%('total',total)
    txt=('%s %s \n%s %s %.2f%% \n%s %s %.2f%%  \n%s %.2f ')%\
            ('chiping:',equal,'xiajiang:',xiajiang,100*float(xiajiang)/total,\
            'shangtiao:',shangtiao,100*float(shangtiao)/total,\
            'xiajiang:shangtiao:',float(xiajiang)/shangtiao)
            
    print txt    
    print 'index:',(shangtiao*1.8-xiajiang)/(shangtiao+xiajiang) 
    print 'shangtiao(万)',sumshangtiao,sumshangtiao/float(shangtiao)
    print 'xiajiang(万):',sumxiatiao,sumxiatiao/float(xiajiang)
    print '差额:万',sumshangtiao-sumxiatiao  , (sumshangtiao-sumxiatiao )/(float(shangtiao+xiajiang)),'万/每套'    
    f.close() 
    down.close()
    up.close()
    
    f=open('report\\change\\'+name+'ZhenChangeIndex.txt','w')
    txt=''
    txt+='qu'+spliter    
    txt+='zhen'+spliter    
    txt+='shangtiao'+spliter
    txt+='xiajiang'+spliter
    txt+='chiping'+spliter
    txt+='index'+spliter
    txt+='\n'
    f.write(txt)
    
    for zhen in zhendata:
        qu=zhendata[zhen]['qu']        
        shangtiao=zhendata[zhen]['shangtiao']
        xiajiang=zhendata[zhen]['xiajiang']
        chiping=zhendata[zhen]['chiping']
        index=0
        if (shangtiao+xiajiang) != 0:
            index=(shangtiao*1.8-xiajiang)/(shangtiao+xiajiang) 
        txt=('%s$%s$%s$%s$%s$%s\n')%(qu,zhen,shangtiao,xiajiang,chiping,index)
        f.write(txt)
    
    f.close() 
    
    f=open('report\\change\\'+name+'QuChangeIndex.txt','w')
    txt=''
    txt+='qu'+spliter       
    txt+='shangtiao'+spliter
    txt+='xiajiang'+spliter
    txt+='chiping'+spliter
    txt+='index'+spliter
    txt+='\n'
    f.write(txt)
    #sorted(qudata.items(),key=lambda item:item[1][1])
    for qu in qudata:              
        shangtiao=qudata[qu]['shangtiao']
        xiajiang=qudata[qu]['xiajiang']
        chiping=qudata[qu]['chiping']
        index=0
        if (shangtiao+xiajiang) != 0:
            index=(shangtiao*1.8-xiajiang)/(shangtiao+xiajiang) 
        txt=('%-4s $ %-4s $ %-4s $ %-4s $ %-4s\n')%(qu,shangtiao,xiajiang,chiping,index)
        f.write(txt)
    
    f.close()    

def TrendXiaoquPriceChange(dblist_change,xiaoqulist):
    
    length=len(dblist_change)
    houses={}
    xiaoqudata={}    
    
    for xiaoqu in xiaoqulist:
        xiaoqudata[xiaoqu]={}
        xiaoqudata[xiaoqu]['shangtiao']=0
        xiaoqudata[xiaoqu]['xiajiang']=0
        xiaoqudata[xiaoqu]['chiping']=0
        xiaoqudata[xiaoqu]['qu']=""
        xiaoqudata[xiaoqu]['zhen']=""
    
    for db in dblist_change:    
        GetRecored(db,houses)   
    
    name=get_current_time_str()
    
    f=open('report\\'+name+'XiaoQuChange.txt','w')
    
    txt=''
    spliter='$'
    txt+='key'+spliter    
    txt+='xiaoqu'+spliter
    txt+='title'+spliter
    txt+='fangxing'+spliter
    txt+='mianji'+spliter
    txt+='qu'+spliter
    txt+='zhen'+spliter
    txt+='louceng'+spliter
    txt+='chaoxiang'+spliter
    txt+='daikan'+spliter
   
    for db in dblist_change:            
        txt+=str(db)+spliter 
    
    txt+='change'+spliter
    txt+='\n' 
    f.write(txt)          
    equal=0;
    shangtiao=0
    xiajiang=0
    
    for key in houses:
        txt=''        
        basic=houses[key]['basic']
        txt+=str(basic[0])+spliter
        xiaoqu=basic[2]
        if xiaoqu not in xiaoqulist:
            continue
        txt+=str(basic[2])+spliter
        txt+=str(basic[1])+spliter        
        txt+=str(basic[3])+spliter
        txt+=str(basic[4])+spliter
        qu=basic[5]
        txt+=str(basic[5])+spliter#qu
        zhen=basic[6]
        txt+=str(basic[6])+spliter #zhen
        txt+=str(basic[7])+spliter
        txt+=str(basic[8])+spliter
        txt+=str(basic[9])+spliter
        
        startprice=''
        endprice=''
        for db in dblist_change:
            if db in houses[key]:
                txt+=str(houses[key][db])+spliter
                if db==dblist_change[0]:
                    startprice=str(houses[key][db])
                if db==dblist_change[length-1]:
                    endprice=str(houses[key][db])
            else:
                txt+=''+spliter
    
         
        if startprice=='' or endprice=='':
            continue
        xiaoqudata[xiaoqu]['qu']=qu
        xiaoqudata[xiaoqu]['zhen']=zhen
        if startprice==endprice:
            equal+=1
            xiaoqudata[xiaoqu]['chiping']+=1
            continue
        elif endprice>startprice:
            xiaoqudata[xiaoqu]['shangtiao']+=1
            shangtiao+=1
        else:
            xiajiang+=1
            xiaoqudata[xiaoqu]['xiajiang']+=1
            
        txt+=str(int(endprice)-int(startprice))+spliter
        txt+='\n'
        f.write(txt)
        
    total=xiajiang+equal+shangtiao
    print ('From %s to %s')%(dblist_change[0],dblist_change[length-1])
    print ('%s:%s')%('total',total)
    txt=('%s %s \n%s %s %.2f%% \n%s %s %.2f%%  \n%s %.2f ')%\
            ('chiping:',equal,'xiajiang:',xiajiang,100*float(xiajiang)/total,\
            'shangtiao:',shangtiao,100*float(shangtiao)/total,\
            'xiajiang:shangtiao:',float(xiajiang)/shangtiao)
    print txt    
    print 'index:',(shangtiao*1.8-xiajiang)/(shangtiao+xiajiang)        
    f.close() 
    
    f=open('report\\'+name+'XiaoQuChangeIndex.txt','w')
    txt=''
    txt+='xiaoqu'+spliter  
    txt+='qu'+spliter    
    txt+='zhen'+spliter    
    txt+='shangtiao'+spliter
    txt+='xiajiang'+spliter
    txt+='chiping'+spliter
    txt+='index'+spliter
    txt+='\n'
    f.write(txt)
    
    for xiaoqu in xiaoqudata:
        qu=xiaoqudata[xiaoqu]['qu']     
        zhen=xiaoqudata[xiaoqu]['zhen']     
        shangtiao=xiaoqudata[xiaoqu]['shangtiao']
        xiajiang=xiaoqudata[xiaoqu]['xiajiang']
        chiping=xiaoqudata[xiaoqu]['chiping']
        index=0
        if (shangtiao+xiajiang) != 0:
            index=(shangtiao*1.8-xiajiang)/(shangtiao+xiajiang) 
        txt=('%s$%s$%s$%s$%s$%s$%s\n')%(xiaoqu,qu,zhen,shangtiao,xiajiang,chiping,index)
        f.write(txt)
    
    f.close()    

def TrendZhenPriceChange(dblist_change,zhenlist):
    
    length=len(dblist_change)
    houses={}
    zhendata={}
    
    zhenlist=GetDistincZhen(dblist_change[0])
    
    for zhen in zhenlist:
        zhendata[zhen]={}
        zhendata[zhen]['shangtiao']=0
        zhendata[zhen]['xiajiang']=0
        zhendata[zhen]['chiping']=0
        zhendata[zhen]['qu']=""
    
    for db in dblist_change:    
        GetRecored(db,houses)   
    
    name=get_current_time_str()
    
    f=open('report\\'+name+'Change.txt','w')
    
    txt=''
    spliter='$'
    txt+='key'+spliter    
    txt+='xiaoqu'+spliter
    txt+='title'+spliter
    txt+='fangxing'+spliter
    txt+='mianji'+spliter
    txt+='qu'+spliter
    txt+='zhen'+spliter
    txt+='louceng'+spliter
    txt+='chaoxiang'+spliter
    txt+='daikan'+spliter
   
    for db in dblist_change:            
        txt+=str(db)+spliter 
    
    txt+='change'+spliter
    txt+='\n' 
    f.write(txt)          
    equal=0;
    shangtiao=0
    xiajiang=0
    
    for key in houses:
        txt=''        
        basic=houses[key]['basic']
        txt+=str(basic[0])+spliter
        txt+=str(basic[2])+spliter
        txt+=str(basic[1])+spliter        
        txt+=str(basic[3])+spliter
        txt+=str(basic[4])+spliter
        qu=basic[5]
        txt+=str(basic[5])+spliter#qu
        zhen=basic[6]
        txt+=str(basic[6])+spliter #zhen
        txt+=str(basic[7])+spliter
        txt+=str(basic[8])+spliter
        txt+=str(basic[9])+spliter
        
        startprice=''
        endprice=''
        for db in dblist_change:
            if db in houses[key]:
                txt+=str(houses[key][db])+spliter
                if db==dblist_change[0]:
                    startprice=str(houses[key][db])
                if db==dblist_change[length-1]:
                    endprice=str(houses[key][db])
            else:
                txt+=''+spliter
    
         
        if startprice=='' or endprice=='':
            continue
        zhendata[zhen]['qu']=qu
        if startprice==endprice:
            equal+=1
            zhendata[zhen]['chiping']+=1
            continue
        elif endprice>startprice:
            zhendata[zhen]['shangtiao']+=1
            shangtiao+=1
        else:
            xiajiang+=1
            zhendata[zhen]['xiajiang']+=1
            
        txt+=str(int(endprice)-int(startprice))+spliter
        txt+='\n'
        f.write(txt)
        
    total=xiajiang+equal+shangtiao
    print ('From %s to %s')%(dblist_change[0],dblist_change[length-1])
    print ('%s:%s')%('total',total)
    txt=('%s %s \n%s %s %.2f%% \n%s %s %.2f%%  \n%s %.2f ')%\
            ('chiping:',equal,'xiajiang:',xiajiang,100*float(xiajiang)/total,\
            'shangtiao:',shangtiao,100*float(shangtiao)/total,\
            'xiajiang:shangtiao:',float(xiajiang)/shangtiao)
    print txt    
    print 'index:',(shangtiao*1.8-xiajiang)/(shangtiao+xiajiang)        
    f.close() 
    
    f=open('report\\'+name+'ZhenChange.txt','w')
    txt=''
    txt+='qu'+spliter    
    txt+='zhen'+spliter    
    txt+='shangtiao'+spliter
    txt+='xiajiang'+spliter
    txt+='chiping'+spliter
    txt+='index'+spliter
    txt+='\n'
    f.write(txt)
    
    for zhen in zhendata:
        qu=zhendata[zhen]['qu']        
        shangtiao=zhendata[zhen]['shangtiao']
        xiajiang=zhendata[zhen]['xiajiang']
        chiping=zhendata[zhen]['chiping']
        index=0
        if (shangtiao+xiajiang) != 0:
            index=(shangtiao*1.8-xiajiang)/(shangtiao+xiajiang) 
        txt=('%s$%s$%s$%s$%s$%s\n')%(qu,zhen,shangtiao,xiajiang,chiping,index)
        f.write(txt)
    
    f.close()    



def QueryPriceFromDbList(dblist,key=None):
    for dbname in dblist:
        conn = sqlite3.connect("database/"+dbname+".db")
        if key!=None:
            cursor=conn.execute('select * from ErShouFang where key=\''+key+'\'')
        else:
            cursor=conn.execute('select * from ErShouFang')
        for row in cursor:
            print dbname,\
            row[ErShouFangDbItem.key],\
            row[ErShouFangDbItem.xiaoqu],  \
            row[ErShouFangDbItem.mianji],  \
            row[ErShouFangDbItem.fangxing],\
            row[ErShouFangDbItem.qu],  \
            row[ErShouFangDbItem.zhen],\
            row[ErShouFangDbItem.zongjia],   \
            row[ErShouFangDbItem.danjia], \
            row[ErShouFangDbItem.kanguo],\
            row[ErShouFangDbItem.title]
                
        conn.close()

def GetPriceFromDbList(key=None):
    global dblist_all
    pricelist=[]
    for dbname in dblist_all[::-1]:
        conn = sqlite3.connect("database/"+dbname+".db")
        if key!=None:
            cursor=conn.execute('select * from ErShouFang where key=\''+key+'\'')
        else:
            cursor=conn.execute('select * from ErShouFang')
            
        for row in cursor: 
            if(len(pricelist)==0):
                pricelist.append(row[ErShouFangDbItem.kanguo])            
            pricelist.append(row[ErShouFangDbItem.zongjia])      
                
        conn.close()
    return pricelist
        
def ReportShanghai(dbname,key,value,mode):
    report = open('report/'+dbname+'/shanghai.txt',mode)    
    report.write(''+key+':'+str(value)+'\n')
    report.close()  
        
def GetTotalKeyCount(dbname):
    count=0
    try:
        conn = sqlite3.connect("database/"+dbname+".db")
        cursor=conn.execute('select count(key) from ErShouFang')
        for row in cursor:            
            count=int(row[0])            
        conn.close()
    except:
        pass    
    return count

def GetTotalDaikan(dbname):
    kanguo=0
    try:
        conn = sqlite3.connect("database/"+dbname+".db")
        cursor=conn.execute('select sum(kanguo) from ErShouFang')
        for row in cursor:            
            kanguo=int(row[0])            
        conn.close()
    except:
        pass 
    return kanguo
    
def CalculateAveragePriceShangHai(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")    
    select='select sum(mianji),sum(zongjia) from ErShouFang '#9003 
    cursor=conn.execute(select)
    mianji=0.0
    zongjia=0.0
    danjia=0.0
    for row in cursor:     
        mianji=row[0]
        zongjia=row[1]
        danjia=zongjia/mianji       
    conn.close()    
    return danjia  

def GetHeaderPriceXiaoqu():  
    splitter='$'
    txt=('%-6s %-2s %-11s %-2s %-11s %-2s %-11s %-2s %-11s %-2s %-11s %-2s %-11s %-2s %-11s \n')%\
    ('qu',splitter,'xiaoqu',splitter,'danjia',splitter,'zhen',splitter,'niandai',splitter,'mianji',splitter,'zongjia',splitter,'count')
    return txt
     
def CalculatePriceByXiaoQu(dbname,xiaoqu=None):
    conn = sqlite3.connect("database/"+dbname+".db")
    xiaoqulist=[]
    slist=[]
    if xiaoqu:
        select='select qu,xiaoqu,zhen,niandai,sum(mianji),sum(zongjia),count(xiaoqu) from ErShouFang where xiaoqu=\''+xiaoqu+'\'group by qu,xiaoqu'
    else:
        select='select qu,xiaoqu,zhen,niandai,sum(mianji),sum(zongjia),count(xiaoqu) from ErShouFang group by qu,xiaoqu'
    cursor=conn.execute(select)
    count=0
    for row in cursor:
        count+=1
        xiaoqulist.append([row[0],row[1],row[2],row[3],row[4],row[5],row[5]/row[4],row[6]])
    conn.close()   
 
    xiaoqulist.sort(key=itemgetter(0),reverse=True)
    splitter='$'
    for entry in xiaoqulist:        
        s=('%-6s %-2s %-11s %-2s %-11.4f %-2s %-11s %-2s %-11s %-2s %-11.2f %-2s %-11.2f %-2s %-11d \n')%\
        (entry[0],splitter,entry[1],splitter,(entry[6]),splitter,\
         entry[2],splitter,(entry[3]),splitter,(entry[4]),\
        splitter,(entry[5]),splitter,(entry[7]))
        slist.append(s)       
    
    return slist

def GetHeaderPriceZhen():  
    splitter='$'        
    txt=(u'%-8s %-2s %-11s %-2s %-11s %-2s %-11s %-2s %-11s %-2s %-11s \n')%\
    ('qu',splitter,'zhen',splitter,'danjia',splitter,'zongjia',splitter,'mianji',splitter,'shuliang')  
    return txt
        
def CalculatePriceByZhen(dbname,zhen=None):
    conn = sqlite3.connect("database/"+dbname+".db")
    xiaoqulist=[]
    slit=[]
    if zhen:
        select='select qu,zhen,sum(mianji),sum(zongjia),count(zhen) from ErShouFang where zhen=\''+zhen+'\'group by zhen order by qu'
    else:
        select='select qu,zhen,sum(mianji),sum(zongjia),count(zhen) from ErShouFang group by zhen order by qu'#9003    
    cursor=conn.execute(select)
    count=0
    for row in cursor:
        count+=1
        xiaoqulist.append([row[0],row[1],row[2],row[3],row[3]/row[2],row[4]])
    conn.close()
    
    xiaoqulist.sort(key=itemgetter(0),reverse=True)
        
    splitter='$'
    
    for entry in xiaoqulist:         
        qu=entry[0]   
        zhen=entry[1] 
        mianji=(entry[2]) 
        zongjia=(entry[3]) 
        danjia=(entry[4]) 
        shuliang=(entry[5])
        
        s=(u'%-8s %-2s %-11s %-2s %-11.4f %-2s %-11.2f %-2s %-11.2f %-2s %-11d \n')%\
        (qu,splitter,zhen,splitter,danjia,splitter,mianji,splitter,zongjia,splitter,shuliang)
        slit.append(s)  
    
    return slit   

def GetHeaderPriceQu():
    splitter=u'$'  
    txt=(u'%-8s %-2s %-11s %-2s %-11s %-2s %-11s %-2s %-6s \n')%\
    ('qu',splitter,'danjia',splitter,'zongjia',splitter,'mianji',splitter,'shuliang')
    return txt

def CalculatePriceByQu(dbname,qu=None):
    conn = sqlite3.connect("database/"+dbname+".db")
    xiaoqulist=[]
    slit=[]
    if qu:
        select='select qu,sum(mianji),sum(zongjia),count(qu) from ErShouFang where qu=\''+qu+'\'group by qu order by qu'
    else:
        select='select qu,sum(mianji),sum(zongjia),count(qu) from ErShouFang group by qu order by qu'    
    cursor=conn.execute(select)
    count=0
    for row in cursor:
        count+=1
        xiaoqulist.append([row[0],row[1],row[2],row[2]/row[1],row[3]])
    conn.close()
    xiaoqulist.sort(key=itemgetter(3),reverse=True)
#     qufile=open('report/'+dbname+'Qu'+qu+'.txt','w')
    splitter=u'$'  
    for entry in xiaoqulist:           
        qu=entry[0].strip()                 
        mianji=(entry[1]) 
        zongjia=(entry[2]) 
        danjia=(entry[3]) 
        shuliang=(entry[4])
        s=(u'%-6s %-2s %-11.4f %-2s %-11.2f %-2s %-11.2f %-2s %-6d \n')%\
        (qu,splitter,danjia,splitter,zongjia,splitter,mianji,splitter,shuliang)
        slit.append(s)        
#         s=qu+splitter+mianji\
#         +splitter+zongjia+splitter+danjia+splitter+shuliang+'\n'    
    
    return slit    
 
def GenerateShanghaiData(dblist):    
    format='%-8s %-6s %-12.3f %6s %-12.3f'
    txt='%-8s %-6s %-12s %6s %-12s'%('date','count','averageprice','daikan','averagedaikan')
    print txt
    for dbname in dblist:  
        if not os.path.exists('report\\'+dbname) :
            os.mkdir('report\\'+dbname)     
        count=GetTotalKeyCount(dbname)
        daikan=GetTotalDaikan(dbname)
        averageprice=CalculateAveragePriceShangHai(dbname)
        averagedaikan=float(daikan)/count
        ReportShanghai(dbname, 'count', count, 'w')
        ReportShanghai(dbname, 'averageprice', averageprice, 'a+')
        ReportShanghai(dbname, 'daikan', daikan, 'a+')
        ReportShanghai(dbname, 'averagedaikan', averagedaikan, 'a+')
        txt=format%(dbname,count,averageprice,daikan,averagedaikan)
        print txt
     
        WriteStringList('report/'+dbname+'/Qu.txt',GetHeaderPriceQu(),'w')
        slist=CalculatePriceByQu(dbname)
        WriteStringList('report/'+dbname+'/Qu.txt', slist, 'a+')
        InsertQuPrice(dbname, slist)
        
        slist=[]
        slist=CalculatePriceByZhen(dbname)
        WriteStringList('report/'+dbname+'/ZhenPrice.txt',GetHeaderPriceZhen(),'w')
        WriteStringList('report/'+dbname+'/ZhenPrice.txt',slist , 'a+')
        InsertZhenPrice(dbname, slist)
        
        slist=[]
        slist=CalculatePriceByXiaoQu(dbname)
        WriteStringList('report/'+dbname+'/XiaoQuPrice.txt',GetHeaderPriceXiaoqu(),'w')
        WriteStringList('report/'+dbname+'/XiaoQuPrice.txt', slist, 'a+')
        InsertXiaoQuPrice(dbname, slist)
        
def ShowShanghaiStep(dblist,step=7):    
    format='%-8s %-6s %-12.3f %6s %-12.3f'
    txt='%-8s %-6s %-12s %6s %-12s'%('date','count','averageprice','daikan','averagedaikan')
    print txt
    i=0
    length=len(dblist)
    for dbname in dblist:  
        i+=1
        if(i<length-3)and(i%step!=0):
            continue
        count=GetTotalKeyCount(dbname)
        daikan=GetTotalDaikan(dbname)
        averageprice=CalculateAveragePriceShangHai(dbname)
        averagedaikan=float(daikan)/count        
        txt=format%(dbname,count,averageprice,daikan,averagedaikan)
        print txt
        
def ShowShanghai(dblist,latest=3):    
    format='%-8s %-6s %-12.4f %6s %-12.3f'
    txt='%-8s %-6s %-12s %6s %-12s'%('date','count','averageprice','daikan','averagedaikan')
    print txt
    l=dblist[-latest:]
    
    for dbname in l:  
        count=GetTotalKeyCount(dbname)
        daikan=GetTotalDaikan(dbname)
        averageprice=CalculateAveragePriceShangHai(dbname)
        averagedaikan=float(daikan)/count        
        txt=format%(dbname,count,averageprice,daikan,averagedaikan)
        print txt
        
def TrendQu(dblist_all,name):
    
    print GetHeaderPriceQu()
    for dbname in dblist_all:  
        l = CalculatePriceByQu(dbname,name)
        PrintStringList(l,dbname)
        
        
def TrendZhen(dblist_all,name):
  
    print GetHeaderPriceZhen()
    for dbname in dblist_all:  
        PrintStringList(CalculatePriceByZhen(dbname,name),dbname)
        
def TrendXiaoQu(dblist_all,name):
   
    print GetHeaderPriceXiaoqu()
    for dbname in dblist_all:  
        PrintStringList(CalculatePriceByXiaoQu(dbname,name),dbname)
        
def DisplayDbCount(dblist):
    for dbname in dblist:
        print 'dbname',dbname,'ErShouFang',GetTableEntryCount(dbname,'ErShouFang')
        print 'dbname',dbname,'QuPrice',GetTableEntryCount(dbname,'QuPrice')
        print 'dbname',dbname,'ZhenPrice',GetTableEntryCount(dbname,'ZhenPrice')
        print 'dbname',dbname,'XiaoQuPrice',GetTableEntryCount(dbname,'XiaoQuPrice')
        
def HouseTrack(startDate,dateNum):
    pre=set()    
    saled=set()  
    newhouse=set() 
    
    startDate = time.strptime(startDate,"%Y-%m-%d")
    lastdate=startDate
    
    #startDate=datetime.datetime(startDate[0],startDate[1],startDate[2])
    startDateTime=datetime.datetime(startDate[0],startDate[1],startDate[2])
    dbname=time.strftime('%Y%m%d',lastdate) 
    
    i=0
    step=1.0
    while(i<dateNum):        
        #print len(saled)
        if os.path.exists('database/'+dbname+'.db'):
            temp={}        
            GetRecored(dbname,temp)
                
            for k in temp:      
                if k in saled:
                    saled.remove(k)
                    #print 'Already exists',k
            sc=0
            for k in pre:                
                if k not in temp:
                    sc+=1
                    saled.add(k)
                    
            sc=sc/step
            jz=sc
            if sc>1000:
                jz=1000

            print dbname,jz,sc,step,len(saled) ,len(temp)   
            pre= set(temp)   
            step=1
        else:
            step+=1
            pass
            #print dbname,'Not exists'           

        lastdatetime= startDateTime + datetime.timedelta(days = i+1)
        
        dbname=lastdatetime.strftime('%Y%m%d')   
        i+=1
        #print dbname,len(saled)
def HouseTrack2(startDate,dateNum):
    pre={}   
    saled={}   
    
    
    startDate = time.strptime(startDate,"%Y-%m-%d")
    lastdate=startDate
    
    #startDate=datetime.datetime(startDate[0],startDate[1],startDate[2])
    startDateTime=datetime.datetime(startDate[0],startDate[1],startDate[2])
    dbname=time.strftime('%Y%m%d',lastdate) 
    
    i=0
    step=1.0
    while(i<dateNum):        
        
        if os.path.exists('database/'+dbname+'.db'):
            temp={}        
            GetRecored(dbname,temp)
                
            for k in temp:      
                if k in saled:
                    del saled[k]                   
                    #print 'Already exists',k
            sc=0
            for k in pre:                
                if k not in temp:
                    sc+=1                   
                    saled[k]=pre[k]
                    
            sc=sc/step
            jz=sc
            if sc>1000:
                jz=1000
            
            print dbname,jz,sc,step,len(saled) ,len(temp)   
            pre= temp 
            step=1
        else:
            step+=1
            pass
            #print dbname,'Not exists'           

        lastdatetime= startDateTime + datetime.timedelta(days = i+1)
        
        dbname=lastdatetime.strftime('%Y%m%d')   
        i+=1
    totalprice=0.0
    totalmianji=0.0
    for k in saled:
        #print saled[k]['basic'][4]
        #print saled[k]['basic'][9]
        
        totalmianji+=saled[k]['basic'][4]
        totalprice+=saled[k]['basic'][9]
        
        #print dbname,len(saled)
    print 'TotalPrice:',totalprice/totalmianji

        
        
    
        
dblist=['20170101',
        
        ]    

dblist_all=[
       '20170302'
        ]   

dblist_change=[
       
        '20170302'
        
        ]    
if 1:     
    TrendHousePriceChange(dblist_change)
    pass
else:   
    DisplaySummary()
    TrendHousePriceChange(dblist_change)
    TrendXiaoquPriceChange(dblist_change,[u'**小区',u'**小区'])
    
    GenerateShanghaiData(['20170205'])
    QueryPriceFromDbList(dblist_all,'sh4313364') 
    
    ShowShanghai(dblist_all)
    ShowShanghaiStep(dblist_all)
    DisplayDbCount(dblist_all)  
    
    TrendQu(dblist_all,u'嘉定')
    TrendQu(dblist_all,u'浦东')
    TrendQu(dblist_all,u'闵行')
    
    TrendZhen(dblist_all,u'金桥')
    TrendZhen(dblist_all,u'张江')
    TrendZhen(dblist_all,u'川沙')
    TrendZhen(dblist_all,u'三林')
    TrendZhen(dblist_all,u'北蔡')
    TrendZhen(dblist_all,u'周浦')
    TrendZhen(dblist_all,u'九亭')
    
    TrendXiaoQu(dblist_all,u'**小区') 
   
   
    
    pass
    
    
                
            

    