import board
import busio
import adafruit_lsm303dlh_mag
import math
from time import sleep

class Heading():
    
    def __init__(self):

        i2c = busio.I2C(board.GP3, board.GP2)
        self.mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)


    def heading_angle(self):
        data = self.mag.magnetic
        
        angle = math.atan2(data[1], data[0])*180/math.pi
        angle2 = math.atan2(data[2], data[1])*180/math.pi
        angle3 = math.atan2(data[0], data[2])*180/math.pi
        #if angle <0:
        #    angle = 360 + angle

        return angle
    
# heading = Heading()
# while True:
#     
#     angle= heading.heading_angle()
#     print(angle)
#     sleep(0.1)