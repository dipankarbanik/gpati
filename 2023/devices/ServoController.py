try:
    from Adafruit_PCA9685 import Adafruit_PCA9685
except ImportError:
    from .mock_PCA9685 import PCA9685 as Adafruit_PCA9685

import time


class ServoController:
    def __init__(self):
        self.pwm = Adafruit_PCA9685()
        self.pwm.set_pwm_freq(50)
        self.current_angles = {}

    def set_angle(self, servo_channel, angle):
        pulse_width_min = 150
        pulse_width_max = 600
        pulse_width = int(((angle / 180) * (pulse_width_max - pulse_width_min)) + pulse_width_min)
        self.pwm.set_pwm(servo_channel, 0, pulse_width)
        time.sleep(0.3)
        self.current_angles[servo_channel] = angle

    def move_to_angle(self, servo_channel, target_angle, step=1):
        current_angle = self.get_current_angle(servo_channel)
        num_steps = abs(target_angle - current_angle)
        step = step if target_angle > current_angle else -step

        for _ in range(num_steps):
            current_angle += step
            self.set_angle(servo_channel, current_angle)

    def get_current_angle(self, servo_channel):
        return self.current_angles.get(servo_channel, 0)
