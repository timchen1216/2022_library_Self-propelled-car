#!/usr/bin/python
#-*- coding: utf-8 -*-
import cv2
import numpy as np
import time
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
count = 0
take = 0

#預先處理圖片: 灰階>高斯模糊>Canny邊緣偵測>膨脹>侵蝕
def preProcessing(img):
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Gray",imgGray) 
        imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
        #cv2.imshow("Blur",imgBlur) 
        imgCanny = cv2.Canny(imgBlur,200,200)
       # cv2.imshow("Canny",imgCanny) 
        kernel = np.ones((5,5))
        imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
        imgThres = cv2.erode(imgDial,kernel,iterations=1)
        imgStack = stackImages(0.8,([img,imgGray,imgBlur],[imgCanny,imgDial,imgThres]))
        cv2.imshow("Stack",imgStack)
        return imgThres                

#框出標籤的矩形: 利用findContours找出封閉區域且有四個邊的部分將其框起來
def getContours(img):
        biggest = np.zeros([20,1,2])
        amount = 0 #用來計算畫面內一次有幾個矩形
        contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>5000: 
                #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                #print ("approx",len(cnt))
                if len(approx) == 4:
                    amount = amount + 1
                    approx = reorder(approx,amount)
                    biggest[4*amount - 4:4*amount] = approx
                    cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
        return biggest,amount

#重新整理getContours算出的矩形四個點的矩陣，依序整理成左上>右上>左下>右下 
def reorder (myPoints,amount):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

#將框出的矩形擷取出來，並且能將直向的標籤反轉成橫向
def getWarp(img,biggest,amount):
    imgOutput = list()
    for i in range (1,amount+1):
         width = (biggest[4*i-1][0][0] - biggest[4*i-4][0][0])*2
         height = (biggest[4*i-1][0][1] - biggest[4*i-4][0][1])*2
         widthImg = width.astype('int32')
         heightImg = height.astype('int32')
         pts1 = np.float32(biggest[4*i-4:4*i])
         if widthImg < heightImg: 
              #pts2 = np.float32([[widthImg, 0], [widthImg, heightImg], [0, 0], [0, heightImg]])
              pts2 = np.float32([[0, heightImg], [0, 0], [widthImg, heightImg], [widthImg, 0]])
         else :    
              pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
         matrix = cv2.getPerspectiveTransform(pts1, pts2)
         imgOutput.append (cv2.warpPerspective(img, matrix, (widthImg, heightImg)))
         if widthImg < heightImg:
              imgOutput[i-1]=cv2.resize(imgOutput[i-1],(heightImg, widthImg))
         else :
              imgOutput[i-1]= cv2.resize(imgOutput[i-1],(widthImg, heightImg))
         
    return imgOutput
     
     

#判斷出何時將標籤拍照存入資料夾中    
def  getpicture(img,biggest,count,take) :
         name = ['023','714']
         if biggest[0][0][0] > 200  and biggest[0][0][0] < 400  and take == 0:
             count = count + 1 #計算存入照片的數量
             cv2.imwrite(name[0] + "\\" +  str(count) +  ".png",img)
             take = 1 #take = 0(拍) take = 1(不拍)
         elif biggest[0][0][0] > 200  and biggest[0][0][0] < 400  and take == 1:
             pass
         elif  biggest[0][0][0] > 400:
             take = 0
         else :
             pass
         return count,take
 
#將各式img合成同一個視窗輸出，讓img能同框比較        
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver        
      
while True:
        success, img = cap.read()
        imgContour=img.copy()
        imgThres = preProcessing(img)
        biggest,amount = getContours(imgThres) 
        #cv2.line(imgContour, (200,0), (200,480), (255,0,0), 2)
        #cv2.line(imgContour, (400,0), (400,480), (255,0,0), 2)
        cv2.imshow("SSS", imgContour)
        
        if amount >= 1:
          imgWarped=getWarp(img,biggest,amount)
          for i in range(1,amount+1):
              cv2.imshow("Warp"+str(i), imgWarped[i-1])
              count,take = getpicture(imgWarped[i-1],biggest,count,take)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
  


