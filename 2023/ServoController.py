#from Adafruit_PCA9685 import PCA9685try:
try:
    from Adafruit_PCA9685 import Adafruit_PCA9685
except ImportError:
    import mock_Adafruit_PCA9685 as Adafruit_PCA9685

# Your code that uses Adafruit_PCA9685 or the mock
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

import time


class ServoController:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

    def set_angle(self, servo_channel, angle):
        pulse_width_min = 150
        pulse_width_max = 600
        pulse_width = int(((angle / 180) * (pulse_width_max - pulse_width_min)) + pulse_width_min)
        self.pwm.set_pwm(servo_channel, 0, pulse_width)
        time.sleep(0.3)

    def move_to_angle(self, servo_channel, target_angle):
        current_angle = self.get_current_angle(servo_channel)
        num_steps = abs(target_angle - current_angle)
        step = 1 if target_angle > current_angle else -1

        for _ in range(num_steps):
            current_angle += step
            self.set_angle(servo_channel, current_angle)

    def get_current_angle(self, servo_channel):
        # Implement this method based on your specific setup and requirements
        # For demonstration purposes, let's assume it returns a random angle between 0 and 180
        current_angle = 0  # Replace this with your actual implementation
        print(f"Current angle of servo {servo_channel}: {current_angle}")
        return current_angle

# Example usage:
# servo = ServoController()
# servo.move_to_angle(servo_channel=0, target_angle=90)
