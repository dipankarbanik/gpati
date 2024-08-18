import sys
import time

# Conditional import of the GPIO library
try:
  import RPi.GPIO as GPIO
except ImportError:
  # Use mock GPIO if not on a compatible Raspberry Pi environment
  from mocks import mock_gpio as GPIO


class Relay:
  def __init__(self, pin, name):
    self.pin = pin
    self.name = name
    GPIO.setup(self.pin, GPIO.OUT)
    self.off()  # Set initial state to OFF

  def on(self):
    print(f"{self.name} (Pin {self.pin}) - ON")
    GPIO.output(self.pin, GPIO.HIGH)

  def off(self):
    print(f"{self.name} (Pin {self.pin}) - OFF")
    GPIO.output(self.pin, GPIO.LOW)

  def switch_on_for_period(self, period):
    self.on()
    time.sleep(period)
    self.off()

  def cleanup(self):
    GPIO.cleanup(self.pin)


def main():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  if len(sys.argv) != 5:
    print(
        "Usage: python relay_util.py <PIN_NUMBER> <RELAY_NAME> <ON/OFF> <DURATION_IN_SECONDS>")
    sys.exit(1)

  pin_number = int(sys.argv[1])
  relay_name = sys.argv[2]
  action = sys.argv[3].upper()
  duration = float(sys.argv[4])

  relay = Relay(pin_number, relay_name)

  try:
    if action == "ON":
      relay.switch_on_for_period(duration)
    elif action == "OFF":
      relay.off()
    else:
      print("Invalid action specified. Use 'ON' or 'OFF'.")
      sys.exit(1)
  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    relay.cleanup()


if __name__ == "__main__":
  main()
