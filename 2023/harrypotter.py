import threading
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    import fakeRPi.GPIO as GPIO

from devices.RelaySwitch import RelaySwitch
from devices.ServoController import ServoController
from devices.BluetoothSpeakerPlayer import BluetoothSpeakerPlayer

class HarryPotterPlay:
    def __init__(self):
        # Initialize class attributes
        self.TROLLEY_SERVO_CHANNEL = 0
        self.TROLLEY_INITIAL_ANGLE = 90
        self.STAIRCASE_1_SERVO_CHANNEL = 1
        self.STAIRCASE_1_INITIAL_ANGLE = 180
        self.STAIRCASE_2_SERVO_CHANNEL = 2
        self.STAIRCASE_2_INITIAL_ANGLE = 0

    def setup(self):
        # All hardware interactions and initializations
        self.trolley = ServoController()
        self.staircase1 = ServoController()
        self.staircase2 = ServoController()
        self.train = RelaySwitch("SWITCH1", "train")
        self.castle = RelaySwitch("SWITCH2", "castle")
        self.quidditch = RelaySwitch("SWITCH3", "quidditch")
        self.fightScene = RelaySwitch("SWITCH4", "fightScene")
        self.music = BluetoothSpeakerPlayer("sound.m4a")

    def playscene(self):
        self.setup()  # Set up devices

        # Play music in a separate thread
        music_thread = threading.Thread(target=self.music.play)
        music_thread.start()

        self.pause()
        self.trolley.move_to_angle(self.TROLLEY_SERVO_CHANNEL, 180)
        self.train.switch_on_for_period(30)
        self.castle.switch_on_for_period(30)

        for _ in range(3):
            self.move_staircases()

        self.quidditch.switch_on_for_period(50)
        self.fightScene.switch_on_for_period(100)
        self.reset()

    def move_staircases(self):
        self.staircase1.move_to_angle(self.STAIRCASE_1_SERVO_CHANNEL, self.STAIRCASE_1_INITIAL_ANGLE - 90)
        self.staircase2.move_to_angle(self.STAIRCASE_2_SERVO_CHANNEL, self.STAIRCASE_2_INITIAL_ANGLE + 90)
        time.sleep(1)
        self.staircase1.move_to_angle(self.STAIRCASE_1_SERVO_CHANNEL, self.STAIRCASE_1_INITIAL_ANGLE)
        self.staircase2.move_to_angle(self.STAIRCASE_2_SERVO_CHANNEL, self.STAIRCASE_2_INITIAL_ANGLE)
        time.sleep(1)

    def reset(self):
        print("Resetting...")
        self.music.cleanup()
        self.trolley.move_to_angle(self.TROLLEY_SERVO_CHANNEL, self.TROLLEY_INITIAL_ANGLE)
        self.staircase1.move_to_angle(self.STAIRCASE_1_SERVO_CHANNEL, self.STAIRCASE_1_INITIAL_ANGLE)
        self.staircase2.move_to_angle(self.STAIRCASE_2_SERVO_CHANNEL, self.STAIRCASE_2_INITIAL_ANGLE)

    def destroy(self):
        print('Cleaning Up...')
        self.reset()
        GPIO.cleanup()

    def pause(self, seconds=0, prompt="Press Enter to continue..."):
        start_time = time.time()

        if seconds:
            print(f"Pausing for {seconds} seconds.")
            time.sleep(seconds)
        else:
            input(prompt)

        pause_duration = time.time() - start_time
        print(f"Paused for {pause_duration:.2f} seconds.")
        return pause_duration

if __name__ == '__main__':
    print('Starting Harry Potter Play...')
    play = HarryPotterPlay()
    try:
        play.playscene()
        play.destroy()
    except KeyboardInterrupt:
        print("Interrupted by user.")
        play.destroy()
    except Exception as e:
        print(f"An error occurred: {e}")
        play.destroy()