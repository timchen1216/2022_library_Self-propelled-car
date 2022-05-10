from cv2 import THRESH_BINARY_INV
import numpy as np
import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\7134.png')

def auto_canny(image, sigma=0.2):
    # 計算單通道像素強度的中位數
    v = np.median(image)
    # 選擇合適的lower和upper值，然後應用它們
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

def sharpen(img, sigma=100):    
    # sigma = 5、15、25
    blur_img = cv2.GaussianBlur(img, (0, 0), sigma)
    usm = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)

    return usm


def auto_thresh(image, sigma=0.2):
    # 計算單通道像素強度的中位數
    v = np.median(image)
    # 選擇合適的lower和upper值，然後應用它們
    lower = int(max(0, (1.0 - sigma) * v))
    ret, edged = cv2.threshold(image, lower, 255, THRESH_BINARY_INV)
    return edged

sharp = sharpen(img)
gray = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
th1 = auto_thresh(gray)
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(th1, kernal, iterations=2)
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
no_border = cv2.bitwise_and(th1, mask)



contours, hierarchy = cv2.findContours(
            no_border, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
imgContour = img.copy()
position = []
for cnt in contours:
    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 1)
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    if area > 150:                
        vertices = cv2.approxPolyDP(cnt, peri*0.05, True)
        x, y, w, h = cv2.boundingRect(vertices)                
        pos = [x, y, w, h]
        position.append(pos)
        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 2)

position.sort()

crop_img = []
for p in position:
    x, y, w, h = p            
    crop = no_border[y:y+h, x:x+w]
    crop_img.append(crop)

imgInput = []
for cro in crop_img:

    # resize to x*28 or 28*x
    himg, wimg = cro.shape[:2]
    if himg == wimg:
        cro = cv2.resize(cro, (28, 28))
    elif himg > wimg:
        cro = cv2.resize(cro, (int(wimg/himg*28), 28))
    elif himg < wimg:
        cro = cv2.resize(cro, (28, int(himg/wimg*28)))
    
    # resize to rectangle
    h, w = cro.shape
    bg = np.zeros([28,28], dtype=np.uint8)
    if h == w :
        pass
    elif h > w :
        l = (h-w)//2
        bg[0:28, l:l+w] = cro
    elif w > h :
        l = (w-h)//2
        bg[l:l+h, 0:28] = cro

    inp = cv2.resize(bg, (0, 0), fx=10, fy=10)
    imgInput.append(inp)





cv2.imshow('img', img)
print(img.shape)
cv2.imwrite('img.jpg', img)
cv2.imshow('sharp', sharp)
cv2.imshow('gray', gray)
cv2.imshow('th', th)
cv2.imshow('horimg', horImg)
cv2.imshow('verimg', verImg)
cv2.imshow('mask', mask)
cv2.imshow('no_border', no_border)
cv2.imwrite('no_border.jpg', no_border)
cv2.imshow('th1', th1)
cv2.imwrite('th1.jpg', th1)
cv2.imshow('imgContour', imgContour)
cv2.imwrite('imgContour.jpg', imgContour)


for l,inp in enumerate(imgInput):
    cv2.imshow('Input'+'-'+str(l), inp)
    cv2.imwrite('Input'+'-'+str(l)+'.jpg', inp)

cv2.waitKey(0)