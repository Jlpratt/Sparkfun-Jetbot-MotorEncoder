# Sparkfun-Jetbot-MotorEncoder
Motor Encoder Code for Jetbots using Sparkfun hardware

## Hardware and Setup:
This repository is tailored for modified [Sparkfun Jetbots](https://www.sparkfun.com/products/18486)

### The two major modifications are as follows:
1. Addition of a [Sparkfun qwiic GPIO board](https://www.sparkfun.com/products/17047)
2. Replacement of the hobby motors with the [Hobby Motor with Encoder](https://www.sparkfun.com/products/16413)

#### Outside of component mounting parts there are a few other modifications to the jetbots used in the creation of this repository. These are optional and only truly affect the data found in the EncoderDataCollection/Setting_Data folder (which is part of this repository as more of a guideline, data should be taken for each Jetbot, and not used as coverall to reduce error in use.)
1. Motor Mounting hole locations on the lower chassis board were moved back half an inch to be more central and allow for easier turning.
2. Motors were taken from the original yellow hobby motors (1) and used to replace the motors within the Hobby Motors with Encoders (2), as the Hobby Motors with Encoders (2) were found to be less powerful than the original Hobby Motors (1). [Guide here](https://github.com/Jlpratt/Sparkfun-Jetbot-MotorEncoder/blob/9ddc63910c4ba56080ec4a598fcfce3009fc2665/Jetbot%20Motor%20Swap.pdf)
3. Foam within original wheel interior was replaced with 3D printed inserts

### Hardware Setup is as follows:
The Left Hall encoder output signals 1 and 2 go to the gpio pinouts 6 and 7 respectively

The Right Hall encoder output signals 1 and 2 go to the gpio pinouts 4 and 5 respectively

#### Note: The documentation for Hobby Motor with Encoder wiring setup is incorrect depending on the source used for setup (ie. Sparkfun's pinout sheet is in reverse order).

Pin 1 (brown wire) connects to the GPIO ground.

Pins 2 and 3 (red and orange wires respectively) correspond to encoder outputs 1 and 2 respectively.

Pin 4 (yellow wire) corresponds to the GPIO 3V connection.

Pins 5 and 6 (green and blue wires respectively) correspond to the desired motor driver pins for the motor.  

## Sparkfun Hall-Encoder Code Information
encoder.py contains an encoder class which can be used in combination with threading/multiprocessing to return the angular velocity of both wheels at once.

The EncoderDataCollection contains the files NewEncoderCode.py numbrot.py, data.m, a setting to velocity fit sheet, and a folder containing all data collected when running NewEncoderCode.py.
1. NewEncoderCode.py is used for acquiring velocity information over an array of motor settings and saving them to individual .csv files for each setting.
2. The file numbrot.py measures rotation in degrees.
3. Data.m takes the .csv generated by NewEncoderCode.py and averages it
4. MotorEncoderData_for_Fit_Function_Generation.xlsx is just a plot of the Data.m finaltable. This file does not create a fit for the data, and is more for easy visualization. Best fit results found utilizing the gaussian fit option within Matlab???s curve fitting tool.
    * The final fit function can be useful in creating a function that give an output for a desired angular velocity, however it should be verified in a controlled environment such as a motion capture area as variables such as slip and wheel misalignment hinder on-board localization.

Note: NewEncoderCode.py is the most up to date/functional file currently, and can be used as a template for multiprocessing and exporting data. The code avoids .csv exportation issues found in the files within the Outdated Encoder Code folder, in which data would only export for one motor/one motor at a time.

The numbrot.py file allows the user to spin the motor by hand and the file will output the degrees the motor was turned. This file still contains all comments used while troubleshooting, as well as the rotation_check() function which can create inaccurate readings if the angular velocity is high enough. (see below for more info)

All files within the Outdated Encoder Code folder are previous iterations of the motor encoder code. The code within this file is for the most part outdated, however, the "rotation_check():" function may prove useful if a negative motor value is possible or wanting to be measured. The function was replaced by a simpler count method to reduce output noise, and remove outliers created if the wheel spins faster than the code can update/account for.


