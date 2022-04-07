import numpy as np
import cv2
import os

for i in range(1,4,1):
    initial_count = 0
    dir = 'C:/Users/timch\MyPython/2022_library_Self-propelled-car/'+str(i)
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    for j in range(1,initial_count+1,1):
        img = cv2.imread("C:/Users/timch\MyPython/2022_library_Self-propelled-car/"+str(i)+'/'+str(j)+'.jpg')
        cv2.imshow('img'+str(i)+'-'+str(j),img)
    print(initial_count)

cv2.waitKey(0)

