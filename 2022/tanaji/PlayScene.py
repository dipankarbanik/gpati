import time

import RPi.GPIO as GPIO

from utils import Relay


def destroy():
    GPIO.cleanup()  # Release resource


switch1 = Relay.Relay("RELAY1")
switch2 = Relay.Relay("RELAY2")
switch3 = Relay.Relay("RELAY3")


def playscene():
    switch1.on()
    time.sleep(2)
    switch1.off()
    time.sleep(2)

if __name__ == '__main__':  # Program entrance
    print ('Starting Tanaji Play...')
    try:
        playscene()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
