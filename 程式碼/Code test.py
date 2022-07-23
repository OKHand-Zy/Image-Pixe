# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:36:03 2020

@author: Zi-Yu
"""
"""
import skimage.io as io
import matplotlib.pyplot as plt
import skimage.util as util
import numpy as np
import skimage.exposure as ex
from PIL import Image
import colorsys
img = Image.open('Red.png')
width = img.size[0]    #圖片的寬
height = img.size[1]   #圖片的高
img = img.convert('RGB')
count=0
array = []
for x in range(width):
    for y in range(height):
        r, g, b = img.getpixel((x,y))
        #HSV轉RGB公式
        HSV_r, HSV_g, HSV_b = r / 255.0, g / 255.0, b / 255.0
        mx = max(HSV_r, HSV_g, HSV_b)
        mn = min(HSV_r, HSV_g, HSV_b)
        diff = mx - mn
        s=0
        h=0
        l=0
        # 计算H
        if mx == mn:
            h = 0
        elif mx == r:
            if g >= b:
                h = 60 * ((g - b) / diff) + 0
            else:
                h = 60 * ((g - b) / diff) + 360
        elif mx == g:
            h = 60 * ((b - r) / diff) + 120
        elif mx == b:
            h = 60 * ((r - g) / diff) + 240
        # 先计算L
        l = (mx + mn) / 2.0
        # 再计算S
        if mx == min:
            s = 0
        elif l > 0 and l <= 0.5:
            s = (diff / l) / 2.0
        elif l > 0.5:
            s = (diff / (1 - l)) / 2.0   
            
        if ((h >= 0  and h <= 10) or (h >= 125  and h <= 180)) and s>= 240 and l>= 120:          #找到 r:66 g:66 b:66 就轉
            img.putpixel((x,y), (255,255,255)) #轉白色
            r, g, b = img.getpixel((x,y))      #在讀取一次讀到改成的顏色
            rgb = (r, g, b)
            array.append(rgb)
            
print(r,"/",g,"/",b)
print(HSV_r,"/",HSV_g,"/",HSV_b)
print(h,"/",s,"/",l)
print(colorsys.rgb_to_hsv(r/255, g/255, b/255))

img.show()
img.save("Temporary.jpg")
"""
"""
import cv2
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
def RGB2HSI(rgb_img):
    
    #这是将RGB彩色图像转化为HSI图像的函数
    #:param rgm_img: RGB彩色图像
    #:return: HSI图像
    
    #保存原始图像的行列数
    row = np.shape(rgb_img)[0]
    col = np.shape(rgb_img)[1]
    #对原始图像进行复制
    hsi_img = rgb_img.copy()
    #对图像进行通道拆分
    B,G,R = cv2.split(rgb_img)
    #把通道归一化到[0,1]
    [B,G,R] = [ i/ 255.0 for i in ([B,G,R])]
    H = np.zeros((row, col))    #定义H通道
    
    I = (R + G + B) / 3.0       #计算I通道
    
    S = np.zeros((row,col))      #定义S通道
    
    for i in range(row):
        den = np.sqrt((R[i]-G[i])**2+(R[i]-B[i])*(G[i]-B[i]))
        thetha = np.arccos(0.5*(R[i]-B[i]+R[i]-G[i])/den)   #计算夹角
        
        h = np.zeros(col)               #定义临时数组
        #den>0且G>=B的元素h赋值为thetha
        h[B[i]<=G[i]] = thetha[B[i]<=G[i]]
        #den>0且G<=B的元素h赋值为thetha
        h[G[i]<B[i]] = 2*np.pi-thetha[G[i]<B[i]]
        #den<0的元素h赋值为0
        h[den == 0] = 0
        H[i] = h/(2*np.pi)      #弧度化后赋值给H通道
    #计算S通道
    for i in range(row):
        min = []
        #找出每组RGB值的最小值
        for j in range(col):
            arr = [B[i][j],G[i][j],R[i][j]]
            min.append(np.min(arr))
        min = np.array(min)
        #计算S通道
        S[i] = 1 - min*3/(R[i]+B[i]+G[i])
        #I为0的值直接赋值0
        S[i][R[i]+B[i]+G[i] == 0] = 0
    #扩充到255以方便显示，一般H分量在[0,2pi]之间，S和I在[0,1]之间
    hsi_img[:,:,0] = H*255
    hsi_img[:,:,1] = S*255
    hsi_img[:,:,2] = I*255

    print(H)
    print(I)
    print(S)
    
    print(den)
    print(thetha)
    return hsi_img
    
