import numpy as np
from scipy.io.wavfile import write
import sounddevice
import time

class SineWaveWAV:
    def __init__(self):
        """
        Instantiate all class variables following provided specification on the sine wave to generate.
        """
        # Specifications for sine wave:
        # Channels per frame: 1 (mono)
        # Sample Format: 16 bit signed (values in the range -32767..32767)
        self.fourth_amplitude = 8192    # 1/4 maximum possible 16-bit amplitude (values in the range -8192..8192)
        self.frequency = 440            # Hz, cycles per second
        self.duration = 1               # second
        self.sample_rate = 48000        # samples per second

        self.half_amplitude = self.fourth_amplitude * 2    # 1/2 16-bit amplitude (values in the range -16384..16384)

        # Although sine wave is a continuous function, digital audio must discretize / take
        # snapshots of the audio signal, hence sample rate to capture samples of audio

        # Digital Audio Basics... by Griffin Brown
        # https://www.izotope.com/en/learn/digital-audio-basics-sample-rate-and-bit-depth.html

        # Construct equally spaced time points array (separated apart by 1/sample rate)
        # Duration of Sine Wave is 1 second, sample rate is per second, 
        # so we generate 48000 * 1 sample points to fit in that duration. 
        self.time_points = np.linspace(0, self.duration, self.sample_rate * self.duration, False)
    
    def writeSineWAV(self):
        """
        Calculates a discretized sine wave according to the specifications and writes the
        result into a file `sine.wav`. The wave mimics the continious flow of a sine function by
        applying the sine formula at equally spaced apart samples according to the sample rate.

        Sine Wave Formula: https://en.wikipedia.org/wiki/Sine_wave#Sinusoid_form

        Amplitude * sin(2 * pi * frequency * time + phase)
        """
        # Apply the sine equation to all the time points to generate sine wave
        # No phase provided, essentially + 0
        sine_wave = self.fourth_amplitude * np.sin(2 * np.pi * self.frequency * self.time_points)

        # Since sine_wave could have floats, convert wave values to 16 bit intgers to follow
        # specification (sample format states 16 bit signed to write to WAV file)
        wav_sine_wave = sine_wave.astype(np.int16)

        print("Writing sine.wav to current directory...")
        write('sine.wav', self.sample_rate, wav_sine_wave)
        print("Write Successful")

    def writeClippedWAV(self):
        """
        Generates a sine wave with 1/2 maximum amplitude (-16384..16384) except samples that
        exceed the minimum and maximum amplitude (-8192..8192) are clipped to those bounds.

        Writes the clipped sine wave to a file `clipped.wav`, then plays the wave to an
        audio output using the sounddevice library.
        """
        sine_wave = self.half_amplitude * np.sin(2 * np.pi * self.frequency * self.time_points)
        
        # Limit the values in the array to satisfy capping at 1/4 amplitude
        clipped_sine = np.clip(sine_wave, -self.fourth_amplitude, self.fourth_amplitude)

        # Convert array values to expected WAV format
        wav_clipped_sine = clipped_sine.astype(np.int16)

        print("Writing clipped.wav to current directory...")
        write('clipped.wav', self.sample_rate, wav_clipped_sine)
        print("Write Successful")
        
        print("Playing clipped sine wave directly to audio output...")
        sounddevice.play(wav_clipped_sine, self.sample_rate)
        sounddevice.wait()
        print("Sound has finished playing.")

if __name__ == "__main__":
    wav = SineWaveWAV()
    # (1) create sine.wav
    wav.writeSineWAV()

    time.sleep(1)
    print()
    
    # (2) create clipped.wav, (3) play a clipped sine wave (directly).
    wav.writeClippedWAV()
    print()
    