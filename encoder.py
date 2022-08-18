#!/usr/bin/env python
import qwiic_scmd
import qwiic_gpio
import time
from collections import deque

class Encoder:
    def __init__(self):
        self.myMotor = qwiic_scmd.QwiicScmd()
        self.d = deque(maxlen=300)
        self.myGPIO = qwiic_gpio.QwiicGPIO()
        self.UpdateTime = 0.05

    def gpioSetup(self):
        if self.myGPIO.isConnected() == False:
            print("The Qwiic GPIO isn't connected to the system. Please check your connection")
            return

                #count = 0
        self.myGPIO.begin()
        self.myGPIO.mode_4 = self.myGPIO.GPIO_IN
        self.myGPIO.mode_5 = self.myGPIO.GPIO_IN
        self.myGPIO.mode_6 = self.myGPIO.GPIO_IN
        self.myGPIO.mode_7 = self.myGPIO.GPIO_IN
        self.myGPIO.setMode()
        self.myGPIO.inversion_4 = self.myGPIO.NO_INVERT
        self.myGPIO.inversion_5 = self.myGPIO.NO_INVERT
        self.myGPIO.inversion_6 = self.myGPIO.NO_INVERT
        self.myGPIO.inversion_7 = self.myGPIO.NO_INVERT
        self.myGPIO.setInversion()
        self.myGPIO.getGPIO()

    def left(self):
        self.prevLOn = 3
        self.prevLTw = 3
        self.countLeft = 0
        self.startTimeL = time.time()
        self.myGPIO.getGPIO()
        self.currLOn = self.myGPIO.in_status_6
        self.currLTw = self.myGPIO.in_status_7
        if self.prevLOn == 3:
                self.prevLOn = self.currLOn
                self.prevLTw = self.currLTw
        if self.currLOn != self.prevLOn:
            self.countLeft = self.countLeft+1
        if self.currLTw != self.prevLTw:
            self.countLeft = self.countLeft+1
        self.prevLOn = self.currLOn
        self.prevLTw = self.currLTw
        if self.startTimeL < (time.time()-self.UpdateTime):
            self.startTimeL = time.time()
            self.LeftRPM = self.countLeft/540/self.UpdateTime*60
            #print(self.LeftRPM)
            self.countLeft = 0
        return self.LeftRPM

    def right(self):
        self.prevROn = 3
        self.prevRTw = 3
        self.countRight = 0
        self.startTimeR = time.time()
        self.myGPIO.getGPIO()
        self.currROn = self.myGPIO.in_status_4
        self.currRTw = self.myGPIO.in_status_5
        if self.prevROn == 3:
                self.prevROn = self.currROn
                self.prevRTw = self.currRTw

        if self.currROn != self.prevROn:
            self.countRight = self.countRight+1
        if self.currRTw != self.prevRTw:
            self.countRight = self.countRight+1
        self.prevROn = self.currROn
        self.prevRTw = self.currRTw
        if self.startTimeR < (time.time()-self.UpdateTime):
            self.startTimeR = time.time()
            self.RightRPM = self.countRight/540/self.UpdateTime*60
            #print(self.RightRPM)
            self.countRight = 0    
        return self.RightRPM




