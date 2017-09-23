# -*- coding: utf-8 -*- 
'''
@author: wj3235@126.com
说明：（1）程序仅供技术学习，严禁用于任何商业用途
               （2）对于抓取内容及其分析，请勿乱发布，后果自负
               （3）软件可能有bug，如果发现望及时告知
'''
import  xdrlib ,sys
import xlrd
import xlwt
import datetime


import  xdrlib ,sys
import xlrd

def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
        return None
#����������ȡExcel����е�����   ����:file��Excel�ļ�·��     colnameindex����ͷ���������е�����  ��by_index���������
def excel_table_byindex(file= 'file.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #����
    ncols = table.ncols #����
    colnames =  table.row_values(colnameindex) #ĳһ������ 
    list =[]
    for rownum in range(1,nrows):

         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
             list.append(app)
    return list

#�������ƻ�ȡExcel����е�����   ����:file��Excel�ļ�·��     colnameindex����ͷ���������е�����  ��by_name��Sheet1����
def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #���� 
    colnames =  table.row_values(colnameindex) #ĳһ������ 
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

def main():
   tables = excel_table_byindex()
   for row in tables:
       print row

   tables = excel_table_byname()
   for row in tables:
       print row

def write_to_excel_record(sheet,row,recordstr):
    record = recordstr.split(u' ')    
    write_to_excel(sheet,row,record[0],record[1],record[2],record[3],record[4],record[5],record[9],record[13],record[16])
    
def write_header(sheet):
    row=0
    sheet.write(row, 0, u"小区")
    sheet.write(row, 1, u'房型')   
   
    sheet.write(row, 2, u'面积')
    sheet.write(row, 3, u'区')
    sheet.write(row, 4, u'镇')
    sheet.write(row, 5, u'日期')
    
    
    sheet.write(row, 6, u'单价') 
    
    sheet.write(row, 7, u'总价')
    sheet.write(row, 8, u'介绍')
    
def write_to_excel(sheet,row,xiaoqu,fangxin,mianji,qu,zhen,date,danjia,zongjia,inroduce):
    sheet.write(row, 0, xiaoqu)
    sheet.write(row, 1, fangxin)
    mianji=mianji.strip(u"平米")
    mianji=float(mianji)
    sheet.write(row, 2, mianji)
    sheet.write(row, 3, qu)
    sheet.write(row, 4, zhen)
    date=date.split(u"-")
    
    date=datetime.date(int(date[0]),int(date[1]),int(date[2]))
    style = xlwt.XFStyle()
    style.num_format_str = 'M/D/YY'
    sheet.write(row, 5, date,style)
    danjia=danjia.strip(u"元/平")
    danjia=int(danjia)
    sheet.write(row, 6, danjia)
    zongjia=zongjia.strip(u"万")
    zongjia=int(zongjia)
    sheet.write(row, 7, zongjia)
    sheet.write(row, 8, inroduce)    
    pass

def write_to_excels(sheet,row,xiaoqu,fangxin,mianji,qu,zhen,date,danjia,zongjia,inroduce):
    sheet.write(row, 0, xiaoqu)
    sheet.write(row, 1, fangxin)   
    sheet.write(row, 2, mianji)
    sheet.write(row, 3, qu)
    sheet.write(row, 4, zhen)
    style = xlwt.XFStyle()
    style.num_format_str = 'M/D/YY'
    sheet.write(row, 5, date,style)    
    sheet.write(row, 6, danjia)   
    sheet.write(row, 7, zongjia)
    sheet.write(row, 8, inroduce)    
    pass

def save_write_excel(workbook,name):
    workbook.save(name) 
    
def open_write_excel():
    #http://www.tuicool.com/articles/BFFbUvu
    workbook = xlwt.Workbook(style_compression=2)     
    return workbook

def add_write_sheet(workbook):
    #http://www.tuicool.com/articles/BFFbUvu    
    sheet = workbook.add_sheet("record") 
    return sheet

def copy_old_data(str_pre_day,work_book,sheet,row):
    path=r"F:\source_code\workspace\lianjia\src\shanghai"
    data = open_excel(path+"\\"+str_pre_day)
    if data iChengJiao
        return
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    print "old_record:",nrows," updae:",row
    for rownum in range(1,nrows):

        old_row = table.row_values(rownum)
        if old_row:
           write_to_excels(sheet,row,old_row[0],old_row[1],old_row[2],old_row[3],\
                          old_row[4],old_row[5],old_row[6],old_row[7],old_row[8])
           row+=1
 





