#!/usr/bin/python
#-*- coding: utf-8 -*-
import cv2
import numpy as np
import time

class Webcam2label:
    def __init__(self,img):
       self.img = img
       self.imgContour = img.copy()
       self.amount = 0 #用來計算畫面內一次有幾個矩形
       self.biggest = []
       self.imgOutput = []
       
#預先處理圖片: 灰階>高斯模糊>Canny邊緣偵測>膨脹>侵蝕
    def preProcessing(self,img):
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
        imgCanny = cv2.Canny(imgBlur,120,180)
        imgCCC = self.auto_canny(imgBlur)
        kernel = np.ones((5,5))
        imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
        imgThres = cv2.erode(imgDial,kernel,iterations=1)
        imgDial1 = cv2.dilate(imgCCC,kernel,iterations=2)
        imgThres1 = cv2.erode(imgDial1,kernel,iterations=1)
        imgStack = self.stackImages(0.8,([img,imgGray,imgThres1],[imgCanny,imgCCC,imgThres]))
        # cv2.imshow("Stack",imgStack)
        return imgThres                
    
    
    def auto_canny(self,image, sigma=0.2):
    # 計算單通道像素強度的中位數
       v = np.median(image)
    # 選擇合適的lower和upper值，然後應用它們
       lower = int(max(0, (1.0 - sigma) * v))
       upper = int(min(255, (1.0 + sigma) * v))
       edged = cv2.Canny(image, lower, upper)
       return edged

#框出標籤的矩形: 利用findContours找出封閉區域且有四個邊的部分將其框起來
    def getContours(self,img):
        self.amount = 0
        contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>3000: 
                #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                if len(approx) == 4 :
                    approx = self.reorder(approx)
                    width = (((approx[0][0][0]-approx[1][0][0])**2 + (approx[0][0][1]-approx[1][0][1])**2)**0.5)
                    height = (((approx[0][0][0]-approx[2][0][0])**2 + (approx[0][0][1]-approx[2][0][1])**2)**0.5)
                    #print ("Area",area)
                    #print ("Calculate",width*height)
                    if width*height < area*1.5 and width*height > area*0.5:
                       self.amount += 1
                       self.biggest.append(approx)
                       cv2.drawContours(self.imgContour, cnt, -1, (255, 0, 0), 3)
        return self.amount

#重新整理getContours算出的矩形四個點的矩陣，依序整理成左上>右上>左下>右下 
    def reorder (self,myPoints):
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
    def getWarp(self,img):
        for i in range (1,self.amount+1):
             width = (((self.biggest[i-1][0][0][0]-self.biggest[i-1][1][0][0])**2 + (self.biggest[i-1][0][0][1]-self.biggest[i-1][1][0][1])**2)**0.5)*2
             height = (((self.biggest[i-1][0][0][0]-self.biggest[i-1][2][0][0])**2 + (self.biggest[i-1][0][0][1]-self.biggest[i-1][2][0][1])**2)**0.5)*2
             widthImg = width.astype('int32')
             heightImg = height.astype('int32')
             pts1 = np.float32(self.biggest[i-1][0:4])
             if widthImg < heightImg: 
                  #pts2 = np.float32([[widthImg, 0], [widthImg, heightImg], [0, 0], [0, heightImg]])
                  pts2 = np.float32([[0, heightImg], [0, 0], [widthImg, heightImg], [widthImg, 0]])
             else :    
                  pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
             matrix = cv2.getPerspectiveTransform(pts1, pts2)
             self.imgOutput.append (cv2.warpPerspective(img, matrix, (widthImg, heightImg)))
             cutw = int(widthImg/50)
             cuth = int(heightImg/50)
             if widthImg <= 0 or heightImg <= 0:
                 pass
             elif widthImg < heightImg:
                  self.imgOutput[i-1]=cv2.resize(self.imgOutput[i-1],(heightImg, widthImg))
                  self.imgOutput[i-1] = self.imgOutput[i-1][cutw:widthImg-cutw,cuth:heightImg-cuth]
             else :
                  self.imgOutput[i-1] = self.imgOutput[i-1][cuth:heightImg-cuth,cutw:widthImg-cutw]
        return self.imgOutput

#將各式img合成同一個視窗輸出，讓img能同框比較        
    def stackImages(self,scale,imgArray):
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
 


