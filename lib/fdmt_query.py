# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

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
        
    return para_query

def sp_json(flag="access_token",label1="",label2="",label3="",label4="",label5="",label6=""):
    #print(time.strftime('%Y/%m/%d %T')+" - Special Json")   

    para_query=""

    #Access Token Json
    if flag=="access_token":
        para_query='''
            {
            	"Agentid":"'''+label1+'''",
            	"AccessToken":"'''+label2+'''",
            	"UpdateTime":"'''+label3+'''",
            	"ExpireTime":"'''+label4+'''"
            }'''    
                
    return para_query
    
    
    
    
    
    
    
    
    
    
    
    
