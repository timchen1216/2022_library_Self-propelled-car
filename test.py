import cv2

img = cv2.imread(
    r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\mnist_png\validation\0\54927.png')
print(img.shape)
cv2.imshow('img', img)

cv2.waitKey(0)
