import imageio
from luma.core.interface.serial import spi
from luma.oled.device import ssd1351
from luma.core.render import canvas
import time

class OledPlayer:
    def __init__(self, gif_path):
        self.gif_path = gif_path
        self.device = self._init_device()
        self.stop_playing = False  # Flag to control GIF playback

    def _init_device(self):
        serial = spi(device=0, port=0)
        return ssd1351(serial)

    def play(self, duration=0.1):
        # Read the GIF using imageio
        im = imageio.mimread(self.gif_path)

        # Check if the gif is the correct size
        if im[0].shape[:2] != (128, 128):
            raise ValueError("GIF must be 128x128 pixels")

        # Play each frame of the GIF
        for frame in im:
            if self.stop_playing:  # Check the flag before playing each frame
                break
            with canvas(self.device) as draw:
                draw.bitmap((0, 0), frame, fill="white")
            time.sleep(duration)

    def stop(self):  # Method to stop the GIF playback
        self.stop_playing = True

if __name__ == "__main__":
    player = OledPlayer("../picture.gif")
    try:
        player.play()
    except KeyboardInterrupt:  # Stop playback with Ctrl+C
        player.stop()
