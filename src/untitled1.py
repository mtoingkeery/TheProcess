# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 06:19:07 2018

@author: houz
"""

import os,time
import pandas as pd
import fdmt_data as fdt
import fdmt_date as fda

data_path=fdt.data_path

para_date_start=fda.current_date_str
para_date_end=fda.current_date_str

if fda.current_date_str>=fda.date_add(fda.current_month_str,5):
    para_date_start=fda.current_month_str
    para_date_end=fda.date_add(fda.current_month_str,1,"MM")
else:
    para_date_start=fda.date_add(fda.current_month_str,-1,"MM")
    para_date_end=fda.date_add(fda.current_month_str,1,"MM")

para_date_start='2014-01-01'
para_date_end='2015-01-01'

para_mon_start=fda.date_format(para_date_start,"yyyymm")
para_mon_end=fda.date_format(para_date_end,"yyyymm")


hist_list=[]
for parent,dirnames,filenames in os.walk(data_path+"idx_hist/"):
    for filename in filenames:
        if (filename[-4:].lower()=='.txt')&(filename[-17:-11]>=para_mon_start)&(filename[-17:-11]<=para_mon_end):
            hist_list.append(parent+filename)

for para in hist_list:
    print(time.strftime("%Y/%m/%d %T")+" - "+para[-17:])
    para_df1=pd.read_csv(para,dtype={'id':str})

    
#    para_df2=para_df1.rename(columns={"utime":"dtime"})
#    para_df2["utime"]=fda.current_time_str


print(para_df1)
print("X1199000")