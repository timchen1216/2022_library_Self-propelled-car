import numpy as np
import cv2


class img2lable:
    def __init__(self, img):
        self.imgContour = img.copy()
        self.biggest = np.zeros([20, 1, 2])
        self.amount = 0  # 用來計算畫面內一次有幾個矩形
        self.count = 0
        self.take = 0
        self.imgArray = []

    #預先處理圖片: 灰階>高斯模糊>Canny邊緣偵測>膨脹>侵蝕
    def preProcessing(self, img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray",imgGray)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        # cv2.imshow("Blur",imgBlur)
        imgCanny = cv2.Canny(imgBlur, 200, 200)
       # cv2.imshow("Canny",imgCanny)
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
        imgThres = cv2.erode(imgDial, kernel, iterations=1)
        return imgThres

    #框出標籤的矩形: 利用findContours找出封閉區域且有四個邊的部分將其框起來
    def getContours(self, img):
        contours, hierarchy = cv2.findContours(
            img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 5000:
                #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                self.approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
                #print ("approx",len(cnt))
                if len(self.approx) == 4:
                    self.amount = self.amount + 1
                    self.approx = img2lable.reorder(self)
                    self.biggest[4*self.amount - 4:4*self.amount] = self.approx
                    cv2.drawContours(self.imgContour, cnt, -1, (255, 0, 0), 3)
        return self.biggest, self.amount

    # 重新整理getContours算出的矩形四個點的矩陣，依序整理成左上>右上>左下>右下
    def reorder(self):
        myPoints = self.approx.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), np.int32)
        add = myPoints.sum(1)
        myPointsNew[0] = myPoints[np.argmin(add)]
        myPointsNew[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis=1)
        myPointsNew[1] = myPoints[np.argmin(diff)]
        myPointsNew[2] = myPoints[np.argmax(diff)]
        return myPointsNew

    # 將框出的矩形擷取出來，並且能將直向的標籤反轉成橫向
    def getWarp(self, img):
        if self.amount >= 1:
            imgOutput = list()
            for i in range(1, self.amount+1):
                width = (self.biggest[4*i-1][0][0] - self.biggest[4*i-4][0][0])*2
                height = (self.biggest[4*i-1][0][1] - self.biggest[4*i-4][0][1])*2            
                widthImg = width.astype('int32')
                heightImg = height.astype('int32')
                pts1 = np.float32(self.biggest[4*i-4:4*i])
                if widthImg < heightImg:
                    #pts2 = np.float32([[widthImg, 0], [widthImg, heightImg], [0, 0], [0, heightImg]])
                    pts2 = np.float32(
                        [[0, heightImg], [0, 0], [widthImg, heightImg], [widthImg, 0]])
                else:
                    pts2 = np.float32(
                        [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                imgOutput.append(cv2.warpPerspective(
                    img, matrix, (widthImg, heightImg)))            
                if 0 < widthImg < heightImg :
                    imgOutput[i-1] = cv2.resize(imgOutput[i-1],
                                                (heightImg, widthImg))
                elif 0 < heightImg < widthImg:
                    imgOutput[i-1] = cv2.resize(imgOutput[i-1],
                                                (widthImg, heightImg))

        return imgOutput

    # 判斷出何時將標籤拍照存入資料夾中
    def getpicture(self, img):
        name = ['023', '714']
        if self.biggest[0][0][0] > 200 and self.biggest[0][0][0] < 400 and self.take == 0:
            self.count = self.count + 1  # 計算存入照片的數量
            cv2.imwrite(name[0] + "\\" + str(self.count) + ".png", img)
            self.take = 1  # take = 0(拍) take = 1(不拍)
        elif self.biggest[0][0][0] > 200 and self.biggest[0][0][0] < 400 and self.take == 1:
            pass
        elif self.biggest[0][0][0] > 400:
            self.take = 0
        else:
            pass
        return self.count, self.take


# frameWidth = 640
# frameHeight = 480
# cap = cv2.VideoCapture(0)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)


# while True:
#     success, img = cap.read()
#     label = img2lable(img)
#     imgContour = img.copy()
#     imgThres = label.preProcessing(img)
#     biggest, amount = label.getContours(imgThres)
#     #cv2.line(imgContour, (200,0), (200,480), (255,0,0), 2)
#     #cv2.line(imgContour, (400,0), (400,480), (255,0,0), 2)
#     cv2.imshow("SSS", imgContour)

#     if amount >= 1:
#         imgWarped = label.getWarp(img)
#         for i in range(1, amount+1):
#             cv2.imshow("Warp"+str(i), imgWarped[i-1])
#             count, take = label.getpicture(imgWarped[i-1])

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
