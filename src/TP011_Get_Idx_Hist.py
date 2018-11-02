# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import time,random
import pandas as pd
import fdmt_date
import fdmt_data
import fdmt_tushare
import pickle

def main():
    data_path=fdmt_data.data_path
    
    para_date_start=fdmt_date.current_date_str
    para_date_end=fdmt_date.current_date_str
    
    if fdmt_date.current_date_str>=fdmt_date.date_add(fdmt_date.current_month_str,5):
        para_date_start=fdmt_date.current_month_str
        para_date_end=fdmt_date.date_add(fdmt_date.current_month_str,1,"MM")
    else:
        para_date_start=fdmt_date.date_add(fdmt_date.current_month_str,-1,"MM")
        para_date_end=fdmt_date.date_add(fdmt_date.current_month_str,1,"MM")

    para_date_start='2018-07-01'
    para_date_end='2018-11-01'

    para_date_list=fdmt_date.date_list(para_date_start,para_date_end,"MM")

    pickle_file_path=data_path+"config/idx.pkl"
    pickle_file=open(pickle_file_path,"rb+")
    para_res=pickle.load(pickle_file)
    pickle_file.close()

    para_id_list=[x[1:] for x in para_res["id"].tolist()]

    print(para_id_list)

    target_list=[]
    except_list=[]
    log_list=[]

    for para_id in para_id_list:
        for para_mon in para_date_list:
            target_list.append([para_id,para_mon])
    
    for para in target_list:
        [para_id,para_mon]=para
        fdmt_tushare.get_stk_hist(para_id,para_mon,except_list,label="idx")
        time.sleep(8+4*random.random())
    
    if len(except_list)>0:
        print(time.strftime("%Y/%m/%d %T")+" - Retry Exception List")
        time.sleep(300)
        
        for para in except_list:
            [para_id,para_mon,except_dep]=para
            print(except_dep)
            fdmt_tushare.get_stk_hist(para_id,para_mon,log_list,label="idx")
            time.sleep(10+5*random.random())
    
    if len(log_list)>0:
        print(time.strftime("%Y/%m/%d %T")+" - Log Failed List")
        
        para_df=pd.DataFrame(log_list)
        para_df.columns=[["para_id","para_mon","except_dep"]]
        log_list_file=data_path+"update_log/idx_hist_failed_list_"+fdmt_date.current_date_str+".txt"
        para_df.to_csv(log_list_file,float_format='%.2f',na_rep=None,index=False,encoding='gb2312',mode="w+",header=True)  

if __name__ == '__main__':
    main()    

