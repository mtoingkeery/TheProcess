# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import time,os
import tushare as ts
import pandas as pd
import numpy as np
from sqlalchemy import create_engine as creg
import fdmt_date as fd
import psycopg2 as cxo

import fdmt_date as fda
import fdmt_query as fdq


main_path=os.environ["THE_PROCESS"].replace("\\","/")+"/"
data_path=main_path+"data/"

db_config=os.environ["THE_PROCESS_DB"]
[db_host,db_port,db_db,db_user,db_passwd]=db_config.split(";")

magic_box = creg("postgresql+psycopg2://"+db_user+":"+db_passwd+"@"+db_host+"/"+db_db)

def update_idx_list():
    print(time.strftime("%Y/%m/%d %T")+" - Start - IDX List")
    para_df1 = ts.get_idx()
    para_df1["tdate"]=fd.current_date_str
    para_df1["utime"]=fd.current_time_str
    para_df2=para_df1.rename(columns={"code":"id"})
    para_res=para_df2[["tdate","id","name","change","open","preclose","close","high","low","volume","amount","utime"]]    
    para_res.to_sql("tmp_idx",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - Index List")


def update_stk_classify():
    #industry
    print(time.strftime("%Y/%m/%d %T")+" - Start - Industry List")
    para_df1 = ts.get_industry_classified()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="industry"
    para_df2=para_df1.rename(columns={"code":"id","c_name":"label"})
    para_res=para_df2[["id","name","label","flag","utime"]]
    para_res.to_sql("tmp_stk_classify",magic_box,if_exists="repalce",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - Industry List")

    #concept
    print(time.strftime("%Y/%m/%d %T")+" - Start - Concept List")
    para_df1 = ts.get_concept_classified()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="concept"
    para_df2=para_df1.rename(columns={"code":"id","c_name":"label"})
    para_res=para_df2[["id","name","label","flag","utime"]]
    para_res.to_sql("tmp_stk_classify",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - Concept List")

    #area
    print(time.strftime("%Y/%m/%d %T")+" - Start - Area List")
    para_df1 = ts.get_area_classified()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="area"
    para_df2=para_df1.rename(columns={"code":"id","area":"label"})
    para_res=para_df2[["id","name","label","flag","utime"]]
    para_res.to_sql("tmp_stk_classify",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - Area List")

def update_idx_component():
    print(time.strftime("%Y/%m/%d %T")+" - Start - sme")
    para_df1 = ts.get_sme_classified()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="sme"
    para_df1["weight"]=1.0
    para_df1["tdate"]=fd.current_date_str
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="repalce",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - sme")

    print(time.strftime("%Y/%m/%d %T")+" - Start - gem")
    para_df1 = ts.get_gem_classified()
    para_df1["utime"]=fd.current_time_str    #Rename
    para_df1["flag"]="gem"
    para_df1["weight"]=1.0
    para_df1["tdate"]=fd.current_date_str
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - gem")

    print(time.strftime("%Y/%m/%d %T")+" - Start - hs300")
    para_df1 = ts.get_hs300s()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="hs300"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - hs300")
    
    print(time.strftime("%Y/%m/%d %T")+" - Start - sz50")
    para_df1 = ts.get_sz50s()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="sz50"
    para_df1["weight"]=1.0
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - sz50")

    print(time.strftime("%Y/%m/%d %T")+" - Start - zz500")
    para_df1 = ts.get_zz500s()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="zz500"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - zz500")

    print(time.strftime("%Y/%m/%d %T")+" - Start - sz50")
    para_df1 = ts.get_sz50s()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="sz50"
    para_df1["weight"]=1.0
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - sz50")
    
    print(time.strftime("%Y/%m/%d %T")+" - Start - zz500")
    para_df1 = ts.get_zz500s()
    para_df1["utime"]=fd.current_time_str
    para_df1["flag"]="zz500"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(time.strftime("%Y/%m/%d %T")+" - End - zz500")


def get_stk_list(limiter="10000"):
    list_query="""SELECT ID FROM MAIN.D_IDX_COMPONENT WHERE FLAG IN ('hs300','sz50','zz500') GROUP BY ID ORDER BY ID LIMIT """+limiter   
    tunnel_conn = cxo.connect(host=db_host,port=int(db_port),user=db_user,password=db_passwd,database=db_db)
    tunnel_cur = tunnel_conn.cursor()
    tunnel_cur.execute(list_query)    
    res_stk_list = tunnel_cur.fetchall()    
    tunnel_cur.close()
    tunnel_conn.close()
    res_arr=np.array(res_stk_list)
    return res_arr[:,0].tolist()
     
def get_idx_list(limiter="100"):
    list_query="""SELECT ID FROM MAIN.D_IDX ORDER BY ID LIMIT """+limiter   
    tunnel_conn = cxo.connect(host=db_host,port=int(db_port),user=db_user,password=db_passwd,database=db_db)
    tunnel_cur = tunnel_conn.cursor()
    tunnel_cur.execute(list_query)    
    res_stk_list = tunnel_cur.fetchall()    
    tunnel_cur.close()
    tunnel_conn.close()
    res_arr=np.array(res_stk_list)
    return res_arr[:,0].tolist()        

def get_stk_hist(para_id,para_mon,except_list,label="stk",mon_interval=1):
    print(time.strftime('%Y/%m/%d %T')+" - "+para_mon+" - "+para_id)
    para_mon_till=fd.date_add(para_mon,mon_interval,"MM",1)
    para_file=data_path+label+"_hist/"+fd.date_format(para_mon,"yyyymm")+"_"+para_id+".txt"
    
    try:
        if label=="idx":
            para_df = ts.get_h_data(para_id, para_mon, para_mon_till, index=True)
            print(label)
        else:
            para_df = ts.get_h_data(para_id, para_mon, para_mon_till)            
        para_df["id"]=para_id
        para_df["tdate"]=para_df.index
        para_df["utime"]=fd.current_time_str
        para_df2=para_df[["tdate","id","open","high","close","low","volume","amount","utime"]]
        para_df2.to_csv(para_file,float_format='%.2f',na_rep=None,index=False,encoding='gb2312',mode="w+",header=True)  

    except Exception as ErrorCode:
        except_list.append([para_id,para_mon,str(ErrorCode)])
        print(time.strftime('%Y/%m/%d %T')+" - "+para_mon+" - "+para_id+" - Exception Occurs!")
        print("-----------------------------------------------------------------------------")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")


def pgs_select_query(para_query):
    try:
        print(time.strftime('%Y/%m/%d %T')+" - Select Query")
        print("-----------------------------------------------------------------------------")
        print(para_query)
        print("-----------------------------------------------------------------------------")
        
        tunnel_conn = cxo.connect(host=db_host,port=int(db_port),user=db_user,password=db_passwd,database=db_db)
        tunnel_cur = tunnel_conn.cursor()
        tunnel_cur.execute(para_query)
        res_stk_list = tunnel_cur.fetchall()    
        tunnel_cur.close()
        tunnel_conn.close()
        
        res_arr=np.array(res_stk_list)
        return res_arr[:,:].tolist()

    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")


def pgs_execute_query(para_query):
    try:
        print(time.strftime('%Y/%m/%d %T')+" - Execute Query")
        print("-----------------------------------------------------------------------------")
        print(para_query)
        print("-----------------------------------------------------------------------------")
        tunnel_conn = cxo.connect(host=db_host,port=int(db_port),user=db_user,password=db_passwd,database=db_db)
        cur = tunnel_conn.cursor()
        cur.execute(para_query)
        tunnel_conn.commit()
        cur.close()
        tunnel_conn.close()
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")

def pgs_update_stk_cov(cov_days_len='20',cov_para_count='10',label=0):
    print(time.strftime('%Y/%m/%d %T')+" - Update Stk Cov")
    try:
        res_list=[]
        
        id_com_list_query=fdq.query('hs300_com',cov_para_count)
        id_com_list_res=pgs_select_query(id_com_list_query)
        
        conn = magic_box.engine.connect()
        conn.begin()
        
        for para in id_com_list_res:                        
            [pa_id,pb_id]=para
            com_hist_query=fdq.query('hs300_cov','100000000',cov_days_len,pa_id,pb_id)    
            
            df = pd.read_sql(com_hist_query,conn)
            
            df_pa_close=df.iloc[:,5]
            df_pb_close=df.iloc[:,6]
            
            df_pa_amount=df.iloc[:,7]
            df_pb_amount=df.iloc[:,8]
            
            cov_len=len(df_pa_close)
            
            cov_close=df_pa_close.corr(df_pb_close)
            cov_amount=df_pa_amount.corr(df_pb_amount)
            
            cdate=fda.current_date_str
            utime=fda.current_time_str
            
            para_res=[cdate,cov_days_len,pa_id,pb_id,cov_len,cov_close,cov_amount,utime]
            res_list.append(para_res)
            
            if label==1:
                print(time.strftime('%Y/%m/%d %T')+" - ",pa_id,pb_id)
            
        conn.close()
        
        res_df=pd.DataFrame(res_list, columns=['cdate','cov_days_len', 'pa_id', 'pb_id', 'cov_len', 'cov_close', 'cov_amount', 'utime'])    
        pgs_execute_query("truncate table main.tmp_stk_cov")    
        res_df.to_sql("tmp_stk_cov",magic_box,if_exists="append",schema="main",index=False)
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")
