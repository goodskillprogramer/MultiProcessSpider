# -*- coding: utf-8 -*-
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import subprocess
import os
import time

def exceute_cmd(start,end,cur):   
    print start,end
   
    path = os.path.join(os.getcwd(), "ErShouFang.py")    
    
    script_cmd_file='python '+path+" "+start+' '+end+' '+cur
    
    proc = subprocess.Popen(script_cmd_file)#, stdout=subprocess.PIPE,stderr=subprocess.PIPE   
     
range='210'

def load():
    exceute_cmd('1',range,'0')
    time.sleep(1)
    exceute_cmd('200',range,'0')
    exceute_cmd('400',range,'0')
    exceute_cmd('600',range,'0')
    exceute_cmd('800',range,'0')
    exceute_cmd('1000',range,'0')
    exceute_cmd('1200',range,'0')
    exceute_cmd('1400',range,'0')
    exceute_cmd('1600',range,'0')
    exceute_cmd('1800',range,'0')
    exceute_cmd('2000',range,'0')
    exceute_cmd('2200',range,'0')
    exceute_cmd('2400',range,'0')
    exceute_cmd('2600',range,'0')
    exceute_cmd('2800',range,'0')
    exceute_cmd('3000',range,'0')
    exceute_cmd('3200',range,'0')
    exceute_cmd('3400',range,'0')
    exceute_cmd('3600',range,'0')
    exceute_cmd('3800',range,'0')
    exceute_cmd('4000',range,'0')

if __name__ == "__main__":
    load()
