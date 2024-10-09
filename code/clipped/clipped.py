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
    
    def writeSineWAV(self):
        """
        Calculates a discretized sine wave according to the specifications and writes the
        result into a file `sine.wav`. The wave mimics the continious flow of a sine function by
        applying the sine formula at equally spaced apart samples according to the sample rate.

        Sine Wave Formula: https://en.wikipedia.org/wiki/Sine_wave#Sinusoid_form

        Amplitude * sin(2 * pi * frequency * time + phase)
        """
        # Although sine wave is a continuous function, digital audio must discretize / take
        # snapshots of the audio signal, hence sample rate to capture samples of audio
        # Digital Audio Basics... by Griffin Brown
        # https://www.izotope.com/en/learn/digital-audio-basics-sample-rate-and-bit-depth.html

        # Construct equally spaced time points array (separated apart by 1/sample rate)
        # Duration of Sine Wave is 1 second, sample rate is per second, 
        # so we generate 48000 * 1 sample points to fit in that duration. 
        time_points = np.linspace(0, self.duration, self.sample_rate * self.duration, False)

        # Apply the sine equation to all the time points to generate sine wave
        # No phase provided, essentially + 0
        sine_wave = self.fourth_amplitude * np.sin(2 * np.pi * self.frequency * time_points)

if __name__ == "__main__":
    wav = SineWaveWAV()
    # (1) create sine.wav
    wav.writeSineWAV()