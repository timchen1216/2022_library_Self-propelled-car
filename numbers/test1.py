import numpy as np
import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\6.jpg')
white = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\white.jpg')
cv2.imshow('img', img)
# cv2.imshow('white', white)

# resize to x*28 or 28*x
himg, wimg, channel = img.shape
if himg == wimg:
    img = cv2.resize(img, (28, 28))
elif himg > wimg:
    img = cv2.resize(img, (int(wimg/himg*28), 28))
elif himg < wimg:
    img = cv2.resize(img, (28, int(himg/wimg*28)))

# gray & binary thresh
cro_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th2 = cv2.threshold(cro_gray, 150, 255, cv2.THRESH_BINARY_INV) 

# resize to rectangle
h, w = th2.shape
bg = np.zeros([28,28], dtype=np.uint8)
if h == w :
    pass
elif h > w :
    l = (h-w)//2
    bg[0:28, l:l+w] = th2
elif w > h :
    l = (w-h)//2
    bg[l:l+h, 0:28] = th2




img = cv2.resize(img, (0, 0), fx=10, fy=10)
th2 = cv2.resize(th2, (0, 0), fx=10, fy=10)
bg = cv2.resize(bg, (0, 0), fx=10, fy=10)

cv2.imshow('resize', img)
cv2.imshow('th2', th2)
cv2.imshow('bg', bg)


cv2.waitKey(0)
