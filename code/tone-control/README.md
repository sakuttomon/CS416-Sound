# Adaptive Tone Control - Irvin Lu

This assignment project takes in a provided WAV file and arbitrarily divedes its audio frequencies into three arbitrary bands: low (0-300 Hz), mid (300-2000 Hz), and high (2000+ Hz). An FFT is used to calculate the sound energy within the three frequency bands across short time windows.

Tone filters are then applied to adjust the energy in each band, balancing them so that the energies of the three bands are roughly
equal. This process demonstrates **tone control** - adjusting the volume within specific frequency bands independently. Through
manipulating individual frequencies to be softer or louder by adjusting their energies, the original audio with its varied band
"levels" can sound more balanced or neutral in volume.

## Reflections

This objective was a very "deep-end" experience for me, especially so given my lack of knowledge in digital sound processing.
Throughout my commits, I've slowly understood more and more of how this process operates, described in the following sub-section,
but I have not fully wrapped my head around a way to implement it.

### How it works

The essential process is that for each band level, three filters are created. In a separate instance, an FFT is applied to measure energies of the low, mid, and high band ranges within a window. After determining the gain necessary to roughly equalize the overall
energies of the three bands, the filters and gains are "combined" to adjust a band to be more similar to the other two bands, thus resulting in a more balanced audio signal.

1. An input WAV file is loaded through `scipy.wavfile`, extracting the sample rate and audio data array.
2. Three filters are made for each band (low, mid, high). All filters are made using the
   [butterworth filter](https://en.wikipedia.org/wiki/Butterworth_filter), a filter designed to produce a flat frequency response in the passband, resulting in minimal ripples. Each filter is outputted as a second-order-section (`sos`) formatted list, a stable implementation structure that `scipy` recommends for general-purpose filtering.

   The filter type and cutoffs to generate a filter for are determined by the corresponding band level. For example the `low_filter` is made using the band type `lowpass` and a cutoff of `300`.

3. The program works for both mono and stereo audio by looping through 1 or 2 channels (array dimensions) of the audio data. Within each channel, an inner loop increments through windows, meant for viewing view short time segments of the overall signal and analyze frequency content. These windows are sized as 1024 samples, with a movement of 512 samples to smooth the transitions between eventual adjustments.

4. Within each window, frequencies and magnitudes (absolute values of the frequency indexes) are calculated by applying an FFT.

5. Energies for each band are calculated by taking the **average** of the frequencies within the respective cutoffs.

6. Using an overall average calculated from the previous energies, gains are calculated for each band level. The purpose of these gains is to determine the amplification necessary for the frequencies within each band to approach the overall average.

7. An `sosfilt` is then applied to the window data, multiplied alongside the respective gain. The gain informs the filter how to
   adjust each band to manifest a balanced sound effect.

8. The filtered results for each band are then combined to an `adjusted_window`, which is then applied back to the channel before moving on to the next window and repeating this process.

### Limitations

The code's current state seemingly produces "filter transients" where ripples are occuring between each window end. To provide context to each `sosfilt` call of the filter results before it, I used [`sosfilt_zi`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfilt_zi.html#sosfilt-zi) and the `zi` parameter to supply the previous state to the filter methods. However, the
resulting WAV files still showed the same ripples.

As a bandaid fix, I applied a [Hann window function](https://en.wikipedia.org/wiki/Hann_function) to smooth transitions.
Realistically, windowing is not necessary since filters would automatically perform such smoothing due to how they operate.
Some research indicates that the Butterworth filter I used has the disadvantage of causing
[transients](https://en.wikipedia.org/wiki/Transient_response), but there are a lot of
possible factors, linked below, that make it difficult to pinpoint the exact solution.

- [Transient Explanation](https://www.dsprelated.com/freebooks/filters/Transient_Response_Steady_State.html)
- [Step Response](https://stackoverflow.com/questions/27540434/filter-gain-issue-when-using-scipy-signal-in-python)
- [Filter Order](https://dsp.stackexchange.com/questions/94015/butterworth-filter-vs-elliptic-filter-artefacts-and-huge-transient#:~:text=If%20I%20change%20the%20filter,infinite%2Dimpulse%2Dresponse)
- [Signal Length and Edge Samples](https://www.mathworks.com/matlabcentral/answers/407690-why-is-there-a-ripple-in-the-response-of-the-low-pass-butterworth-filter)
