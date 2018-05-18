# -*- coding: utf-8 -*-
""" 
Created on Fri Apr  6 15:21:50 2018

@author: Marcus
"""

import os
import fdmt_date as fda
import fdmt_data as fdt

def main():
    main_path=fdt.main_path
    bin_path=main_path+"bin/"

    ##################################################################################
    #Bat 01
    exec_query01=''
    for para in os.environ["Path"].split(";"):
        if para.replace("\\","").replace("\/","")[-9:]=="Anaconda3":
            exec_query01=para.replace("\\","/")+"/python.exe"
    exec_query02=main_path+"src/TP100_The_Process_Daily.py"
    exec_query03=main_path+"log/"+"RUNNING_LOG.log"
    exec_query04=main_path+"log/"+"ERROR_LOG.log"
    exec_query00=exec_query01+" "+exec_query02+" >> "+exec_query03+" 2>> "+exec_query04+"\n"

    bat_file=open(bin_path+"the_process.bat",'w+')

    bat_file.write("cd/\n")
    bat_file.write("c:\n")
    bat_file.write(exec_query00)

    bat_file.close()

    ##################################################################################
    #Bat 02
    bat_file=open(bin_path+"regular_update.bat",'w+')

    bat_file.write("cd/\n")
    bat_file.write("c:\n")
    bat_file.write("cd "+main_path+"\n")
    bat_file.write("git pull\n")
    bat_file.write("git add .\n")
    bat_file.write("git status\n")    
    bat_file.write('''git commit -m "system regular upate"\n''')
    bat_file.write("git push origin master:develop")

    bat_file.close()

if __name__ == '__main__':
    main()

