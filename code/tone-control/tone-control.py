import numpy as np
from scipy.io import wavfile
from scipy.fft import irfft, rfft, rfftfreq
from scipy.signal import butter, sosfilt, sosfilt_zi

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

def saveWAV(file, sample_rate, audio_data):
    """
    Saves an audio data array to a WAV file.
    
    Args:
        file_path (str): Path to save the WAV file.
        sample_rate (int): Sample rate of the audio.
        audio_data (np.array): Audio data array.
    """
    wavfile.write(file, sample_rate, audio_data)

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
    # Higher order = sharper cutoffs at band boundary conditions. Butterworth produces flat frequency response 
    # in passband, so smooth response is maintained while still offering sharp cutoff.
    sos = butter(32, cutoffs, btype=filter_type, fs=sample_rate, output='sos')

    # Thread used to understand how increasing order sharpens the transition between preserved and filtered 
    # frequencies and get closer to the "ideal brick wall" that our boundary conditions try to set:
    # https://dsp.stackexchange.com/questions/34127/higher-order-butterworth-filters

    return sos

def measureWithFFT(window_data, sample_rate):
    """
    Applies a real FFT using [`scipy.rfft`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.rfft.html) 
    to a window of audio data, extracting the frequencies and magnitudes.

    Real FFT is used since the FFT of real-valued inputs (e.g. an audio signal) results in a symmetric
    complex conjugate sequence, where positive frequency components have a corresponding negative component.
    This symmetry means only the positive frequencies are relevant when dealing with audio, hence the use of `rfft`.
    Reference: https://docs.scipy.org/doc/scipy/tutorial/fft.html#

    Args:
        window_data (np.array): Segment of the audio data.
        sample_rate (int): Number of samples per second of the audio.

    Returns:
        frequencies (np.array): Array of positive frequencies from the FFT result.
        magnitudes (np.array): Array of magnitudes for each frequency component.
    """
    fft_result = rfft(window_data)

    # Since the FFT result is complex (real and imaginary parts), absolute value will calculate √(a² + b²)
    # for the two parts, obtaining single values representing the relative strength of each frequency.
    # Reference: https://realpython.com/python-scipy-fft/
    magnitudes = np.abs(fft_result)
    frequencies = rfftfreq(len(window_data), d=1/sample_rate)

    return frequencies, magnitudes

def calculateBandEnergy(frequencies, magnitudes):
    """
    Take frequencies and magnitudes supplied from an FFT result and sums the magnitudes within defined 
    low, mid, and high band boundaries. Used for calculating the total sound energy for each band.

    Args:
        magnitudes (np.array): Magnitudes extracted from an FFT operation.
        frequencies (np.array): Frequencies extracted from an FFT operation.
    
    Returns:
        low_energy (float): Energy in the 0-300 Hz range.
        mid_energy (float): Energy in the 301-2000 Hz range.
        high_energy (float): Energy in the 2000+ Hz range.
    """
    # Filter magnitude elements to sum based on frequency value.
    low_energy = np.average(magnitudes[(frequencies >= 0) & (frequencies <= 300)])
    mid_energy = np.average(magnitudes[(frequencies > 300) & (frequencies <= 2000)])
    high_energy = np.average(magnitudes[frequencies > 2000])
    # If looking for peak energy, can use np.max()

    return low_energy, mid_energy, high_energy

def toneEqualizer(audio_data: np.ndarray, sample_rate, window_size=1024, window_move=512):
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
    # Tone filters for each band, has to be run with every sample
    low_filter = makeFilter(300, 'low', sample_rate)
    mid_filter = makeFilter((300, 2000), 'band', sample_rate)
    high_filter = makeFilter(2000, 'high', sample_rate)

    low_state = sosfilt_zi(low_filter)
    mid_state = sosfilt_zi(mid_filter)
    high_state = sosfilt_zi(high_filter)

    # If data has multiple dimensions, it is a 2D array of stereo audio
    stereo_bool = audio_data.ndim > 1
    # Put audio data in a list, transposing stereo will result in [2 arrays, left and right audio]
    channels = [audio_data] if not stereo_bool else audio_data.T
    adjusted_channels = []

    for channel in channels:
        adjusted_channel = np.zeros(len(channel))
        num_windows = (len(channel) - window_size) // window_move + 1

        for window_position in range(num_windows):
            # Determine which array elements in audio to place window
            start = window_position * window_move
            end = start + window_size
            window_data = channel[start:end]

            # Measure sound energy using FFT
            frequencies, magnitudes = measureWithFFT(window_data, sample_rate)
            
            # Calculate energy in each band tier
            low_energy, mid_energy, high_energy = calculateBandEnergy(frequencies, magnitudes)
            average_energy = (low_energy + mid_energy + high_energy) / 3

            # Set a threshold to turn off low-energy bands
            energy_threshold = 0.15 * average_energy

            # Gain calculation, multiplier for adjusting energy to the desired balance
            # Adjust gains with slight boosts for high frequencies if they’re being attenuated too much
            low_gain = np.sqrt(average_energy / low_energy) if low_energy > energy_threshold else 0.8
            mid_gain = np.sqrt(average_energy / mid_energy) if mid_energy > energy_threshold else 1.0
            high_gain = np.sqrt(average_energy / high_energy) if high_energy > energy_threshold else 1.2
            
            # Filter each frequency and scale to make the energies roughly equal
            # Scipy assumes there's 0s from the previous block if not given context of zi
            low_band, low_state = sosfilt(low_filter, window_data * low_gain, zi=low_state)
            mid_band, mid_state = sosfilt(mid_filter, window_data * mid_gain, zi=mid_state)
            high_band, high_state = sosfilt(high_filter, window_data * high_gain, zi=high_state)

            # Sum the bands to get the adjusted signal for this window
            # Apply a window function to smooth the edges
            window_function = np.hanning(window_size)
            adjusted_window = (low_band + mid_band + high_band) * window_function
            adjusted_channel[start:end] += adjusted_window[:end - start]

        adjusted_channels.append(adjusted_channel)

    # Combine adjusted channels back into a stereo (or mono) format
    adjusted_audio = np.array(adjusted_channels).T if stereo_bool else adjusted_channels[0]

    return adjusted_audio.astype(np.int16)

if __name__ == "__main__":
    sample_rate, audio_data = loadWAV('sine.wav')
    print(f"{sample_rate}")

    # 100ms with 48000 samples per second means 4800, so 4096 is closest power of 2
    adjusted_audio = toneEqualizer(audio_data, sample_rate, 1024, 512)
    saveWAV("adjusted-sine.wav", sample_rate, adjusted_audio)