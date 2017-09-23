# -*- coding: utf-8 -*-
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import time

class ErShouFangDbItem:
        key=0
        title=1
        xiaoqu=2
        fangxing=3
        mianji=4
        qu=5
        zhen=6
        louceng=7
        chaoxiang=8
        niandai=9
        zongjia=10
        danjia=11
        kanguo=12
        
def strips(source):
    s=u""
    lens=len(source)
    i=0
    pre=cur=source[0]
    
    while(i<lens-1):
        if (pre==u'\n' or pre== u'\t' or pre== u'\r') and (cur==u'\n' or cur== u'\t' or cur== u'\r'):
            pre=cur
            cur=source[i+1]
            i+=1
            continue    
        
        if(cur==u'\n' or cur== u'\t' or cur== u'\r'):
            cur=" "
        s =s+ cur 
        pre=cur
        cur=source[i+1]
        i=i+1         
             
    return s

def strip_space(source):
    s=u""
    for cur in source:
        if(cur==u'\n' or cur== u'\t' or cur== u'\r' or cur == u' '):
                continue
        else:
            s+=cur
    return s

def strip_chinese_space(l):
    r=[]
    for item in l:
        if item!=u'\xa0' and item != u' ' and item !=u'':
            r.append(item)
    return r

def get_qoute(str):
    str=u'\''+str+u'\''
    return str

def get_current_time_str():
    name=time.strftime('%Y%m%d',time.localtime())
    return name

def WriteStringList(fname,slist,mode,other=''):
    f=open(fname,mode)
    for s in slist:
        
        f.write(s)
    f.close()

def PrintStringList(slist,other=''):    
    for s in slist:
        s=s.strip('\n')
        print other,s
    