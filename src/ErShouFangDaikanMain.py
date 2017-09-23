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
from AdvancedAnalysisErShouFangMain import dblist_all
import sys
import os
from operator import itemgetter

reload(sys)

sys.setdefaultencoding('UTF-8') 

def GetRecoredKanGuo(dbname,house):
    conn = sqlite3.connect("database/"+dbname+".db")
    
    cursor=conn.execute('select * from ErShouFang where kanguo > 0')
    
    for row in cursor:
        if row[ErShouFangDbItem.key] in house:
            house[row[ErShouFangDbItem.key]][dbname]=row[ErShouFangDbItem.kanguo]
           
        else:
            house[row[ErShouFangDbItem.key]]={}
            house[row[ErShouFangDbItem.key]][dbname]=row[ErShouFangDbItem.kanguo]
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
    houses={}
    zhendata={}
    qudata={}
    dblist_change=dblist_change[-10:]
    length=len(dblist_change)
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
        GetRecoredKanGuo(db,houses)   
    
    name=''#get_current_time_str()
    name+='from_'+dblist_change[0]+'_to_'+dblist_change[length-1]
    
    f=open('report\\kanguo\\'+name+'ChangeKanguo.txt','w')
    
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
    txt+='zongjia'+spliter
   
    for db in dblist_change:            
        txt+=str(db)+spliter 
    
    txt+='\n' 
    f.write(txt)          
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
        isignore=False
        for db in dblist_change:
            if db in houses[key]:
                txt+=str(houses[key][db])+spliter
            else:
                txt+=''+spliter
                isignore=True
        if isignore:
            continue      
        
        txt+='\n'
        f.write(txt)
    f.close()
    
kanguo=[
        '20170302',]

def GetInvalidDaiKan(dblist):
    for db in dblist:
        conn = sqlite3.connect("database/"+db+".db")
    
        cursor=conn.execute('select count(key) from ErShouFang where kanguo <3')
        invalidcount=0
        for row in cursor:
            invalidcount=row[0]
        totalcount=GetTableEntryCount(db,'ErShouFang')
        print db,invalidcount,totalcount,totalcount-invalidcount,float(invalidcount)/float(totalcount)
        
    
if __name__ == "__main__":
    if 1:
        global dblist_all
        TrendHousePriceChange(dblist_all)
    else:
        TrendHousePriceChange(kanguo)
        GetInvalidDaiKan(dblist_all)
