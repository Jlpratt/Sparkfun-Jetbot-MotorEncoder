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
#import xlsxwriter
#with open('250.csv', 'w', newline='') as csvfile:
#    filewriter = csv.writer(csvfile)
myMotor = qwiic_scmd.QwiicScmd()
#global count #use for debug
dL = deque(maxlen=300)
dR = deque(maxlen=300)
myGPIO = qwiic_gpio.QwiicGPIO()
#runtime = time.time() + 7
currentLSpeed = 250
currentRSpeed = 250

def motor(RS, LS):
    myMotor.set_drive(0,0,RS)
    myMotor.set_drive(1,0,LS)
    myMotor.enable()
    time.sleep(1)
    #print('hi')

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
    #print('hi2')
    while time.time() < runtime:     
        myGPIO.getGPIO()
        startTimeL = time.time()
        currLOn = myGPIO.in_status_6
        currLTw = myGPIO.in_status_7
        #print(startTimeL)
        if prevLOn == 3:
    	    prevLOn = currLOn

        if prevLTw == 3:
    	    prevLTw = currLTw

        if currLOn != prevLOn:
            angVL = rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTimeL, dL)
            startTimeL = time.time()
            Ldat=['l',angVL]
            filewriter.writerow(Ldat)
        elif currLTw != prevLTw:
            angVL = rotation_check(currLOn, currLTw, prevLOn, prevLTw, startTimeL, dL)
            startTimeL = time.time()
            Ldat = ['l',angVL]
            filewriter.writerow(Ldat)
        else: 1 == 1  
        prevLOn = currLOn
        prevLTw = currLTw
      

def right():
    prevROn = 3
    prevRTw = 3
    #print('hi3')
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
            Rdat=['r',angVR]
            filewriter.writerow(Rdat)
        elif currRTw != prevRTw:
            angVR = rotation_check(currROn, currRTw, prevROn, prevRTw, startTimeR, dR)
            startTimeR = time.time()
            Rdat=['r', angVR]
            filewriter.writerow(Rdat)
        else: 1==1
        prevROn = currROn
        prevRTw = currRTw
        
        
    

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
    #print(divTim)
    #count = count+1
    #print(newState)
    #print(divTim)
    rps = (1/540/divTim)
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
    #Cside1 = Pside1
    #Cside2 = Pside2
    #side.append(rps)
    #print("RPS")
    #print(rps)
    #avg_rps = statistics.mean(side)
    #print(avg_rps)
    #vel = avg_rps*2*3.14*0.03
    #print(vel,"m/s")
    #return avg_rps
    return rps

def goStraight(rt, lt, rts, lts):
    initRS = rts
    initLS = lts
    while time.time() < runtime:
        diff = rt - lt
        if rt > lt:
            currentSpeedR = initLS + diff*2
            myMotor.set_drive(0,0,currentSpeedR)
        elif rt < lt:
            currentSpeedL = initRS + diff*2
            myMotor.set_drive(1,0,currentSpeedL)

def turnAround():
    myMotor.set_drive(0,0,250)
    myMotor.set_drive(1,1,-250)
    myMotor.enable()
    time.sleep(3)


#if __name__ == '__main__':
#
#    motor(250, 250)
#    gpioSetup()
#    pL = Process(target=left)
#    pR = Process(target=right)
#    with open('250.csv', 'w', newline='') as csvfile:
#        filewriter = csv.writer(csvfile)
#        #count = 0
#        #pL = Process(target=left)
#        pL.start()
#        #pR = Process(target=right)
#        pR.start()
#        #pS = Process(target=goStraight)
#        #pS.start()
#        pL.join()
#        pR.join()
#        #pS.join()
#        #all_stop()
#        #time.sleep(1)    
#    turnAround()
#    all_stop()
#    #file.close
#    sys.exit(all_stop())

if __name__ == '__main__':
    for i in range(1):
        runtime = time.time() +10
        sped = 250-(i-1)
        print(sped)
        gpioSetup()
        motor(250,250)
        pL = Process(target=left)
        pR = Process(target=right)
        gpioSetup()
        filename = '%s.csv' %sped
        with open(filename, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            #count = 0
            #pL = Process(target=left)
            pL.start()
            #pR = Process(target=right)
            pR.start()
            #pS = Process(target=goStraight)
            #pS.start()
            pL.join()
            pR.join()
            #pS.join()
            #all_stop()
            #time.sleep(1)    
        #turnAround()
        all_stop()
        time.sleep(0.5)
        
    #file.close
    sys.exit(all_stop())
