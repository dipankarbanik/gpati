import os
from pydub import AudioSegment
import simpleaudio as sa


class BluetoothSpeakerPlayer:
    def __init__(self, mp4_path):
        self.mp4_path = mp4_path
        # Create a temporary audio file name based on the mp4 file's name
        self.audio_path = os.path.splitext(mp4_path)[0] + ".wav"
        self._extract_audio()

    def _extract_audio(self):
        """Extract audio from the MP4 file and save it as a WAV."""
        audio = AudioSegment.from_file(self.mp4_path, format="mp4")
        audio.export(self.audio_path, format="wav")

    def play(self):
        """Play the extracted audio."""
        song = AudioSegment.from_wav(self.audio_path)
        playback_obj = sa.play_buffer(
            song.raw_data,
            num_channels=2,
            bytes_per_sample=song.sample_width,
            sample_rate=song.frame_rate
        )
        playback_obj.wait_done()

    def cleanup(self):
        """Remove the temporary audio file."""
        os.remove(self.audio_path)


if __name__ == "__main__":
    player = BluetoothSpeakerPlayer("../sound.m4a")
    player.play()
    player.cleanup()
