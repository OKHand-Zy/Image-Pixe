# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 17:40:28 2020

@author: Zi-Yu
"""

from PIL import Image

def count(x,y):
    r, g, b = img.getpixel((x,y))
    #hsv_r, hsv_g, hsv_b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
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
    return h,s,v

def color_home(colors,pixe):
    if scores[0][1]=="black":
        print("此圖大部分都是黑的佔",round(pixe, 2),"%")
    elif scores[0][1]=="wite":
        print("此圖大部分都是白的佔",round(pixe, 2),"%")
    elif scores[0][1]=="gray":
        print("此圖大部分都是灰的佔",round(pixe, 2),"%")
    elif scores[0][1]=="red":
        print("此圖大部分都是紅的佔",round(pixe, 2),"%")
    elif scores[0][1]=="yello":
        print("此圖大部分都是黃的佔",round(pixe, 2),"%")
    elif scores[0][1]=="gree":
        print("此圖大部分都是綠的佔",round(pixe, 2),"%")
    elif scores[0][1]=="blue":
        print("此圖大部分都是藍的佔",round(pixe, 2),"%")
    else:
        print("此圖大部分都是紫的佔",round(pixe, 2),"%")

img = Image.open('C:\\Users\\Zi-Yu\\Desktop\\finalproject\\pixe\\image\\night.jpg')
width = img.size[0]    #圖片的 寬
height = img.size[1]   #圖片的 高
img = img.convert('RGB')
array = []
black=0;wite=0;gray=0;red=0;yello=0;gree=0;blue=0;people=0
for x in range(width):
    for y in range(height):
        h,s,v=count(x,y)  
        if v>=0.5 and v<=0:
            img.putpixel((x,y), (0,0,0))         #黑
            black+=1
        else:
            if s<=0.43:
               if v>0.5 :
                   img.putpixel((x,y), (255,255,255))   #白
                   wite+=1
               else:
                   img.putpixel((x,y), (192,192,192))   #灰
                   gray+=1
            else:
                if h>0 and h<30 or h>=330 and h<=360:
                    img.putpixel((x,y), (255,0,0))           #紅
                    red+=1
                elif h>=30 and h<90:
                    img.putpixel((x,y), (255,255,0))         #黃
                    yello+=1
                elif h>=90 and h<210:  #原本210 嘗試200
                    img.putpixel((x,y), (0,255,0))           #綠
                    gree+=1
                elif h>=210 and h<270:
                    img.putpixel((x,y), (0,0,255))           #藍
                    blue+=1
                elif h>=270 and h<330:
                    img.putpixel((x,y), (255,0,255))         #紫
                    people+=1
            
scores = [(black,'black'), (wite,'wite'), (gray,'gray'), (red,'red'), (yello,'yello'), (gree,'gree'), (blue,'blue'), (people,'people')]
scores.sort(reverse=True)
pixe=(scores[0][0])/(width*height)*100
color_home(scores[0],pixe)

#print(scores[0])
#print(scores[1])




img.save("Temporary.jpg")
img.show()
    