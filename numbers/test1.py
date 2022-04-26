from cv2 import THRESH_BINARY_INV
import numpy as np
import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\7134.png')

def sharpen(img, sigma=100):    
    # sigma = 5、15、25
    blur_img = cv2.GaussianBlur(img, (0, 0), sigma)
    usm = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)

    return usm

blur_img = cv2.GaussianBlur(img, (0, 0), 100)
sharp = sharpen(img)

cv2.imshow('img', img)
cv2.imshow('sharp', sharp)
cv2.imshow('blur', blur_img)

cv2.waitKey(0)