from fuzzy_rossi_ang import fuzzy_controller
from mag_heading import Heading
from servo import Servo
from angular_vel import Angular_velocity
from mpu6050 import Gyro

import gc
from time import sleep
import time
import board
import digitalio
import sys
import select

Heading = Heading()
Servo = Servo()
Angular = Angular_velocity()
gy = Gyro()

led1 = digitalio.DigitalInOut(board.GP6)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.GP4)
led2.direction = digitalio.Direction.OUTPUT

heading=[0,0]
desired_angle = input('Enter desired angle: ')
desired_angle = float(desired_angle)

try:
    while True:
        #led1.value = True
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.readline().strip()
            if user_input is float:
                desired_angle = user_input
            print(user_input)
            
        angle =Heading.heading_angle()-desired_angle
        ang_vel = gy.gyro_data()
        
        if angle> 180:
            angle = -(360 - angle)
        
        rudder_angle = fuzzy_controller(angle,ang_vel)
        crispOutputFinal = rudder_angle.get_angle()
        Servo.servo_angle(-crispOutputFinal)
        
        if abs(angle) < 5:
            led1.value = True
            led2.value = False
        else:
            led2.value = True
            led1.value = False

        print("Goal: ", angle," Rudder Angle: ", -crispOutputFinal,"Angular Velocity", ang_vel)

        sleep(0.05)
        gc.collect
        
except KeyboardInterrupt:
    led1.value = False
    led2.value = True
    servo_angle(0)
    gc.collect()
    print("Program terminated")