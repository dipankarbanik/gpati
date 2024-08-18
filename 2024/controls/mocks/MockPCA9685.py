class MockPCA9685:
  def __init__(self):
    self.frequency = 60

  def set_pwm_freq(self, frequency):
    self.frequency = frequency
    print(f"Mock: PWM frequency set to {frequency} Hz.")

  def set_pwm(self, channel, on, off):
    print(f"Mock: PWM set on channel {channel}, on={on}, off={off}.")
