import os
import board
import busio as io
import digitalio
import storage
import adafruit_sdcard
import microcontroller
from time import sleep

CS = board.GP5 #CSn
SCK = board.GP6 #SCK
MOSI = board.GP7 #TX
MISO = board.GP4 #RX

storage.mount(storage.VfsFat(adafruit_sdcard.SDCard(io.SPI(SCK, MOSI, MISO), digitalio.DigitalInOut(CS))), "/sd")
with open("/sd/data.csv", "a") as appendfile:
    print("Time, Heading, Rudder, Yaw Rate", file = appendfile)
appendfile.close()
while True:
    with open("/sd/data.csv", "a") as appendfile:
        print("data", file = appendfile)
        print("ok")
    appendfile.close()
    sleep(5)