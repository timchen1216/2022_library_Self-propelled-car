import cv2

img = cv2.imread(r'C:\Users\timch\MyPython\opencv_test\12345.png')
print(img.shape)
cv2.imshow('img', img)
img_1 = cv2.resize(img, (480, 480))
print(img_1.shape)
cv2.imshow('img_1', img_1)

cv2.waitKey(0)