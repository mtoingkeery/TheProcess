# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 06:19:07 2018

@author: houz
"""

import os,time
import pandas as pd
import pickle
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

    #para_date_start='2014-01-01'
    #para_date_end='2018-06-01'

    para_list=fdmt_date.date_list(para_date_start,para_date_end,"MM")

    for para_mon in para_list:
        para_mon=fdmt_date.date_format(para_mon,"yyyymm")
        print(time.strftime("%Y/%m/%d %T")+" - "+para_mon)

        hist_list=[]
        for parent,dirnames,filenames in os.walk(data_path+"idx_hist/"):
            for filename in filenames:
                if (filename[-4:].lower()=='.txt')&(para_mon in filename):
                    hist_list.append(parent+filename)

        para_df_res = pd.DataFrame(columns=['id'])

        for para in hist_list:
            para_df1=pd.read_csv(para,dtype={'id':str})
            para_df2=para_df1.rename(columns={"utime":"dtime"})
            para_df2["utime"]=time.strftime("%Y/%m/%d %T")

            para_df_res=pd.concat([para_df_res,para_df2],ignore_index=True)
            para_df_res=para_df_res.sort_values(by=['id','tdate'])
            para_df_res.reset_index(drop=True)

            para_df_res=para_df_res[["tdate","id","open","high","close","low","volume","amount","dtime","utime"]]


        pickle_file_path=data_path+"idx_pkl/idx_"+para_mon+".pkl"
        pickle_file=open(pickle_file_path,"wb+")

        if para_df_res.__len__()>0:
            pickle.dump(para_df_res,pickle_file)

        pickle_file.close()

if __name__ == '__main__':
    main()
