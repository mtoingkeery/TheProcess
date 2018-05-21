# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import fdmt_date as _fdmt_date
import fdmt_data as _fdmt_data
import fdmt_query as _fdmt_query
import fdmt_procedure as _fdmt_procedure

import pickle as _pickle
import time as _time
import tushare as _ts

__magic_box=_fdmt_data.magic_box
__data_path=_fdmt_data.data_path

#dump & load  序列化到文件 & 从文件读取
#dumps & loads  序列化成二进制对象 & 从二进制对象读取


pickle_file_path=__data_path+"config/idx.pkl"
pickle_file=open(pickle_file_path,"rb+")
para_res=_pickle.load(pickle_file)
pickle_file.close()

print(para_res)
print(type(para_res))