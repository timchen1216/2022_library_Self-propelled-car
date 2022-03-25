import numpy as np
import cv2

img = cv2.imread(r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\038.png')
height, weight, channel = img.shape
sy, ly, sx, lx = int(0.1*height), int(0.9*height) , int(0.1*weight), int(0.9*weight)
img1 = img[sy:ly, sx:lx]
imgGray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
print(imgGray.dtype)

cv2.imshow('img',img)
cv2.imshow('img1',img1)
cv2.imshow('gray',imgGray)
cv2.waitKey(0)