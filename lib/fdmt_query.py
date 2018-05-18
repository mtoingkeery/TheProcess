# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import time as _time


def query(flag="hs300",limit="300",label1="",label2="",label3="",label4="",label5=""):
    #print(time.strftime('%Y/%m/%d %T')+" - Special Query")    
    para_query=""
    #HS300 ID List
    if flag=="hs300":
        para_query="""
        SELECT ID FROM MAIN.D_IDX_COMPONENT WHERE FLAG='hs300' ORDER BY ID
        LIMIT """+limit+"""
        """

    #All Idx
    elif flag=="all_idx":
        para_query="""
        SELECT ID FROM MAIN.D_IDX ORDER BY ID
        LIMIT """+limit+"""
        """

    #All Stk in 
    elif flag=="all_stk":
        para_query="""
        SELECT ID FROM MAIN.D_IDX_COMPONENT WHERE FLAG IN ('hs300','sz50','zz500') GROUP BY ID ORDER BY ID
        LIMIT """+limit+"""
        """

    elif flag=="stk_hist_hs300":
        para_query="""
        SELECT
           HIST.TDATE   AS TDATE,
           'S'||HIST.ID AS ID,
           IDX.SNAME    AS SNAME,
           HIST.AMOUNT  AS AMOUNT
        FROM
           (SELECT
              TDATE           AS TDATE,
              ID              AS ID,
              """+label1+"""  AS AMOUNT
           FROM
              DW.F_STK_HIST
           )HIST
        JOIN
           (SELECT
                TDATE
           FROM DW.F_IDX_HIST IDX
           WHERE IDX.ID='000009'
           ORDER BY TDATE DESC
           LIMIT """+limit+"""
           )DD
        ON
           HIST.TDATE=DD.TDATE   
        JOIN
           (SELECT
              ID    AS ID,
              NAME  AS SNAME
           FROM
              MAIN.D_IDX_COMPONENT
           WHERE
              FLAG='hs300'
           )IDX
        ON
           HIST.ID=IDX.ID
        ORDER BY
           HIST.ID,
           HIST.TDATE"""

    elif flag=="basic_idx_stk":
        para_query="""
        SELECT
           CASE
              WHEN CA  >10
                 AND CB>1000
                 AND CC>10000 THEN 1
              ELSE 0
           END AS LABEL,
           CA  AS IDX,
           CB  AS IDX_COMPONENT,
           CC  AS STK_CLASSIFY
        FROM
           ( SELECT COUNT(1) AS CA FROM DW.D_IDX
           )CA,
           ( SELECT COUNT(1) AS CB FROM DW.D_IDX_COMPONENT
           )CB,
           ( SELECT COUNT(1) AS CC FROM DW.D_STK_CLASSIFY
           )CC;"""

    return para_query.replace("  "," ")

def json(flag="wechat_access_token",label1="",label2="",label3="",label4="",label5="",label6=""):
    #print(time.strftime('%Y/%m/%d %T')+" - Special Json")   
    para_query=""
    #Access Token Json
    if flag=="wechat_access_token":
        para_query='''
            {
            	"Agentid":"'''+label1+'''",
            	"AccessToken":"'''+label2+'''",
            	"UpdateTime":"'''+label3+'''",
            	"ExpireTime":"'''+label4+'''"
            }'''    

    #Header
    elif flag=="header":
        para_query='''{
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
            }'''    

    #Post Data Send Message
    elif flag=="post_data_send_message":
        para_query='''{
               "touser" : "'''+label1+'''",
               "msgtype" : "text",
               "agentid" : '''+label2+''',
               "text" : {
                   "content" : "'''+label3+'''"
                   },
               "safe":0
           }'''    
                
    #Post Data Send Pictures
    elif flag=="post_data_send_pictures":
        para_query='''{
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
            }'''    
                
    return para_query.replace("  ","")
   
