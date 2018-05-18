# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import os as _os
import pandas as _pd
import sqlalchemy as _sqlalchemy
import time as _time

def procedure(flag="basic_idx_stk",limit="300",label1="",label2="",label3="",label4="",label5=""):
    #print(time.strftime('%Y/%m/%d %T')+" - Procedure")

    para_query=[]
    #Basic Index & Stock Info
    if flag=="basic_idx_stk":
        para_query=["""
        INSERT INTO MAIN.F_IDX
        SELECT * FROM MAIN.TMP_IDX;""",
        """
        INSERT INTO MAIN.F_IDX_COMPONENT
        SELECT * FROM MAIN.TMP_IDX_COMPONENT;""",
        """
        INSERT INTO MAIN.F_STK_CLASSIFY
        SELECT * FROM MAIN.TMP_STK_CLASSIFY;""",
        """
        TRUNCATE TABLE DW.D_IDX;""",
        """
        TRUNCATE TABLE DW.D_IDX_COMPONENT;""",
        """
        TRUNCATE TABLE DW.D_STK_CLASSIFY;""",
        """
        INSERT INTO DW.D_IDX
        SELECT ID,NAME,CURRENT_TIMESTAMP AS UTIME FROM MAIN.TMP_IDX
        GROUP BY ID,NAME ORDER BY ID;""",
        """
        INSERT INTO DW.D_IDX_COMPONENT
        SELECT ID,NAME,WEIGHT,FLAG,CURRENT_TIMESTAMP AS UTIME FROM MAIN.TMP_IDX_COMPONENT
        GROUP BY ID,NAME,WEIGHT,FLAG
        ORDER BY FLAG,ID;""",
        """
        INSERT INTO DW.D_STK_CLASSIFY
        SELECT ID,NAME,LABEL,FLAG,CURRENT_TIMESTAMP AS UTIME FROM MAIN.TMP_STK_CLASSIFY
        GROUP BY ID,NAME,LABEL,FLAG
        ORDER BY FLAG,ID;""",
        """
        TRUNCATE TABLE MAIN.TMP_IDX;""",
        """
        TRUNCATE TABLE MAIN.TMP_IDX_COMPONENT;""",
        """
        TRUNCATE TABLE MAIN.TMP_STK_CLASSIFY;"""]

    return para_query