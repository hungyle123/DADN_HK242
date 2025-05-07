from ultralytics import YOLO    
import cv2
model = YOLO('best.pt')

import sys
from Adafruit_IO import MQTTClient
import time
import random
from uart import *
#from simple_ai import *

timer = time.time()
AIO_FEED_ID = ["temp", "humi", "light_level", "led_button", "door_button", "fan", "fire_detect","pump","set-h", "set-t"]
AIO_USERNAME = ""
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


cap = cv2.VideoCapture(0)
class_names = model.names

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Nếu không lấy được frame thì dừng

    results = model.predict(source=frame, imgsz=640, conf=0.78, show=True)
    r = results[0]
    boxes = r.boxes

    if boxes is not None and boxes.cls.numel() > 0:
        for cls_id in boxes.cls:
            class_id = int(cls_id.item())
            class_name = class_names[class_id]

            if class_name == "fire":
                print("Detecting the FIRE-------!!!!!!")
                writeData("11")
                client.publish("fire_detect",1)

    # Thoát nếu người dùng nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()