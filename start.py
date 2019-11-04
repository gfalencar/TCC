import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(24)
    if input_state == False:
        print('Button Pressed')
        os.system('python3 /home/pi/Documents/TCC/automation.py')
        time.sleep(0.2)