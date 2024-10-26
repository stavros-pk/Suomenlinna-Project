import board
import busio
import adafruit_lsm303dlh_mag
import math

class mag_data:
    def __init__():
        i2c = busio.I2C(board.GP3, board.GP2)
        mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
        return mag

    def heading_angle():
        data = mag.magnetic
        
        angle = math.atan2(data[1], data[0])*180/math.pi;
        if angle <0:
            angle = 360 + angle

        return angle
