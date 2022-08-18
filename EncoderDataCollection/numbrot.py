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
import csv

dL = deque(maxlen=30)
dR = deque(maxlen=30)
myGPIO = qwiic_gpio.QwiicGPIO()
runtime = time.time()+10
myMotor = qwiic_scmd.QwiicScmd()

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

def motor(RS, LS):
    myMotor.set_drive(0,0,RS)
    myMotor.set_drive(1,1,LS)
    myMotor.enable()
    #time.sleep(1)
    #print('hi')

def left(c):
    prevLOn = 3
    prevLTw = 3
    print('hi2')
    while time.time() < runtime:
        myGPIO.getGPIO()
        startTimeL = time.time()
        currLOn = myGPIO.in_status_6
        currLTw = myGPIO.in_status_7
        if prevLOn == 3:
            prevLOn = currLOn

        if prevLTw == 3:
            prevLTw = currLTw

        if currLOn != prevLOn:
            angVL = rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTimeL, dL)
            startTimeL = time.time()
            Ldat=['l',angVL]
            c = c+1
            #filewriter.writerow(Ldat)
        elif currLTw != prevLTw:
            angVL = rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTimeL, dL)
            startTimeL = time.time()
            Ldat = ['l',angVL]
            c = c+1
            #filewriter.writerow(Ldat)
        else: 1 == 1
        prevLOn = currLOn
        prevLTw = currLTw
    return c
        

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
    return avg_rps

def all_stop():
    myMotor.set_drive(0, 0, 0)
    myMotor.set_drive(0, 0, 0)
    myMotor.disable()

if __name__ == '__main__':
    gpioSetup()
    count = 0
    #motor(0,190)
    count = left(count)
    #count = count*360/526
    
    count = count/540*360
    print(count)
    all_stop()
