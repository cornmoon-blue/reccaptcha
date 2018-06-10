# -*- coding: utf-8 -*-
# Thanks to Jerry Yang's contribution.

import  cv2
import numpy as np
from PIL import Image,ImageFilter
from pyocr import pyocr
import os
import re

'''
captchadir = 'path-to-your-captcha-files'
if os.path.exists(captchadir):
	dir_files = os.listdir(captchadir)
	for dir_file in dir_files:
		file_path = os.path.join(captchadir,dir_file)
		#print file_path
else:
	print "Dir not exists."
'''
imgName = 'path-to-your-captcha-files\xx.jpg'

#调整图片的对比度和亮度
img=cv2.imread(imgName)
#cv2.imshow('img',img)

rows,cols,channels=img.shape
dst=img.copy()

a=1.5 
b=100
for i in range(rows):
    for j in range(cols):
        for c in range(3):
            color=img[i,j][c]*a+b
            if color>255:
                dst[i,j][c]=255
            elif color<0:
                dst[i,j][c]=0

#cv2.imwrite('img1.png',dst)
cv2.namedWindow("captcha",0);
cv2.resizeWindow("captcha", 240, 100)
#cv2.imshow('test8',dst)
#cv2.waitKey(0)

#对图片实现高斯模糊
kernel_size = (3, 3);
sigma = 0;
gaosi = cv2.GaussianBlur(dst, kernel_size, sigma);
#cv2.imshow("test8",gaosi)
#cv2.waitKey(0)

#整体磨皮
#双边模糊系数
bilateralFilterVal = 1
mop = cv2.bilateralFilter(gaosi,bilateralFilterVal,bilateralFilterVal*2,bilateralFilterVal/2) 
#cv2.imshow("test8",mop)
#cv2.waitKey(0)

#图像增强
finalImg = cv2.addWeighted(mop,0.9,dst,0.9,2)

im_gray = cv2.cvtColor(finalImg, cv2.COLOR_BGR2GRAY)  #灰度化
retval, im_at_fixed = cv2.threshold(im_gray, 250, 255, cv2.THRESH_BINARY)  #二值化
im_at_mean = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 111, 1) 

cv2.imwrite('img1.jpg', im_at_mean)

# 通过tesseract-OCR识别字符
im = Image.open('img1.jpg')
tools = pyocr.get_available_tools()[:]
if len(tools) == 0:
	print("No OCR tool found")
	sys.exit(1)

res = tools[0].image_to_string(im, lang='eng')
print "The length is: ", len(res), re.sub("[^A-Za-z0-9]", "", res)
print "The result is: "+res.replace(' ','')

cv2.imshow("captcha", im_at_mean)
cv2.waitKey(0)

cv2.destroyAllWindows()
