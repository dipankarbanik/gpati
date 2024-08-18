# mock_gpio.py
class MockGPIO:
  BCM = 'BCM'
  OUT = 'OUT'
  IN = 'IN'
  HIGH = 1
  LOW = 0

  @staticmethod
  def setmode(mode):
    print(f"MockGPIO: Setting mode to {mode}")

  @staticmethod
  def setwarnings(flag):
    print(f"MockGPIO: Set warnings to {flag}")

  @staticmethod
  def setup(pin, mode):
    print(f"MockGPIO: Setting up pin {pin} to mode {mode}")

  @staticmethod
  def output(pin, state):
    print(f"MockGPIO: Setting pin {pin} to state {state}")

  @staticmethod
  def input(pin):
    print(f"MockGPIO: Getting state of pin {pin}")
    return MockGPIO.HIGH  # Simulate always high

  @staticmethod
  def cleanup():
    print("MockGPIO: Cleaning up all pins")

  @staticmethod
  def cleanup(pin):
    print(f"MockGPIO: Cleaning up pin {pin}")
