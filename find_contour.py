import cv2
from cv2 import arcLength

img = cv2.imread(r'C:\Users\timch\MyPython\opencv_test\12345.png')
imgContour = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(img, 150, 200)
contours, hierarchy = cv2.findContours(
    canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

position = []
for cnt in contours:
    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 1)
    arcLengthh = cv2.arcLength(cnt, True)
    if arcLengthh > 100:
        peri = cv2.arcLength(cnt, False)
        vertices = cv2.approxPolyDP(cnt, peri*0.02, False)
        x, y, w, h = cv2.boundingRect(vertices)
        pos = [x, y, w, h]
        position.append(pos)
        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)

# sort position
position.sort()

# crop img
crop_img = []
for p in position:
    x, y, w, h = p
    if w > h :
        if y+h/2-w/2 > 0 :
            crop = img[int(y+h/2-w/2):int(y+h/2+w/2), x:x+w]
        else:
            crop = img[0:2*x+h, x:x+w]
    elif h > w :
        if x+w/2-h/2 > 0 :
            crop = img[y:y+h, int(x+w/2-h/2):int(x+w/2+h/2)]
        else :
            crop = img[y:y+h, 0:2*x+w]
    crop_img.append(crop)
n = 1
for cro in crop_img:
    cv2.imshow('crop'+str(n), cro)
    n += 1

cv2.imshow('img', img)
cv2.imshow('canny', canny)
cv2.imshow('imgContour', imgContour)

cv2.waitKey(0)
