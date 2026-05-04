# PWM control example for RPi Pico
# Using L293D motor driver

import time
import pwmio
import board
import digitalio

class Motor_thrust():
    
    def __init__(self):
        
        self.enable1 = digitalio.DigitalInOut(board.GP15)
        self.enable1.direction = digitalio.Direction.OUTPUT
        self.enable1.value = 1

        self.rotate1F = pwmio.PWMOut(board.GP12, frequency=5000, duty_cycle=0)
        self.rotate1B = pwmio.PWMOut(board.GP13, frequency=5000, duty_cycle=0)

        self.enable2 = digitalio.DigitalInOut(board.GP14)
        self.enable2.direction = digitalio.Direction.OUTPUT
        self.enable2.value = 1

        self.rotate2F = pwmio.PWMOut(board.GP10, frequency=5000, duty_cycle=0)
        self.rotate2B = pwmio.PWMOut(board.GP11, frequency=5000, duty_cycle=0)
        
    def forwards_2(self, throttle):
        
        #self.enable1.value = 1
        self.rotate1B.duty_cycle = throttle*10000+5535
        self.rotate1F.duty_cycle = 0
        
        #self.enable2.value = 1
        self.rotate2F.duty_cycle = throttle*10000
        self.rotate2B.duty_cycle = 0
    
    def backwards_2(self, throttle):
        
        self.enable1.value = 1
        self.rotate1F.value = 0
        self.rotate1B.value = 1
        
        self.enable2.value = 1
        self.rotate2F.value = 0
        self.rotate2B.value = 1
        
    def stop(self):
        
        #self.enable1.value = 0
        self.rotate1F.duty_cycle = 0
        self.rotate1B.duty_cycle = 0
        
        #self.enable2.value = 0
        self.rotate2F.duty_cycle = 0
        self.rotate2B.duty_cycle = 0
        
    
    
    
    
    