from turtle import position
import numpy as np
import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\2\2.jpg')

def auto_canny(image, sigma=0.2):
    # 計算單通道像素強度的中位數
    v = np.median(image)
    # 選擇合適的lower和upper值，然後應用它們
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),1)
canny = auto_canny(blur)
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(canny, kernal, iterations=2)
th = cv2.erode(dilate, kernal, iterations=1)
horImg = th.copy()
verImg = th.copy()
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (60,3))
horImg = cv2.erode(horImg, kernal, iterations=1)
horImg = cv2.dilate(horImg, kernal, iterations=2)
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,60))
verImg = cv2.erode(verImg, kernal, iterations=1)
verImg = cv2.dilate(verImg, kernal, iterations=2)
mask = horImg + verImg
kernal_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
mask = cv2.dilate(mask, kernal_mask, iterations=2)
mask = 255 - mask
no_border = cv2.bitwise_and(th, mask)



contours, hierarchy = cv2.findContours(
            no_border, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
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