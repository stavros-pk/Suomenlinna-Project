class Angular_velocity():
    def __init__(self):
        pass
    
    def get_ang_velocity(self,start_time,end_time,heading):
        
        if start_time >=0:
            
            heading1 = heading[0]   
            heading2 = heading[1]
            
            elapsed = end_time-start_time
            delta_heading = heading2 - heading1
            ang_velocity = delta_heading/elapsed
        else:
            ang_velocity = 0
        
        return ang_velocity