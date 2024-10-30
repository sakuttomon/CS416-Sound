import numpy as np
from scipy.io import wavfile
from scipy.signal import butter

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

def makeFilter(cutoffs, filter_type, sample_rate):
    """
    Designs a [butterworth filter](https://en.wikipedia.org/wiki/Butterworth_filter) 
    using [`scipy.signal.butter`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html) 
    with supplied cutoff frequencies and band type. Outputs resulting filter coefficients in second-order sections 
    (sos) format, a common method for general-purpose filtering.
    
    Args:
        cutoffs (int or int tuple): Cutoff frequency/frequencies for the filter.
        filter_type (str): The type of filter to create, expects 'lowpass', 'bandpass', or 'highpass'.
        sample_rate (int): Number of samples per second of the audio.
    
    Returns:
        sos (np.array): Second-order sections representation of the filter.
    """
    # Asked ChatGPT for a suggestion on filter order (N=10), an order of 10 results in sharp enough
    # cutoffs to enforce our band boundary conditions. Butterworth produces flat frequency response 
    # in passband, so smooth response is maintained while still offering sharp cutoff.
    sos = butter(10, cutoffs, btype=filter_type, fs=sample_rate, output='sos')

    # Thread used to understand how increasing order sharpens the transition between preserved and filtered 
    # frequencies and get closer to the "ideal brick wall" that our boundary conditions try to set:
    # https://dsp.stackexchange.com/questions/34127/higher-order-butterworth-filters

    return sos

def toneEqualizer(audio_data: np.ndarray, sample_rate, window_size, window_move):
    """
    Adjust the tone of an audio input, using FFT to measure sound energy across a
    given window size. 
    
    Within each window, frequencies are organized into low, mid, and high level bands. 
    For each band level, a tone filter adjusts the frequencies to the overall **average** 
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
    # Tone filters for each band
    low_filter = makeFilter(300, 'lowpass', sample_rate)
    mid_filter = makeFilter((300, 2000), 'bandpass', sample_rate)
    high_filter = makeFilter(2000, 'highpass', sample_rate)

    # If data has multiple dimensions, it is a 2D array of stereo audio
    stereo_bool = audio_data.ndim > 1
    # Put audio data in a list, transposing stereo will result in [2 arrays, left and right audio]
    channels = [audio_data] if not stereo_bool else audio_data.T

    for channel in channels:
        audio_to_adjust = np.copy(audio_data)
        num_windows = (len(channel) - window_size) // window_move + 1

        for window in range(num_windows):
            pass

if __name__ == "__main__":
    sample_rate, audio_data = loadWAV('sine.wav')
    print(f"{sample_rate}")