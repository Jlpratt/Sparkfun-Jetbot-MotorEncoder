#!/usr/bin/env python
import qwiic_scmd
import qwiic_gpio
import time
import sys
import math
import numpy as np

class encoder:
    def __init__(self):
        self.myGPIO = qwiic_gpio.QwiicGPIO()
        if self.myGPIO.isConnected() == False:
            print("The Qwiic GPIO isn't connected to the system. Please check your connection")
            return
        self.startTime = 0
        self.Lcount = 0
        self.Rcount = 0
        self.rpsR = 0
        self.rpsL = 0
        self.currentLSpeed = 200
        self.currentRSpeed = 200
        self.myMotor = qwiic_scmd.QwiicScmd()
        self.motor_left_ID = 0
        self.motor_right_ID = 1
        self.currL = 0
        self.currR = 0
        self.prevL = 0
        self.prevR = 0
        self.gpioInit()
        self.initialTimeL = time.time()
        self.initialTimeR = time.time()
        self.minicountL = 0
        self.minicountR = 0
        self.runavgL = 0
        self.runavgR = 0
        self.rpsR = 0
        self.rpsL = 0
        self.boost = 15
        self.minpower = 150
        self.performFor = 10
        self.runtime = time.time() + self.performFor
        self.gate = 0
        self.elapseTimeL = 0
        self.elapseTimeR = 0
        self.runTotL = 0
        self.runTotR = 0
        self.count = 0
        self.drive()

    def drive(self):
        self.myMotor.enable()
        self.myMotor.set_drive(self.motor_left_ID, 0, self.currentLSpeed)
        self. myMotor.set_drive(self.motor_right_ID, 0, self.currentRSpeed)

    def gpioInit(self):
        self.myGPIO.begin()
        self.myGPIO.mode_5 = self.myGPIO.GPIO_IN
        self.myGPIO.mode_7 = self.myGPIO.GPIO_IN
        self.myGPIO.setMode()
        self.myGPIO.inversion_5 = self.myGPIO.NO_INVERT
        self.myGPIO.inversion_7 = self.myGPIO.NO_INVERT
        self.myGPIO.setInversion()
        self.currR = self.myGPIO.in_status_5
        self.currL = self.myGPIO.in_status_7
        self.prevL = self.currL
        self.prevR = self.currR

    def all_stop(self):
        self.myMotor.set_drive(self.motor_left_ID, 0, 0)
        self.myMotor.set_drive(self.motor_right_ID, 0, 0)
        self.myMotor.disable()

    def encoderRun(self):
        self.initialTimeL = time.time()
        self.initialTimeR = time.time()
        while time.time() < self.runtime:
            self.myGPIO.getGPIO()
            self.currR = self.myGPIO.in_status_5
            self.currL = self.myGPIO.in_status_7
            self.gate = 0
            if self.prevL != self.currL:
                self.swapTimeL = time.time()
                self.elapseTimeL = self.swapTimeL-self.initialTimeL
                self.rpsL = (np.pi/4)/(self.elapseTimeL*2)
                time.sleep(0.01)
                self.initialTimeL = self.swapTimeL
                #print('Left RPS')
                #print(self.rpsL)
                self.gate = 1
                self.Lcount = self.Lcount + 1
                self.runTotL = self.runTotL + self.rpsL
                self.runavgL = self.runTotL/self.Lcount

            self.prevL = self.currL
            
            if self.prevR != self.currR:
                self.swapTimeR = time.time()
                self.elapseTimeR = self.swapTimeR-self.initialTimeR
                self.rpsR = (np.pi/4)/(self.elapseTimeR*2)
                time.sleep(0.01)
                self.initialTimeR = self.swapTimeR
                #print('Right RPS')
                #print(self.rpsR)
                self.gate = 1
                self.Rcount = self.Rcount + 1
                self.runTotR = self.runTotR + self.rpsR
                self.runavgR = self.runTotR/self.Rcount

            self.prevR = self.currR
            self.count = self.count+1
            if self.gate == 1:
                dif = self.rpsL - self.rpsR
                absdiff = np.absolute(dif)
                
                if absdiff > 0.05:
                    time.sleep(0.01)
                    if self.rpsL > self.rpsR:
                        self.currentLSpeed = self.currentLSpeed - 1
                        print('r')
                        print(self.currentRSpeed)
                        print('l')
                        print(self.currentLSpeed)
                        self.myMotor.set_drive(self.motor_left_ID, 0, self.currentLSpeed)
                        self.myMotor.set_drive(self.motor_right_ID, 0, self.currentRSpeed)
                        print("left lowered")
                        if self.currentLSpeed < self.minpower:
                            self.currentLSpeed = self.currentLSpeed+self.boost
                            self.currentRSpeed = self.currentRSpeed+self.boost
                            #return
                        #return
                    if self.rpsR > self.rpsL:
                        self.currentRSpeed = self.currentRSpeed - 1
                        print('r')
                        print(self.currentRSpeed)
                        print('l')
                        print(self.currentLSpeed)
                        self.myMotor.set_drive(self.motor_left_ID, 0, self.currentLSpeed)
                        self.myMotor.set_drive(self.motor_right_ID, 0, self.currentRSpeed)
                        print("right lowered")
                        if self.currentRSpeed < self.minpower:
                            self.currentLSpeed = self.currentLSpeed+self.boost
                            self.currentRSpeed = self.currentRSpeed+self.boost
                            #return
                        #return

def main():
    encoderTesting = encoder()
    encoderTesting.encoderRun()
    encoderTesting.all_stop()
    print('left average %5.3f.' % encoderTesting.runavgL)
    print('right average %5.3f.' % encoderTesting.runavgR)

if __name__ == '__main__':
    sys.exit(main())
