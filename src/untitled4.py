# -*- coding: utf-8 -*-
"""
Created on Mon May 14 15:33:35 2018

@author: houz
"""

import os as _os
import pandas as _pd
import sqlalchemy as _sqlalchemy
import statsmodels.formula.api as _smapi

import fdmt_date as _fda
import fdmt_data as _fdt
import fdmt_query as _fdq

main_path=_os.environ["THE_PROCESS"].replace("\\","/")+"/"
data_path=main_path+"data/"

db_config=_os.environ["THE_PROCESS_DB"]
[__db_host,__db_port,__db_db,__db_user,__db_passwd]=db_config.split(";")

magic_box = _sqlalchemy.create_engine("postgresql+psycopg2://"+__db_user+":"+__db_passwd+"@"+__db_host+"/"+__db_db)


"""
#RegressionResults
http://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.RegressionResults.html
"""

query=_fdq.query("stk_hist_hs300","200","CLOSE")   


query_res=_fdt.pgs_select_query_df(query)
para_df=query_res[1]
para_df2=para_df.pivot(index='tdate', columns='id', values='amount')
para_df3=para_df2.corr(min_periods=100)

res_list_hs300=para_df3.columns.tolist()

para_list=[]

for stka in res_list_hs300:
    for stkb in res_list_hs300:
        if stka<stkb:
            cov_res=round(para_df3.loc[stka,stkb].item(),4)
            if (cov_res>0.8)|(cov_res<-0.8):
                para_list.append([stka,stkb,cov_res])

res_list_parainfo=[]

for para in para_list:
    [stka,stkb,cov]=para
    lendays="200"
    metrics="CLOSE"

    df_stk=para_df2.loc[:,[stka,stkb]]
    res = _smapi.ols(formula=stka+" ~ "+stkb, data=df_stk).fit()
    
    rsquared =res.rsquared
    [intercept,slope]=res.params.tolist()
    summary=str(res.summary())
    udate=_fda.current_date_str
    utime=_fda.current_time_str
    res_list_parainfo.append([udate,stka,stkb,metrics,cov,rsquared,intercept,slope,summary,lendays,utime])
    
res_df=_pd.DataFrame(res_list_parainfo)    
res_df.columns=["udate","stka","stkb","metrics","cov","rsquared","intercept","slope","summary","lendays","utime"]
res_df.to_sql("tmp_stk_hist_corr_info",magic_box,if_exists="append",schema="main",index=False)




    
    