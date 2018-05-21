# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import fdmt_date as _fdmt_date
import fdmt_data as _fdmt_data
import fdmt_query as _fdmt_query
import fdmt_procedure as _fdmt_procedure

import pandas as _pd
import pickle as _pickle
import time as _time
import tushare as _ts

__magic_box=_fdmt_data.magic_box
__data_path=_fdmt_data.data_path

def update_idx_list(label=0):
    #index list
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - IDX List")
    para_df1 = _ts.get_index()
    para_df1["tdate"]=_fdmt_date.current_date_str
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df2=para_df1.rename(columns={"code":"id"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["X"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["tdate","id","name","utime"]]

    pickle_file_path=__data_path+"config/idx.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_idx",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Index List")


def update_stk_classify(label=0):
    #industry
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - Industry List")
    para_df1 = _ts.get_industry_classified()
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df1["flag"]="industry"
    para_df2=para_df1.rename(columns={"code":"id","c_name":"label"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["id","name","label","flag","utime"]]

    pickle_file_path=__data_path+"config/stk_industry_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_stk_classify",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Industry List")

    #concept
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - Concept List")
    para_df1 = _ts.get_concept_classified()
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df1["flag"]="concept"
    para_df2=para_df1.rename(columns={"code":"id","c_name":"label"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["id","name","label","flag","utime"]]

    pickle_file_path=__data_path+"config/stk_concept_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_stk_classify",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Concept List")

    #area
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - Area List")
    para_df1 = _ts.get_area_classified()
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df1["flag"]="area"
    para_df2=para_df1.rename(columns={"code":"id","area":"label"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["id","name","label","flag","utime"]]

    pickle_file_path=__data_path+"config/stk_area_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_stk_classify",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - Area List")


def update_idx_component(label=0):
    #sme
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - sme")
    para_df_total = _pd.DataFrame(columns=['id'])

    para_df1 = _ts.get_sme_classified()
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df1["flag"]="sme"
    para_df1["weight"]=1.0
    para_df1["tdate"]=_fdmt_date.current_date_str
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_df_total=_pd.concat([para_df_total,para_res],ignore_index=True)

    pickle_file_path=__data_path+"config/idx_sme_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_idx_component",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - sme")

    #gem
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - gem")
    para_df1 = _ts.get_gem_classified()
    para_df1["utime"]=_fdmt_date.current_time_str    #Rename
    para_df1["flag"]="gem"
    para_df1["weight"]=1.0
    para_df1["tdate"]=_fdmt_date.current_date_str
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_df_total=_pd.concat([para_df_total,para_res],ignore_index=True)

    pickle_file_path=__data_path+"config/idx_gem_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_idx_component",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - gem")

    #hs300
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - hs300")
    para_df1 = _ts.get_hs300s()
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df1["flag"]="hs300"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_df_total=_pd.concat([para_df_total,para_res],ignore_index=True)

    pickle_file_path=__data_path+"config/idx_hs300_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_idx_component",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - hs300")

    #sz50
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - sz50")
    para_df1 = _ts.get_sz50s()
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df1["flag"]="sz50"
    para_df1["weight"]=1.0
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_df_total=_pd.concat([para_df_total,para_res],ignore_index=True)

    pickle_file_path=__data_path+"config/idx_sz50_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_idx_component",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - sz50")

    #zz500
    ####################################################################
    print(_time.strftime("%Y/%m/%d %T")+" - Start - zz500")
    para_df1 = _ts.get_zz500s()
    para_df1["utime"]=_fdmt_date.current_time_str
    para_df1["flag"]="zz500"
    para_df2=para_df1.rename(columns={"date":"tdate","code":"id"})

    para_id_list=para_df2["id"].values.tolist()
    para_id_list2=["S"+x for x in para_id_list]
    para_df2["id"]=para_id_list2

    para_res=para_df2[["tdate","id","name","weight","flag","utime"]]
    para_df_total=_pd.concat([para_df_total,para_res],ignore_index=True)

    pickle_file_path=__data_path+"config/idx_zz500_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_res,pickle_file)
    pickle_file.close()

    if label==1:
        print(_time.strftime("%Y/%m/%d %T")+" - Insert Into Database")
        para_res.to_sql("tmp_idx_component",__magic_box,if_exists="replace",schema="main",index=False)
    print(_time.strftime("%Y/%m/%d %T")+" - End - zz500")

    para_df_total.drop_duplicates()
    para_df_total=para_df_total.sort_values(by=['id'])
    para_df_total.reset_index(drop=True)

    pickle_file_path=__data_path+"config/idx_component_list.pkl"
    pickle_file=open(pickle_file_path,"wb+")
    _pickle.dump(para_df_total,pickle_file)
    pickle_file.close()

def get_stk_hist(para_id,para_mon,except_list,label="stk",mon_interval=1):
    print(_time.strftime('%Y/%m/%d %T')+" - "+para_mon+" - "+para_id)
    para_mon_till=_fdmt_date.date_add(para_mon,mon_interval,"MM",1)
    para_file=__data_path+label+"_hist/"+_fdmt_date.date_format(para_mon,"yyyymm")+"_"+para_id+".txt"
    
    try:
        if label=="idx":
            para_df = _ts.get_h_data(para_id, para_mon, para_mon_till, index=True)
            para_df["id"]="X"+para_id
        else:
            para_df = _ts.get_h_data(para_id, para_mon, para_mon_till)            
            para_df["id"]="S"+para_id
        para_df["tdate"]=para_df.index
        para_df["utime"]=_fdmt_date.current_time_str
        para_df2=para_df[["tdate","id","open","high","close","low","volume","amount","utime"]]
        para_df2.to_csv(para_file,float_format='%.2f',na_rep=None,index=False,encoding='gb2312',mode="w+",header=True)  

    except Exception as ErrorCode:
        except_list.append([para_id,para_mon,str(ErrorCode)])
        print(_time.strftime('%Y/%m/%d %T')+" - "+para_mon+" - "+para_id+" - Exception Occurs!")
        print("-----------------------------------------------------------------------------")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")

def main():

    #Update Date
    ####################################################################
    update_idx_list()
    update_stk_classify()
    update_idx_component()

    """
    #Run Procedure
    ####################################################################
    para_pre=_fdmt_procedure.procedure(flag="basic_idx_stk")
    _fdmt_data.pgs_execute_procedure(para_pre)

    #Check Data
    ####################################################################
    para_query=_fdmt_query.query(flag="basic_idx_stk")
    para_res=_fdmt_data.pgs_select_query(para_query)

    if para_res[0][0]==1:
        print(_time.strftime('%Y/%m/%d %T')+" - ",para_res)
        print(_time.strftime('%Y/%m/%d %T')+" - Successfully!!!")
    else:
        print(_time.strftime('%Y/%m/%d %T')+" - ",para_res)
        print(_time.strftime('%Y/%m/%d %T')+" - Basic Index & Stock Errors!!!")
    """

if __name__ == '__main__':
    main()

