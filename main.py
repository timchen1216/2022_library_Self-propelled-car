#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
from cv2 import Canny
import numpy as np
import time
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
count = 0
take = 0

#預先處理圖片: 灰階>高斯模糊>Canny邊緣偵測>膨脹>侵蝕


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray",imgGray)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # cv2.imshow("Blur",imgBlur)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
   # cv2.imshow("Canny",imgCanny)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    imgStack = stackImages(0.8, ([img, imgGray, imgBlur], [
                           imgCanny, imgDial, imgThres]))
    return imgThres


#框出標籤的矩形: 利用findContours找出封閉區域且有四個邊的部分將其框起來


def getContours(img):
    biggest = np.zeros([32, 1, 2])
    amount = 0  # 用來計算畫面內一次有幾個矩形
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
                amount = amount + 1
                approx = reorder(approx, amount)
                biggest[4*amount - 4:4*amount] = approx
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
    return biggest, amount


# 重新整理getContours算出的矩形四個點的矩陣，依序整理成左上>右上>左下>右下


def reorder(myPoints, amount):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

# 將框出的矩形擷取出來，並且能將直向的標籤反轉成橫向


def getWarp(img, biggest, amount):
    imgOutput = list()
    for i in range(1, amount+1):
        width = (biggest[4*i-1][0][0] - biggest[4*i-4][0][0])*2
        height = (biggest[4*i-1][0][1] - biggest[4*i-4][0][1])*2
        widthImg = width.astype('int32')
        heightImg = height.astype('int32')
        pts1 = np.float32(biggest[4*i-4:4*i])
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
            imgOutput[i-1] = cv2.resize(imgOutput[i-1], (heightImg, widthImg))
        else:
            imgOutput[i-1] = cv2.resize(imgOutput[i-1], (widthImg, heightImg))

    return imgOutput


# 判斷出何時將標籤拍照存入資料夾中
def getpicture(img, biggest, count, take):
    name = ['023', '714']
    if biggest[0][0][0] > 200 and biggest[0][0][0] < 400 and take == 0:
        count = count + 1  # 計算存入照片的數量
        cv2.imwrite(name[0] + "\\" + str(count) + ".png", img)
        take = 1  # take = 0(拍) take = 1(不拍)
    elif biggest[0][0][0] > 200 and biggest[0][0][0] < 400 and take == 1:
        pass
    elif biggest[0][0][0] > 400:
        take = 0
    else:
        pass
    return count, take

# 將各式img合成同一個視窗輸出，讓img能同框比較


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def preProcessing_2(img, i):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(img_gray, 150, 200)
    # cv2.imshow('canny'+str(i), canny)
    return canny


def find_contours(canny, img, i):
    imgContours = img.copy()
    Contours, hierarchy = cv2.findContours(
        canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    position = []
    for cnt in Contours:
        cv2.drawContours(imgContours, cnt, -1, (255, 0, 0), 1)
        arcLengthh = cv2.arcLength(cnt, False)
        area = cv2.contourArea(cnt)
        if arcLengthh > 200 and arcLengthh < 800:
            peri = cv2.arcLength(cnt, False)
            vertices = cv2.approxPolyDP(cnt, peri*0.02, False)
            x, y, w, h = cv2.boundingRect(vertices)
            pos = [x, y, w, h]
            position.append(pos)
            cv2.rectangle(imgContours, (x, y), (x+w, y+h), (0, 255, 0), 4)
    cv2.imshow('imgContours'+str(i), imgContours)

    position.sort()
    return imgContours, position


def crop(img, position):
    global crop
    crop_img = []
    for p in position:
        x, y, w, h = p
        if w > h:
            if y+h/2-w/2 > 0:
                crop = img[int(y+h/2-w/2):int(y+h/2+w/2), x:x+w]
            else:
                crop = img[0:0+w, x:x+w]
        elif h > w:
            if x+w/2-h/2 > 0:
                crop = img[y:y+h, int(x+w/2-h/2):int(x+w/2+h/2)]
            else:
                crop = img[y:y+h, 0:0+h]
        crop_img.append(crop)
    return crop_img


def predict(img, position,i):
    from keras.models import load_model
    model = load_model('my_model.h5')
    # model.summary()
    model.load_weights('my_model_weights.h5')

    crop_img = []
    for p in position:
        x, y, w, h = p
        if w > h:
            if y+h/2-w/2 > 0:
                crop = img[int(y+h/2-w/2):int(y+h/2+w/2), x:x+w]
            else:
                crop = img[0:0+w, x:x+w]
        elif h > w:
            if x+w/2-h/2 > 0:
                crop = img[y:y+h, int(x+w/2-h/2):int(x+w/2+h/2)]
            else:
                crop = img[y:y+h, 0:0+h]
        crop_img.append(crop)

    n = 1
    for cro in crop_img:
        cro = cv2.resize(cro, (480, 480))
        cro_gray = cv2.cvtColor(cro, cv2.COLOR_BGR2GRAY)
        img_3 = 255 - cro_gray
        img_3 = img_3.astype('float32')
        img_3_min = np.amin(img_3)
        img_4 = img_3 - np.amin(img_3)
        img_5 = 255 * img_4 / (np.amax(img_4))
        kernel = np.ones((5, 5), np.uint8)
        img_6 = cv2.dilate(img_5, kernel, iterations=3)
        img_7 = cv2.resize(img_6, (28, 28), 1)
        img_8 = img_6.astype('uint8')
        cv2.imshow('input'+str(n), img_8)

        x_test_image = np.reshape(img_7, (1, 28, 28))

        # convert 2-D 28x28 image to 4-D nx28x28x1  array
        x_Test4D = x_test_image.reshape(
            x_test_image.shape[0], 28, 28, 1).astype('float32')
        # normalize the image numbers to 0~1
        x_Test4D_normalize = (x_Test4D / np.amax(x_test_image))
        # prediction=model.predict(x_Test4D_normalize)
        prediction = model.predict(x_Test4D_normalize)
        #prediction = (model.predict(x_Test4D_normalize) > 0.5).astype("int32")
        # print(prediction.max())
        # print(prediction.shape)

        pre_max = prediction.max()
        for pre in range(prediction.shape[1]):
            if prediction[0, pre] == pre_max:
                pre_num = pre

        # print(pre_num)
        filename = '%s%s%s' % ('./numbers/number_', str(pre_num), '.jpg')
        img_9 = cv2.imread(filename)
        img_10 = cv2.resize(img_9, (480, 480), 1)
        cv2.imshow('inference'+str(i)+'-'+str(n), img_10)
        n += 1
    return


while True:
    success, img = cap.read()
    imgContour = img.copy()
    imgThres = preProcessing(img)
    biggest, amount = getContours(imgThres)
    #cv2.line(imgContour, (200,0), (200,480), (255,0,0), 2)
    #cv2.line(imgContour, (400,0), (400,480), (255,0,0), 2)
    cv2.imshow("SSS", imgContour)

    if amount >= 1:
        imgWarped = getWarp(img, biggest, amount)
        for i in range(1, amount+1):
            CANNY = preProcessing_2(imgWarped[i-1], i)
            img_1, Position = find_contours(CANNY, imgWarped[i-1], i)
            # cropping = crop(img_1, Position)
            # predict(imgWarped[i-1],Position,i)
            #   count,take = getpicture(imgWarped[i-1],biggest,count,take)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
