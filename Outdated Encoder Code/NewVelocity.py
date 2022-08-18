#!/usr/bin/env python
from concurrent.futures import process
import qwiic_scmd
import qwiic_gpio
import time
import sys
import math
import statistics
from collections import deque
from multiprocessing import Process

myMotor = qwiic_scmd.QwiicScmd()
#global count #use for debug
dL = deque(maxlen=30)
dR = deque(maxlen=30)
myGPIO = qwiic_gpio.QwiicGPIO()
runtime = time.time() + 300
currentLSpeed = 200
currentRSpeed = 200

def motor(RS, LS):
    myMotor.set_drive(0,0,currentRSpeed)
    myMotor.set_drive(1,0,currentLSpeed)
    myMotor.enable()

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
    speed = 50
    maxl = 0
    maxset = 0
    angVL = 0
    while time.time() < runtime:     
        myGPIO.getGPIO()
        startTimeL = time.time()
        currLOn = myGPIO.in_status_7
        currLTw = myGPIO.in_status_6
        if prevLOn == 3:
    	    prevLOn = currLOn
        
        if prevLTw == 3:
    	    prevLTw = currLTw
        
        if currLOn != prevLOn:
            angVL = rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTimeL, dL)
            startTimeL = time.time()
            print("l", angVL)
        elif currLTw != prevLTw:
            angVL = rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTimeL, dL)
            startTimeL = time.time()
            print("l", angVL)
        else: 1 == 1  
        #myMotor.set_drive(1,0,speed)
        time.sleep(0.5)
        prevLOn = currLOn
        prevLTw = currLTw
        if maxl < angVL:
            maxl = angVL
            maxset = speed
        speed = speed +1
        myMotor.set_drive(1,1,speed)
        #myMotor.enable()
        print(speed)
        print("the maximum velocity for left is", maxl, "at setting" , maxset)
        

def right():
    prevROn = 3
    prevRTw = 3
    speedr = 50
    maxr = 0
    maxsetr = 0
    angVR = 0
    print("begin Right")
    while time.time() < runtime: 
        
        myGPIO.getGPIO()
        startTimeR = time.time()
        currROn = myGPIO.in_status_4
        currRTw = myGPIO.in_status_5
        if prevROn == 3:
    	    prevROn = currROn
        if prevRTw == 3:
    	    prevRTw = currRTw 
        if currROn != prevROn:
            angVR = rotation_check(currROn, currRTw, prevROn, prevRTw, startTimeR, dR)
            startTimeR = time.time()
            #print("r", angVR)
        elif currRTw != prevRTw:
            angVR = rotation_check(currROn, currRTw, prevROn, prevRTw, startTimeR, dR)
            startTimeR = time.time()
            #print("r", angVR)
        else: 1==1
        myMotor.set_drive(0,0,speedr)
        time.sleep(2)
        prevROn = currROn
        prevRTw = currRTw
        if maxr < angVR:
            maxr = angVR
            maxsetr = speedr
        speedr = speedr+1
        print("the maximum velocity for right is", maxr, "at setting" , maxsetr)
        #myMotor.set_drive(0,0,speedr)

         


def all_stop():
    myMotor.set_drive(0, 0, 0)
    myMotor.set_drive(0, 0, 0)
    myMotor.disable()


def rotation_check(Cside1, Cside2, Pside1, Pside2, tiempo,side):
    #global count
    newTime = time.time()
    newState = "{}{}".format(Cside1,Cside2)
    prevState = "{}{}".format(Pside1, Pside2)
    divTim = newTime - tiempo
    #count = count+1
    #print(newState)
    #print(divTim)
    rps = 1/520/divTim/(360)
    if newState == "00":
        if prevState == "10":
            rps = rps
        elif prevState == "01":
            rps=-rps
    if newState == "01":
        if prevState == "00":
            rps = rps
        elif prevState == "11":
            rps=-rps
    if newState == "11":
        if prevState == "01":
            rps = rps
        elif prevState == "10":
            rps=-rps
    if newState == "10":
        if prevState == "11":
            rps = rps
        elif prevState == "00":
            rps=-rps
    Cside1 = Pside1
    Cside2 = Pside2
    side.append(rps)
    #print("RPS")
    #print(rps)
    avg_rps = statistics.mean(side)
    #print(avg_rps)
    vel = avg_rps*2*3.14*0.03
    #print(vel,"m/s")
    #return avg_rps
    return vel

#def findmax(vl, vr):
#    speed = 0
#    while time.time() < runtime:
#        motor(speed,speed)
#        time.sleep(1)
#        speed = speed+1
#        if maxr < vr:
#            maxr = vr
#            maxpowerR = speed
#        if maxl < vl:
#            maxl = vl
#            maxpowerL = speed
#    print("max speed left came at setting", maxpowerL, "with a velocity of", maxl)
#    print("max speed right came at setting", maxpowerR, "with a velocity of", maxr)    



if __name__ == '__main__':
    #count = 0
    motor(currentRSpeed, currentLSpeed)
    gpioSetup()
    pL = Process(target=left)
    pL.start()
    pR = Process(target=right)
    pR.start()
    #pS = Process(target=findmax(pL, pR))
    #pS.start()
    pL.join()
    pR.join()
    #pS.join()

    
    all_stop()

    sys.exit(all_stop())
