# -*- coding: utf-8 -*-
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import sqlite3

def CreateChengJiaoTable(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    conn.execute('''CREATE TABLE ChengJiao
       (key TEXT PRIMARY KEY     NOT NULL,       
       xiaoqu            TEXT     ,
       fangxing            TEXT    ,
       mianji            DECIMAL(10,5)    ,
       qu            TEXT    ,
       zhen TEXT,      
       zongjia            DECIMAL(10,5)    ,
       danjia            DECIMAL(10,5),
       manji TEXT,
       riqi Datetime);''')       
    conn.close()
    pass

def Display(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select * from chengjiao order by riqi')
    for row in cursor:
        print row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]
    conn.close()
    pass

def GetCount(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select count(*) from chengjiao')
    for row in cursor:
        print 'chengjiao count:',row[0]
    conn.close()
    pass

def GetMaxRiQi(dbname='chengjiao'):
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select max(riqi) from chengjiao')
    date=None
    for row in cursor:        
        date=row[0]
    conn.close()
    print date
    

def GetMinRiQi(dbname):
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select min(riqi) from chengjiao')
    for row in cursor:
        print 'From:',row[0]
    conn.close()
    pass

def DbToTxt(dbname):
    splitter='$'
    conn = sqlite3.connect("database/"+dbname+".db")
    cursor=conn.execute('select * from chengjiao order by qu')
    f=open('report\\'+dbname+".txt",'w+')
    txt='key $ xiaoqu $ fangxing $ mianji $ qu $ zhen $ zongjia $ danjia $ manji $ riqi\n'
    f.write(txt.encode('utf-8'))
    for row in cursor:        
        txt=('%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n')%\
        (row[0],splitter,row[1],splitter,row[2],splitter,\
         row[3],splitter,row[4],splitter,row[5],splitter,\
         row[6],splitter,row[7],splitter,row[8],splitter,row[9])
        f.write(txt.encode('utf-8'))
       
    conn.close()
    f.close()
    pass

#sh4481010$牡丹路186弄             2室1厅 66.14平         $高区/6层|朝南|中装$2017.04.1$480万$浦东|花木$单价72573元/$满五  距离2号线世纪公园站597米 $
def InsertChenJiao(txt):
    #print txt
    parser=txt.split('$')
#     print  len(parser)
    key=parser[0]#key
#     print key   
    basic=parser[1]#凌桥二村 1室1厅 39.85平米 
    basic=basic.split()
    xiaoqu=basic[0]
    fangxing=basic[1]
    mianji=basic[2]
    mianji=mianji.strip(u'平')
    
    riqi=parser[3].replace('.','-')
    zongjia=parser[4].strip(u'万')
    quzhen=parser[5].split('|')#浦东  
    qu=quzhen[0]
    zhen=quzhen[1]#waigaoqiao
    danjia=parser[6].strip(u'单价')  
    danjia=danjia.strip(u'元/平') 

    
    manji=parser[7]#      
     
    value=''
    value+='\''+key+'\','    
    value+='\''+xiaoqu+'\','
    value+='\''+fangxing+'\','
    value+=mianji+','
    value+='\''+qu+'\','
    value+='\''+zhen+'\','
    value+=zongjia+','
    value+=danjia+','
    value+='\''+manji+'\','
    value+='\''+riqi+'\''  
    
    
    insertString="INSERT INTO ChengJiao (key,xiaoqu,fangxing,mianji,qu,zhen,zongjia,danjia,manji,riqi) VALUES ("+value+")"
#     print insertString
#     return 
    cx = sqlite3.connect("database/chengjiao.db")
    try:      
        print insertString
        cx.execute(insertString);
        cx.commit()
        cx.close()
    except Exception,e:
        print 'insert error',key,e
        cx.close()
        pass
    pass

#sh4396989$凌桥二村 1室1厅 39.85平米$浦东$外高桥$2016-12-18 链家网签约   40903元/平 挂牌单价   163万 挂牌总价  满五
def InsertChenJiaoPre(txt):
    #print txt
    parser=txt.split('$')
#     print  len(parser)
    key=parser[0]#key
#     print key   
    basic=parser[1]#凌桥二村 1室1厅 39.85平米 
    basic=basic.split()
    xiaoqu=basic[0]
    fangxing=basic[1]
    mianji=basic[2]
    mianji=mianji.strip(u'平米')
    qu=parser[2]#浦东  
    zhen=parser[3]#waigaoqiao
    extent=parser[4]#浦东
    extent=extent.split()  
    riqi=extent[0] 
    qianyue=extent[1]
    danjia=extent[2]
    danjia=danjia.strip(u'元/平')
    guapai=extent[3]
    zongjia=extent[4]
    zongjia=zongjia.strip(u'万')
    guapai=extent[5]
    manji=extent[6]    
     
    value=''
    value+='\''+key+'\','    
    value+='\''+xiaoqu+'\','
    value+='\''+fangxing+'\','
    value+=mianji+','
    value+='\''+qu+'\','
    value+='\''+zhen+'\','
    value+=zongjia+','
    value+=danjia+','
    value+='\''+manji+'\','
    value+='\''+riqi+'\''  
    
    cx = sqlite3.connect("database/chengjiao.db")
    insertString="INSERT INTO ChengJiao (key,xiaoqu,fangxing,mianji,qu,zhen,zongjia,danjia,manji,riqi) VALUES ("+value+")"
   
    try:      
        print insertString
        cx.execute(insertString);
        cx.commit()
        cx.close()
    except Exception,e:
        print 'insert error',key,e
        cx.close()
        pass
    pass
if __name__ == '__main__':
    if 1:
       
        GetMinRiQi('chengjiao')
        GetMaxRiQi('chengjiao')
        pass
    else:    
        GetMinRiQi('chengjiao')
        GetMaxRiQi('chengjiao')
        GetCount('chengjiao')
        DbToTxt('chengjiao')
        pass

#Display('chengjiao')
#InsertChenJiao(u'sh4396989$凌桥二村 1室1厅 39.85平米$浦东$外高桥$2016-12-18 链家网签约   40903元/平 挂牌单价   163万 挂牌总价  满五')

#CreateChengJiaoTable('chengjiao')