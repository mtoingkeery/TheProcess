# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:27 2018

@author: houz
"""

import time
import TP011_Get_Index_Hist as tp011
import TP012_Get_Stock_Hist as tp012
import TP021_Update_Index_Hist as tp021
import TP022_Update_Stock_Hist as tp022

def main():
    print("------------------------------------------------------")
    print(time.strftime("%Y/%m/%d %T")+" - The Process Daily - Global Start")
    print("------------------------------------------------------")

    tp011.main()
    tp012.main()
    tp021.main()
    tp022.main()
 
    print("------------------------------------------------------")
    print(time.strftime("%Y/%m/%d %T")+" - The Process Daily - Global End")
    print("------------------------------------------------------")
    print("------------------------------------------------------")

if __name__ == '__main__':
    main()
