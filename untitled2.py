# -*- coding: utf-8 -*-
"""
Created on Wed May 16 17:15:23 2018

@author: houz
"""

import pandas as pd
import numpy as np
from PIL import Image

rnk_list_x=[[x,x%2,int(x*x*(x+1)/135252*960)] for x in range(1,52)]
rnk_list_y=[[x,x%2,int(x*x*(x+1)/135252*540)] for x in range(1,52)]

sp_para_x=1
res_list_x=[]

for para in rnk_list_x:
    para_list=[[para[0],para[1],x] for x in range(sp_para_x,para[2]+1)]
    res_list_x.extend(para_list)

    sp_para_x=para[2]+1


sp_para_y=1
res_list_y=[]

for para in rnk_list_y:
    para_list=[[para[0],para[1],x] for x in range(sp_para_y,para[2]+1)]
    res_list_y.extend(para_list)

    sp_para_y=para[2]+1

print(res_list_x)
print(res_list_y)

np_r=np.zeros([540,960])
np_g=np.zeros([540,960])
np_b=np.zeros([540,960])


for pa in res_list_y:
    for pb in res_list_x:
        if pa[1]!=pb[1]:
            np_r[pa[2]-1][pb[2]-1]=255
            np_g[pa[2]-1][pb[2]-1]=242
            np_b[pa[2]-1][pb[2]-1]=246
        else:
            np_r[pa[2]-1][pb[2]-1]=38
            np_g[pa[2]-1][pb[2]-1]=203
            np_b[pa[2]-1][pb[2]-1]=2

"""
"""
img_r=Image.fromarray(np_r).convert('L')
img_g=Image.fromarray(np_g).convert('L')
img_b=Image.fromarray(np_b).convert('L')

pic=Image.merge('RGB',(img_r,img_g,img_b)) #合并三通道
pic.show()
