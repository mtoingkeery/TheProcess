#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 15:21:50 2018

@author: Marcus
"""
import pcap,dpkt,datetime,math,os

sniffer=pcap.pcap(immediate=True)

for para_time,para_content in sniffer:
    fmt_para_time=datetime.datetime.fromtimestamp(para_time)
    fmt_para_time_str=fmt_para_time.strftime('%Y-%m-%d %H:%M:%S')
    print(fmt_para_time_str)

    fmt_para_content=para_content
    type_para_content=type(fmt_para_content)
    print(type_para_content)
    print(fmt_para_content.decode("utf8","ignore"))
"""
    if type_para_content=='dpkt.ip.IP':
#        print(fmt_para_content)
        1
    elif type_para_content=='dpkt.arp.ARP':
#        print(fmt_para_content)
        1çc
    elif type_para_content=='dpkt.llc.LLC':
#        print(fmt_para_content)
    elif type_para_content=='bytes':
        print(fmt_para_content)
    else:
        print(type_para_content)
        print("--------------------------------------------------")
"""            
