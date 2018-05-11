# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:16:13 2018

@author: houz
"""


import fdmt_data as fdt
import pandas as pd
import fdmt_query as fdq


pa_id='000001'
pb_id='000002'

[db_host,db_port,db_db,db_user,db_passwd]=fdt.db_config.split(";")
id_com_list_query=fdq.query('hs300_cov','20',pa_id,pb_id)

