# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 06:19:07 2018

@author: houz
"""

import os,time
import pandas as pd
import fdmt_data as fdt
import fdmt_date as fda
import fdmt_wechat as fdw
import urllib as _urllib
import json


url = "http://apis.baidu.com/apistore/weatherservice/weather?citypinyin="

city= "shanghai"
#完整api访问接口
target_url=url+city

headers={"apikey", "vMUI0wh6BUDLR2WkiP3P0oaZtwNgL5iE"}

post_request = _urllib.request.Request(target_url,headers=headers)
post_res = eval(_urllib.request.urlopen(post_request).read().decode('utf-8'))
