import sys
from Adafruit_IO import MQTTClient
import time
import random
from uart import *
#from simple_ai import *

timer = time.time()
AIO_FEED_ID = ["temp", "humi", "light_level", "led_button", "door_button", "fan", "fire_detect","pump","set-h", "set-t"]
AIO_USERNAME = "phamlehuuhiep27"
AIO_KEY = ""
AIO_KEY = AIO_KEY.replace(AIO_KEY[:3], "aio")

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " , feed id:", feed_id)
    global timer
    if time.time() - timer < 0.2:
        time.sleep(0.3 - (time.time() - timer))
    if feed_id == "door_button":
        if payload == "1":
            writeData("1")
        else:
            writeData("2")
    if feed_id == "led_button":
        if payload == "1":
            writeData("3")
        else:
            writeData("4")
    if feed_id == "fan":
        if payload == "1":
            writeData("5")
        elif payload == "2":
            writeData("6")
        elif payload == "3":
            writeData("7")
        else:
            writeData("8")
    if feed_id == "pump":
        if payload == "1":
            writeData("9")
        else:
            writeData("10")
    if feed_id == "set-t":
            writeData("00000"+payload)
    if feed_id == "set-h":
            writeData("0000000"+payload)
    timer = time.time()


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

#main program
# counter_updateValue = 1
# counter_readSever = 1
while True:
    print("waiting")
    time.sleep(1)
# counter_ai = 20
# readSerial(client)
# while True:
#     counter_updateValue = counter_updateValue - 1
#     if counter_updateValue <= 0:
#         counter_updateValue = 1
#         #TODO1 - adding sensor value to server
#         counter_ai -=1
#         if counter_ai <=0:
#             counter_ai = 10
#             # ai_result = image_detector()
#             # client.publish("ai_detect",ai_result)
#         readSerial(client)
#     time.sleep(1)
#     pass