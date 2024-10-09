import numpy as np
from scipy.io.wavfile import write
import sounddevice

class SineWaveWAV:
    def __init__(self):
        """
        Instantiate all class variables following provided specification on the sine wave to generate.
        """
        # Specifications for sine wave:
        # Channels per frame: 1 (mono)
        # Sample Format: 16 bit signed (values in the range -32767..32767)
        self.amplitude = 8192           # 1/4 maximum possible 16-bit amplitude (values in the range -8192..8192)
        self.frequency = 440            # Hz, cycles per second
        self.duration = 1               # second
        self.sample_rate = 48000        # samples per second

if __name__ == "__main__":
    wav = SineWaveWAV()