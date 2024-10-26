# SPDX-FileCopyrightText: 2019 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
from fuzzy_rossi import fuzzy_controller

import gc
from time import sleep
import board
import busio
import adafruit_lsm303dlh_mag
import math
import time


i2c = busio.I2C(board.GP3, board.GP2)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)


def heading_angle():
    data = mag.magnetic
    
    angle = math.atan2(data[1], data[0])*180/math.pi;
    if angle <0:
        angle = 360 + angle

    return angle

import board, pwmio
from adafruit_motor import servo

pwm1 = pwmio.PWMOut(board.GP16, frequency = 50)
pwm2 = pwmio.PWMOut(board.GP17, frequency = 50)

def servo_angle(rudder_angle):
    rudder_angle = rudder_angle + 90
    servo_1 = servo.Servo(pwm1, min_pulse = 465)
    servo_1.angle = rudder_angle
    servo_2 = servo.Servo(pwm2, min_pulse = 655, max_pulse = 2500)
    servo_2.angle = rudder_angle


import board
import digitalio

led1 = digitalio.DigitalInOut(board.GP6)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.GP4)
led2.direction = digitalio.Direction.OUTPUT


def get_ang_velocity(start_time,end_time):
    
    if start_time >=0:
        
        heading1 = heading[0]
        
        
        heading2 = heading[1]
        
        elapsed = end_time-start_time
        delta_heading = heading2 - heading1
        ang_velocity = delta_heading/elapsed
    else:
        ang_velocity = 0
        
        
        
    return ang_velocity

heading=[0,0]
desired_angle = 0
start_time = -1
mean = [0,0,0,0,0]
try:
    while True:
        led1.value = True
        
        angle =heading_angle()-desired_angle
        
        if angle> 180:
            angle = -(360 - angle)
        
        rudder_angle = fuzzy_controller(angle)
        crispOutputFinal = rudder_angle.get_angle()
        servo_angle(-crispOutputFinal)
        
        heading[1] = angle
        stop_time = time.monotonic()
        ang_vel = get_ang_velocity(start_time, stop_time)
        
        mean[0] = mean[1]
        mean[1] = mean[2]
        mean[2] = mean[3]
        mean[3] = mean[4]
        mean[4] = ang_vel
        mean_ang_vel = (mean[0]+mean[1]+mean[2]+mean[3]+mean[4])/5
        
        print("Goal: ", angle," Rudder Angle: ", -crispOutputFinal,"Angular Velocity", mean_ang_vel)
        heading[0] = heading[1]
        start_time = time.monotonic()
        sleep(0.1)
        gc.collect
        
except KeyboardInterrupt:
    led1.value = False
    led2.value = True
    servo_angle(0)
    gc.collect()
    print("Program terminated")
