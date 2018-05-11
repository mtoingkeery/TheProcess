# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import time,random
import pandas as pd
import fdmt_date as fda
import fdmt_data as fdt


def main():
    data_path=fdt.data_path

    para_date_start=fda.current_date_str
    para_date_end=fda.current_date_str

    if fda.current_date_str>=fda.date_add(fda.current_month_str,5):
        para_date_start=fda.current_month_str
        para_date_end=fda.date_add(fda.current_month_str,1,"MM")
    else:
        para_date_start=fda.date_add(fda.current_month_str,-1,"MM")
        para_date_end=fda.date_add(fda.current_month_str,1,"MM")

    para_date_list=fda.date_list(para_date_start,para_date_end,"MM")
    para_id_list=fdt.get_stk_list()

    target_list=[]
    except_list=[]
    log_list=[]

    for para_id in para_id_list:
        for para_mon in para_date_list:
            target_list.append([para_id,para_mon])

    for para in target_list:
        [para_id,para_mon]=para
        fdt.get_stk_hist(para_id,para_mon,except_list,label="stk")
        time.sleep(8+4*random.random())

    if len(except_list)>0:
        print(time.strftime("%Y/%m/%d %T")+" - Retry Exception List")
        time.sleep(300)

        for para in except_list:
            [para_id,para_mon,except_dep]=para
            print(except_dep)
            fdt.get_stk_hist(para_id,para_mon,log_list,label="stk")
            time.sleep(10+5*random.random())

    if len(log_list)>0:
        print(time.strftime("%Y/%m/%d %T")+" - Log Failed List")

        para_df=pd.DataFrame(log_list)
        para_df.columns=[["para_id","para_mon","except_dep"]]
        log_list_file=data_path+"update_log/stk_hist_failed_list_"+fda.current_date_str+".txt"
        para_df.to_csv(log_list_file,float_format='%.2f',na_rep=None,index=False,encoding='gb2312',mode="w+",header=True)

if __name__ == '__main__':
    main()
