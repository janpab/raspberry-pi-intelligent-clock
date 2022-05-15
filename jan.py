#!/usr/bin/env python
import ZeroSeg.led as led
import time
from datetime import datetime
import urllib.request
import json
import RPi.GPIO as GPIO
import threading

button1 = 17
button2 = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN)
auto = 0

def autogo():
    global mode
    threading.Timer(10.0, autogo).start()
    global auto
    if auto == 1:
        mode += 1
        if mode == 5:
            mode = 1
        print ("Auto Switch: ", mode)

def weather():
    global mode
    threading.Timer(5.0, weather).start()
    response = urllib.request.urlopen('https://danepubliczne.imgw.pl/api/data/synop/station/poznan')
    data = json.loads(response.read())
    data1 = data["temperatura"]

    if len(data1)>2:
        tem = data1[:2]
    else:
        tem = data1
    return tem

device = led.sevensegment(cascaded=2)
print ("Start!")
time.sleep(2)
mode = 1
level = 1
device.brightness(level)
autogo()


while True:
    now = datetime.now()
    if mode ==1:
        hour = now.hour
        minute = now.minute
        second = now.second
        dot = second % 2 == 0
        device.letter(1, 8, int(hour / 10))
        device.letter(1, 7, hour % 10)
        device.letter(1, 6, " ", 1)
        device.letter(1, 5, int(minute / 10))
        device.letter(1, 4, minute % 10)
        device.letter(1, 3, " ", 1)
        device.letter(1, 2, int(second / 10))
        device.letter(1, 1, second % 10)
    if mode == 2:
        day = now.day
        month = now.month
        year = now.year - 2000
        device.letter(1, 8, int(day / 10))
        device.letter(1, 7, day % 10)
        device.letter(1, 6, '-')
        device.letter(1, 5, int(month / 10))
        device.letter(1, 4, month % 10)
        device.letter(1, 3, '-')
        device.letter(1, 2, int(year / 10))
        device.letter(1, 1, year % 10)
    if mode == 3:
        device.write_text(1,"Poz "+weather()+" C") #showing weather - make sure that your 7 segment display is long enought
    if mode == 4:
        auto = 1
        mode = 1

    if not GPIO.input(button2):
        if auto == 1:
            auto = 0
            mode = 1
            print("Auto Off")
        elif mode < 4:
            mode += 1
        else:
            mode = 1

        if mode == 1:
            device.write_text(1, "CZAS")
        if mode == 2:
            device.write_text(1, "DATA")
        if mode == 3:
            device.write_text(1, "POGODA")
        if mode == 4:
            device.write_text(1, "AUTO")
        time.sleep(1)
    #Brightness
    elif not GPIO.input(button1):
        if level <= 2:
            level = 5
        elif level == 5:
            level = 10
        elif level == 10:
            level = 14
        elif level >= 14:
            level = 1
        device.brightness(level)
        print("Brightness level:", level)
        time.sleep(0.5)
    else:
        pass
