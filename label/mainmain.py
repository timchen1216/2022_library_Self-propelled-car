#!/usr/bin/python
#-*- coding: utf-8 -*-
import cv2
import numpy as np
import time
from number import Webcam2label 
from car import Car

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
        success, img = cap.read()
        catch = Webcam2label(img)
        BMW = Car()
        BMW.setting()
        BMW.working()
        if BMW.counter % 2 == 1 :
            imgThres = catch.preProcessing(img)
            catch.getContours(imgThres) 
            cv2.imshow("SSS", catch.imgContour)
            if catch.amount >= 1:
              imgWarped=catch.getWarp(img)
              for i in range(1,catch.amount+1):
                  cv2.imshow("Warp"+str(i), imgWarped[i-1])
        else:
            pass
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

