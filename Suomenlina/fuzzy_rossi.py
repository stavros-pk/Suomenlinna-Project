import ulab.numpy as np
#Heading = -100


#Acceleration = 125

class fuzzy_controller():
    def __init__(self,heading):
        self.heading = heading

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

    #Fuzzy Partition 
    def partitionH(x):
        HHL = 0;  HL = 0; ML = 0; SL = 0; ZE = 0; SR = 0; MR = 0; HR = 0; HHR = 0; 
        
        if x>= -180 and x<-80:
            HHL = fuzzy_controller.openLeft(x,-90,-80)
        if x> -100 and x<-20:
            HL = fuzzy_controller.trapezoid(x,-100,-90,-60,-50)
        if x> -30 and x<-10:
            ML = fuzzy_controller.triangular(x,-60,-40,-20)
        if x> -20 and x<0:
            SL = fuzzy_controller.triangular(x,-40,-20,0)
        if x> -10 and x<10:
            ZE = fuzzy_controller.triangular(x,-20,0,20)
        if x> 0 and x<20:
            SR = fuzzy_controller.triangular(x,0,20,40)
        if x> 10 and x<30:
            MR = fuzzy_controller.triangular(x,20,40,60)
        if x> 20 and x<100:
            HR = fuzzy_controller.trapezoid(x,40,60,90,100)
        if x> 80 and x<=180:
            HHR = fuzzy_controller.openRight(x,80,90)
    
        return HHL, HL, ML, SL, ZE, SR, MR, HR ,HHR

    #def partitionA(x):
    #    HL = 0; ML = 0; SL = 0; ZE = 0; SR = 0; MR = 0; HR = 0; 
        
    #    if x> -60 and x<-30:
    #        HL = openLeft(x,-40,-30)
    #    if x> -40 and x<-10:
    #        ML = trapezoid(x,-40,-30,-20,-10)
    #    if x> -20 and x<0:
    #        SL = triangular(x,-20,-10,0)
    #    if x> -10 and x<10:
    #        ZE = triangular(x,-10,0,10)
    #    if x> 0 and x<20:
    #        SR = triangular(x,0,10,20)
    #    if x> 10 and x<40:
    #        MR = trapezoid(x,10,20,30,40)
    #    if x> 30 and x<60:
    #        HR = openRight(x,30,40)
    #
    #    return HL, ML, SL, ZE, SR, MR, HR


    # Rules implementation
    def compare(TC1, TC2):
        TC = 0
        if TC1>TC2 and TC1 !=0 and TC2 !=0:
            TC = TC2
        else:
            TC = TC1
        
        if TC1 == 0 and TC2 !=0:
            TC = TC2
            
        if TC2 == 0 and TC1 !=0:
            TC = TC1
            
        return TC


    def rule(HHLH, HLH, MLH, SLH, ZEH, SRH, MRH, HRH ,HHRH):
        
        HL = HLH
        ML = MLH
        SL = SLH
        ZE = ZEH
        SR = SRH
        MR = MRH
        HR = HRH
        if HHLH or HHRH !=0:
            HR = HHRH
            HL = HHLH
        
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
            areaHL, cHL = fuzzy_controller.areaOL(HL, -40, -30)
                    
        if ML != 0:
            areaML = fuzzy_controller.areaTP(ML, -40, -30, -20, -10)
            cML = -25
        
        if SL != 0:
            areaSL = fuzzy_controller.areaTR(SL, -20, -10, 0)
            cSL = -10
            
        if ZE != 0:
            areaZE = fuzzy_controller.areaTR(ZE, -10, 0, 10)
            cZE = 0
            
        if SR !=0:
            areaSR= fuzzy_controller.areaTR(SR, 0, 10, 20)
            cSR = 10

        if MR != 0:
            areaMR = fuzzy_controller.areaTP(MR, 10, 20, 30, 40)
            cMR = 25   

        if HR != 0:
            
            areaHR, cHR = fuzzy_controller.areaOR(HR, 30, 40)
            
        numerator = areaHL*cHL + areaML*cML + areaSL*cSL + areaZE*cZE + areaSR*cSR + areaMR*cMR + areaHR*cHR
        denominator = areaHL + areaML + areaSL + areaZE + areaSR + areaMR + areaHR
        if denominator == 0:
            print("No rules exist to give the result")
            return 0
        else:
            crispOutput = numerator/denominator
            return crispOutput

    def get_angle(self):
        HHL, HL, ML, SL, ZE, SR, MR, HR ,HHR = fuzzy_controller.partitionH(self.heading)
        HL, ML, SL, ZE, SR, MR, HR = fuzzy_controller.rule(HHL, HL, ML, SL, ZE, SR, MR, HR ,HHR)
        crispOutputFinal = fuzzy_controller.defuzzyfication(HL, ML, SL, ZE, SR, MR, HR)
        
        return crispOutputFinal

rudder_angle = fuzzy_controller(-40)
crispOutputFinal = rudder_angle.get_angle()
print("\nThe crisp TC value is: ", crispOutputFinal)

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

