import numpy as np
import cv2
from keras.models import load_model



class label2number:
    def __init__(self, img):
        self.imgContour = img.copy()
        self.position = []
        self.crop_img = []
        self.predict = []

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
    
    def findContour(self,imgThres):
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
    
    def crop(self,img):
        for p in self.position:
            x, y, w, h = p
            if w > h :
                if y+h/2-w/2 > 0 :
                    crop = img[int(y+h/2-w/2):int(y+h/2+w/2), x:x+w]
                else:
                    crop = img[0:0+w, x:x+w]
            elif h > w :
                if x+w/2-h/2 > 0 :
                    crop = img[y:y+h, int(x+w/2-h/2):int(x+w/2+h/2)]
                else :
                    crop = img[y:y+h, 0:0+h]
            self.crop_img.append(crop)
        return self.crop_img

    def prediction(self):
        for cro in self.crop_img:
            cro = cv2.resize(cro, (480, 480))
            cro_gray = cv2.cvtColor(cro, cv2.COLOR_BGR2GRAY)
            img_3 = 255 - cro_gray
            img_3 = img_3.astype('float32')
            img_4 = img_3 - np.amin(img_3)
            img_5 = 255 * img_4 / (np.amax(img_4))
            kernel = np.ones((5, 5), np.uint8)
            img_6 = cv2.dilate(img_5, kernel, iterations=3)
            img_7 = cv2.resize(img_6, (28, 28), 1)
            # cv2.imshow('input'+str(n), img_8)

            x_test_image = np.reshape(img_7, (1, 28, 28))

            # convert 2-D 28x28 image to 4-D nx28x28x1  array
            x_Test4D = x_test_image.reshape(
                x_test_image.shape[0], 28, 28, 1).astype('float32')
            # normalize the image numbers to 0~1
            x_Test4D_normalize = (x_Test4D / np.amax(x_test_image))
            # prediction=model.predict(x_Test4D_normalize)
            prediction = self.model.predict(x_Test4D_normalize)
            #prediction = (model.predict(x_Test4D_normalize) > 0.5).astype("int32")
            # print(prediction.max())
            # print(prediction.shape)


            pre_max = prediction.max()
            for i in range(prediction.shape[1]):
                if prediction[0,i] == pre_max:
                    self.predict.append(i)
            
        return self.predict



img = cv2.imread(r'C:\Users\timch\MyPython\opencv_test\369.png')
cv2.imshow('img', img)
main = label2number(img)
imgGray,imgBlur,imgCanny,imgDial,imgThres = main.preProcessing(img)
imgContour = main.findContour(imgThres)
crop = main.crop(img)
predict = main.prediction()

cv2.imshow("Gray",imgGray)
cv2.imshow("Blur",imgBlur)  
cv2.imshow("Canny",imgCanny) 
cv2.imshow('dilate', imgDial)
cv2.imshow('erode', imgThres)
cv2.imshow('imgContour', imgContour)

# for i,cro in enumerate(crop):
#     cv2.imshow('inference'+str(i), cro)

print(predict)

cv2.waitKey(0)





    