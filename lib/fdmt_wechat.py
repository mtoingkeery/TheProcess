# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:24:23 2018

@author: houz
"""

import json as _json
import datetime as _datetime
import time as _time
import os as _os
import urllib as _urllib
from urllib.request import urlopen as _urlopen
import pandas as _pd
import fdmt_query as _fdq

__config_path=_os.environ["THE_PROCESS"].replace("\\","/")+"/config/"
__wechat_config_file=__config_path+"wechat_config.json"
__wechat_config=_json.load(open(__wechat_config_file))

__current_time = _datetime.datetime.now()
__current_time_str=__current_time.strftime("%Y-%m-%d %H:%M:%S")

def wechat_access_token(agent_name="Message"):
    try:        
        corp_id=__wechat_config["Main"]["CorpID"]

        message_agent_id=__wechat_config[agent_name]["AgentID"]
        message_agent_secret=__wechat_config[agent_name]["Secret"]
        
        access_token_file=__config_path+"wechat_access_token_"+message_agent_id+".json"
        access_token_obj=_json.load(open(access_token_file))

        if access_token_obj["ExpireTime"]>__current_time_str:
            print(_time.strftime('%Y/%m/%d %T')+" - Access Token Valid")
            return [0,access_token_obj["AccessToken"]]

    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")

    try:
        target_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+corp_id+"&corpsecret="+message_agent_secret        
        request_res_raw = _urlopen(target_url).read()
        request_res=eval(request_res_raw.decode("utf-8"))
        
        if request_res["errcode"]==0:
            access_token=request_res["access_token"]
            expire_time_str=(__current_time+_pd.tseries.offsets.DateOffset(minutes=int(request_res["expires_in"])/60-10)).strftime("%Y-%m-%d %H:%M:%S")
            para_content=_fdq.json('wechat_access_token',str(corp_id),access_token,__current_time_str,expire_time_str)
    
            access_token_update=open(access_token_file,'w+')
            access_token_update.writelines(para_content)                
            access_token_update.close()
                        
            print(_time.strftime('%Y/%m/%d %T')+" - Get New Access Token")
            return [1,access_token]
        else:
            print(_time.strftime('%Y/%m/%d %T')+" - Access Token Invalid & Get Net Access Token Failed")
            return [100,"Access Token Invalid & Get Net Access Token Failed"]
        
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(_time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")
        return [200,"Exception Occurs!"]

def wechat_send(message_content="Hello World! via Python",to_users="",agent_name="Message"):
    para_res=wechat_access_token("Message")    
    if para_res[0]<=1:
        access_token=para_res[1]
        target_url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token

        if to_users=="":
            contact_user=__wechat_config["Contact"]["UserID"]
        else:
            contact_user=to_users
            
        message_agent_id=__wechat_config[agent_name]["AgentID"]

        headers = eval(_fdq.json("header"))

        post_data=eval(_fdq.json("post_data_send_message",contact_user,str(message_agent_id),message_content))           
        post_data_enc = _json.dumps(post_data).encode('utf-8')
        
        post_request = _urllib.request.Request(target_url,data=post_data_enc,headers=headers)
        post_res = eval(_urllib.request.urlopen(post_request).read().decode('utf-8'))
        
        if post_res["errcode"]==0:
            print(_time.strftime('%Y/%m/%d %T')+" - Send Successfully")
            return [1,"Send Successfully"]
        else:
            print(_time.strftime('%Y/%m/%d %T')+" - Failed to Send")
            return [100,"Failed to Send"]            
    else:
        print(_time.strftime('%Y/%m/%d %T')+" - No Access Token Available")
        return [200,"No Access Token Available"]
