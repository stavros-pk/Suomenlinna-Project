import time
import board
import adafruit_mpu6050
import busio
import math

class Gyro():
    
    def __init__(self):

        i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
        self.mpu = adafruit_mpu6050.MPU6050(i2c)


    def gyro_data(self):
        mean = 0
        for i in range(4):
            data = self.mpu.gyro
            ang_vel = data[2]*180/math.pi
            mean = mean + ang_vel
        ang_vel = mean/(i+1)
        return ang_vel

# gy = Gyro()
# 
# while True:
#     data=gy.gyro_data()
#     #print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration))
#     print(data)
#     #print("Temperature: %.2f C"%mpu.temperature)
#     #print("")
#     time.sleep(0.1)
#     
    