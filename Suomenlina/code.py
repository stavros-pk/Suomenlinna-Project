from fuzzy_rossi_ang import fuzzy_controller #https://www.youtube.com/watch?v=cs0lWfXb3Wo
from mag_heading import Heading
from servo import Servo
from angular_vel import Angular_velocity
from mpu6050 import Gyro
from pid_controller import PID_Control
from motors import Motor_thrust
from data_logging import Logger

import microcontroller
import gc
from time import sleep
import time
import board
import digitalio
import os, ssl, socketpool, wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import busio as io
import storage
import adafruit_sdcard
from adafruit_datetime import datetime

CS = board.GP5 #CSn
SCK = board.GP6 #SCK
MOSI = board.GP7 #TX
MISO = board.GP4 #RX

Heading = Heading()
Servo = Servo()
Angular = Angular_velocity()
gy = Gyro()
Motors = Motor_thrust()
storage.mount(storage.VfsFat(adafruit_sdcard.SDCard(io.SPI(SCK, MOSI, MISO), digitalio.DigitalInOut(CS))), "/sd")

#log = Logger()


led1 = digitalio.DigitalInOut(board.GP21)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.GP20)
led2.direction = digitalio.Direction.OUTPUT
led2.value = True
led1.value = False
#log.loginit

#test

PID_Control = PID_Control()
heading=[0,0]
#desired_angle = input('Enter desired angle: ')
#desired_angle = float(desired_angle)
desired_angle = 0

print("Connecting to %s" % os.getenv("WIFI_SSID"))
while True:
    try:
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
    except:
        print("Trying to connect...", end = "\r")
    else:
        break

led1.value = True
led2.value = False
sleep(1)
led1.value = False
pool = socketpool.SocketPool(wifi.radio)


aio_username = os.getenv('AIO_USERNAME')
aio_key = os.getenv('AIO_KEY')

mode = aio_username + "/feeds/Mode"
thrust = aio_username + "/feeds/THRUST"
rudder = aio_username + "/feeds/STEER"
target = aio_username + "/feeds/TARGET"
rudderfeed = aio_username + "/feeds/RUDDERANGLE"
streamdata = aio_username + "/feeds/STREAMDATA"
poweroff = aio_username + "/feeds/POWEROFF"
controller = aio_username + "/feeds/CONTROLLER"

def connected(client, userdata,flags, rc):
    print("Connected to Dashboard.")
    client.subscribe(mode)
    client.subscribe(thrust)
    client.subscribe(rudder)
    client.subscribe(target)
    client.subscribe(rudderfeed)
    client.subscribe(streamdata)
    client.subscribe(poweroff)
    client.subscribe(controller)
    
def disconnected(client, userdata, rc):
    print("Disconnected...")
   
def msg(client, topic, mode): 
    print(f"Topic:{topic}, Message1:{mode}")
    if topic == aio_username + "/feeds/Mode":
        global mod
        mod=mode
    elif topic == aio_username + "/feeds/THRUST":
        global thrust_val
        thrust_val = int(mode)
    elif topic == aio_username + "/feeds/STEER":
        global rudder_ang
        rudder_ang = float(mode)
    elif topic == aio_username + "/feeds/TARGET":
        global desired_angle
        desired_angle = float(mode)
    elif topic == aio_username + "/feeds/POWEROFF":
        global switch
        switch = int(mode)
    elif topic == aio_username + "/feeds/CONTROLLER":
        global control
        control = mode



mqtt_client = MQTT.MQTT(
    broker = os.getenv("BROKER"),
    port = os.getenv("PORT"),
    username = aio_username,
    password = aio_key,
    socket_pool = pool,
    ssl_context = ssl.create_default_context(),
    socket_timeout = 0.101,
)

mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = msg

print("Connecting to Dashboard.")

mqtt_client.connect()

mod = "MAN"
control = "PD"
rudder_ang = 0
thrust_val = 0
elapsed_time = 0
switch = 0
test = 0
try:
    while switch == 0:
        start_time = time.monotonic()
        mqtt_client.loop(0.101)
        #led1.value = True
        if mod == "AUTO":
            if elapsed_time == 0:
                test = test+1
                with open("/sd/data"+str(test)+".csv", "a") as appendfile:
                    print("Time Heading Rudder Yaw_Rate", file = appendfile)
                appendfile.close()
            angle =Heading.heading_angle()-desired_angle
            ang_vel = gy.gyro_data()
            
            if angle> 180:
                angle = -(360 - angle)
            elif angle < -180:
                angle = (360 + angle)
                
            if control == "FUZ":
                rudder_angle = fuzzy_controller(angle,ang_vel)
                crispOutputFinal = rudder_angle.get_angle()
                
            elif control == "PD":
                crispOutputFinal = PID_Control.PIDController(angle,ang_vel)
                
            if crispOutputFinal>60:
                crispOutputFinal = 60
            elif crispOutputFinal<-60:
                crispOutputFinal = -60
            Servo.servo_angle(crispOutputFinal)
            
            #Motors.forwards_2(0)
            if thrust_val == 0:
                Motors.stop()
            else:
                Motors.forwards_2(thrust_val)
                
            if abs(angle) < 5:
                led1.value = True
                led2.value = False
            else:
                led2.value = True
                led1.value = False
            current_time = time.monotonic()
            elapsed_time = elapsed_time + (current_time - start_time)
            
#            if elapsed_time >= 1:
#                mqtt_client.publish(rudderfeed,-crispOutputFinal*2)
#                mqtt_client.publish(streamdata,angle)#+","+float(-crispOutputFinal*2)+","+str(ang_vel))
#                elapsed_time = 0
            print("Goal: ", round(angle,2)," Rudder Angle: " , round(-crispOutputFinal,2) , "Angular Velocity: " , round(ang_vel,2))
            with open("/sd/data"+str(test)+".csv", "a") as appendfile:
                print(elapsed_time, round(angle,2), round(-crispOutputFinal,2), round(ang_vel,2), control, file = appendfile)
            appendfile.close()
            #log.write
        elif mod == "MAN":
            elapsed_time = 0
            
            rudder_ang = rudder_ang
            Servo.servo_angle(rudder_ang)
            if thrust_val == 0:
                Motors.stop()
            else:
                Motors.forwards_2(thrust_val)
        
#          current_time = time.monotonic()
#          elapsed_time = elapsed_time + (current_time - start_time)
        sleep(0.01)
        gc.collect
    
    else:
        led1.value = False
        led2.value = True
        Servo.servo_angle(0)
        Servo.servo_stop(90)
        sleep(1)
        Motors.stop()
        #log.close
        gc.collect()
        print("Program terminated")
        
        
except KeyboardInterrupt:
    led1.value = False
    led2.value = True
    Servo.servo_angle(0)
    sleep(1)
    Motors.stop()
    #log.close
    gc.collect()
    print("Program terminated")