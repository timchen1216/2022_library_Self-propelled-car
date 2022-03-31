import numpy as np
import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\11.png')

img = cv2.resize(img, (100,100))
cv2.imshow('img', img)

cv2.waitKey(0)