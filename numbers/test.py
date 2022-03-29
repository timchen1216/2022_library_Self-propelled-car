from turtle import position
import numpy as np
import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\7134.png')


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
horImg = th.copy()
verImg = th.copy()
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (50,3))
horImg = cv2.erode(horImg, kernal, iterations=1)
horImg = cv2.dilate(horImg, kernal, iterations=2)
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,50))
verImg = cv2.erode(verImg, kernal, iterations=1)
verImg = cv2.dilate(verImg, kernal, iterations=2)
mask = horImg + verImg
kernal_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
mask = cv2.dilate(mask, kernal_mask, iterations=3)
mask = 255 - mask
no_border = cv2.bitwise_and(th, mask)
canny = cv2.Canny(no_border, 0, 255)


contours, hierarchy = cv2.findContours(
            canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
imgContour = img.copy()
position = []
for cnt in contours:
    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 1)
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    if area > 200:                
        vertices = cv2.approxPolyDP(cnt, peri*0.05, True)
        x, y, w, h = cv2.boundingRect(vertices)                
        pos = [x, y, w, h]
        position.append(pos)
        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)




cv2.imshow('img', img)
cv2.imshow('gray', gray)
cv2.imshow('th', th)
cv2.imshow('horimg', horImg)
cv2.imshow('verimg', verImg)
cv2.imshow('mask', mask)
cv2.imshow('no_border', no_border)
cv2.imshow('canny', canny)
cv2.imshow('imgContour', imgContour)

cv2.waitKey(0)