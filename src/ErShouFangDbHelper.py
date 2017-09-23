# -*- coding: utf-8 -*-
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import sqlite3
import HousePrice
import os
from utility import strip_chinese_space,get_qoute,strips,strip_space

# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

def CreateErshouFangTable(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    conn.execute('''CREATE TABLE ErShouFang
       (key TEXT PRIMARY KEY     NOT NULL,
       title           TEXT   ,
       xiaoqu            TEXT     ,
       fangxing            TEXT    ,
       mianji            DECIMAL(10,5)    ,
       qu            TEXT    ,
       zhen TEXT,
       louceng            TEXT    ,
       chaoxiang            TEXT    ,
       niandai            TEXT    ,
       zongjia            DECIMAL(10,5)    ,
       danjia            DECIMAL(10,5)    ,
       kanguo            int    );''')  
    conn.commit()     
    conn.close()
    pass

def CreateErshouFangSumarryTable(dbname='Summary'):
    conn = sqlite3.connect("database/"+dbname+".db")
    conn.execute('''CREATE TABLE  Summary
       (key TEXT PRIMARY KEY     NOT NULL,       
       junjia            DECIMAL(10,5)    ,
        count            int  ,  
        chenjiao int,
       daikan            int           
      );''')  
    conn.commit()     
    conn.close()
    pass


#  zhen $  qu             $  danjia      $  zongjia     $  mianji      $  shuliang    $daikan
def CreateZhenPriceTable(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    conn.execute('''CREATE TABLE ZhenPrice
       (zhen TEXT PRIMARY KEY     NOT NULL,       
       qu            TEXT    ,
       danjia            DECIMAL(10,5)    ,
       zongjia            DECIMAL(10,5)    ,
       mianji            DECIMAL(10,5)    ,
       shuliang    int    ,
       daikan int);''')  
    conn.commit()     
    conn.close()
    pass
# xiaoqu  $ qu         $  danjia      $  zhen        $  niandai     $  mianji      $  zongjia     $  shuliang $ daikan  
def CreateXiaoQuPriceTable(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    conn.execute('''CREATE TABLE XiaoQuPrice
       (xiaoqu TEXT PRIMARY KEY     NOT NULL,
       qu            TEXT    ,
       danjia            DECIMAL(10,5)    ,
       zhen TEXT,
       niandai            TEXT    ,
       mianji            DECIMAL(10,5)    ,
       zongjia            DECIMAL(10,5)    ,
        shuliang            int,   
        daikan            int);''')  
    conn.commit()     
    conn.close()
    pass

def CreateQuPriceTable(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    conn.execute('''CREATE TABLE QuPrice
       (qu TEXT PRIMARY KEY     NOT NULL,      
       danjia            DECIMAL(10,5)    ,
       zongjia            DECIMAL(10,5)    ,
       mianji            DECIMAL(10,5)    ,
       shuliang            int,   
       daikan            int);''')  
    conn.commit()     
    conn.close()
    pass

def GetTableEntryCount(dbname,tablename):
    conn = sqlite3.connect("database/"+dbname+".db")
   
    select='select count(*) from '+tablename#9003
    
    cursor=conn.execute(select)
    count=0
    for row in cursor:
        count=row[0]
    conn.close()
    return count
  
def DisplayDistincXiaoquCount(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
   
    select='select DISTINCT qu,xiaoqu from ErShouFang'#9003
    select='select DISTINCT qu,xiaoqu from ErShouFang where zhen!=\'无\''#7774
    cursor=conn.execute(select)
    count=0
    for row in cursor:
        count+=1
    conn.close()
    print count

def DisplaySummary(dbname='Summary'):
    conn = sqlite3.connect("database/"+dbname+".db")   
    
    select='select * from Summary'#7774
    cursor=conn.execute(select)
    print 'riqi junjia taoshu chenjiao90 daikan'
    for row in cursor:
        print row[0],row[1],row[2],row[3],row[4]
    conn.close()
def GetCountFromSummary(date,dbname='Summary'):
    conn = sqlite3.connect("database/"+dbname+".db")   
    
    select=('select * from Summary where key=\'%s\'')%date
    cursor=conn.execute(select)
   # print 'riqi junjia taoshu chenjiao90 daikan'
    chenjiao90=0
    for row in cursor:
        chenjiao90=row[3]      
    
    conn.close()
    return chenjiao90
    
    
    
def GetDistincZhen(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
   
    select='select DISTINCT zhen from ErShouFang order by qu'#9003    
    cursor=conn.execute(select)
    zhenlist=[]
    for row in cursor:
        zhenlist.append(row[0])
    conn.close()
    return zhenlist

def GetDistincQu(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
   
    select='select DISTINCT qu from ErShouFang '#9003    
    cursor=conn.execute(select)
    qulist=[]
    for row in cursor:
        qulist.append(row[0])
    conn.close()
    return qulist    
    
def GetZhenName(dblist,key,xiaoqu):
    zhen=u'无'
    for db in dblist:        
        conn = sqlite3.connect("database/"+db+".db")       
        select='select DISTINCT xiaoqu,zhen,qu from ErShouFang where xiaoqu=\''+xiaoqu+'\''#9003    
        cursor=conn.execute(select)        
        for row in cursor:
            zhen=row[1]
            conn.close()
            return zhen
        conn.close()
    
    (issold,price,zhen)=HousePrice.get_house_price(key)
    return zhen

def GetDistincXiaoquQu(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    xiaoqulist=[]
    select='select DISTINCT xiaoqu,qu from ErShouFang'#9003    
    cursor=conn.execute(select)
    count=0
    for row in cursor:
        count+=1
        xiaoqulist.append([row[0],row[1]])
    conn.close()
    return xiaoqulist
    
def update_zhen(dbname,key,zhen):
    conn = sqlite3.connect("database/"+dbname+".db")
    try:        
        update='update ErShouFang set zhen=\''+zhen.decode('gbk')+'\' where key=\''+key.decode('gbk')+'\''
        print update
        conn.execute(update)   
        conn.commit() 
        conn.close()
    except:
        print 'update error',dbname,key,zhen
        conn.close()

def update_zhen_qu_xiaoqu(dbname,qu,xiaoqu,zhen):
    conn = sqlite3.connect("database/"+dbname+".db")
 
    update='update ErShouFang set zhen='+get_qoute(zhen)+' where qu='+get_qoute(qu)+' and  xiaoqu='+get_qoute(xiaoqu)
    try:   
        print update
        conn.execute(update)   
        conn.commit() 
        conn.close()
    except:
        zhen=get_qoute(zhen)
        print 'update error',dbname,qu,xiaoqu,zhen
        conn.close()
        
def update_zhen_all(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select key,xiaoqu,qu from ErShouFang where zhen==\'无\' or zhen=\'\' order by xiaoqu')
    record_list=[]
    num=0
    for row in cursor:
        num+=1
        l=[]
        l.append(row[0])
        l.append(row[1])
        l.append(row[2])
        record_list.append(l)
        #print num,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]        
    conn.close()
    quered=[]
    for record in record_list:        
        key=record[0]
        xiaoqu=record[1]
        qu=record[2]
        if [qu,xiaoqu] in quered:
            print qu,xiaoqu,'skiped'
            continue
        (issold,price,zhen)=HousePrice.get_house_price(key)
        #update_zhen(dbname,key,zhen)
        update_zhen_qu_xiaoqu(dbname,qu,xiaoqu,zhen)
        quered.append([qu,xiaoqu])
        #DisplayErShouFangDetail(key)
        #DisplayDistincXiaoquCount()
        
def DisplayErShouFangDetail(dbname,key=None):
    conn = sqlite3.connect("database/"+dbname+".db")
    if key!=None:
        cursor=conn.execute('select * from ErShouFang where key=\''+key+'\'')
    else:
        cursor=conn.execute('select * from ErShouFang')
    for row in cursor:
        print row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]
    conn.close()

def DisplayErShouFangXiaoquDetail(dbname,xiaoqu=None):
    conn = sqlite3.connect("database/"+dbname+".db")
    if xiaoqu:
        cursor=conn.execute('select * from ErShouFang where xiaoqu=\''+xiaoqu+'\'')
    else:
        cursor=conn.execute('select * from ErShouFang')
    for row in cursor:
        print row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]
    conn.close()

def DisplayZhenName(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select * from ErShouFang where zhen==\'\' or zhen==\'无\'')
    for row in cursor:
        print row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]
    conn.close()
    #sql:qu       $  danjia      $  zongjia     $  mianji      $  shuliang  $daikan
    #slist:qu       $  danjia      $  zongjia     $  mianji      $  shuliang 
def InsertQuPrice(dbname,slist):
    insertlist=[]
    for txt in slist:
        #print txt
        parser=txt.split('$')
    
        qu=parser[0].strip()   
        danjia=parser[1]    
        zongjia=parser[2]      
        mianji=parser[3]     
        shuliang=parser[4]
        daikan=0
                 
        value=''
        value+='\''+qu+'\','
        value+=str(danjia)+','
        value+=str(zongjia)+','
        value+=str(mianji)+','
        value+=str(shuliang)+','
        value+=str(daikan)
               
        insertString="INSERT or ignore INTO QuPrice(qu,danjia,zongjia,mianji,shuliang,daikan) VALUES ("+value+")"
        insertlist.append(insertString)
        
    
    while(1):
        try:
            sql = sqlite3.connect("database/"+dbname+".db")
            sql.execute('BEGIN')
            
            for insert in insertlist:
                sql.execute(insert);                  
            sql.commit()   
            sql.close()   
            break
        except sqlite3.IntegrityError,e:
            #insertlist.pop()
            print str(e)
        except sqlite3.OperationalError,e:
            print str(e)            
        except Exception,e:
            print str(e)
    pass
#  zhen $  qu             $  danjia      $  zongjia     $  mianji      $  shuliang    $daikan
def InsertZhenPrice(dbname,slist):
    insertlist=[]
    for txt in slist:
        #print txt
        parser=txt.split('$')
        qu=parser[0].strip()    
        zhen=parser[1].strip()   
        
        danjia=parser[2]       
        zongjia=parser[3]
        mianji=parser[4]
        shuliang=parser[5]
        daikan=0
                 
        value=''
        value+='\''+zhen+'\','
        value+='\''+qu+'\','
        value+=str(danjia)+','
        value+=str(zongjia)+','
        value+=str(mianji)+','
        value+=str(shuliang)+','
        value+=str(daikan)
               
        insertString="INSERT or ignore INTO ZhenPrice(zhen,qu,danjia,zongjia,mianji,shuliang,daikan) VALUES ("+value+")"
        insertlist.append(insertString)
        
    
    while(1):
        try:
            sql = sqlite3.connect("database/"+dbname+".db")
            sql.execute('BEGIN')
            
            for insert in insertlist:
                sql.execute(insert);                  
            sql.commit()   
            sql.close()   
            break
        except sqlite3.IntegrityError,e:
            #insertlist.pop()
            print str(e)
        except sqlite3.OperationalError,e:
            print str(e)            
        except Exception,e:
            print str(e)
    pass
    pass
# xiaoqu  $ qu         $  danjia      $  zhen        $  niandai     $  mianji      $  zongjia     $  shuliang $ daikan 
def InsertXiaoQuPrice(dbname,slist):
    insertlist=[]
    for txt in slist:
        #print txt
        parser=txt.split('$')
        
        qu=parser[0].strip() 
        xiaoqu=parser[1].strip()  
        danjia=parser[2] 
        zhen=parser[3].strip() 
        niandai=parser[4].strip()
        mianji=parser[5]
        zongjia=parser[6]       
        shuliang=parser[7]
        daikan=0
                 
        value=''
        value+='\''+xiaoqu+'\','
        value+='\''+qu+'\','
        value+=str(danjia)+','
        value+='\''+zhen+'\','
        value+='\''+niandai+'\','
        value+=str(mianji)+','
        value+=str(zongjia)+','
        value+=str(shuliang)+','
        value+=str(daikan)
               
        insertString="INSERT or ignore INTO XiaoQuPrice(xiaoqu,qu,danjia,zhen,niandai,mianji,zongjia,shuliang,daikan) VALUES ("+value+")"
        insertlist.append(insertString)
       
    
    while(1):
        try:
            sql = sqlite3.connect("database/"+dbname+".db")
            sql.execute('BEGIN')
            
            for insert in insertlist:
                sql.execute(insert);                  
            sql.commit()   
            sql.close()   
            break
        except sqlite3.IntegrityError,e:
            #insertlist.pop()
            print str(e)
        except sqlite3.OperationalError,e:
            print str(e)            
        except Exception,e:
            print str(e)
    pass
    pass      

def InsertSummary(date,summary,dbname='Summary'):
 
    if os.path.exists("database/"+dbname+'.db') == False:
        CreateErshouFangSumarryTable()
    
    sql = sqlite3.connect("database/"+dbname+".db")
    
    sql.execute('BEGIN') 
    summary           
    parser=summary.split('$') 
    junjia=parser[0]
    taoshu=parser[1]
    chenjiao=parser[2]
    daikan=parser[3]
    value=""
    value+=date+","+junjia+','+taoshu+','+chenjiao+','+daikan
    insertString="INSERT or ignore INTO Summary(key,junjia,count,chenjiao,daikan) VALUES ("+value+")"
    print insertString
    sql.execute(insertString);                  
    sql.commit()   
    sql.close()  

def get_qu(strqu):
    qulist=[u'静安',u'金山',u'嘉定',u'宝山',u'松江',u'普陀',u'虹口',u'浦东',
            u'闸北',u'闵行',u'青浦',u'徐汇',u'崇明',u'黄浦',u'上海周边',u'杨浦',u'奉贤',u'长宁']
    for qu in qulist:        
        if strqu.find(qu)!=-1:            
            return qu
        
    print '未找到区',strqu,repr(strqu)
    return strqu
#sh4393949$开鲁三村，业主信赖，满五年少税，链家有钥匙$开鲁三村  2室1厅  75.54平  $杨浦|低区/18层|朝南北|1996年建$380万 50304元/$97人 
def InsertErShouFang(dbname,currentpage,startPage,endPage,txt_list):
 
    if os.path.exists("database/"+dbname+'.db') == False:
        CreateErshouFangTable(dbname)
        CreateQuPriceTable(dbname)
        CreateZhenPriceTable(dbname)
        CreateXiaoQuPriceTable(dbname)
        
    insertlist=[]
    for txt in txt_list:
        #print txt
        parser=txt.split('$')
    #     print  len(parser)
        key=parser[0]#key
    #     print key
        title=parser[1]#title
    #     print title
        #2室1厅|47.88平|低区/6层|朝南
        other=parser[2]#other'
        chaoxiang=''
        basic=other.split(u'|')   
        for e in basic:
            if e.find(u'层')!=-1:
                louceng=e      
            elif e.find(u'朝')!=-1:
                chaoxiang=e  
            elif e.find(u'平')!=-1:
                mianji=e  
            
        fangxing=basic[0]  
        totalprice=parser[3]
        #金杨新村十街坊|浦东|金杨|1995年建
        extent=parser[4].split(u'|')  
        xiaoqu=  extent[0]
        qu=(extent[1]) 
        zhen=extent[2]   
        if len(extent)==4:     
            niandai=extent[3]     
        else:
            niandai=''    
        
        perprice=parser[5]#other       
         
        value=''
        value+='\''+key+'\','
        value+='\''+title+'\','
        value+='\''+xiaoqu+'\','
        value+='\''+fangxing+'\','
        mianji=mianji.strip(u'平')
        value+=mianji+','
        value+='\''+qu+'\','
        value+='\''+zhen+'\','
        value+='\''+louceng+'\','
        value+='\''+chaoxiang+'\','
        value+='\''+niandai+'\','
        totalprice=totalprice.strip(u'万')
        value+=totalprice+','
        perprice=perprice.strip(u'单价')
        perprice=perprice.strip(u'元/平')
        value+=perprice+','
       
        daikan='0'
        value+=daikan       
         
        insertString="INSERT or ignore INTO ErShouFang(key,title,xiaoqu,fangxing,mianji,qu,zhen,louceng,chaoxiang,niandai,zongjia,danjia,kanguo) VALUES ("+value+")"
        insertlist.append(insertString)  
        #print       insertString
    
    while(1):
        try:
            sql = sqlite3.connect("database/"+dbname+".db")
            sql.execute('BEGIN')
            
            for insert in insertlist:
                sql.execute(insert);                  
            sql.commit()   
            sql.close()   
            break
        except sqlite3.IntegrityError,e:
            #insertlist.pop()
            print str(e)
        except sqlite3.OperationalError,e:
            print str(e)            
        except Exception,e:
            print str(e)
                
#     print insertString
#     sql.execute(insertString);  
#     sql.commit()      
#     sql.close()       
       
    filename=dbname+'_'+str(startPage)+'_'+str(startPage+endPage-1)
    rollback=open('database\\'+filename+'.txt','a+')
    for txt in txt_list:
        txt=str(currentpage+startPage)+'$'+txt
        txt=str(currentpage)+'$'+txt
        rollback.write(txt.encode('utf-8'))
    rollback.close()  
    
    
#sh4393949$开鲁三村，业主信赖，满五年少税，链家有钥匙$开鲁三村  2室1厅  75.54平  $杨浦|低区/18层|朝南北|1996年建$380万 50304元/$97人 
def InsertErShouFang0413(dbname,currentpage,startPage,endPage,txt_list):
 
    if os.path.exists("database/"+dbname+'.db') == False:
        CreateErshouFangTable(dbname)
        CreateQuPriceTable(dbname)
        CreateZhenPriceTable(dbname)
        CreateXiaoQuPriceTable(dbname)
        
    insertlist=[]
    for txt in txt_list:
        #print txt
        parser=txt.split('$')
    #     print  len(parser)
        key=parser[0]#key
    #     print key
        title=parser[1]#title
    #     print title
        other=parser[2]#other'
        basic=other.split(u'\xa0')
        r=strip_chinese_space(basic)   
        xiaoqu=r[0]
        fangxing=r[1]
        mianji=r[2]
        other=parser[3]#other   
        extent=other.split(u'|')    
        qu=get_qu(extent[0]) 
        zhen=GetZhenName(['20170101','20170109','20170110','20170112'],key,xiaoqu)
        louceng=''
        niandai=''
        chaoxiang=''
        for e in extent:
            if e.find(u'层')!=-1:
                louceng=e;
            elif e.find(u'年') != -1:
                niandai=e
            elif e.find(u'朝')!=-1:
                chaoxiang=e       
        price=parser[4]#other
        price=price.split(u' ')
    #     print price[0],price[1]
        totalprice=price[0]
        perprice=price[1]
        daikan=parser[5]#other
    #     print key,title,xiaoqu,fangxing,mianji,\
    #        qu,louceng,niandai,chaoxiang,  \
    #        totalprice,perprice,\
    #        daikan
         
        value=''
        value+='\''+key+'\','
        value+='\''+title+'\','
        value+='\''+xiaoqu+'\','
        value+='\''+fangxing+'\','
        mianji=mianji.strip(u'平')
        value+=mianji+','
        value+='\''+qu+'\','
        value+='\''+zhen+'\','
        value+='\''+louceng+'\','
        value+='\''+chaoxiang+'\','
        value+='\''+niandai+'\','
        totalprice=totalprice.strip(u'万')
        value+=totalprice+','
        perprice=perprice.strip(u'元/')
        value+=perprice+','
        daikan=strip_space(daikan)
        daikan=daikan.strip(u'人')
        value+=daikan       
        
        insertString="INSERT or ignore INTO ErShouFang(key,title,xiaoqu,fangxing,mianji,qu,zhen,louceng,chaoxiang,niandai,zongjia,danjia,kanguo) VALUES ("+value+")"
        insertlist.append(insertString)
    
    while(1):
        try:
            sql = sqlite3.connect("database/"+dbname+".db")
            sql.execute('BEGIN')
            
            for insert in insertlist:
                sql.execute(insert);                  
            sql.commit()   
            sql.close()   
            break
        except sqlite3.IntegrityError,e:
            #insertlist.pop()
            print str(e)
        except sqlite3.OperationalError,e:
            print str(e)            
        except Exception,e:
            print str(e)
                
#     print insertString
#     sql.execute(insertString);  
#     sql.commit()      
#     sql.close()       
       
    filename=dbname+'_'+str(startPage)+'_'+str(startPage+endPage-1)
    rollback=open('database\\'+filename+'.txt','a+')
    for txt in txt_list:
        txt=str(currentpage+startPage)+'$'+txt
        txt=str(currentpage)+'$'+txt
        rollback.write(txt.encode('utf-8'))
    rollback.close()                  

def HandleNewDb(olddb,newdb):
    conn = sqlite3.connect("database/"+olddb+".db")
    cursor=conn.execute('select * from ErShouFang')
    
    new = sqlite3.connect("database/"+newdb+".db")
    for row in cursor:
        print row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]
        value=''
        value+='\''+row[0]+'\','#key
        value+='\''+row[1]+'\','#title
        value+='\''+row[2]+'\','#xiaoqu
        value+='\''+row[3]+'\','#fangxing
        value+=row[4].strip(u'平')+','#mianji
        value+='\''+row[5]+'\','#qu
        value+='\''+row[6]+'\','#zhen
        value+='\''+row[7]+'\','#louceng
        value+='\''+row[8]+'\','#chaoxiang
        value+='\''+row[9]+'\','#niandai
        value+=row[10].strip(u'万')+','#zongjia
        value+=row[11].strip(u'元/')+','#danjia
        daikan=strip_space(row[12])
        daikan=daikan.strip(u'人')
        value+=daikan.strip(u'人')#daikan
    
        
        insertString="INSERT INTO ErShouFang (key,title,xiaoqu,fangxing,mianji,qu,zhen,louceng,chaoxiang,niandai,zongjia,danjia,kanguo) VALUES ("+value+")"
       
     
        print insertString
        new.execute(insertString);
        new.commit()

    conn.close()
    new.close()
  
#get record from db write them to txt splitter by $
def DbToTxt(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select * from ErShouFang order by xiaoqu  ')
    report=open(dbname+'.txt','w')
    for row in cursor:
        spliter=u'$'
        str= row[0]+spliter;
        str+=row[1]+spliter;
        str+=row[2]+spliter
        str+=row[3]+spliter
        str+=row[4]+spliter
        str+=row[5]+spliter
        str+=row[6]+spliter
        str+=row[7]+spliter
        str+=row[8]+spliter
        str+=row[9]+spliter
        str+=row[10]+spliter
        str+=row[11]+spliter    
        str+=row[12] 
        
        report.write(str.encode('gbk'))
    conn.close()
    report.close()

def GetXiaoquNianDai(dbname):
    xiaoqu={}
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select DISTINCT xiaoqu,niandai from ErShouFang')    
    
    for row in cursor:
        xiaoqu[row[0]]=row[1]
        #print row[0],row[1]
    
    conn.close()
    for key in xiaoqu:
        pass
        #print key,xiaoqu[key]
        
    return xiaoqu
    
# def CreateErshouFangTable(dbname):
#     conn = sqlite3.connect("database/"+dbname+".db")
#     conn.execute('''CREATE TABLE ErShouFang
#        (key TEXT PRIMARY KEY     NOT NULL,
#        title           TEXT   ,
#        xiaoqu            TEXT     ,
#        fangxing            TEXT    ,
#        mianji            TEXT    ,
#        qu            TEXT    ,
#        zhen TEXT,
#        louceng            TEXT    ,
#        chaoxiang            TEXT    ,
#        niandai            TEXT    ,
#        zongjia            TEXT    ,
#        danjia            TEXT    ,
#        kanguo            TEXT    );''')       
#     conn.close()
#     pass 
#GetXiaoquNianDai('20170107')
#CreateErshouFangTable2('20170106')
#HandleNewDb(dbname,'20170101')
#DisplayDistincXiaoquCount(dbname) 
#DbToTxt(dbname)
#DisplayDistincZhen('20170109')
#DisplayZhenName('20170109')
def CreateAllTable():
    dblist_all=[
        '20170101',
        '20170102',
        '20170103',
        '20170104',
        '20170106',
        '20170107',
        '20170108',
        '20170109',
        '20170110',
        '20170111',
        '20170112',
        '20170113',
        ]   
    for db in dblist_all:
        CreateQuPriceTable(db)
        CreateZhenPriceTable(db)
        CreateXiaoQuPriceTable(db)
        
#CreateAllTable()
#update_zhen_all('20170116')
#DisplayErShouFangDetail(dbname)
