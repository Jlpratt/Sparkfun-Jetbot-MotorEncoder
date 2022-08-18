# Sparkfun-Jetbot-MotorEncoder
Motor Encoder Code for Jetbots using Sparkfun hardware

encoder.py contains an encoder class which can be used in combination with threading/multiprocessing to return the angular velocity of both wheels at once.

The EncoderDataCollection contains the file NewEncoderCode.py which is the code used for aquiring velocity information over an array of motor settings and saving them to individual .csv files for each setting. 

Note: NewEncoderCode.py is the most up to date/functional file currently, and can be used as a template for multiprocessing and exporting data. The code avoids .csv exportation issues found in (folder with all bad code), in which data would only export for one motor/one motor at a time.
