import RPi.GPIO as GPIO
import time

class Car:
    def __init__(self):
       self.counter = 0 #遇到黑色橫線會+1 藉此得知車子目前所在的區域
       self.in1 = 24
       self.in2 = 23
       self.ena = 25
       self.in3 = 17
       self.in4 = 27
       self.enb = 22
       self.ltrack = 5
       self.mtrack = 6
       self.rtrack = 13
       self.hold = False
       
    def setting(self):   # 設腳位跟馬達的PWM
       GPIO.setwarnings(False)
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(self.in1,GPIO.OUT)
       GPIO.setup(self.in2,GPIO.OUT)
       GPIO.setup(self.ena,GPIO.OUT) 
       GPIO.setup(self.in3,GPIO.OUT)
       GPIO.setup(self.in4,GPIO.OUT)
       GPIO.setup(self.enb,GPIO.OUT)
       GPIO.setup(self.mtrack,GPIO.IN,pull_up_down=GPIO.PUD_UP)
       GPIO.setup(self.ltrack,GPIO.IN,pull_up_down=GPIO.PUD_UP)
       GPIO.setup(self.rtrack,GPIO.IN,pull_up_down=GPIO.PUD_UP)
       GPIO.output(self.in1,GPIO.LOW)
       GPIO.output(self.in2,GPIO.LOW)
       GPIO.output(self.in3,GPIO.LOW)
       GPIO.output(self.in4,GPIO.LOW)
       p1=GPIO.PWM(self.ena,1000)
       p2=GPIO.PWM(self.enb,1000)
       p1.start(35)
       p2.start(35)
       
    def front(self):
       GPIO.output(self.in1,GPIO.HIGH)
       GPIO.output(self.in2,GPIO.LOW)
       GPIO.output(self.in3,GPIO.HIGH)
       GPIO.output(self.in4,GPIO.LOW)
    
    def stop(self):
       GPIO.output(self.in1,GPIO.LOW)
       GPIO.output(self.in2,GPIO.LOW)
       GPIO.output(self.in3,GPIO.LOW)
       GPIO.output(self.in4,GPIO.LOW)   
    
    def left(self):
       GPIO.output(self.in1,GPIO.HIGH)
       GPIO.output(self.in2,GPIO.LOW)
       GPIO.output(self.in3,GPIO.LOW)
       GPIO.output(self.in4,GPIO.HIGH)   
       
    def right(self):
       GPIO.output(self.in1,GPIO.LOW)
       GPIO.output(self.in2,GPIO.HIGH)
       GPIO.output(self.in3,GPIO.HIGH)
       GPIO.output(self.in4,GPIO.LOW) 
       
    def back(self):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)    
       
    def walkside(self): #在非偵測書本時的行進方式(只會往前)
       if GPIO.input(self.rtrack) == GPIO.LOW and GPIO.input(self.ltrack) == GPIO.LOW:
          if GPIO.input(self.mtrack) == GPIO.LOW:
              self.back()
          else:
              self.front()
       elif GPIO.input(self.rtrack) == GPIO.HIGH and GPIO.input(self.ltrack) == GPIO.HIGH and GPIO.input(self.mtrack) == GPIO.HIGH: 
              if self.hold == False:
                 self.front()
                 self.counter += 1   
                 self.hold = True
              else :
                 self.front() 
                 self.hold = False
       elif GPIO.input(self.ltrack) == GPIO.HIGH:#CAR NEED TURN LEFT
              self.left()
       elif GPIO.input(self.rtrack) == GPIO.HIGH:#CAR NEED TURN right
              self.right()    
       else :
              self.front()
       time.sleep(0.5) 
       
    def book(self): #在偵測書本時的行進方式(會停一下走一下)
       if GPIO.input(self.rtrack) == GPIO.LOW and GPIO.input(self.ltrack) == GPIO.LOW:
          if GPIO.input(self.mtrack) == GPIO.LOW:
              self.back()
          else:
              self.front()
              time.sleep(0.2)
              self.stop()
              time.sleep(1)
       elif GPIO.input(self.rtrack) == GPIO.HIGH and GPIO.input(self.ltrack) == GPIO.HIGH and GPIO.input(self.mtrack) == GPIO.HIGH: 
              if self.hold == False:
                 self.front()
                 self.counter += 1   
                 self.hold = True
              else :
                 self.front() 
                 self.hold = False      
       elif GPIO.input(self.ltrack) == GPIO.HIGH:#CAR NEED TURN LEFT
              self.left()
       elif GPIO.input(self.rtrack) == GPIO.HIGH:#CAR NEED TURN right
              self.right()    
       else:
              self.front()
       time.sleep(0.5)   
       
    def working(self): #counter奇數時為偵測書本區，偶數則為其他區域
        if (self.counter%2 == 0):
            self.walkside()
        else:
            self.book()



     
        
       
        
       
        
       
        
       
        
       
        
           
 