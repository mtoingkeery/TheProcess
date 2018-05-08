# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:06:39 2018

@author: houz
"""

import os

azkp="C:\\Users\\houz\\Branch\\azkaban\\"
file_list=[]
key_words="etl-ods-rdb2hive.notify-stage"
key_words2=key_words
target_list=[]

write_label=0
    
# Config json
for parent,dirnames,filenames in os.walk(azkp):
    for filename in filenames:
        if  ('_DL_' not in parent+'\\'+filename) & (filename[-4:].lower()=='.job'):# and 'spark_prm_manual' in parent+'\\'+filename:
            file_list.append(parent+'\\'+filename)    

for para_file in file_list:
    para_file_obj=open(para_file,'r',errors='ignore')
    file_content=para_file_obj.readlines()
    para_file_obj.close()

    for para_content in file_content:
        if (key_words in para_content) & (key_words2 in para_content):
            target_list.append([para_file,para_content])
            break
    if write_label==1:
        para_file_obj2=open(para_file,'w+',errors='ignore')
        for para_content in file_content:
            print(para_content)
            if (key_words in para_content) & (key_words2 in para_content):
                para_file_obj2.write("spark-script=/home/ubuntu/sparkjob/procedures/spark_prm_manual/special_data_etl.sc"+"\n")
            else:
                para_file_obj2.write(para_content)
        para_file_obj2.close()
    
for para_file in target_list:
    print(para_file[0])
    print(para_file[1])
