# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:33:03 2018

@author: houz
"""

import fdmt_date as _fda
import fdmt_data as _fdt
import os as _os
import pandas as pd
import statsmodels.formula.api as sm
import sqlalchemy as _sqlalchemy
import time as _time

df = pd.DataFrame({"A100": [10,20,30,40,50], "B100": [20, 30, 10, 40, 50], "C100": [32, 234, 23, 23, 42523]})
res = sm.ols(formula="A100 ~ B100 + C100", data=df).fit()

print(res.summary())
