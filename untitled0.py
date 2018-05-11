# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:24:23 2018

@author: houz
"""

from urllib.request import urlopen
import requests,json

corp_id="wwf972aeec5c872dd3"
corp_secret="Z5R2GCHnBL1Xa3xl61yW6fgGfGn9E25pBaSYklndIUI"
#target_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+corp_id+"&corpsecret="+corp_secret
target_url='https://www.baidu.com/'
print(target_url)
html = urlopen(target_url).read()
html=b'{"errcode":0,"errmsg":"ok","access_token":"UwmFuJzUPSBFfXwI__OgvnRI_6JJKFK5XeOLBABF8DTFciht5RALNWWUjoIBRP2DfjoL89pXzjn9yHc1nNRZdIHZMYPBOivrXpcRkcKONAKAm3wO3jyKthdPRpdcM6Rum_iyOmAl7c0k94TExzvvewDVEICmMdoKvVSIYB4W4Uyadno2Jat5bRIrDb81_IunWhsTEEAMVwFJB0N9NZpvQA","expires_in":7200}'

res=eval(html.decode("utf-8"))

print(res)
