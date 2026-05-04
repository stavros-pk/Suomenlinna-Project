import os, ssl, socketpool, wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time

print(f"Connecting to WiFi")
wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
print("Connected!")

pool = socketpool.SocketPool(wifi.radio)

aio_username = os.getenv('AIO_USERNAME')
aio_key = os.getenv('AIO_KEY')

feed = aio_username + "/feeds/Mode"



def connected(client, userdata,flags, rc):
    print("Connected to Dashboard.")
    client.subscribe(feed)
    
def disconnected(client, userdata, rc):
    print("Disconnected...")
    
def message(client, topic, message):
    
    print(f"Topic:{topic}, Message:{message}")
    
    if message == "AUTO":
        print("AUTO")
    elif message == "MAN":
        print("MAN")


mqtt_client = MQTT.MQTT(
    broker = os.getenv("BROKER"),
    port = os.getenv("PORT"),
    username = aio_username,
    password = aio_key,
    socket_pool = pool,
    ssl_context = ssl.create_default_context(),
)

mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

print("Connecting to Dashboard.")
mqtt_client.connect()

while True:
    
    mqtt_client.loop(timeout=1)


