# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:24:23 2018

@author: houz
"""

import json,datetime,time,os
import urllib
from urllib.request import urlopen
import pandas as pd
import fdmt_query as fdq


config_path=os.environ["THE_PROCESS"].replace("\\","/")+"/config/"
wechat_config_file=config_path+"wechat_config.json"
wechat_config=json.load(open(wechat_config_file))

current_time = datetime.datetime.now()
current_time_str=current_time.strftime("%Y-%m-%d %H:%M:%S")

corp_id=wechat_config["Main"]["CorpID"]

def wechat_access_token(agent_name="Message"):
    try:        
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
        return [200,""]

def wechat_send(message_content="Hello World! via Python",agent_name="Message"):
    para_res=wechat_access_token("Message")    
    if para_res[0]<=1:
        access_token=para_res[1]
        target_url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token

        contact_user=wechat_config["Contact"]["UserID"]
        message_agent_id=int(wechat_config[agent_name]["AgentID"])

        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        }

        post_data={
           "touser" : contact_user,
           "msgtype" : "text",
           "agentid" : message_agent_id,
           "text" : {
               "content" : message_content
           },
           "safe":0
           }
           
        post_date_enc=json.dumps(post_data).encode('utf-8')
        post_request = urllib.request.Request(target_url,data=post_date_enc,headers=headers)
        post_res = eval(urllib.request.urlopen(post_request).read().decode('utf-8'))
        
        if post_res["errcode"]==0:
            print(time.strftime('%Y/%m/%d %T')+" - Send Successfully")
            return [1,"Send Successfully"]
        else:
            print(time.strftime('%Y/%m/%d %T')+" - Send Successfully")
            return [100,"Failed to Send"]            
        
    else:
        print(time.strftime('%Y/%m/%d %T')+" - No Access Token Available")
        return [200,""]
