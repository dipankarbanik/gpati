#!/usr/bin/python

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class RelaySwitch:
    relaypins = {
        "SWITCH1": 26,
        "SWITCH2": 20,
        "SWITCH3": 21,
        "SWITCH4": 16
    }

    def __init__(self, relay_name, object_name=None):
        self.relay = relay_name
        self.object_name = object_name or relay_name

        if self.relay not in self.relaypins:
            raise ValueError(
                f"Invalid relay name: {self.relay}. Available options are: {', '.join(self.relaypins.keys())}.")

        self.pin = self.relaypins[self.relay]
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()  # Set initial state to OFF

    def on(self):
        print(f"{self.object_name} ({self.relay}) - ON")
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        print(f"{self.object_name} ({self.relay}) - OFF")
        GPIO.output(self.pin, GPIO.LOW)

    def switch_on_for_period(self, period):
        self.on()
        time.sleep(period)
        self.off()
