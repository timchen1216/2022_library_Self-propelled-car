from cv2 import THRESH_BINARY_INV
import numpy as np
import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\2\2.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
sigma=0.2
# 計算單通道像素強度的中位數
v = np.median(gray)
# 選擇合適的lower和upper值，然後應用它們
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))

ret, th1 = cv2.threshold(gray, v, 255, THRESH_BINARY_INV)
ret, th2 = cv2.threshold(gray, lower, 255, THRESH_BINARY_INV)
ret, th3 = cv2.threshold(gray, upper, 255, THRESH_BINARY_INV)

cv2.imshow('gray', gray)
cv2.imshow('th1', th1)
cv2.imshow('th2', th2)
cv2.imshow('th3', th3)


cv2.waitKey(0)