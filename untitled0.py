# -*- coding: utf-8 -*-
"""
Created on Tue May  8 15:54:34 2018

@author: houz
"""

import pandas as pd

from sklearn import linear_model
reg = linear_model.Ridge (alpha = .5)


para_alpha = "C:/Users/houz/Branch/theProcess/data/stock_hist/201804_600837.txt"
para_beta = "C:/Users/houz/Branch/theProcess/data/stock_hist/201804_601688.txt"


df_alpha=pd.read_csv(para_alpha,dtype={'id':str}).sort_values(by='tdate')
df_beta=pd.read_csv(para_beta,dtype={'id':str}).sort_values(by='tdate')

list_alpha = df_alpha["close"].tolist()
list_beta = df_beta["close"].tolist()

i=1
para_com = []
for para in list_alpha:
    para_com.append([para,i])
    i+=1

reg.fit(para_com,list_beta)    

print(reg.coef_)
print(reg.intercept_)