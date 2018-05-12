# -*- coding: utf-8 -*-
"""
Created on Sat May 12 17:19:09 2018

@author: Marcus
"""

import fdmt_wechat as _fdw
import fdmt_query as _fdq

headers = eval(_fdq.json("header"))


_fdw.wechat_send("Beautiful Day!!!","marcus.houzy")