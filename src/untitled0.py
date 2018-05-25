# -*- coding: utf-8 -*-
'''
    百度即用API -- 天气调用
    通过拼音访问城市天气
'''

import urllib as _urllib
import json


url = "http://apis.baidu.com/apistore/weatherservice/weather?citypinyin="

city= "shanghai"
#完整api访问接口
target_url=url+city

headers={"apikey", "vMUI0wh6BUDLR2WkiP3P0oaZtwNgL5iE"}

post_request = _urllib.request.Request(target_url,headers=headers)
post_res = eval(_urllib.request.urlopen(post_request).read().decode('utf-8'))
