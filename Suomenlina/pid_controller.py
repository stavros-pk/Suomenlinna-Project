class PID_Control:

    def __init__(self):
        self.PGain = 1
        self.DGain = 0.5
        self.IGain = 0
        

    def PIDController(self, angle, angle_rate):
        self.angle = angle
        self.angle_rate = angle_rate
        output = self.PGain * self.angle - self.DGain * self.angle_rate +self.IGain * self.angle/self.angle_rate
        return output
