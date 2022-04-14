import numpy as np
import cv2
import os
from keras.models import load_model
import pymongo

client = pymongo.MongoClient("mongodb+srv://che:che@mycluster.6t3lr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.book
correct=db.correct
detect=db.detect
mis=db.mis


class label2number:
    def __init__(self, imgLable):       
        self.imgCanny = []              
        self.position = []
        self.crop_img = []
        self.predict = []

        # loadModel        
        self.model = load_model(r'C:\Users\User\2022_library_Self-propelled-car\numbers\my_model.h5')
        self.model.load_weights(r'C:\Users\User\2022_library_Self-propelled-car\numbers\my_model_weights.h5')

    def sharpen(img, sigma=100):    
        # sigma = 5、15、25
        blur_img = cv2.GaussianBlur(img, (0, 0), sigma)
        usm = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)

        return usm


    def auto_thresh(image, sigma=0.2):
        # 計算單通道像素強度的中位數
        v = np.median(image)
        # 選擇合適的lower和upper值，然後應用它們
        lower = int(max(0, (1.0 - sigma) * v))
        ret, edged = cv2.threshold(image, lower, 255, cv2.THRESH_BINARY_INV)
        return edged
    
    def reimg(self,imgLable):
        self.imgContour = imgLable.copy()
        sharp = label2number.sharpen(img)
        gray = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
        th1 = label2number.auto_thresh(gray)
        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        dilate = cv2.dilate(th1, kernal, iterations=1)
        th = cv2.erode(dilate, kernal, iterations=1)
        horImg = th.copy()
        verImg = th.copy()
        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (60,2))
        horImg = cv2.erode(horImg, kernal, iterations=1)
        horImg = cv2.dilate(horImg, kernal, iterations=2)
        kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (2,60))
        verImg = cv2.erode(verImg, kernal, iterations=1)
        verImg = cv2.dilate(verImg, kernal, iterations=2)
        mask = horImg + verImg
        kernal_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        mask = cv2.dilate(mask, kernal_mask, iterations=2)
        mask = 255 - mask
        self.no_border = cv2.bitwise_and(th1, mask)
        self.imgCanny = cv2.Canny(self.no_border, 0, 255)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        self.imgDial = cv2.dilate(self.no_border,kernel,iterations=1)
        self.imgThres = cv2.erode(self.imgDial,kernel,iterations=1)
        return self.imgDial, self.imgThres, self.no_border, gray, th

   
    def findContour(self):
        contours, hierarchy = cv2.findContours(
            self.no_border, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            cv2.drawContours(self.imgContour, cnt, -1, (255, 0, 0), 1)
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            if area > 150:                
                vertices = cv2.approxPolyDP(cnt, peri*0.02, True)
                x, y, w, h = cv2.boundingRect(vertices)                
                pos = [x, y, w, h]
                self.position.append(pos)
                cv2.rectangle(self.imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)

        self.position.sort()
        return self.imgContour
    
    def crop(self,imgLable):
        self.crop_img = []
        for p in self.position:
            x, y, w, h = p            
            crop = self.no_border[y:y+h, x:x+w]
            self.crop_img.append(crop)
        return self.crop_img

    def prediction(self):
        imgInput = []
        for cro in self.crop_img:

            # # preprocessing
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            # Dial = cv2.dilate(cro,kernel,iterations=2)
            # cro = cv2.erode(Dial,kernel,iterations=2) 

            # resize to x*28 or 28*x
            himg, wimg = cro.shape[:2]
            if himg == wimg:
                cro = cv2.resize(cro, (28, 28))
            elif himg > wimg:
                cro = cv2.resize(cro, (int(wimg/himg*28), 28))
            elif himg < wimg:
                cro = cv2.resize(cro, (28, int(himg/wimg*28)))
            
            # resize to rectangle
            h, w = cro.shape
            bg = np.zeros([28,28], dtype=np.uint8)
            if h == w :
                pass
            elif h > w :
                l = (h-w)//2
                bg[0:28, l:l+w] = cro
            elif w > h :
                l = (w-h)//2
                bg[l:l+h, 0:28] = cro

            inp = cv2.resize(bg, (0, 0), fx=10, fy=10)
            imgInput.append(inp)

            x_test_image = np.reshape(bg, (1, 28, 28))

            # convert 2-D 28x28 image to 4-D nx28x28x1  array
            x_Test4D = x_test_image.reshape(
                x_test_image.shape[0], 28, 28, 1).astype('float32')
            # normalize the image numbers to 0~1
            x_Test4D_normalize = (x_Test4D / np.amax(x_test_image))
            # prediction=model.predict(x_Test4D_normalize)
            prediction = self.model.predict(x_Test4D_normalize)
            #prediction = (model.predict(x_Test4D_normalize) > 0.5).astype("int32")
            # print(prediction.max())
            print(prediction)


            pre_max = prediction.max()
            for i in range(0,10,1):
                if prediction[0,i] == pre_max:
                    self.predict.append(i)
            
        return self.predict,imgInput
    
detect.drop()
for i in range(1,4,1):
    initial_count = 0
    dir = 'C:/Users/User/2022_library_Self-propelled-car/'+str(i)
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    for j in range(1,initial_count+1,1):
        img = cv2.imread("C:/Users/User/2022_library_Self-propelled-car/"+str(i)+'/'+str(j)+'.jpg')
        # cv2.imshow('img'+str(i)+'-'+str(j),img)
        main = label2number(img)
        imgDial, imgThres, no_border, gray, th = main.reimg(img)
        imgContour = main.findContour()
        crop = main.crop(img)
        predict,imgInput = main.prediction()
        # cv2.imshow('imgContour'+str(i)+'-'+str(j), imgContour)
        # cv2.imshow('imgDial'+str(i)+'-'+str(j), imgDial)
        # cv2.imshow('imgThres'+str(i)+'-'+str(j), imgThres)
        cv2.imshow('no_border'+str(i)+'-'+str(j), no_border)
        # cv2.imshow('gray'+str(i)+'-'+str(j), gray)
        # cv2.imshow('th'+str(i)+'-'+str(j), th)


        # for i,cro in enumerate(crop):
        #     cv2.imshow('inference'+str(i), cro)

        # for l,inp in enumerate(imgInput):
        #     cv2.imshow('Input'+str(i)+'-'+str(j)+'-'+str(l), inp)

        print(predict)
       
        if len(predict) == 4:
            num = str(predict[0])+str(predict[1])+str(predict[2])+"."+str(predict[3])
            num = float(num)
            contain = correct.find_one({
                "編號" : num
            })
            if contain != None:    
                result = detect.find_one({
                    "書櫃" : i,
                    "編號" : num
                })

                if result == None:
                    detect.insert_one({
                        "書櫃":i,
                        "編號":num
                    })
            
            
    # print(initial_count)

cv2.waitKey(0)
