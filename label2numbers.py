from json.tool import main
import numpy as np
import cv2
from keras.models import load_model



class label2number:
    def __init__(self, img):
        self.imgContour = img.copy()
        self.position = []

        # loadModel        
        self.model = load_model('my_model.h5')
        self.model.load_weights('my_model_weights.h5')

    def preProcessing(self,img):
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)        
        imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)        
        imgCanny = cv2.Canny(imgBlur,200,200)        
        kernel = np.ones((5,5))
        imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
        imgThres = cv2.erode(imgDial,kernel,iterations=1)
        
        return imgGray,imgBlur,imgCanny,imgDial,imgThres
    
    def findContour(self):
        contours, hierarchy = cv2.findContours(
            imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for cnt in contours:
            cv2.drawContours(self.imgContour, cnt, -1, (255, 0, 0), 1)
            arcLengthh = cv2.arcLength(cnt, True)
            if arcLengthh > 100 and arcLengthh < 800:
                peri = cv2.arcLength(cnt, False)
                vertices = cv2.approxPolyDP(cnt, peri*0.02, False)
                x, y, w, h = cv2.boundingRect(vertices)
                pos = [x, y, w, h]
                self.position.append(pos)
                cv2.rectangle(self.imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)
        cv2.imshow('imgContour', self.imgContour)

        self.position.sort()
        return self.imgContour






        


img = cv2.imread(r'C:\Users\timch\MyPython\opencv_test\12345.png')
cv2.imshow('img', img)
main = label2number(img)
imgGray,imgBlur,imgCanny,imgDial,imgThres = main.preProcessing(img)
imgContour = main.findContour()
# cv2.imshow("Gray",imgGray)
# cv2.imshow("Blur",imgBlur)  
# cv2.imshow("Canny",imgCanny) 
# cv2.imshow('dilate', imgDial)
# cv2.imshow('erode', imgThres)
cv2.imshow('imgContour', imgContour)
cv2.waitKey(0)





    