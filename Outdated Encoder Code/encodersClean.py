#!/usr/bin/env python
import qwiic_scmd
import qwiic_gpio
import time
import sys
import math
import statistics
from collections import deque

myMotor = qwiic_scmd.QwiicScmd()
global count
d = deque(maxlen=10) 

def gpioSetup():
    myGPIO = qwiic_gpio.QwiicGPIO()
    if myGPIO.isConnected() == False:
        print("The Qwiic GPIO isn't connected to the system. Please check your connection")
        return
    currentLSpeed = 200
    currentRSpeed = 0
    myMotor.set_drive(0,0,currentRSpeed)
    myMotor.set_drive(1,0,currentLSpeed)
    myMotor.enable()
    count = 0
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
    startTime = time.time()
    currLOn = myGPIO.in_status_7
    currLTw = myGPIO.in_status_6
    currROn = myGPIO.in_status_5
    currRTw = myGPIO.in_status_4
    prevLOn = currLOn
    prevLTw = currLTw
    prevROn = currROn
    prevRTw = currRTw
    runtime = time.time()+1.025
    rps = 0
    beginTim = time.time()
    
#ef leftMeas():
#   LStRotTime = time.time()

     
    while time.time() < runtime:
        myGPIO.getGPIO()  # This function updates each in_status_x variable
        currLOn = myGPIO.in_status_7
        currLTw = myGPIO.in_status_6
        currROn = myGPIO.in_status_5
        currRTw = myGPIO.in_status_4
        #print(currLOn)
        #print(prevLOn)
        if currLOn != prevLOn:
            rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTime)
            startTime = time.time()
        elif currLTw != prevLTw:
            rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTime)
            startTime = time.time()
        elif currROn != prevROn:
            rotation_check(currROn, currRTw, prevROn, prevRTw, startTime)
            startTime = time.time()
        elif currRTw != prevRTw:
            rotation_check(currROn, currRTw, prevROn, prevRTw, startTime)
            startTime = time.time()
        else :
            1==1
        prevLOn = currLOn
        prevLTw = currLTw
        prevROn = currROn
        prevRTw = currRTw           
        #print(startTime)
        #print(myGPIO.in_status_0)
        #print("GPIO 1:")
        #print(myGPIO.in_status_1)
        #print("GPIO 2:")
        #print(myGPIO.in_status_2)
        #print("GPIO 3:")
        #print(myGPIO.in_status_3)

       #print("GPIO 5:")
     #  print(myGPIO.in_status_5)
       #print("GPIO 6:")
       #print(myGPIO.in_status_6)
       #print("GPIO 7:")
       #print(myGPIO.in_status_7)
        

def all_stop():
    myMotor.set_drive(0, 0, 0)
    myMotor.set_drive(0, 0, 0)
    myMotor.disable()

def rotation_check(Cside1, Cside2, Pside1, Pside2, tiempo):
    global count
    newTime = time.time()
    newState = "{}{}".format(Cside1,Cside2)
    prevState = "{}{}".format(Pside1, Pside2)
    divTim = newTime - tiempo
    count = count+1
    #print(newState)
    #print(divTim)
    rps = 1/520/divTim/(2)
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
    d.append(rps)
    #print("RPS")
    #print(rps)
    avg_rps = statistics.mean(d)
    #print(avg_rps)
    vel = avg_rps*2*3.14*0.03
    print(vel,"m/s")


	
if __name__ == '__main__':
    
    count = 0
    gpioSetup()
    print(count)
    all_stop()

    sys.exit(1)
    all_stop()
