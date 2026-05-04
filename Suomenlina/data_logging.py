import time
from time import sleep
import adafruit_datetime as datetime

class Logger:


    def __init__(self):
        self.path = "data.csv"
        self.file = open(self.path,"a")


    def loginit(self):
        print("Initializing logger...")
        #if os.stat("/home/spk/Desktop/data_log.csv").st_size ==0:
        
        self.file.write("Time, x, y, z\n")        

    def write(self,*values):
        now = datetime.now()
        self.file.write(str(now))
        for value in values:
            self.file.write(","+str(value))
        
        self.file.write("\n")
        self.file.flush()
