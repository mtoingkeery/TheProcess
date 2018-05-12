#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 14:00:36 2018

@author: Marcus
"""

import json,time
import shutil,os
import aircv as ac
import cv2

import fdmt_data as fdt

#GLOBAL
the_pentagon=fdt.main_path
config_path=the_pentagon+"config//"
screen_config_file=config_path+"stk_screen.json"
    
screen_config=json.load(open(screen_config_file))
screen_png=the_pentagon+"screen.png"

label="stock"

status_homepage=0
status_app=0
status_exit=0
status_login=0

def screen_shot_backup():
    print(time.strftime('%Y/%m/%d %T')+" - Screen Shot - Backup")
    screen_bak=the_pentagon+"pics/screen"+time.strftime('%Y%m%d%H%M%S')+".png"
    shutil.copyfile(screen_png,screen_bak)

def screen_shot(label=0):
    print(time.strftime('%Y/%m/%d %T')+" - Screen Shot")
    
    cmd_script="adb shell screencap -p /sdcard/screen.png"
    os.system(cmd_script)
    time.sleep(2)
    cmd_script="adb pull /sdcard/screen.png ."
    os.system(cmd_script)
    
    if label==1:
        screen_shot_backup()
   
def screen_click(click_position):
    cmd_script = "adb shell input tap "+ click_position
    os.system(cmd_script)
    time.sleep(1)
    
def screen_click_list(click_list):
    for para in click_list:
        para_cmd_script="adb shell input tap "+ para
        os.system(para_cmd_script)
        time.sleep(1)

def screen_icons(para_str,para_dict):
    click_list=[]
    for para in para_str:
        click_list.append(para_dict[para])
    screen_click_list(click_list)
    
def draw_circle(imsrc, pos, circle_radius=100, color=(0,0,0), line_width=5):
    cv2.circle(imsrc, pos, int(circle_radius), color, line_width)
    cv2.imshow('objDetect', imsrc) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def stock_login(label="stock"):
    screen_shot(1)    
    print(time.strftime('%Y/%m/%d %T')+" - Stock Login")    
    time.sleep(1)    
    click_position=screen_config["stock"]["wode"]["hp"]
    screen_click(click_position)    
    time.sleep(1)    
    click_position=screen_config["stock"]["wode"]["login"]
    screen_click(click_position)    
    time.sleep(1)    
    screen_icons(screen_config["stock"]["master"],screen_config["stock"]["icons"])    

    print(time.strftime('%Y/%m/%d %T')+" - Stock Login Info")    
    screen_shot(1)    
    imsrc = ac.imread(screen_png)
    imobj = ac.imread(config_path+label+"_confirm.png")    
    # find the match position
    pos = ac.find_template(imsrc, imobj)
    
    if pos is not None:
        if pos["confidence"]>0.5:
            para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
            screen_click(para)
    screen_shot(1)    
    
    print(time.strftime('%Y/%m/%d %T')+" - Stock Login Check")    
    screen_shot()    
    imsrc = ac.imread(screen_png)
    imobj = ac.imread(config_path+label+"_login_check.png")    
    # find the match position
    pos = ac.find_template(imsrc, imobj)
    
    if pos is not None:
        if pos["confidence"]>0.5:
            print(time.strftime('%Y/%m/%d %T')+" - Stock Login - Success")
            return pos["confidence"]
    screen_shot(1)  
    print(time.strftime('%Y/%m/%d %T')+" - Stock Login Failed")
    return 0
    
def stock_exit(label="stock"):
    cir_label=0
    screen_shot(1)
    while(cir_label<5):    
        print(time.strftime('%Y/%m/%d %T')+" - Exit Stock")    
        cmd_script="adb shell input keyevent 4"    
        os.system(cmd_script)
        screen_shot(1)
    
        imsrc = ac.imread(screen_png)
        imobj = ac.imread(config_path+label+"_confirm.png")
    
        # find the match position
        pos = ac.find_template(imsrc, imobj)
        if pos is not None:
            if pos["confidence"]>0.5:
                para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
                screen_click(para)
                print(time.strftime('%Y/%m/%d %T')+" - Exit Click")
                return pos["confidence"]
        cir_label+=1    
    cmd_script="adb shell input keyevent 3"    
    os.system(cmd_script)    
    print(time.strftime('%Y/%m/%d %T')+" - Exit Pseudo - Back to Homepage")
    return 0

def check_homepage(label="stock"):
    print(time.strftime('%Y/%m/%d %T')+" - HomePage Check")    
    screen_shot(1)
    # Homepage Chek
    imsrc = ac.imread(screen_png)
    imobj = ac.imread(config_path+label+"_start.png")
    # find the match position
    pos = ac.find_template(imsrc, imobj)
    if pos is not None:
        if pos["confidence"]>0.5:
            print(time.strftime('%Y/%m/%d %T')+" - Start Stock App")    
            para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
            screen_click(para)
            time.sleep(5)
            return pos["confidence"]
    else:
        print(time.strftime('%Y/%m/%d %T')+" - Not in HomePage")            
        return 0

def check_app(flags="wode",label="stock",):
    print(time.strftime('%Y/%m/%d %T')+" - App Check")    
    screen_shot(1)
    # Homepage Chek
    imsrc = ac.imread(screen_png)
    imobj = ac.imread(config_path+label+"_bottom_"+flags+".png")
    # find the match position
    pos = ac.find_template(imsrc, imobj)
    if pos is not None:
        if pos["confidence"]>0.5:
            print(time.strftime('%Y/%m/%d %T')+" - Inside the App")    
            return pos["confidence"]
    else:
        print(time.strftime('%Y/%m/%d %T')+" - Outside the App")            
        return 0

def check_jiaoyipage(flags="mairu",label="stock"):
    print(time.strftime('%Y/%m/%d %T')+" - Jiaoyi Page Check")    
    screen_shot(1)
    # Homepage Chek
    imsrc = ac.imread(screen_png)
    imobj = ac.imread(config_path+label+"_jiaoyi_"+flags+".png")
    # find the match position
    pos = ac.find_template(imsrc, imobj)
    if pos is not None:
        if pos["confidence"]>0.99:
            print(time.strftime('%Y/%m/%d %T')+" - On Jiaoyi "+flags+" Page")    
            return pos["confidence"]
    print(time.strftime('%Y/%m/%d %T')+" - Not On Jiaoyi "+flags+" Page")    
    return 0

def global_start():
    print(time.strftime('%Y/%m/%d %T')+" - Global Start")
    print("-------------------------------------------------------")

    status_homepage=check_homepage()
    status_app=check_app()        
    
    print(time.strftime('%Y/%m/%d %T')+" - Global Start - Retry")
    if (status_homepage==0)&(status_app==0):
        status_exit=stock_exit()
        status_homepage=check_homepage()
        status_app=check_app()

    if status_app>0:
        stock_login()
        return 1
    print(time.strftime('%Y/%m/%d %T')+" - Global Start - FAILED!!")
    return 0

def global_exit():
    stock_exit()
    print("-------------------------------------------------------")
    print(time.strftime('%Y/%m/%d %T')+" - Global End")

def stock_jiaoyi(label="stock"):
    print(time.strftime('%Y/%m/%d %T')+" - Trade Page")    
    status_app=check_app("jiaoyi",label)

    if status_app>0.95:
        print(time.strftime('%Y/%m/%d %T')+" - On Trade Page")    
        return status_app
    elif status_app>0.5:
        screen_shot(1)    
        print(time.strftime('%Y/%m/%d %T')+" - Insert App & Not Trade Page")    
        click_position=screen_config[label]["jiaoyi"]["hp"]
        screen_click(click_position)
        
    print(time.strftime('%Y/%m/%d %T')+" - Trade Page - Retry")    
    status_app=check_app("jiaoyi",label)
    if status_app>0.95:
        print(time.strftime('%Y/%m/%d %T')+" - On Trade Page")    
        return status_app
    else:
        print(time.strftime('%Y/%m/%d %T')+" - Trade Page - FAILED!!")   
        return 0
  
def stock_jiaoyi_exec(stock_id,amount,price,trade_flags="mairu",label="stock"):
    print(time.strftime('%Y/%m/%d %T')+" - Trade Mairu")    
    click_position=screen_config[label]["jiaoyi"][trade_flags]["hp"]
    screen_click(click_position)

    para_status=check_jiaoyipage(flags=trade_flags,label="stock")
    if para_status>0:
        print(time.strftime('%Y/%m/%d %T')+" - Stock ID")    
        click_position=screen_config[label]["jiaoyi"][trade_flags]["stock"]
        screen_click(click_position)
        screen_icons(stock_id,screen_config["stock"]["jiaoyi"]["keys"])  

        print(time.strftime('%Y/%m/%d %T')+" - Trade Amount")    
        click_position=screen_config[label]["jiaoyi"][trade_flags]["amount"]
        screen_click(click_position)
        screen_icons(amount,screen_config["stock"]["jiaoyi"]["keys"])  

        print(time.strftime('%Y/%m/%d %T')+" - Trade Enter")    
        screen_shot(1)
        click_position=screen_config[label]["jiaoyi"][trade_flags]["enter"]
        screen_click(click_position)

        print(time.strftime('%Y/%m/%d %T')+" - Trade Confirm")    
        screen_shot(1)
        imsrc = ac.imread(screen_png)
        imobj = ac.imread(config_path+label+"_confirm.png")
        # find the match position
        pos = ac.find_template(imsrc, imobj)
        if pos is not None:
            if pos["confidence"]>0.5:
                para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
                screen_click(para)
        else:
            print(time.strftime('%Y/%m/%d %T')+" - Trade Apply Failed")    
            return 0

        print(time.strftime('%Y/%m/%d %T')+" - Trade Info")    
        screen_shot(1)
        imsrc = ac.imread(screen_png)
        imobj = ac.imread(config_path+label+"_confirm.png")
        # find the match position
        pos = ac.find_template(imsrc, imobj)
        if pos is not None:
            if pos["confidence"]>0.5:
                para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
                screen_click(para)
                print(time.strftime('%Y/%m/%d %T')+" - Trade Info - Success")    
                cmd_script="adb shell input keyevent 4"    
                os.system(cmd_script)    
                return pos["confidence"]
    else:
        print(time.strftime('%Y/%m/%d %T')+" - Trade Failed")    
        return 0
    
def stock_chedan_all(label="stock"):
    print(time.strftime('%Y/%m/%d %T')+" - Chedan All")    
    click_position=screen_config[label]["jiaoyi"]["chedan"]["hp"]
    screen_click(click_position)

    para_status=check_jiaoyipage("chedan",label)
    if para_status>0:
        print(time.strftime('%Y/%m/%d %T')+" - Start to Chedan")    
        while(1):
            screen_shot(1)      
            imsrc = ac.imread(screen_png)
            imobj = ac.imread(config_path+label+"_chedan.png")    
            # find the match position
            pos = ac.find_template(imsrc, imobj)
            if pos is not None:
                if pos["confidence"]>0.95:
                    para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
                    screen_click(para)

                    screen_shot(1)
                    imsrc = ac.imread(screen_png)
                    imobj = ac.imread(config_path+label+"_confirm.png")
                    pos = ac.find_template(imsrc, imobj)
                    if pos is not None:
                        if pos["confidence"]>0.5:
                            para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
                            screen_click(para)

                    screen_shot(1)
                    imsrc = ac.imread(screen_png)
                    imobj = ac.imread(config_path+label+"_confirm.png")
                    pos = ac.find_template(imsrc, imobj)
                    if pos is not None:
                        if pos["confidence"]>0.5:
                            para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
                            screen_click(para)
                else:                    
                    cmd_script="adb shell input keyevent 4"    
                    os.system(cmd_script)    
                    print(time.strftime('%Y/%m/%d %T')+" - Chedan All")    
                    return 1
    else:
        return 0
    
    
    
    
    
    
    
    