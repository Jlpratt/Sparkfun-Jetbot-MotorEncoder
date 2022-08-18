# Sparkfun-Jetbot-MotorEncoder
Motor Encoder Code for Jetbots using Sparkfun hardware

## Hardware and setup:

encoder.py contains an encoder class which can be used in combination with threading/multiprocessing to return the angular velocity of both wheels at once.

The EncoderDataCollection contains the file NewEncoderCode.py which is the code used for aquiring velocity information over an array of motor settings and saving them to individual .csv files for each setting. 

Note: NewEncoderCode.py is the most up to date/functional file currently, and can be used as a template for multiprocessing and exporting data. The code avoids .csv exportation issues found in the files within the Outdated Encoder Code folder, in which data would only export for one motor/one motor at a time. 

The numbrot.py file allows the user to spin the motor by hand and the file will output the degrees the motor was turned. This file still contains all comments used while troubleshooting, as well as the rotation_check() function which can create inacurate readings if the angular velocity is high enough. (see below for more info)

All files within the Outdated Encoder Code folder are previous itterations of the motor encoder code. The code within this file is for the most part outdated, however, the "rotation_check():" function may prove useful if a negative motor value is possible or wanting to be measured. The function was replaced by a simpler count method to reduce output noise, and remove outliers created if the wheel spins faster than the code can update/account for. 
