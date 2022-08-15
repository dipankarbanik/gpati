import time
import RPi.GPIO as GPIO
from c_servokit import ServoKit

# stepper motor
# define pins connected to four phase ABCD of stepper motor
motorPins = (12, 16, 18, 22)
# define power supply order for rotating anticlockwise
CCWStep = (0x01, 0x02, 0x04, 0x08)
# define power supply order for rotating clockwise
CWStep = (0x08, 0x04, 0x02, 0x01)

#servo motor
kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500, 2750)
kit.servo[1].set_pulse_width_range(500, 2750)


def setupStepper():
    GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
    for pin in motorPins:
        GPIO.setup(pin,GPIO.OUT)


def servoMove(channel = 0, start = 10, stop = 170, speed = 1):
	print("Speed: ", speed)
	print("Servo Channel: ", channel)
	print("Move from", start, "to", stop)
	print("")
	speed = float(0.02 / speed)

	for x in range(90, stop):
		kit.servo[channel].angle = x
		time.sleep(speed)

	for x in range(stop, start, -1):
		kit.servo[channel].angle = x
		time.sleep(speed)

	for x in range(start, 90):
		kit.servo[channel].angle = x
		time.sleep(speed)

	time.sleep(0.5)
	
try:
	while True:
		servoMove(0, 20, 160, 1)
		time.sleep(1)
		
		servoMove(1, 20, 160, 1)
		time.sleep(1)

		servoMove(2, 20, 160, 4)
		time.sleep(1)

except KeyboardInterrupt:
	print("Program Stop")

except:
	print("Other Error or exception occured!")

# as for four phase stepping motor, four steps is a cycle. the function is used to drive the stepping motor clockwise or anticlockwise to take four steps
def moveOnePeriod(direction,ms):
    for j in range(0,4,1):      # cycle for power supply order
        for i in range(0,4,1):  # assign to each pin
            if (direction == 1):# power supply order clockwise
                GPIO.output(motorPins[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
            else :              # power supply order anticlockwise
                GPIO.output(motorPins[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
        if(ms<3):       # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
            ms = 3
        time.sleep(ms*0.002)

# continuous rotation function, the parameter steps specifies the rotation cycles, every four steps is a cycle
def moveSteps(direction, ms, steps):
    for i in range(steps):
        moveOnePeriod(direction, ms)

# function used to stop motor
def motorStop():
    for i in range(0,4,1):
        GPIO.output(motorPins[i],GPIO.LOW)

def playscene():
    while True:
        moveSteps(1,3,1024)  # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles
        time.sleep(20.5)
        moveSteps(0,3,1024)  # rotating 360 deg anticlockwise
        time.sleep(5.5)


def destroy():
    kit.servo[0].angle = 90
	kit.servo[1].angle = 90
    GPIO.cleanup() # Release resource

if __name__ == '__main__':     # Program entrance
    print ('Starting Kaliya Daman Play...')
    setupStepper()
    try:
        playscene()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()