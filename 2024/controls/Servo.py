import time

try:
  import Adafruit_PCA9685

  use_real_hw = True
except ImportError:
  use_real_hw = False
  from mocks import MockPCA9685  # Importing the mock class

  print(
      "Running on a non-Raspberry Pi system or Adafruit_PCA9685 library not found. Using mock.")


class Servo:
  def __init__(self, pwm_freq=60):
    if use_real_hw:
      self.pwm = Adafruit_PCA9685.PCA9685()
    else:
      self.pwm = MockPCA9685()  # Use the mock class instead
    self.pwm.set_pwm_freq(pwm_freq)

  def set_servo_angle(self, channel, angle):
    pulse_length = 4096
    min_pulse = 150
    max_pulse = 600
    pulse = int(((angle / 180.0) * (max_pulse - min_pulse)) + min_pulse)
    self.pwm.set_pwm(channel, 0, pulse)

  def rotate_servo(self, channel, start_angle, end_angle, delay=0.03):
    step = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle + step, step):
      self.set_servo_angle(channel, angle)
      time.sleep(delay)


if __name__ == "__main__":
  servo = Servo()
  servo.rotate_servo(0, 0, 180)
  servo.rotate_servo(0, 180, 0)
