# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 17:02:32 2020

@author: Zi-Yu
"""

#import cv2
#from matplotlib import pyplot as plt
from PIL import Image
#from scipy.ndimage import filters
#import numpy as np
#import colorsys

img = Image.open('t7.jpg')
width = img.size[0]    #圖片的 寬
height = img.size[1]   #圖片的 高
img = img.convert('RGB')
count=0
array = []
for x in range(width):
    for y in range(height):
        r, g, b = img.getpixel((x,y))
        hsv_r, hsv_g, hsv_b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        #以下計算還能再改還不夠好
        #h
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        #s
        if mx == 0:
            s = 0
        else:
            s = df/mx
        #v
        v = mx
        
        #print(h,s,v)


        #用角度去分析顏色 (先把 V 切成2段  => 黑色   
        #                 剩下的部份 把 S 切成2段  
        #                 低飽和度的部份 => 用V再切一半分出 灰跟白 
        #                 高飽和度的部份 => 套用原本算法)
        if v>=0.5 and v<=0:
            img.putpixel((x,y), (0,0,0))         #黑
            #array.append(h)
        else:
            if s<=0.43:
               if v>0.5 :
                   img.putpixel((x,y), (255,255,255))   #白
                   #array.append(h)
               else:
                   img.putpixel((x,y), (192,192,192))   #灰
                   #array.append(h)
            else:
                if h>0 and h<30 or h>=330 and h<=360:
                    img.putpixel((x,y), (255,0,0))           #紅
                    #array.append(h)
                elif h>=30 and h<90:
                    img.putpixel((x,y), (255,255,0))         #黃
                    #array.append(h)
                elif h>=90 and h<210:  #原本210 嘗試200
                    img.putpixel((x,y), (0,255,0))           #綠
                    #array.append(h)
                elif h>=210 and h<270:
                    img.putpixel((x,y), (0,0,255))           #藍
                    #array.append(h)
                elif h>=270 and h<330:
                    img.putpixel((x,y), (255,0,255))         #紫
                    #array.append(h)
                            

#print(array)
#print(r,g,b)
#print(h,s,v)
img.save("Temporary.jpg")
img.show()
