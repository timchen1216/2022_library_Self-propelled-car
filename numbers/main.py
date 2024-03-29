import numpy as np
import cv2
from Img2label import Webcam2label
from Label2numbers import label2number


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)



prediction = []

while True:
    success, img = cap.read()
    label = Webcam2label(img)
    imgThres = label.preProcessing(img)
    amount = label.getContours(imgThres)
    cv2.imshow("Input", img)
        
    
    if amount >= 1:
        imgWarped = label.getWarp(img)
        for i in range(1, amount+1):
            cv2.imshow("Warp"+str(i), imgWarped[i-1])
            number = label2number(imgWarped[i-1])
            reimg = number.reimg(imgWarped[i-1])
            cv2.imshow("reimg"+str(i), reimg)
            imgGray,imgBlur,imgCanny,imgDial,imgThress = number.preProcessing(reimg)
            # cv2.imshow('imgThress', imgThress)
            contours = number.findContour(imgThress)
            cv2.imshow('imgcontours', contours)
            crop_img = number.crop(reimg)
            for j, cro in enumerate(crop_img):
                 cv2.imshow("In"+str(j), cro)
            predict,imgInput = number.prediction()
            print('predict :',predict)
            prediction.append(predict)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  