# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import psycopg2 as _cxo
import numpy as _np
import os as _os
import pandas as _pd
import time as _time
import tushare as _ts
import sqlalchemy as _sqlalchemy

import fdmt_date as _fda
import fdmt_query as _fdq

main_path=_os.environ["THE_PROCESS"].replace("\\","/")+"/"
data_path=main_path+"data/"

db_config=_os.environ["THE_PROCESS_DB"]
[__db_host,__db_port,__db_db,__db_user,__db_passwd]=db_config.split(";")

magic_box = _sqlalchemy.create_engine("postgresql+psycopg2://"+__db_user+":"+__db_passwd+"@"+__db_host+"/"+__db_db)

def update_idx_list():
    print(_time.strftime("%Y/%m/%d %T")+" - Start - IDX List")
    para_df1 = _ts.get_idx()
    para_df1["tdate"]=_fda.current_date_str
    para_df1["utime"]=_fda.current_time_str
    para_df2=para_df1.rename(columns={"code":"id"})
    para_res=para_df2[["tdate","id","name","change","open","preclose","close","high","low","volume","amount","utime"]]    
    para_res.to_sql("tmp_idx",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Index List")


def update_stk_classify():
    #industry
    print(_time.strftime("%Y/%m/%d %T")+" - Start - Industry List")
    para_df1 = _ts.get_industry_classified()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="industry"
    para_df2=para_df1.rename(columns={"code":"id","c_name":"label"})
    para_res=para_df2[["id","name","label","flag","utime"]]
    para_res.to_sql("tmp_stk_classify",magic_box,if_exists="repalce",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Industry List")

    #concept
    print(_time.strftime("%Y/%m/%d %T")+" - Start - Concept List")
    para_df1 = _ts.get_concept_classified()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="concept"
    para_df2=para_df1.rename(columns={"code":"id","c_name":"label"})
    para_res=para_df2[["id","name","label","flag","utime"]]
    para_res.to_sql("tmp_stk_classify",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Concept List")

    #area
    print(_time.strftime("%Y/%m/%d %T")+" - Start - Area List")
    para_df1 = _ts.get_area_classified()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="area"
    para_df2=para_df1.rename(columns={"code":"id","area":"label"})
    para_res=para_df2[["id","name","label","flag","utime"]]
    para_res.to_sql("tmp_stk_classify",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Area List")

def update_idx_component():
    print(_time.strftime("%Y/%m/%d %T")+" - Start - sme")
    para_df1 = _ts.get_sme_classified()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="sme"
    para_df1["weight"]=1.0
    para_df1["tdate"]=_fda.current_date_str
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="repalce",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - sme")

    print(_time.strftime("%Y/%m/%d %T")+" - Start - gem")
    para_df1 = _ts.get_gem_classified()
    para_df1["utime"]=_fda.current_time_str    #Rename
    para_df1["flag"]="gem"
    para_df1["weight"]=1.0
    para_df1["tdate"]=_fda.current_date_str
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - gem")

    print(_time.strftime("%Y/%m/%d %T")+" - Start - hs300")
    para_df1 = _ts.get_hs300s()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="hs300"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - hs300")
    
    print(_time.strftime("%Y/%m/%d %T")+" - Start - sz50")
    para_df1 = _ts.get_sz50s()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="sz50"
    para_df1["weight"]=1.0
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - sz50")

    print(_time.strftime("%Y/%m/%d %T")+" - Start - zz500")
    para_df1 = _ts.get_zz500s()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="zz500"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - zz500")

    print(_time.strftime("%Y/%m/%d %T")+" - Start - sz50")
    para_df1 = _ts.get_sz50s()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="sz50"
    para_df1["weight"]=1.0
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - sz50")
    
    print(_time.strftime("%Y/%m/%d %T")+" - Start - zz500")
    para_df1 = _ts.get_zz500s()
    para_df1["utime"]=_fda.current_time_str
    para_df1["flag"]="zz500"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})
    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_res.to_sql("tmp_idx_component",magic_box,if_exists="append",schema="dw",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - zz500")


def get_stk_list(limiter="10000"):
    list_query="""SELECT ID FROM MAIN.D_IDX_COMPONENT WHERE FLAG IN ('hs300','sz50','zz500') GROUP BY ID ORDER BY ID LIMIT """+limiter   
    tunnel_conn = _cxo.connect(host=__db_host,port=int(__db_port),user=__db_user,password=__db_passwd,database=__db_db)
    tunnel_cur = tunnel_conn.cursor()
    tunnel_cur.execute(list_query)    
    res_stk_list = tunnel_cur.fetchall()    
    tunnel_cur.close()
    tunnel_conn.close()
    res_arr=_np.array(res_stk_list)
    return res_arr[:,0].tolist()
     
def get_idx_list(limiter="100"):
    list_query="""SELECT ID FROM MAIN.D_IDX ORDER BY ID LIMIT """+limiter   
    tunnel_conn = _cxo.connect(host=__db_host,port=int(__db_port),user=__db_user,password=__db_passwd,database=__db_db)
    tunnel_cur = tunnel_conn.cursor()
    tunnel_cur.execute(list_query)    
    res_stk_list = tunnel_cur.fetchall()    
    tunnel_cur.close()
    tunnel_conn.close()
    res_arr=_np.array(res_stk_list)
    return res_arr[:,0].tolist()        

def get_stk_hist(para_id,para_mon,except_list,label="stk",mon_interval=1):
    print(_time.strftime('%Y/%m/%d %T')+" - "+para_mon+" - "+para_id)
    para_mon_till=_fda.date_add(para_mon,mon_interval,"MM",1)
    para_file=data_path+label+"_hist/"+_fda.date_format(para_mon,"yyyymm")+"_"+para_id+".txt"
    
    try:
        if label=="idx":
            para_df = _ts.get_h_data(para_id, para_mon, para_mon_till, index=True)
            print(label)
        else:
            para_df = _ts.get_h_data(para_id, para_mon, para_mon_till)            
        para_df["id"]=para_id
        para_df["tdate"]=para_df.index
        para_df["utime"]=_fda.current_time_str
        para_df2=para_df[["tdate","id","open","high","close","low","volume","amount","utime"]]
        para_df2.to_csv(para_file,float_format='%.2f',na_rep=None,index=False,encoding='gb2312',mode="w+",header=True)  

    except Exception as ErrorCode:
        except_list.append([para_id,para_mon,str(ErrorCode)])
        print(_time.strftime('%Y/%m/%d %T')+" - "+para_mon+" - "+para_id+" - Exception Occurs!")
        print("-----------------------------------------------------------------------------")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")


def pgs_select_query(para_query):
    try:
        print(_time.strftime('%Y/%m/%d %T')+" - Select Query")
        print("-----------------------------------------------------------------------------")
        print(para_query)
        print("-----------------------------------------------------------------------------")
        
        tunnel_conn = _cxo.connect(host=__db_host,port=int(__db_port),user=__db_user,password=__db_passwd,database=__db_db)
        tunnel_cur = tunnel_conn.cursor()
        tunnel_cur.execute(para_query)
        res_stk_list = tunnel_cur.fetchall()    
        tunnel_cur.close()
        tunnel_conn.close()
        
        res_arr=_np.array(res_stk_list)
        return res_arr[:,:].tolist()

    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")


def pgs_execute_query(para_query,label=0):
    try:
        print(_time.strftime('%Y/%m/%d %T')+" - Execute Query")
        print("-----------------------------------------------------------------------------")
        if label==1:
            print(para_query)
            print("-----------------------------------------------------------------------------")
        tunnel_conn = _cxo.connect(host=__db_host,port=int(__db_port),user=__db_user,password=__db_passwd,database=__db_db)
        cur = tunnel_conn.cursor()
        cur.execute(para_query)
        tunnel_conn.commit()
        cur.close()
        tunnel_conn.close()
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")

def pgs_execute_query_df(para_query,label=0):
    try:
        print(_time.strftime('%Y/%m/%d %T')+" - Execute Query DataFrame")
        print("-----------------------------------------------------------------------------")
        if label==1:
            print(para_query)
            print("-----------------------------------------------------------------------------")        

        conn = magic_box.engine.connect()
        conn.begin()
        para_df = _pd.read_sql(para_query,conn)
        conn.close()
        return [1,para_df]
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")
        return [200,'']

def pgs_update_stk_cov(lendays='60',flag='hs300',label='close'):    
    try:
        query_res="""SELECT STK.TDATE,STK.ID,STK.CLOSE AS VAL FROM DW.F_STK_HIST STK JOIN MAIN.D_IDX_COMPONENT IDX ON STK.ID=IDX.ID AND IDX.FLAG='"""+flag+"""' JOIN (SELECT TDATE FROM DW.F_IDX_HIST WHERE ID='000001' ORDER BY TDATE DESC LIMIT """+lendays+""" )DD ON STK.TDATE=DD.TDATE ORDER BY STK.TDATE,STK.ID"""
        query_idx="""SELECT ID FROM MAIN.D_IDX_COMPONENT IDX WHERE IDX.FLAG='"""+flag+"""' ORDER BY ID"""
        
        db_config=_os.environ["THE_PROCESS_DB"]
        [db_host,db_port,db_db,db_user,db_passwd]=db_config.split(";")
        magic_box = _sqlalchemy.create_engine("postgresql+psycopg2://"+db_user+":"+db_passwd+"@"+db_host+"/"+db_db)
        
        conn = magic_box.engine.connect()
        conn.begin()
        query_idx_df = _pd.read_sql(query_idx,conn)
        conn.close()    
    
        query_list_res=query_idx_df.values[:,0].tolist()
        
        para_list_mid=""
        for para in query_list_res:
            para_list_mid+="S"+para+" float8,\n"
    
        query_list_str="""\nAS \n( \nTDATE VARCHAR(10),\n"""+para_list_mid+")"
        query_list_str=query_list_str.replace(",\n)","\n)")
        
        final_query="""SELECT * FROM DW.CROSSTAB \n(\n'"""+query_res.replace("'","''")+"""',\n'"""+query_idx.replace("'","''")+"""'\n)"""+query_list_str
    
        para_df_res=pgs_execute_query_df(final_query)
        para_cov_df_res=para_df_res[1].corr(min_periods=int(int(lendays)/2))    
        
        list_index=para_cov_df_res.index.tolist()
        
        pgs_execute_query("DELETE FROM MAIN.TMP_STK_HIST_COV WHERE LENDAYS="+lendays+";")

        for para in para_cov_df_res.columns.tolist():        
            print(_time.strftime('%Y/%m/%d %T')+" - "+para)
            para_df=para_cov_df_res.loc[:,[para]]
            para_df['stkb']=para
            para_df['stka']=list_index
            para_df['lendays']=int(lendays)
            para_df['utime']=_fda.current_time_str
            para_df.columns=['cov','stkb','stka','lendays','utime']
            
            para_df2=para_df[['stka', 'stkb', 'cov','lendays','utime']].reset_index(drop=True)
            
            para_df2.to_sql("tmp_stk_hist_cov",magic_box,if_exists="append",schema="main",index=False)
        
        return [1,"Success"]
        
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")
        return [200,str(ErrorCode)]

def pgs_update_stk_cov_p2():    
    try:
        pgs_execute_query("DELETE FROM MAIN.F_STK_HIST_COV WHERE REPORT_DATE=CURRENT_DATE;")
        query_stk_hist_cov=_fdq.query("stk_hist_cov")
        pgs_execute_query(query_stk_hist_cov)        
        
        return [1,"Success"]
        
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")
        return [200,str(ErrorCode)]

#pgs_update_stk_cov(lendays='60',flag='hs300',label='close')
pgs_update_stk_cov_p2()
