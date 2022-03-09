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
        self.imgStack = img2lable.stackImages(
            0.8, ([img, imgGray, imgBlur], [imgCanny, imgDial, imgThres]))
        cv2.imshow("Stack", self.imgStack)
        return imgThres

    #框出標籤的矩形: 利用findContours找出封閉區域且有四個邊的部分將其框起來
    def getContours(self,img):
        contours, hierarchy = cv2.findContours(
            img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 5000:
                #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
                #print ("approx",len(cnt))
                if len(approx) == 4:
                    self.amount = self.amount + 1
                    approx = img2lable.reorder(approx, self.amount)
                    self.biggest[4*self.amount - 4:4*self.amount] = approx
                    cv2.drawContours(self.imgContour , cnt, -1, (255, 0, 0), 3)
        return self.biggest, self.amount

    # 重新整理getContours算出的矩形四個點的矩陣，依序整理成左上>右上>左下>右下
    def reorder(self):
        myPoints = self.amount.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), np.int32)
        add = myPoints.sum(1)
        myPointsNew[0] = myPoints[np.argmin(add)]
        myPointsNew[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis=1)
        myPointsNew[1] = myPoints[np.argmin(diff)]
        myPointsNew[2] = myPoints[np.argmax(diff)]
        return myPointsNew

    # 將框出的矩形擷取出來，並且能將直向的標籤反轉成橫向
    def getWarp(self,img):
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
            if widthImg < heightImg:
                imgOutput[i-1] = cv2.resize(imgOutput[i-1],
                                            (heightImg, widthImg))
            else:
                imgOutput[i-1] = cv2.resize(imgOutput[i-1],
                                            (widthImg, heightImg))

        return imgOutput

    # 判斷出何時將標籤拍照存入資料夾中
    def getpicture(self,img):
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

    # 將各式img合成同一個視窗輸出，讓img能同框比較
    def stackImages(self,scale):
        rows = len(self.imgArray)
        cols = len(self.imgArray[0])
        rowsAvailable = isinstance(self.imgArray[0], list)
        width = self.imgArray[0][0].shape[1]
        height = self.imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    if self.imgArray[x][y].shape[:2] == self.imgArray[0][0].shape[:2]:
                        self.imgArray[x][y] = cv2.resize(
                            self.imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        self.imgArray[x][y] = cv2.resize(
                            self.imgArray[x][y], (self.imgArray[0][0].shape[1], self.imgArray[0][0].shape[0]), None, scale, scale)
                    if len(self.imgArray[x][y].shape) == 2:
                        self.imgArray[x][y] = cv2.cvtColor(
                            self.imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(self.imgArray[x])
            self.imgStack = np.vstack(hor)
        else:
            for x in range(0, rows):
                if self.imgArray[x].shape[:2] == self.imgArray[0].shape[:2]:
                    self.imgArray[x] = cv2.resize(
                        self.imgArray[x], (0, 0), None, scale, scale)
                else:
                    self.imgArray[x] = cv2.resize(
                        self.imgArray[x], (self.imgArray[0].shape[1], self.imgArray[0].shape[0]), None, scale, scale)
                if len(self.imgArray[x].shape) == 2:
                    self.imgArray[x] = cv2.cvtColor(self.imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(self.imgArray)
            self.imgStack = hor
        return self.imgStack
