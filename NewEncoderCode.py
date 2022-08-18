#!/usr/bin/env python
import qwiic_scmd
import qwiic_gpio
import time
import sys
from collections import deque
import csv
import threading
import os

myMotor = qwiic_scmd.QwiicScmd()

d = deque(maxlen=300)
myGPIO = qwiic_gpio.QwiicGPIO()

currentLSpeed = 250
currentRSpeed = 250

def motor(RS, LS):
    myMotor.set_drive(0,0,RS)
    myMotor.set_drive(1,0,LS)
    myMotor.enable()
    time.sleep(1)


def gpioSetup():
 
    if myGPIO.isConnected() == False:
        print("The Qwiic GPIO isn't connected to the system. Please check your connection")
        return

    #count = 0
    myGPIO.begin()
    myGPIO.mode_4 = myGPIO.GPIO_IN
    myGPIO.mode_5 = myGPIO.GPIO_IN
    myGPIO.mode_6 = myGPIO.GPIO_IN
    myGPIO.mode_7 = myGPIO.GPIO_IN
    myGPIO.setMode()
    myGPIO.inversion_4 = myGPIO.NO_INVERT
    myGPIO.inversion_5 = myGPIO.NO_INVERT
    myGPIO.inversion_6 = myGPIO.NO_INVERT
    myGPIO.inversion_7 = myGPIO.NO_INVERT
    myGPIO.setInversion()
    myGPIO.getGPIO()

def left():
    prevLOn = 3
    prevLTw = 3
    countLeft = 0
    startTimeL = time.time()

    while time.time()<runtime:
        while time.time() < runtime:     
            myGPIO.getGPIO()
            currLOn = myGPIO.in_status_6
            currLTw = myGPIO.in_status_7

            if prevLOn == 3:
    	        prevLOn = currLOn

            if prevLTw == 3:
    	        prevLTw = currLTw

            if currLOn != prevLOn:
                countLeft = countLeft+1

            elif currLTw != prevLTw:
                countLeft = countLeft+1
            else: 1 == 1  
            prevLOn = currLOn
            prevLTw = currLTw
            if startTimeL < (time.time() - 0.01):
                startTimeL = time.time()
                RPS = countLeft/540/0.01
                countLeft = 0
                Ldat=['l', RPS]
                d.append(Ldat)

def right():
    prevROn = 3
    prevRTw = 3
    startTimeR = time.time()
    countRight = 0
    while time.time() < runtime:
        while time.time() < runtime: 
            myGPIO.getGPIO()
            currROn = myGPIO.in_status_4
            currRTw = myGPIO.in_status_5
            if prevROn == 3:
    	        prevROn = currROn
            if prevRTw == 3:
    	        prevRTw = currRTw 
            if currROn != prevROn:
                countRight = countRight+1
            elif currRTw != prevRTw:
                countRight=countRight+1
            else: 1==1
            prevROn = currROn
            prevRTw = currRTw
            if startTimeR < (time.time() - 0.01):
                startTimeR = time.time()
                RPS = countRight/540/0.01
                countRight = 0
                Rdat=['r', RPS]
                d.append(Rdat)


        
        
        
        
    

def all_stop():
    myMotor.set_drive(0, 0, 0)
    myMotor.set_drive(0, 0, 0)
    myMotor.disable()


def turnAround(): 
    #Note: Function does not turn the jetbot 180 deg, it just changes the orientation so it stays in the mocap area
    motor(150,-150)
    time.sleep(0.15)





if __name__ == '__main__':
    for i in range(1,125):
        runtime = time.time() +3
        sped = 255-(i-1)

        gpioSetup()
        motor(sped,sped)
        gpioSetup()
        tr = threading.Thread(target=right)
        tl = threading.Thread(target=left)
        tr.start()

        tl.start()

        tl.join()
        tr.join()
        filename = '%s.csv' %sped
        os.remove(filename)

        with open(filename, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerows(d)

        all_stop()
        time.sleep(0.5)
        turnAround()
        all_stop()
        time.sleep(0.5)
        d.clear()
        time.sleep(0.01)
        
    #file.close
    sys.exit(all_stop())
