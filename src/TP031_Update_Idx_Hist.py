# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 06:19:07 2018

@author: houz
"""

import os,time
import pandas as pd
import fdmt_data
import fdmt_date

def main():
    data_path=fdmt_data.data_path
    magic_box=fdmt_data.magic_box

    para_date_start=fdmt_date.current_date_str
    para_date_end=fdmt_date.current_date_str

    if fdmt_date.current_date_str>=fdmt_date.date_add(fdmt_date.current_month_str,5):
        para_date_start=fdmt_date.current_month_str
        para_date_end=fdmt_date.date_add(fdmt_date.current_month_str,1,"MM")
    else:
        para_date_start=fdmt_date.date_add(fdmt_date.current_month_str,-1,"MM")
        para_date_end=fdmt_date.date_add(fdmt_date.current_month_str,1,"MM")

    #Be careful!!!
    inital_flag=False

    if inital_flag==True:
        para_date_start='2014-01-01'
        para_date_end=fdmt_date.current_date_str

    para_mon_start=fdmt_date.date_format(para_date_start,"yyyymm")
    para_mon_end=fdmt_date.date_format(para_date_end,"yyyymm")


    if inital_flag==False:
        fdt.pgs_execute_query("TRUNCATE TABLE MAIN.TMP_IDX_HIST")

    hist_list=[]
    for parent,dirnames,filenames in os.walk(data_path+"idx_pkl/"):
        for filename in filenames:
            if (filename[-4:].lower()=='.pkl')&(filename[-17:-11]>=para_mon_start)&(filename[-17:-11]<=para_mon_end):
                hist_list.append(parent+filename)

    for para in hist_list:
        print(time.strftime("%Y/%m/%d %T")+" - "+para[-17:])

        para_df1=pd.read_csv(para,dtype={'id':str})
        para_df2=para_df1.rename(columns={"utime":"dtime"})
        para_df2["utime"]=fda.current_time_str

        para_df2.to_sql("tmp_idx_hist",magic_box,if_exists="append",schema="main",index=False)

    if inital_flag==True:
        fdt.pgs_execute_query("CREATE TABLE MAIN.F_IDX_HIST AS SELECT * FROM MAIN.TMP_IDX_HIST)")
    else:
        fdt.pgs_execute_query("DELETE FROM MAIN.F_IDX_HIST WHERE TDATE>=(SELECT MIN(TDATE) FROM MAIN.TMP_IDX_HIST)")
        fdt.pgs_execute_query("INSERT INTO MAIN.F_IDX_HIST SELECT * FROM MAIN.TMP_IDX_HIST")

    fdt.pgs_execute_query("SELECT DW.PGS_UPDATE_HIST_IDX('"+para_date_start+"')")

if __name__ == '__main__':
    main()
