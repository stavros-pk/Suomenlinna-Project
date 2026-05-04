import board, pwmio
from adafruit_motor import servo


class Servo():
    def __init__(self):
        
        self.pwm1 = pwmio.PWMOut(board.GP16, frequency = 50)
        self.pwm2 = pwmio.PWMOut(board.GP17, frequency = 50)

    def servo_angle(self,rudder_angle):
        rudder_angle1 = rudder_angle + 90
        #servo_1 = servo.Servo(self.pwm1, min_pulse = 655, max_pulse = 2500)
        servo_1 = servo.Servo(self.pwm1, min_pulse = 750, max_pulse = 2300)
        servo_1.angle = rudder_angle1
        rudder_angle2 = -rudder_angle + 90
        #servo_2 = servo.Servo(self.pwm2, min_pulse = 900, max_pulse = 2400)
        servo_2 = servo.Servo(self.pwm2, min_pulse = 750, max_pulse = 2300)
        servo_2.angle = rudder_angle2
        
    def servo_stop(self,rudder_angle):
        rudder_angle1 = rudder_angle + 90
        servo_1 = servo.Servo(self.pwm1, min_pulse = 750, max_pulse = 2300)
        servo_1.angle = rudder_angle1