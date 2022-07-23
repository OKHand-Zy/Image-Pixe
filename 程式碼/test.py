# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 23:27:36 2020

@author: Zi-Yu
"""
'''
import cv2
from PIL import Image
import numpy as np
import colorsys
img = Image.open('123.jpg')
width = img.size[0]    #圖片的寬
height = img.size[1]   #圖片的高
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
        
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
            
        if mx == 0:
            s = 0
        else:
            s = df/mx
        v = mx
        if h>0 and h<60:
            img.putpixel((x,y), (255,0,0)) #紅
        elif h>=60 and h<120:
            img.putpixel((x,y), (255,255,0)) #黃
        elif h>=120 and h<180:
            img.putpixel((x,y), (0,255,0))  #綠
        elif h>=180 and h<240:
            img.putpixel((x,y), (0,0,255)) #藍
        elif h>=240 and h<=360:
            img.putpixel((x,y), (255,0,255)) #紫
        else:
            if v==0 and r==0 and g==0 and b==0:
                img.putpixel((x,y), (0,0,0))
            elif v==1 and r==1 and g==1 and b==1:
                img.putpixel((x,y), (255,255,255))
            else:
                img.putpixel((x,y), (192,192,192))
print(mx,mn) 
print(h,s,v)    
img.show()
'''
import colorsys
import PIL.Image as Image
 
def get_dominant_color(image):
    max_score = 0.0001
    dominant_color = None
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]):
        # 转为HSV标准
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)
        y = (y-16.0)/(235-16)
 
        #忽略高亮色
        if y > 0.9:
            continue
        score = (saturation+0.1)*count
        if score > max_score:
            max_score = score
            dominant_color = (r,g,b)
    return dominant_color
 
 
if __name__ == '__main__':
    image = Image.open('t8.jpg')
    image = image.convert('RGB')
    print(get_dominant_color(image))
