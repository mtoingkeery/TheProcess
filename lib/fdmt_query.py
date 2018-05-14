# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import os as _os
import pandas as _pd
import sqlalchemy as _sqlalchemy
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

    #HS300 ID Combinations
    elif flag=="hs300_com":
        para_query="""
        SELECT
           PA.ID AS PA_ID,
           PB.ID AS PB_ID
        FROM
           ( SELECT ID FROM MAIN.D_IDX_COMPONENT WHERE FLAG='hs300'
           )PA
        LEFT JOIN
           ( SELECT ID FROM MAIN.D_IDX_COMPONENT WHERE FLAG='hs300'
           )PB
        ON
           PA.ID<PB.ID
        ORDER BY
           PA.ID,
           PB.ID
        LIMIT """+limit+"""
        """

    #HS300 ID Combinations Hist
    elif flag=='hs300_cov':
        para_query="""
        SELECT
           DD.TDATE          AS TDATE,
           DD.IDX_CLOSE      AS IDX_CLOSE,
           DD.IDX_AMOUNT     AS IDX_AMOUNT,
           HIST_A.ID         AS PA_ID,
           HIST_B.ID         AS PB_ID,
           HIST_A.CLOSE      AS PA_CLOSE,
           HIST_B.CLOSE      AS PB_CLOSE,
           HIST_A.AMOUNT     AS PA_AMOUNT,
           HIST_B.AMOUNT     AS PB_AMOUNT
           --CURRENT_TIMESTAMP AS UPDATE_TIME
        FROM
           (SELECT
              TDATE                                                AS TDATE,
              CLOSE                                                AS IDX_CLOSE,
              AMOUNT                                               AS IDX_AMOUNT,
              ROW_NUMBER()OVER(PARTITION BY 1 ORDER BY TDATE DESC) AS RNK
           FROM
              DW.F_IDX_HIST
           WHERE
              ID='000300'
           )DD
        JOIN DW.F_STK_HIST HIST_A
        ON
           DD.TDATE     =HIST_A.TDATE
           AND HIST_A.ID='"""+label2+"""'
        JOIN DW.F_STK_HIST HIST_B
        ON
           DD.TDATE      =HIST_B.TDATE
           AND HIST_B.ID='"""+label3+"""'
        WHERE
           DD.RNK<="""+label1+"""
        ORDER BY
           HIST_A.ID,
           HIST_B.ID,
           DD.TDATE
        LIMIT """+limit+"""
        """         
    
    elif flag=="stk_hist_cov":
        para_query="""
        INSERT INTO MAIN.F_STK_HIST_COV
        SELECT
           CURRENT_DATE AS REPORT_DATE,
           HIST.STKA    AS STKA_ID,
           IDXA.NAME    AS STKA_NAME,
           HIST.STKB    AS STKB_ID,
           IDXB.NAME    AS STKB_NAME,
           HIST.COV     AS HIST_COV,
           HIST.LENDAYS AS LENDAYS,
           HIST.UTIME   AS UTIME
        FROM
           (SELECT
              SUBSTRING(STKA,2) AS STKA,
              SUBSTRING(STKB,2) AS STKB,
              COV               AS COV,
              LENDAYS           AS LENDAYS,
              UTIME             AS UTIME
           FROM
              MAIN.TMP_STK_HIST_COV STK
           WHERE
              STKA<STKB
              AND COV IS NOT NULL
           ORDER BY
              LENDAYS,
              STKA,
              STKB
           )HIST
        LEFT JOIN
           (SELECT
              ID,
              NAME,
              ROW_NUMBER() OVER(PARTITION BY ID ORDER BY 1) RN
           FROM
              MAIN.D_IDX_COMPONENT
           )IDXA
        ON
           IDXA.RN    =1
           AND IDXA.ID=HIST.STKA
        LEFT JOIN
           (SELECT
              ID,
              NAME,
              ROW_NUMBER() OVER(PARTITION BY ID ORDER BY 1) RN
           FROM
              MAIN.D_IDX_COMPONENT
           )IDXB
        ON
           IDXB.RN    =1
           AND IDXB.ID=HIST.STKB
        ORDER BY
           HIST.LENDAYS,
           HIST.STKA,
           HIST.STKB"""        
        
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
   

    
