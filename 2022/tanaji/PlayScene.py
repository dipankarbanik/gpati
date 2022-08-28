#!/usr/bin/python
import time
import RPIservo
import RPi.GPIO as GPIO
from threading import Thread

import PiRelay

from DRV8825 import DRV8825
import Adafruit_PCA9685

sc = RPIservo.ServoCtrl()
switch1 = PiRelay.Relay("SWITCH1")
switch2 = PiRelay.Relay("SWITCH2")
switch3 = PiRelay.Relay("SWITCH3")

wallHeight = 10
warLength = 50

Tanaji = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16,17,20))
Soldiers = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21,22,27))

def setup():
    print("Initializing Setup")
    sc.start()

def playscene():
    invokeSwitch(switch1,5)
    print("Tanaji climbing ...")
    rotateMotors(Tanaji,'forward',wallHeight)
    invokeSwitch(switch2,5)
    print("War Starting ...")
    Thread(target=rotateMotors,args=(Soldiers,'forward',warLength)).start()
    #rotateMotors(Soldiers,'forward',warLength)
    fightTanaji()
    mughalFall()
    waveShivaji()
    reset()

def fightTanaji():
    fightIteration = 10;
    while fightIteration > 0:
        print("Moving Tanaji..."+str(fightIteration))
        delaytime = 2
        sc.certSpeed([0, 7], [60, 0], [40, 60])
        time.sleep(delaytime)
        sc.certSpeed([0, 7], [0, 60], [40, 60])
        time.sleep(delaytime+2)
        fightIteration -= 1
        
def mughalFall():
    print('Mughal fall...')
    delaytime = 2
    sc.certSpeed([1, 7], [60, 0], [40, 60])
    time.sleep(delaytime)

def waveShivaji():
    waveIteration = 5;
    while waveIteration > 0:
        print("Moving Shivaji..."+str(waveIteration))
        delaytime = 2
        sc.certSpeed([2, 7], [60, 0], [40, 60])
        time.sleep(delaytime)
        sc.certSpeed([2, 7], [0, 60], [40, 60])
        time.sleep(delaytime+2)
        waveIteration -= 1
        
def reset():
    print('Mughal reset...')
    delaytime = 2
    sc.certSpeed([1, 7], [0, 60], [40, 60])
    time.sleep(delaytime+2)
    print("Sending tanaji back..."+str(wallHeight))
    rotateMotors(Tanaji,'backward',wallHeight)     
       
def invokeSwitch(switch, period):
    print("Starting ..."+switch.relay+" for "+str(period)+" sec")
    Thread(target=switch.on()).start()
    time.sleep(period)
    switch.off()

def rotateMotors(motor,direction, duration):
    s = 200 * 32
    delay = 0
    if (duration > 0):
    	delay = duration/s
    print("..Rotating in "+str(direction)+" direction for "+str(duration) +" sec"+ " with step count "+str(s))
    motor.SetMicroStep('software', '1/4step')
    motor.TurnStep(Dir=direction, steps=int(s), stepdelay=delay)
    motor.Stop()

def destroy():
    print ('Cleaning Up...')
    switch1.off()
    switch2.off()
    switch3.off()
    Tanaji.Stop()
    Soldiers.Stop()
    GPIO.cleanup()  # Release resource

if __name__ == '__main__': 
    print ('Starting Tanaji Play...')
    try:
        setup()
        playscene()
        destroy()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
