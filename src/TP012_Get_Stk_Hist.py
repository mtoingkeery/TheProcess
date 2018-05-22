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

    para_date_list=fdmt_date.date_list(para_date_start,para_date_end,"MM")

    pickle_file_path=data_path+"config/idx_hs300_list.pkl"
    pickle_file=open(pickle_file_path,"rb+")
    para_res1=pickle.load(pickle_file)
    pickle_file.close()

    pickle_file_path=data_path+"config/idx_sz50_list.pkl"
    pickle_file=open(pickle_file_path,"rb+")
    para_res2=pickle.load(pickle_file)
    pickle_file.close()

    pickle_file_path=data_path+"config/idx_zz500_list.pkl"
    pickle_file=open(pickle_file_path,"rb+")
    para_res3=pickle.load(pickle_file)
    pickle_file.close()

    para_res = pd.DataFrame(columns=['id'])
    para_res=pd.concat([para_res,para_res1],ignore_index=True)
    para_res=pd.concat([para_res,para_res2],ignore_index=True)
    para_res=pd.concat([para_res,para_res3],ignore_index=True)

    para_df_res=para_res.loc[:,["id"]]

    para_df_res.drop_duplicates()
    para_df_res.reset_index(drop=True)
    para_df_res=para_df_res.sort_values(by=['id'])

    para_id_list=[x[1:] for x in para_df_res["id"].tolist()]

    target_list=[]
    except_list=[]
    log_list=[]

    for para_id in para_id_list:
        for para_mon in para_date_list:
            target_list.append([para_id,para_mon])

    for para in target_list:
        [para_id,para_mon]=para
        fdmt_tushare.get_stk_hist(para_id,para_mon,except_list,label="stk")
        time.sleep(8+4*random.random())

    if len(except_list)>0:
        print(time.strftime("%Y/%m/%d %T")+" - Retry Exception List")
        time.sleep(300)

        for para in except_list:
            [para_id,para_mon,except_dep]=para
            print(except_dep)
            fdmt_tushare.get_stk_hist(para_id,para_mon,log_list,label="stk")
            time.sleep(10+5*random.random())

    if len(log_list)>0:
        print(time.strftime("%Y/%m/%d %T")+" - Log Failed List")

        para_df=pd.DataFrame(log_list)
        para_df.columns=[["para_id","para_mon","except_dep"]]
        log_list_file=data_path+"update_log/stk_hist_failed_list_"+fdmt_date.current_date_str+".txt"
        para_df.to_csv(log_list_file,float_format='%.2f',na_rep=None,index=False,encoding='gb2312',mode="w+",header=True)

if __name__ == '__main__':
    main()