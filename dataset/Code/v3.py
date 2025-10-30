"""
Welcome to Project:EnAble v3.0
Project:EnAble is under Copyright © 2023 Jeron Osguthorpe

Project: EnAble
Author: Jeron Osguthorpe
Version: v3.1.0 - Beta

BASIC INFORMATION REGARDING PROJECT: ENABLE
Git Hub Organization Link: https://github.com/projectenable
Git Hub Repository Link: https://github.com/projectenable/Project-Enable
Website: https://enable.codingtricksyt.com
Email: enable@codingtricksyt.com
YouTube: https://youtube.com/codingtricks
Twitter: https://twitter.com/proj_enable
License, Code of Conduct, and Contributing: https://github.com/projectenable/Project-Enable
Donate: https://enable.codingtricksyt.com/

ChatGPT Involment: ChatGPT was used to help create part of the project. Among ChatGPT, 
Copilot was also used to help create this part of the project. ChatGPT is a project by OpenAI. 
Copilot is a project by OpenAI and GitHub. Both projects are under the MIT License.

Total Project Lines of Code: 1137

"""
# IMPORTING LIBRARIES
from fileinput import close
from multiprocessing.resource_sharer import stop 
import RPi.GPIO as GPIO 
import time
from time import sleep
import os
import random
import serial

# SETTING MODES
GPIO.setmode(GPIO.BCM)

# IMPORT MICROBIT SERIAL INFORMATION
z1baudrate = 115200
z1port = '/dev/ttyACM0' # This is the port that the microbit is connected to
z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2

# SERVO MOTORS
GPIO.setup(5, GPIO.OUT) # index finger
GPIO.setup(6, GPIO.OUT) # middle finger
GPIO.setup(13, GPIO.OUT) # ring finger
GPIO.setup(19, GPIO.OUT) # pinky finger
GPIO.setup(26, GPIO.OUT) # thumb

# Initialize PWM on all servo pins
index_servo = GPIO.PWM(5, 50) # index finger
index_servo.start(0) # Initialize Index Servo
middle_servo = GPIO.PWM(6, 50) # middle finger
middle_servo.start(0) # Initialize Middle Servo
ring_servo = GPIO.PWM(13, 50) # ring finger
ring_servo.start(0) # Initialize Ring Servo
pinky_servo = GPIO.PWM(19, 50) # pinky finger
pinky_servo.start(0) # Initialize Pinky Servo
thumb_servo = GPIO.PWM(26, 50) # thumb
thumb_servo.start(0) # Initialize Thumb Servo



# PRESSURE SENSORS
# Pin Definitions
CLK = 12
MISO = 16
MOSI = 20
CS = 21

