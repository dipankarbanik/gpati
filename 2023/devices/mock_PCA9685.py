class PCA9685:
    def __init__(self, address=None, **kwargs):
        print(f"Mock PCA9685 initialized with address {address}")

    def set_pwm_freq(self, freq):
        print(f"Setting PWM frequency to {freq}")

    def set_pwm(self, channel, on, off):
        print(f"Setting PWM on channel {channel}, ON: {on}, OFF: {off}")

    def set_all_pwm(self, on, off):
        print(f"Setting all PWM, ON: {on}, OFF: {off}")

    def software_reset(self, **kwargs):
        print("Performing software reset")
