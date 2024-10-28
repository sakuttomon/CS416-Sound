import numpy as np
from scipy.io import wavfile

def loadWAV(file):
    """
    Load a mono audio file, extracting its sample rate and audio data.

    Args:
        file (str): Path to WAV file.
    
    Returns:
        sample_rate (int): Number of samples per second.
        audio_data (np.array): Array containing data read from the WAV file.
    """
    sample_rate, audio_data = wavfile.read(file)
    return sample_rate, audio_data

def toneEqualizer():
    """
    Adjust the tone of an audio input, using FFT to measure sound energy across a
    given window size. 
    
    Within each window, frequencies are organized into low, mid, and high level bands. 
    For each band level, a tone filter scales the frequencies to the overall **average** 
    band energy of the window. The "speed" of adjusting the tone filters is determined by 
    the window size (how many samples to adjust at a time), and the number of samples to 
    move for the next FFT window.

    Args:
        audio_data (np.array): Array containing data read from the WAV file.
        sample_rate (int): Number of samples per second.
        window_size (int): Number of samples in each window to apply FFT on.
        window_move (int): Number of samples to overlap between windows, controlling the frequentness of adjustments.

    Returns:
        adjusted_audio (np.array): Array containing audio data with tone adjustments applied.
    """

if __name__ == "__main__":
    sample_rate, audio_data = loadWAV('sine.wav')
    print(f"{sample_rate}")