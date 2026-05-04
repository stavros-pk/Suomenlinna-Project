import ulab.numpy as np
#Heading = -100


#Acceleration = 125

class fuzzy_controller():
    def __init__(self,heading,ang_vel):
        self.heading = heading
        self.ang_vel = ang_vel

    #Functions for open left-Right fuzzyfication  
    def openLeft(x,alpha, beta):
        if x<alpha:
            return 1
        if alpha<x and x<=beta:
            return (beta - x)/(beta - alpha)
        else:
            return 0
        
    def openRight(x,alpha, beta):
        if x<alpha:
            return 0
        if alpha<x and x<=beta:
            return (x-alpha)/(beta - alpha)
        else:
            return 1

    # Function for traingular fuzzyfication  
    def triangular(x,a,b,c):
        return max(min((x-a)/(b-a), (c-x)/(c-b)),0)

    #----------stavros----------
    def trapezoid(x,a,b,c,d):
        if x<=b:
            return max((x-a)/(b-a),0)
        if b<x and x<=c:
            return 1
        if c<x and x<=d:
            
            return max((d-x)/(d-c),0)
        else:
            return 0
    #----------stavros----------

    def partitionH(x):
        HHL = 0;  HL = 0; ML = 0; SL = 0; ZE = 0; SR = 0; MR = 0; HR = 0; HHR = 0; 
        
        if x>= -180 and x<-80:
            HHL = fuzzy_controller.openLeft(x,-90,-80)
        if x> -100 and x<-20:
            HL = fuzzy_controller.trapezoid(x,-100,-90,-30,-20)
        if x> -30 and x<-10:
            ML = fuzzy_controller.triangular(x,-30,-20,-10)
        if x> -20 and x<0:
            SL = fuzzy_controller.triangular(x,-20,-10,0)
        if x> -10 and x<10:
            ZE = fuzzy_controller.triangular(x,-10,0,10)
        if x> 0 and x<20:
            SR = fuzzy_controller.triangular(x,0,10,20)
        if x> 10 and x<30:
            MR = fuzzy_controller.triangular(x,10,20,30)
        if x> 20 and x<100:
            HR = fuzzy_controller.trapezoid(x,20,30,90,100)
        if x> 80 and x<=180:
            HHR = fuzzy_controller.openRight(x,80,90)
    
        return HHL, HL, ML, SL, ZE, SR, MR, HR ,HHR
    
    def partitionV(ang_vel):
        HL = 0; ML = 0; SL = 0; ZE = 0; SR = 0; MR = 0; HR = 0; 
        
        if ang_vel> -100 and ang_vel< -60:
            HL = fuzzy_controller.openLeft(ang_vel,-100,-60)
        if ang_vel> -80 and ang_vel<-20:
            ML = fuzzy_controller.trapezoid(ang_vel,-70,-60,-35,-25)
        if ang_vel> -40 and ang_vel<-5:
            SL = fuzzy_controller.triangular(ang_vel,-35,-20,-5)
        if ang_vel> -10 and ang_vel<10:
            ZE = fuzzy_controller.triangular(ang_vel,-10,0,10)
        if ang_vel> 5 and ang_vel<40:
            SR = fuzzy_controller.triangular(ang_vel,5,20,35)
        if ang_vel> 20 and ang_vel<80:
            MR = fuzzy_controller.trapezoid(ang_vel,25,35,60,70)
        if ang_vel> 60 and ang_vel<100:
            HR = fuzzy_controller.openRight(ang_vel,60,100)
    
        return HL, ML, SL, ZE, SR, MR, HR
    

    # Rules implementation
    def rule(HHLH, HLH, MLH, SLH, ZEH, SRH, MRH, HRH, HHRH, HLV, MLV, SLV, ZEV, SRV, MRV, HRV):
        
        
        HL_list = []; ML_list = []; SL_list = []; ZE_list = []; SR_list = []; MR_list = []; HR_list = [];
        
        angular_velocity = [HLV, MLV, SLV, ZEV, SRV, MRV, HRV]
        heading = [HHLH, HLH, MLH, SLH, ZEH, SRH, MRH, HRH, HHRH]
        
        
        rudder = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]
        
        for i in range(len(heading)):
            for j in range(len(angular_velocity)):
                rudder[i][j] = min(heading[i], angular_velocity[j])
        
        for i in range(5):
            for j in range(5-i):
                HL_list.append(rudder[i][j])
                
        for i in range(6):
            j = 5-i
            ML_list.append(rudder[i][j])
        
        for i in range(7):
            j = 6-i
            SL_list.append(rudder[i][j])
            
        for i in range(1,8):
            j = 7-i
            ZE_list.append(rudder[i][j])
            
        for i in range(2,9):
            j = 8-i
            SR_list.append(rudder[i][j])
            
        for i in range(3,9):
            j = 9-i
            MR_list.append(rudder[i][j])
            
        for i in range(4,9):
            for j in range(1,i-3):
                k = 6-j
                HR_list.append(rudder[i][k])
                
        HL = max(HL_list)
        ML = max(ML_list)
        SL = max(SL_list)
        ZE = max(ZE_list)
        SR = max(SR_list)
        MR = max(MR_list)
        HR = max(HR_list)
        return HL, ML, SL, ZE, SR, MR, HR
    
    # De-fuzzyfication
    def areaTR(mu, a,b,c):
        x1 = mu*(b-a) + a
        x2 = c - mu*(c-b)
        d1 = (c-a); d2 = x2-x1
        a = (1/2)*mu*(d1 + d2)
        return a # Returning area

    def areaOL(mu, alpha, beta): #-40,-30
        xOL = beta +mu*(alpha - beta)
        aOL = 1/2*mu*((60+beta)+(60+xOL))
        return aOL, (-60-beta)/2+beta

    def areaOR(mu, alpha, beta):
        xOR = (beta - alpha)*mu + alpha
        aOR = (1/2)*mu*((60 - alpha) + (60 - xOR))
        return aOR, (60 - alpha)/2 + alpha

    def areaTP(mu,a,b,c,d):
        x1 = mu*(b-a) + a
        x2 = d - mu*(d-c)
        d1 = (d-a); d2 = x2-x1
        a = (1/2)*mu*(d1 + d2)
        return a # Returning area

    def defuzzyfication(HL, ML, SL, ZE, SR, MR, HR):
        areaHL = 0; areaML = 0; areaSL = 0; areaZE = 0; areaSR = 0; areaMR = 0; areaHR = 0
        cHL = 0; cML = 0; cSL = 0; cZE = 0; cSR = 0; cMR = 0; cHR = 0

        if HL != 0:
            #areaPL, cPL = areaOR(PLTC, 180, 210)
            areaHL, cHL = fuzzy_controller.areaOL(HL, -60, -50)
                    
        if ML != 0:
            areaML = fuzzy_controller.areaTP(ML, -60, -50, -20, -10)
            cML = -30
        
        if SL != 0:
            areaSL = fuzzy_controller.areaTR(SL, -20, -10, 0)
            cSL = -20
            
        if ZE != 0:
            areaZE = fuzzy_controller.areaTR(ZE, -10, 0, 10)
            cZE = 0
            
        if SR !=0:
            areaSR= fuzzy_controller.areaTR(SR, 0, 10, 20)
            cSR = 20

        if MR != 0:
            areaMR = fuzzy_controller.areaTP(MR, 10, 20, 50, 60)
            cMR = 30   

        if HR != 0:
            
            areaHR, cHR = fuzzy_controller.areaOR(HR, 50, 60)
            
        numerator = areaHL*cHL + areaML*cML + areaSL*cSL + areaZE*cZE + areaSR*cSR + areaMR*cMR + areaHR*cHR
        denominator = areaHL + areaML + areaSL + areaZE + areaSR + areaMR + areaHR
        if denominator == 0:
            print("No rules exist to give the result")
            return 0
        else:
            crispOutput = numerator/denominator
            return crispOutput

    def get_angle(self):
        HHLH, HLH, MLH, SLH, ZEH, SRH, MRH, HRH ,HHRH = fuzzy_controller.partitionH(self.heading)
        HLV, MLV, SLV, ZEV, SRV, MRV, HRV = fuzzy_controller.partitionV(self.ang_vel)
        HL, ML, SL, ZE, SR, MR, HR = fuzzy_controller.rule(HHLH, HLH, MLH, SLH, ZEH, SRH, MRH, HRH, HHRH, HLV, MLV, SLV, ZEV, SRV, MRV, HRV)
        
        
        crispOutputFinal = fuzzy_controller.defuzzyfication(HL, ML, SL, ZE, SR, MR, HR)
        
        return crispOutputFinal

#rudder_angle = fuzzy_controller(-40,10)
#crispOutputFinal = rudder_angle.get_angle()
#print("\nThe crisp TC value is: ", crispOutputFinal)

'''
# Display the fuzzy values for all fuzzy sets
outPut = [[HHL, HL, ML, SL, ZE, SR, MR, HR ,HHR]]
print("The fuzzy values of the crisp inputs")
#print(["NL","NM","NS","ZE","PS","PM","PLSD"])
print(np.round(outPut,1))



print("\n")
# Display the fuzzy values for all rules
outPutRules = [[HL, ML, SL, ZE, SR, MR, HR ]]
print("The fuzzy output: ")
print(["HL", "ML", "SL", "ZE", "SR", "MR", "HR"])
print(np.round(outPutRules,2))
'''

