import sys
import os
import time
import logging
import signal

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set up import paths
script_dir = os.path.dirname(
    __file__)  # Get the directory where the script is located
parent_dir = os.path.dirname(
    script_dir)  # Assumes the parent directory contains the 'mocks' and 'controls' directories
sys.path.append(parent_dir)  # Add this directory to sys.path

# Try to import GPIO, fall back to mocks if not available
try:
  import RPi.GPIO as GPIO
except ImportError:
  from controls.mocks import MockGPIO as GPIO

from controls.Servo import Servo
from controls.Relay import Relay


def signal_handler(sig, frame):
  logging.info(f"Signal {sig} received, initiating cleanup.")
  cleanup()
  sys.exit(0)


def setup_signal_handling():
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)


def setup_signal_handling():
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)


def Manthan():
  logging.info("Starting Manthan sequence.")
  servo = Servo()
  try:
    servo.rotate_servo(1, 0, 180)
    servo.rotate_servo(1, 180, 0)
    servo.rotate_servo(2, 180, 0)
    servo.rotate_servo(2, 0, 180)
    time.sleep(20)
    for _ in range(10):
      servo.rotate_servo(3, 0, 90)
      servo.rotate_servo(3, 90, 0)
  except Exception as e:
    logging.error(f"Exception in Manthan: {e}")
  logging.info("Completed Manthan function.")


def Ganga():
  logging.info("Starting Ganga sequence.")
  servo = Servo()
  try:
    servo.set_servo_angle(2, 30)
    time.sleep(20)
    relay = Relay("SWITCH1")
    relay.on()
    time.sleep(20)
    relay.off()
  except Exception as e:
    logging.error(f"Exception in Ganga: {e}")
  logging.info("Completed Ganga function.")


def Tandav():
  logging.info("Starting Tandav sequence.")
  servo = Servo()
  relay = Relay("SWITCH2")
  try:
    servo.rotate_servo(0, 0, 180)
    relay.on()
    time.sleep(20)
    relay.off()
  except Exception as e:
    logging.error(f"Exception in Tandav: {e}")
  logging.info("Completed Tandav function.")


def cleanup():
  logging.info(
      "Running cleanup to reset devices to default positions and clean up GPIO.")
  try:
    servo = Servo()
    servo.set_servo_angle(1, 0)
    servo.set_servo_angle(2, 0)
    servo.set_servo_angle(3, 0)
    Relay("SWITCH1").off()
    Relay("SWITCH2").off()
    GPIO.cleanup()
  except Exception as e:
    logging.error(f"Error during cleanup: {e}")
  logging.info("Cleanup successful, all devices reset and GPIO cleaned up.")


if __name__ == "__main__":
  setup_signal_handling()
  try:
    Manthan()
    Ganga()
    Tandav()
  finally:
    cleanup()
