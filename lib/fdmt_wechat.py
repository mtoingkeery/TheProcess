# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:24:23 2018

@author: houz
"""

import json,datetime,time,os
from urllib.request import urlopen
import pandas as pd
import fdmt_query as fdq

def access_token(agent_name="Message"):
    try:
        config_path=os.environ["THE_PROCESS"].replace("\\","/")+"/config/"
        wechat_config_file=config_path+"wechat_config.json"
        wechat_config=json.load(open(wechat_config_file))
        
        current_time = datetime.datetime.now()
        current_time_str=current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        corp_id=wechat_config["Main"]["CorpID"]
        message_agent_id=wechat_config[agent_name]["AgentID"]
        message_agent_secret=wechat_config[agent_name]["Secret"]
        
        access_token_file=config_path+"wechat_access_token_"+message_agent_id+".json"
        access_token_obj=json.load(open(access_token_file))
        
        if access_token_obj["ExpireTime"]>current_time_str:
            print(time.strftime('%Y/%m/%d %T')+" - Access Token Valid")
            return [0,access_token_obj["AccessToken"]]
        else:
            target_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid="+corp_id+"&corpsecret="+message_agent_secret        
            request_res_raw = urlopen(target_url).read()
            request_res=eval(request_res_raw.decode("utf-8"))
            
            if request_res["errcode"]==0:
                access_token=request_res["access_token"]
                expire_time_str=(current_time+pd.tseries.offsets.DateOffset(minutes=int(request_res["expires_in"])/60-10)).strftime("%Y-%m-%d %H:%M:%S")
                para_content=fdq.sp_json('access_token',corp_id,access_token,current_time_str,expire_time_str).replace("  ","")
        
                access_token_update=open(access_token_file,'w+')
                access_token_update.writelines(para_content)                
                access_token_update.close()
                
                print(time.strftime('%Y/%m/%d %T')+" - Get New Access Token")
                return [1,access_token]
            else:
                print(time.strftime('%Y/%m/%d %T')+" - Access Token Invalid & Get Net Access Token Failed")
                return [100,""]
        
    except Exception as ErrorCode:
        print("-----------------------------------------------------------------------------")
        print(time.strftime('%Y/%m/%d %T')+" - Exception Occurs!")
        print(str(ErrorCode))
        print("-----------------------------------------------------------------------------")