# Set Up GPIO using BCM numbering
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(MOSI, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

# Function to read data from ADC using software SPI
def read_adc(channel):
    # Chip Select Signal
    GPIO.output(CS, GPIO.HIGH)
    GPIO.output(CS, GPIO.LOW)

    # Start Bit
    GPIO.output(MOSI, GPIO.HIGH)
    GPIO.output(CLK, GPIO.HIGH)
    GPIO.output(CLK, GPIO.LOW)

    # Channel Selection
    for i in range(3):
        if (channel & (1 << i)) == 0:
            GPIO.output(MOSI, GPIO.LOW)
        else:
            GPIO.output(MOSI, GPIO.HIGH)
        GPIO.output(CLK, GPIO.HIGH)
        GPIO.output(CLK, GPIO.LOW)
    
    # Dummy Bit
    GPIO.output(MOSI, GPIO.LOW)
    GPIO.output(CLK, GPIO.HIGH)
    GPIO.output(CLK, GPIO.LOW)

    # Read Data
    data = 0
    for i in range(11):
        GPIO.output(CLK, GPIO.HIGH)
        if GPIO.input(MISO) == GPIO.HIGH:
            data |= 1 << (10 - i)
        GPIO.output(CLK, GPIO.LOW)
    
    # Chip Select Signal
    GPIO.output(CS, GPIO.HIGH)

    return data

# DEFINE SENSITIVITY THRESHOLDS
low_threshold = 50
medium_threshold = 100
high_threshold = 150

# CANCEL ALL FUNCTION
def cancel_all():
    print("Stopping All")
    stopall = True
    GPIO.cleanup()

#  MAIN PROGRAM
def start(threshold):
    global stopall
    stopall = False
    while not stopall:

        # READ DATA

        # Add Microbit Data
        size = z1serial.inWaiting()
        data = z1serial.read(size)

        # Globalize Variables
        global index_pressure_sensor
        global middle_pressure_sensor
        global ring_pressure_sensor
        global pinky_pressure_sensor
        global thumb_pressure_sensor

        # Read Pressure Sensor Data
        index_pressure_sensor = read_adc(0)
        middle_pressure_sensor = read_adc(1)
        ring_pressure_sensor = read_adc(2)
        pinky_pressure_sensor = read_adc(3)
        thumb_pressure_sensor = read_adc(4)

        # Print Pressure Sensor Data
        print("Index Pressure Sensor: ", index_pressure_sensor)
        print("Middle Pressure Sensor: ", middle_pressure_sensor)
        print("Ring Pressure Sensor: ", ring_pressure_sensor)
        print("Pinky Pressure Sensor: ", pinky_pressure_sensor)
        print("Thumb Pressure Sensor: ", thumb_pressure_sensor)
        time.sleep(0.5)

        # Move Fingers
        """
        We are now to where most of the editing will be happening. This is where you will edit what the program does
        when the Microbit sends serial data. You can see what each serial data code is by looking at information.md.
        """
        if data == b'1':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("One")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'12':
            print("Shake Hand")
            stop = False
            i = 5
            while not stop:
                # Thresholds
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                
                # Shake Hand
                index_servo.ChangeDutyCycle(i)
                middle_servo.ChangeDutyCycle(i)
                ring_servo.ChangeDutyCycle(i)
                pinky_servo.ChangeDutyCycle(i)
                thumb_servo.ChangeDutyCycle(i)
                sleep(0.25)
                print("Two Value: ", i)
                i += 2.5

                # Fail Safe
                if i > 97:
                    index_servo.stop()
                    middle_servo.stop()
                    ring_servo.stop()
                    pinky_servo.stop()
                    thumb_servo.stop()
                    print("Failed")
                    stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    print("Finished")
                    stop = True 
        
        if data == b'3':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Three")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'4':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Four")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'5':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Five")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'6':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Six")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'7':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Seven")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'8':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Eight")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'9':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Nine")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'10':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Ten")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'11':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Eleven")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'2':
            stop = False
            while not stop:
                if index_pressure_sensor > threshold:
                    index_servo.ChangeDutyCycle.stop()
                if middle_pressure_sensor > threshold:
                    middle_servo.ChangeDutyCycle.stop()
                if ring_pressure_sensor > threshold:
                    ring_servo.ChangeDutyCycle.stop()
                if pinky_pressure_sensor > threshold:
                    pinky_servo.ChangeDutyCycle.stop()
                if thumb_pressure_sensor > threshold:
                    thumb_servo.ChangeDutyCycle.stop()
                print("Twelve")
                stop = True

                # Finish
                if index_pressure_sensor > threshold and middle_pressure_sensor > threshold and ring_pressure_sensor > threshold and pinky_pressure_sensor > threshold and thumb_pressure_sensor > threshold:
                    stop = True
        
        if data == b'13':
            print("Resetting Fingers")
            index_servo.ChangeDutyCycle(0)
            middle_servo.ChangeDutyCycle(0)
            ring_servo.ChangeDutyCycle(0)
            pinky_servo.ChangeDutyCycle(0)
            thumb_servo.ChangeDutyCycle(0)
            sleep(0.25)
            print("Reset Finished")
        
        if data == b'14':
            stopall = True
            print("Stop")
            GPIO.cleanup()   
            client_sock.close()
            server_sock.close()
            break
        
# END OF PROGRAM        
"""
Please refer to information.md for information on the serial data.

b'2' as of right now is when someone is wanting to shake someone hand. They shake the sensor and the hand will go
into position to allow the user to shake hands.

b'14' is the cancel button (AB)


Project: EnAble© is under Copyright 2023 by Jeron Osguthorpe. Though the project is open source, taking all 
credit for works is not. Though you are allowed to use the code for your own projects, you are not allowed to
take credit for the code. If you would like help with the code, please contact Jeron Osguthorpe. Contact 
information can be found on the Project: EnAble© website and GitHub repository/organization.

"""