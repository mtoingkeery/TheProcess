#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 14:00:36 2018

@author: Marcus
"""

import numpy as np
from PIL import Image
import json,time
import shutil,os,socket
import aircv as ac
import cv2


#GLOBAL
machine_name = socket.gethostname()
print(machine_name)

if machine_name=="DESKTOP-O8U9FOM":
    the_pentagon="D:\\Branch\\TheProcess\\"
    config_path=the_pentagon+"config//"
    screen_config_file=config_path+"screen.json"
elif machine_name=="Zongyuans-MacBook-Pro.local":
    the_pentagon="//Users//Marcus//Branch//TheProcess//"    
    config_path=the_pentagon+"config//"
    screen_config_file=config_path+"screen.json"
    
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
    imobj = ac.imread(config_path+label+"_login_info.png")    
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
            return 1
    screen_shot(1)  
    print(time.strftime('%Y/%m/%d %T')+" - Stock Login Failed")
    return 2
    
def stock_exit(label="stock"):
    cir_label=0
    screen_shot(1)
    while(cir_label<5):    
        print(time.strftime('%Y/%m/%d %T')+" - Exit Stock")    
        cmd_script="adb shell input keyevent 4"    
        os.system(cmd_script)
        screen_shot(1)
    
        imsrc = ac.imread(screen_png)
        imobj = ac.imread(config_path+label+"_login_info.png")
    
        # find the match position
        pos = ac.find_template(imsrc, imobj)
        if pos is not None:
            if pos["confidence"]>0.5:
                para=str(int(pos["result"][0]))+" "+str(int(pos["result"][1]))
                screen_click(para)
                print(time.strftime('%Y/%m/%d %T')+" - Exit Click")
                return 1
        cir_label+=1    
    cmd_script="adb shell input keyevent 3"    
    os.system(cmd_script)    
    print(time.strftime('%Y/%m/%d %T')+" - Exit Pseudo - Back to Homepage")
    return 2

def check_homepage():
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
            return 1
    else:
        print(time.strftime('%Y/%m/%d %T')+" - Not in HomePage")            
        return 2

def check_app():
    print(time.strftime('%Y/%m/%d %T')+" - App Check")    
    screen_shot(1)
    # Homepage Chek
    imsrc = ac.imread(screen_png)
    imobj = ac.imread(config_path+label+"_app_bottom.png")
    # find the match position
    pos = ac.find_template(imsrc, imobj)
    if pos is not None:
        if pos["confidence"]>0.5:
            print(time.strftime('%Y/%m/%d %T')+" - Inside the App")    
            return 1
    else:
        print(time.strftime('%Y/%m/%d %T')+" - Outside the App")            
        return 2

def global_start():
    print(time.strftime('%Y/%m/%d %T')+" - Global Start")
    print("-------------------------------------------------------")

    status_homepage=check_homepage()
    status_app=check_app()        
    
    print(time.strftime('%Y/%m/%d %T')+" - Global Start - Retry")
    if (status_homepage==2)&(status_app==2):
        status_exit=stock_exit()
        status_homepage=check_homepage()
        status_app=check_app()

    if status_app==1:
        stock_login()
        return 1
    print(time.strftime('%Y/%m/%d %T')+" - Global Start - FAILED!!")
    return 2

def global_exit():
    stock_exit()
    print("-------------------------------------------------------")
    print(time.strftime('%Y/%m/%d %T')+" - Global End")

status_app=check_app()
if status_app=1:
    
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
imobj = ac.imread(config_path+label+"_login_info.png")    
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
        return 1
screen_shot(1)  
print(time.strftime('%Y/%m/%d %T')+" - Stock Login Failed")
return 2    