def HSI2RGB(hsi_img):
    
    #这是将HSI图像转化为RGB图像的函数
    #:param hsi_img: HSI彩色图像
    #:return: RGB图像
    
    # 保存原始图像的行列数
    row = np.shape(hsi_img)[0]
    col = np.shape(hsi_img)[1]
    #对原始图像进行复制
    rgb_img = hsi_img.copy()
    #对图像进行通道拆分
    H,S,I = cv2.split(hsi_img)
    #把通道归一化到[0,1]
    [H,S,I] = [ i/ 255.0 for i in ([H,S,I])]
    R,G,B = H,S,I
    for i in range(row):
        h = H[i]*2*np.pi
        #H大于等于0小于120度时
        a1 = h >=0
        a2 = h < 2*np.pi/3
        a = a1 & a2         #第一种情况的花式索引
        tmp = np.cos(np.pi / 3 - h)
        b = I[i] * (1 - S[i])
        r = I[i]*(1+S[i]*np.cos(h)/tmp)
        g = 3*I[i]-r-b
        B[i][a] = b[a]
        R[i][a] = r[a]
        G[i][a] = g[a]
        #H大于等于120度小于240度
        a1 = h >= 2*np.pi/3
        a2 = h < 4*np.pi/3
        a = a1 & a2         #第二种情况的花式索引
        tmp = np.cos(np.pi - h)
        r = I[i] * (1 - S[i])
        g = I[i]*(1+S[i]*np.cos(h-2*np.pi/3)/tmp)
        b = 3 * I[i] - r - g
        R[i][a] = r[a]
        G[i][a] = g[a]
        B[i][a] = b[a]
        #H大于等于240度小于360度
        a1 = h >= 4 * np.pi / 3
        a2 = h < 2 * np.pi
        a = a1 & a2             #第三种情况的花式索引
        tmp = np.cos(5 * np.pi / 3 - h)
        g = I[i] * (1-S[i])
        b = I[i]*(1+S[i]*np.cos(h-4*np.pi/3)/tmp)
        r = 3 * I[i] - g - b
        B[i][a] = b[a]
        G[i][a] = g[a]
        R[i][a] = r[a]
    rgb_img[:,:,0] = B*255
    rgb_img[:,:,1] = G*255
    rgb_img[:,:,2] = R*255
    return rgb_img

def run_main():
    
    #这是主函数
    
    #利用opencv读入图片
    rgb_img = cv2.imread('Green.png',cv2.IMREAD_COLOR)
    #进行颜色空间转换
    hsi_img = RGB2HSI(rgb_img)
    rgb_img2 = HSI2RGB(hsi_img)
    #opencv库的颜色空间转换结果
    hsi_img2 = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)
    rgb_img3 = cv2.cvtColor(hsi_img2,cv2.COLOR_HSV2BGR)
    cv2.imshow("Origin",rgb_img)
    cv2.imshow("HSI", hsi_img)
    cv2.imshow("RGB",rgb_img2)
    cv2.imshow("OpenCV_HSI",hsi_img2)
    cv2.imshow("OpenCV_RGB",rgb_img3)
    cv2.imwrite("HSI.jpeg",hsi_img)
    cv2.imwrite("RGB.jpeg", rgb_img2)
    cv2.imwrite("OpenCV_HSI.jpeg", hsi_img2)
    cv2.imwrite("OpenCV_RGB.jpeg", rgb_img3)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_main()

"""
import cv2
import numpy as np  
#描邊開始
img = cv2.imread('qrhauseqhx.png',0)
x = cv2.Sobel(img,cv2.CV_16S,1,0)
y = cv2.Sobel(img,cv2.CV_16S,0,1)
 
absX = cv2.convertScaleAbs(x)   # 转回uint8
absY = cv2.convertScaleAbs(y)
 
dst = cv2.addWeighted(absX,0.5,absY,0.5,0)
 
cv2.imshow("absX", absX)
cv2.imshow("absY", absY)
cv2.imshow("Result", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
#描邊結束