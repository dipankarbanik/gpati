import RPi.GPIO as GPIO
from utils import ServoRun
import time
# from threading import Thread
import threading
# import Adafruit_PCA9685
sc = ServoRun.ServoCtrl()

# Step motor Constants
# (12) BLU GPIO18, (16) BR GPIO23, (18) Y GPIO24, (22) O GPIO25
kaalia = (12, 16, 18, 22)
# (31) RED GPIO06, (33) BR GPIO13, (35) Y GPIO19, (37) GPIO26
krishna = (31, 33, 35, 37)

CCWStep = (0x01, 0x02, 0x04, 0x08)
CWStep = (0x08, 0x04, 0x02, 0x01)

def setup():
    sc.start()
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    for pin1 in kaalia:
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(pin1, 0)
    for pin2 in krishna:
        GPIO.setup(pin2, GPIO.OUT)
        GPIO.output(pin2, 0)

def moveVillagers():
    while True:
        print('Moving villagers...')
        delaytime = 2
        sc.certSpeed([0, 7], [60, 0], [40, 60])
        time.sleep(delaytime)

        sc.certSpeed([0, 7], [0, 60], [40, 60])
        time.sleep(delaytime+2)

        sc.certSpeed([1, 7], [60, 0], [40, 60])
        time.sleep(delaytime)

        sc.certSpeed([1, 7], [0, 60], [40, 60])
        time.sleep(delaytime+2)

        sc.certSpeed([2, 7], [60, 0], [40, 60])
        time.sleep(delaytime)

        sc.certSpeed([2, 7], [0, 60], [40, 60])
        time.sleep(delaytime+2)

        sc.certSpeed([3, 7], [60, 0], [40, 60])
        time.sleep(delaytime)

        sc.certSpeed([3, 7], [0, 60], [40, 60])
        time.sleep(delaytime+2)

        sc.certSpeed([4, 7], [60, 0], [40, 60])
        time.sleep(delaytime)

        sc.certSpeed([4,7], [0,60], [40,60])
        time.sleep(delaytime+2)

        sc.certSpeed([5, 7], [60, 0], [40, 60])
        time.sleep(delaytime)

        sc.certSpeed([5, 7], [0, 60], [40, 60])
        time.sleep(delaytime+2)

# as for four phase stepping motor, four steps is a cycle. the function is
# used to drive the stepping motor clockwise or anticlockwise to take four
# steps
def moveKaliaOnePeriod(direction, ms):
    for j in range(0, 4, 1):      # cycle for power supply order
        for i in range(0, 4, 1):  # assign to each pin
            if (direction == 1):  # power supply order clockwise
                GPIO.output(kaalia[i], ((CCWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
            else: # power supply order anticlockwise
                GPIO.output(kaalia[i], ((CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
        if(ms < 3):  # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
            ms = 3
        time.sleep(ms*0.002)

def moveKrishnaOnePeriod(direction, ms):
    for j in range(0, 4, 1):  # cycle for power supply order
        for i in range(0, 4, 1):  # assign to each pin
            if (direction == 1):  # power supply order clockwise
                GPIO.output(krishna[i], ((CCWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
            else: # power supply order anticlockwise
                GPIO.output(krishna[i],((CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
        if(ms < 3):  # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
            ms = 3
        time.sleep(ms*0.002)


# continuous rotation function, the parameter steps specifies the rotation
# cycles, every four steps is a cycle
def moveKalia(direction, ms, steps):
    for i in range(steps):
        moveKaliaOnePeriod(direction, ms)

def moveKrishna(direction, ms, steps):
    for i in range(steps):
        moveKrishnaOnePeriod(direction, ms)

# function used to stop motor
def motorStop():
    print('Stopping Motor...')
    for i in range(0, 4, 1):
        GPIO.output(kaalia[i], GPIO.LOW)
        GPIO.output(krishna[i], GPIO.LOW)


def kaliaPlay():
    print('Moving Kalia...')
    while True:
        moveKalia(1, 3,100)  # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles
        time.sleep(5.5)
        moveKalia(0, 3, 100)  # rotating 360 deg anticlockwise
        time.sleep(5.5)

def krishnaPlay():
    print('Moving Krishna...')
    while True:
        moveKrishna(0, 3, 1400)  # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles
        time.sleep(1.1)
        moveKrishna(1, 3, 1000)  # rotating 360 deg anticlockwise
        time.sleep(255000)


def destroy():
    motorStop();
    GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup();
    try:
        threading.Thread(target=moveVillagers).start()
        threading.Thread(target=kaliaPlay).start()
        threading.Thread(target=krishnaPlay).start()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()