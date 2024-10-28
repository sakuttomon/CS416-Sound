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


if __name__ == "__main__":
    sample_rate, audio_data = loadWAV('sine.wav')
    print(f"{sample_rate}")