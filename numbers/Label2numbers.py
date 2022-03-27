import numpy as np
import cv2
from keras.models import load_model




class label2number:
    def __init__(self, imgLable):       
        self.img = []
        self.imgCanny = []              
        self.position = []
        self.crop_img = []
        self.predict = []

        # loadModel        
        self.model = load_model(r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\numbers\my_model.h5')
        self.model.load_weights(r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\numbers\my_model_weights.h5')
    
    def reimg(self,imgLable):
        height, weight, channel = imgLable.shape
        sy, ly, sx, lx = int(0.1*height), int(0.9*height) , int(0.1*weight), int(0.9*weight)
        self.img = imgLable[sy:ly, sx:lx]
        self.imgContour = self.img.copy()
        return self.img

    def auto_canny(self, image):
        sigma=0.33
        # 計算單通道像素強度的中位數
        v = np.median(image)

        # 選擇合適的lower和upper值，然後應用它們
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)

        return edged

    def preProcessing(self,img):
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)        
        imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)        
        imgCanny = label2number.auto_canny(self,imgBlur)        
        kernel = np.ones((5,5))
        imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
        imgThres = cv2.erode(imgDial,kernel,iterations=1)
        
        return imgGray,imgBlur,imgCanny,imgDial,imgThres
    
    def findContour(self,img):
        contours, hierarchy = cv2.findContours(
            img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            cv2.drawContours(self.imgContour, cnt, -1, (255, 0, 0), 4)
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            if True:                
                vertices = cv2.approxPolyDP(cnt, peri*0.05, True)
                x, y, w, h = cv2.boundingRect(vertices)                
                pos = [x, y, w, h]
                self.position.append(pos)
                cv2.rectangle(self.imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)

        self.position.sort()
        return self.imgContour
    
    def crop(self,img):
        self.crop_img = []
        for p in self.position:
            x, y, w, h = p            
            crop = img[y:y+h, x:x+w]
            self.crop_img.append(crop)
        return self.crop_img

    def prediction(self):
        imgInput = []
        for cro in self.crop_img:
            # resize to x*28 or 28*x
            himg, wimg = cro.shape[:2]
            if himg == wimg:
                cro = cv2.resize(cro, (28, 28))
            elif himg > wimg:
                cro = cv2.resize(cro, (int(wimg/himg*28), 28))
            elif himg < wimg:
                cro = cv2.resize(cro, (28, int(himg/wimg*28)))
            
            # gray & binary thresh
            cro_gray = cv2.cvtColor(cro, cv2.COLOR_BGR2GRAY)
            ret, th2 = cv2.threshold(cro_gray, 150, 255, cv2.THRESH_BINARY_INV) 

            # resize to rectangle
            h, w = th2.shape
            bg = np.zeros([28,28], dtype=np.uint8)
            if h == w :
                pass
            elif h > w :
                l = (h-w)//2
                bg[0:28, l:l+w] = th2
            elif w > h :
                l = (w-h)//2
                bg[l:l+h, 0:28] = th2

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
            # print(prediction.shape)


            pre_max = prediction.max()
            for i in range(prediction.shape[1]):
                if prediction[0,i] == pre_max:
                    self.predict.append(i)
            
        return self.predict,imgInput



img = cv2.imread(r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\038.png')
cv2.imshow('img', img)
main = label2number(img)
reimg = main.reimg(img)
imgGray,imgBlur,imgCanny,imgDial,imgThres = main.preProcessing(reimg)
imgContour = main.findContour(imgThres)
crop = main.crop(reimg)
predict,imgInput = main.prediction()

# cv2.imshow("Gray",imgGray)
# cv2.imshow("Blur",imgBlur)  
# cv2.imshow("Canny",imgCanny) 
# cv2.imshow('dilate', imgDial)
# cv2.imshow('erode', imgThres)
cv2.imshow('imgContour', imgContour)
print('img', img.shape)
print('reimg', reimg.shape)

# for i,cro in enumerate(crop):
#     cv2.imshow('inference'+str(i), cro)

for j,inp in enumerate(imgInput):
    cv2.imshow('Input'+str(j), inp)

print(predict)

cv2.waitKey(0)





    