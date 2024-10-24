import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import get_window

def plotSpectrogram(wav_file, window_samples=1024, num_overlap=512):
    """
    Plots a basic mono audio WAV file to a spectrogram with Matplotlib.

    Args:
        wav_file: The file path to a WAV file to plot a spectrogram for.
        window_samples: Length of the FFT window, number of samples.
        num_overlap: Number of samples that next window shares with previous window.
    """
    sample_rate, data = wavfile.read(wav_file)

    # Normalize to [-1, 1]
    data = data / np.max(np.abs(data), axis=0)

    # Hann: Bell-shaped curve window function, used for smoothly 
    # reducing amplitude of signal to zero at the edges.
    window = get_window('hann', Nx=window_samples)
    
    plt.figure(figsize=(10, 6))
    # Computes FFT automatically given parameters
    plt.specgram(data, NFFT=window_samples, Fs=sample_rate, window=window, noverlap=num_overlap, cmap='inferno', scale='dB')

    plt.title(f'Spectrogram of {wav_file}')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.colorbar(label='Power/Frequency (dB/Hz)')
    plt.show()

if __name__ == "__main__":
    plotSpectrogram('clipped.wav')

