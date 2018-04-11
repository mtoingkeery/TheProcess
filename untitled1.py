# -*- coding: utf-8 -*-
""" 
Created on Fri Apr  6 15:21:50 2018

@author: Marcus
"""

import os
import fdmt_date as fda
import fdmt_data as fdt


main_path=os.environ["THE_PROCESS"].replace("\\","/")+"/"
data_path=main_path+"data/"
bin_path=main_path+"bin/"

db_config=os.environ["THE_PROCESS_DB"]
[db_host,db_port,db_db,db_user,db_passwd]=db_config.split(";")

bat_file=open(bin_path+"the_process.bat",'w+')

bat_file.write("hello world!")

bat_file.close()


