# -*- coding: utf-8 -*-
"""
The Process
Added by Zach Hou
Version 1.0
"""

import datetime
import pandas as pd

# 日期&时间
current_time = datetime.datetime.now()
current_time_str=current_time.strftime("%Y-%m-%d %H:%M:%S")
current_time_str_sp=current_time.strftime("%Y%m%d%H%M%S")
current_min_str=current_time.strftime("%Y%m%d%H%M")
current_date_str=current_time.strftime("%Y-%m-%d")
current_month_str=current_time.strftime("%Y-%m-01")
current_year_str=current_time.strftime("%y-01-01")

last_min_str=(current_time-datetime.timedelta(minutes=1)).strftime("%Y%m%d%H%M")
last_date_str=(current_time-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
last_month_str=(current_time+pd.tseries.offsets.DateOffset(months=-1)).strftime("%Y-%m-01")
last_year_str=(current_time+pd.tseries.offsets.DateOffset(months=-1)).strftime("%Y-01-01")

def date_add(para_date_str,para_interval,para_label="DD",sp_label=0):
    para_date=datetime.datetime.strptime(para_date_str,"%Y-%m-%d")
    
    if para_label in ("dd","DD"):
        para_result=para_date+pd.tseries.offsets.DateOffset(days=para_interval)
    elif para_label in ("ww","WW"):
        para_result=para_date+pd.tseries.offsets.DateOffset(days=7*para_interval)
    elif para_label in ("mm","MM"):
        para_result=para_date+pd.tseries.offsets.DateOffset(months=para_interval)        
        
    if (sp_label==1) & (para_label in ("mm","MM")):
        if para_interval>0:                
            para_result=para_result+pd.tseries.offsets.DateOffset(days=-1)                
        elif para_interval<0:
            para_result=para_result+pd.tseries.offsets.DateOffset(days=1)                

    para_result_str=para_result.strftime("%Y-%m-%d")       
    return para_result_str    

def date_list(para_start,para_end,para_label="DD",para_interval=1):
    para_list=[]
    if para_start < para_end:
        para_list.append(para_start)
        para_date = date_add(para_start,para_interval,para_label)
        while(para_date<para_end):
            para_list.append(para_date)
            para_date = date_add(para_date,para_interval,para_label)                
    if para_start > para_end:
        para_list.append(para_start)
        para_date = date_add(para_start,-1*para_interval,para_label)
        while(para_date>para_end):
            para_list.append(para_date)
            para_date = date_add(para_date,-1*para_interval,para_label)                
    return para_list

#String日期格式化
def date_format(date_str="2015-01-01",formattor="YYYYMM"):
#-------------------------------Date Format--------------------------#
    formattor=formattor.lower().replace("yyyy","%Y").replace("mm","%m").replace("dd","%d")
    para_date=datetime.datetime.strptime(date_str,'%Y-%m-%d')
    return para_date.strftime(formattor)