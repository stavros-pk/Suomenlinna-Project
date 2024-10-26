import time
import 


class angular_velocity:
    
    def __init__(self):
        
        

        
    def get_ang_velocity():
        
        heading1 = heading_angle()
        start = time.time()
        time.clock()
        heading2 = heading_angle()
        stop = time.time()
        elapsed = stop - start
        delta_heading = heading2 - heading1
        ang_velocity = delta_heading/elapsed
        return ang_velocity
        
        
