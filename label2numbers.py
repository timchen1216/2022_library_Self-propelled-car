from json.tool import main
import numpy as np
import cv2
from keras.models import load_model



class label2number:
    def __init__(self, img):
        self.imgContour = img.copy()

    def loadModel(self):        
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

    # def findContour(self):




        


img = cv2.imread(r'C:\Users\timch\MyPython\opencv_test\12345.png')
cv2.imshow('img', img)
main = label2number(img)
imgGray,imgBlur,imgCanny,imgDial,imgThres = main.preProcessing(img)
cv2.imshow("Gray",imgGray)
cv2.imshow("Blur",imgBlur)  
cv2.imshow("Canny",imgCanny) 
cv2.imshow('dilate', imgDial)
cv2.imshow('erode', imgThres)
cv2.waitKey(0)





    