# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import psycopg2 as _cxo
import numpy as _np
import os as _os
import pandas as _pd
import pickle as _pickle
import time as _time
import tushare as _ts
import sqlalchemy as _sqlalchemy

import fdmt_date as _fdmt_date
import fdmt_query as _fdmt_query

main_path=_os.environ["THE_PROCESS"].replace("\\","/")+"/"
data_path=main_path+"data/"

db_config=_os.environ["THE_PROCESS_DB"]
[__db_host,__db_port,__db_db,__db_user,__db_passwd]=db_config.split(";")

magic_box = _sqlalchemy.create_engine("mysql+pymysql://"+__db_user+":"+__db_passwd+"@"+__db_host+"/"+__db_db)

def pgs_select_query(para_query,label=0):
    try:
        print(_time.strftime('%Y/%m/%d %T')+" - Select Query")
        print("-----------------------------------------------------------------------------")
        if label==1:
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

def pgs_select_query_df(para_query,label=0):
    try:
        print(_time.strftime('%Y/%m/%d %T')+" - Select Query DataFrame")
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

def pgs_execute_procedure(para_procedure,label=0):
    try:
        print(_time.strftime('%Y/%m/%d %T')+" - Execute Query")
        print("-----------------------------------------------------------------------------")

        tunnel_conn = _cxo.connect(host=__db_host,port=int(__db_port),user=__db_user,password=__db_passwd,database=__db_db)
        cur = tunnel_conn.cursor()
        for para_query in para_procedure:
            cur.execute(para_query)
            if label==1:
                print(para_query)
                print("-----------------------------------------------------------------------------")
        tunnel_conn.commit()
        cur.close()
        tunnel_conn.close()
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")

def pgs_df_to_db(para_df,table_name,chunksize=1000):
    #Specific Func & Need to create table manually & Always truncate the target table
    pgs_execute_query("TRUNCATE TABLE "+table_name+";")

    #Setup Connection
    tunnel_conn = _cxo.connect(host=__db_host,port=int(__db_port),user=__db_user,password=__db_passwd,database=__db_db)
    tunnel_cur = tunnel_conn.cursor()

    #Execute Many
    para_str1="""INSERT INTO """+table_name+""" VALUES("""
    para_str2="%s,"*para_df.columns.size

    para_query=para_str1+para_str2[:-1]+")"
    para_list = _np.array(para_df).tolist()
    tunnel_cur.executemany(para_query, para_list)

    tunnel_conn.commit()

    #Close Connection
    tunnel_cur.close()
    tunnel_conn.close()

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
            para_df['utime']=_fdmt_date.current_time_str
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
        query_stk_hist_cov=_fdmt_query.query("stk_hist_cov")
        pgs_execute_query(query_stk_hist_cov)        
        
        return [1,"Success"]
        
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")
        return [200,str(ErrorCode)]

def load_idx_df(flag="hs300"):
    if flag in ["hs300","sme","gem","sz50","zz500","component"]:
        para_file_path=data_path+"config/idx_"+flag+"_list.pkl"
        para_file=open(para_file_path,"rb+")
        para_df=_pickle.load(para_file)
        para_file.close()
    elif flag in ["industry","concept","area"]:
        para_file_path=data_path+"config/stk_"+flag+"_list.pkl"
        para_file=open(para_file_path,"rb+")
        para_df=_pickle.load(para_file)
        para_file.close()
    elif flag in ["idx"]:
        para_file_path=data_path+"config/idx.pkl"
        para_file=open(para_file_path,"rb+")
        para_df=_pickle.load(para_file)
        para_file.close()

    para_df = para_df.sort_values("id")
    para_df = para_df.reset_index(drop=True)

    return para_df

def load_hist_df(flag="idx"):

    stk_path=data_path+"stk_pkl/"
    idx_path=data_path+"idx_pkl/"

    if flag=="idx":
        target_path=idx_path
    else:
        target_path=stk_path

    df_res=_pd.DataFrame()
    for (dirpath, dirname, filenames) in _os.walk(target_path):
        for filename in filenames:
            para_filename=dirpath+filename

            try:
                para_file=open(para_filename,"rb+")
                para_df=_pickle.load(para_file)
            except Exception as e:
                print(str(e))
            finally:
                para_file.close()

            df_res=_pd.concat([df_res,para_df],ignore_index=True,sort=True)
    return df_res
