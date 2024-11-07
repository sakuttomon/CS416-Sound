# Engineering Notebook - Irvin Lu

A document containing notes or reflections about the work and progress done throughout the course, organized by each week and
the estimated date where such activities occured or finished. Notes taken from lecture are prefaced with **_Notes_** in the date header.

| Table of Contents |
| ----------------- |
| [Week 1](#week-1) |
| [Week 2](#week-2) |
| [Week 3](#week-3) |
| [Week 4](#week-4) |
| [Week 5](#week-5) |
| [Week 6](#week-6) |

## Week 1

### 10/1/24 - Beginning

Set up this GitHub repository to act as a student portfolio for the class. Wrote a README describing the repository structure and started this notebook.

## Week 2

### 10/10/24 - Discretization, Sampling, Frequencies

During this week, I did some external research to help me understand the terminology introduced in lecture and
to get more clarity on how to approach the [`clipped`](code/clipped/) assignment. I found an article
"[Digital Audio Basics...](https://www.izotope.com/en/learn/digital-audio-basics-sample-rate-and-bit-depth.html)"
by Griffin Brown that connected the dots on how real sound is translated to digital formats and why certain standards
are imposed the way they are.

Although sine waves are continuous functions, digital audio must **discretize**, or take snapshots of, the audio signal, hence the
process of capturing "samples" from the signal. The sample rate determines the interval between these captures; with a high enough
rate, computers essentially replicate the analog wave by having so many sample points that it appears as a connected line when
visualized. Each sample serves as a data point that builds up the overall shape of the wave when played back.

The [Nyquist Limit](https://www.slack.net/~ant/bl-synth/3.nyquist.html) - Maximum frequency equals half the sample rate (conversely, the rate must be double the frequency) to prevent aliasing distortions. A sample rate of 48,000 Hz is standard for movie and video audio.

The article explains that humans hear frequencies up to around 20 kHz. However, instead of simply doubling the sample rate to 40 kHz,
an extra few kHz is reserved in order to apply a [low-pass filter](https://en.wikipedia.org/wiki/Low-pass_filter) to reduce high
frequencies from causing aliasing. As a result, applying a slightly higher sample rate beyond 40 kHz gives extra headroom for these
filters to reduce frequencies smoothly and preserve the slopes of the original waves.

| Clipping                                        | Low-Pass Filter                                               |
| ----------------------------------------------- | ------------------------------------------------------------- |
| Limit amplitude by trauncating wave             | Gradually reduce down high frequencies that are beyond cutoff |
| Distorts shape due to flattening wave at limits | Attempts to preserve shape of the signal's tone               |

### 10/11/24 - Clipping Portfolio Objective

I merged the [`clipped`](code/clipped/) assignment branch into the main branch. The dedicated [README](code/clipped/README.md) within the directory contains my reflections and lessons learned on how I approached the objective.

## Week 3

### 10/14/24 - Saying Hi in Zulip

Wrote an introduction of myself to share in the course [Zulip](https://zulip.com/). In this introduction, I expressed my inexperience
with sound and digital audio concepts, so the course appealed to me as a way to start establishing the basics. I mentioned interests
in "behind-the-scenes" content of media, but sound and music is a field I've yet to dive deep in. So, this class focused on the
interactions between computers and audio seemed like a perfect motive to start learning this hobby topic and make some fun projects,
while also feeling relevant to my field of study.

### 10/18/24 - _Notes_: Understanding Frequency

This week involved various video lectures introducing many concepts. Notes and takeaways are organized per video topic below.

#### Frequency Domain and Fourier Transform

_Fourier's Theorem_ - Infinitely repeating sound can be represented as a sum of sinusoids (which hearing decomposes to).  
Angular Frequency (`ω`) and normal frequency (`f`) mixed via: **$ \omega = 2 \pi f $**, once around a circle = one cycle.

- Continuous waveform $f(t)$ in the **time domain**.
- Continuous spectrum $\hat{f}(\omega)$ in the **frequency domain**, shows amplitude and phase of sine wave
  at every frequency.

[Euler's Formula](https://en.wikipedia.org/wiki/Euler%27s_formula) allows expressing sum of sinusoids to sum of exponentials.

Application of [Fourier Transform](https://en.wikipedia.org/wiki/Fourier_transform) - Take time domain signal and multiply it by sine
waves integrated throughout all the time. **Unpractical due to infinite domain for integral**. Put in time domain function, transform
it to a function from frequency to sound pressure. Because frequency measured in radians (one cycle = $ 2\pi $), other way around is
near inverse. Conversions between signal of frequences and signal of time points:

$$
\hat{f}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i \omega t} dt \qquad
f(t) = \frac{1}{2 \pi} \int_{-\infty}^{\infty} \hat{f}(\omega) e^{i \omega t} d\omega
$$

#### Discrete Fourier Transform

Use limits to rid of infinite integrals, and take out a chunk out of the infinitely repeating sequence and mark as the period $P$:
$$\hat{f}(\omega) = \int_{0}^{P} f(t) e^{-i \omega t} dt$$

Since $P$ is unknown, take a very large value to capture signals with long periods. Moreover, $f(t)$ is also unknown since it's a
continuous time signal when we have **discrete samples**. By treating the signal as 0 for all places except the discrete sample
points, can express $f(t)$ as a [sum of samples](https://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/)
and compute at discrete frequences $k$.

- $X[k]$ is frequency domain representation, each $k$ corresponds to a frequency bin, showing the amplitude and phase of the signal at that particular frequency.
- $x[n]$ is time domain, where $n$ represents a sample at a discrete time point.

$$
X[k] = \sum_{n=0}^{N-1} x[n] e^{-i k n / N} \qquad
x[n] = \frac{1}{2 \pi N} \sum_{k=0}^{N-1} X[k] e^{i k n / N}
$$

#### Applying the DFT

Above DFT formulas assume $N$ samples cover exactly one period of the overall signal: $x[n]$ _is cyclic, where $x$ is exactly the period._

_Windowing_ - Taper off signal by multiplying ends of DFT by [window function](https://en.wikipedia.org/wiki/Window_function) (bell-curve shape). Acts as a low-pass filter due to filtering signal at ends.  
_Ex_: Sine Window - $sin(\pi n / N) x[n]$

Bins "[leak](https://wiki.besa.de/index.php?title=File:Spectral_%285%29.gif)" to neighboring bins, so amplitude of a bin may not
fully represent the frequency of the bin. DFT thus look like overlapped [Gaussian Filters](https://en.wikipedia.org/wiki/Gaussian_filter).

_Fast Fourier Transform_ - $O(N \lg N)$ performance compared to DFT $O(N^2)$, used to obtain whole spectrum, requires power-of-two
number of samples and output frequencies distributed linearly. Algorithm used to apply DFT, $N$ .

_Discrete Cosine Transformation_ - Similar to FFT, but gives only magnitudes, ignores phase information since amplitude is much more
valuable, used in compression and processing (`MPEG`).

_[Triangle](https://en.wikipedia.org/wiki/Triangle_wave) and [Square](https://en.wikipedia.org/wiki/Square_wave) Waves_ - Fundamental + odd harmonics.  
_Harmonic_ - Multiple of a fundamental. E.g. odd harmonic of $f$ appear at $3f$, $5f$, etc.

- _Total Harmonic Distortion_ - Sine wave input, measure power of non-sine wave components that come out due to distortion.
- _White Noise_ - Random samples, random frequencies of random amplitudes, resulting in irregular distribution of spectrum.

DFT Applications:

- _Frequency Analysis_ - Look for peaks in spectrum post-DFT.
- _Filtering_ - Change frequencies post-DFT, then perform inverse DFT, resulting in tone-controlled signal.
- _Lossy Compression_ - Remove unwanted stuff post-DFT.

#### Musical Notes

_Note_ - Sound with a given fixed frequency "value". Starts at a time (_on time_) and ends at duration (_off time_). Notes can overlap (_polyphony_).  
_Octave_ - Frequency that is 2x some other frequency. **Divided into 12 parts**; since humans hear frequencies on a logarithmic scale, a given part looks like:

$$\textrm{note}_i(f) = f \cdot 2^{i/12}$$

_Ex_: The first note (i=0) simply equals `f`, whilst a note an octave up (i=12), which is the 13th note, equals `2f` since 12/12 = 1.

Base Frequency for a Note: 440 Hz _(Western Scale)_  
[MIDI Key Numbering](https://studiocode.dev/resources/midi-middle-c/) - Based on piano keys. _Ex_: 440Hz A = Key 69, A4, in Octave 4.  
Notes given letter names with **Sharp** (`#`) or **Flat** (`♭`) modifier.

#### Digital Audio Filtering

_Filter_ - Change amplitude or phase to emphasize or de-emphasize frequencies. E.g. tone control, equalizer, band limiter, etc.  
_Filter Shapes_ - Low Pass, High Pass, Bandpass, Band Notch. [Audio Filters Explained](https://www.edmprod.com/audio-filters/)  
_Passband, Stopband_ - Frequences that pass by the filter, otherwise blocked or rejected.

In **time domain**, samples are numbered, sampling rate often disregarded. Amplitude normalized to -1..1  
Frequency Domain: Frequencies range from 0..1 (Nyquist Limit - Samples must be 2x rate of highest frequency).

#### FIR Filters

_Impulse_ - Sample that has maximum amplitude for exactly 1 sample, then 0s afterward.  
_Finite Impulse Response_ - DFT filter would treat impulses identically. When pulse leaves impulse window, DFT would stay 0 forever.
Impulses presented to the filter eventually go away in favor of the 0s.

_IIR Filter_ - Infinite Impulse Response, use previous filter inputs/outputs to decide next filter output. Preserves impulses in
output and contribute to next chunk to filter due to looping the impulse back into the (previous) input. Will eventually damp out
the more an impulse is used, and discretization may fully eliminate such impulses if they end up being too small to represent.

- Ideally reduces amplitude of impulse over time - _stable filter_

## Week 4

### 10/22/24 - _Notes_: Review of DFT

DFT: Given a sequence $x[t]$ of samples at sample rate $r$ (in samples/sec) produce a sequence $X[k]$ of powers at frequencies,
where $k$ is the normalized frequency $k = 2f / r$, $f = k/2r$

```python
# Sequence of frequencies
for k in range(N):
  X[k] = sum([x[n] * exp(-i * k * n / N)] for n in range(N))
```

Output would be a complex number, representing the power of particular frequency $k$, and phase (shift of sine wave).
As $k$ ranges from 0 to N, it ranges from **0 to the Nyquist Rate**.

FFT would give linearly ranged x-axis from 0 to Nyquist frequency.

### 10/24/22 - _Notes_: Filter Design

**FIR Lowpass Filter**

$x[n]$ is the nth sample of input, $y[n]$ is the nth sample of output. Amplitude of sample is assumed -1..1

Equation to implement: $y[n] = \frac{1}{2}(x[n] + x[n - 1])$. Takes the average of the sample and the sample before it.
At first or last sample, no previous sample to reference. Can enforce beginning and end boundaries.

If sample $x[n]$ is positive, sample $x[n-1]$ will tend to be negative, so they will tend to cancel. For
lower frequencies the sample $x[n]$ will be close to $x[n-1]$ so they will reinforce.

$$ Lowpass: y[i] = \frac{1}{k} x[i-k \ldots i] \cdot a[k \ldots 0] $$

Lowpass Advantages

- _Inversion_: Negate all coefficients and add 1 to the "center" coefficient — flips the spectrum, so high-pass.
- _Reversal_: Reverse the order of coefficients — reverses the spectrum, so high-pass.
- _Superposition_: Average the coefficients of two equal-length filters — spectrum that is the product of the filters. If one is low-pass and the other high-pass, this is band-notch. Invert to get bandpass.

Code referenced in class: https://github.com/pdx-cs-sound/soundfreq

Filters allow for resampling by filtering out sequences, then sample the remaining (e.g. every 6th sample)

### 10/25/24 - Playing around with FFT and Spectrograms

Throughout the week, to greater understand how external libraries implement FFT and the process of measuring frequencies,
I made a program [`fft-spectrogram.py`](code/spectrogram-fun/fft-spectrogram.py) within the [`spectogram-fun`](code/spectrogram-fun/)
directory that plots the spectrogram of a WAV file using Matplotlib's FFT functionalities.

Takeaways about the role of window functions when applying FFT:

- FFT assumes input signal is periodic, but real signals don't purely repeat continiously, so FFT would produce spectral leakage discontinuities due to cutting off the signal.
- Window functions mitigate this leakage by tapering signal at edges of the window. The window would smoothly reduce the amplitude of the signal to zero at the edges, reducing discontinuities between windows.
- The [Hann window](https://en.wikipedia.org/wiki/Hann_function) is a normal curve function, which would produce the aspired smoothing effect at the quartile edges.
- Window effectively acts as a filter that smooths the data before applying the FFT

The dedicated [`README`](code/spectrogram-fun/README.md) contains my analysis about the spectrogram results, the patterns I found
from interpreting the frequency plot, and what those patterns mean.

## Week 5

### 10/29/24 - _Notes_: Effects

Wet & Dry - The affected/unaffected parts of the sound signal.  
Wet/Dry Gain - Higher wet gain increases the strength of the reverb, dry signal is sound without reverb.

_Compression_ - Make volume more of the same. Typically implemented as linear (log space b/c volume) gain functions with a "knee".  
_Expansion_ - Make differences in volume wider. E.g. compander: expand sounds, perform effects, then compress back.

_Knee_ - How compressor transitions between non-compressed and compressed states

- _Soft_ - Smoother and more gradual compression.
- _Hard_ - Quickly clamps down on signal upon passing threshold.

<img src=https://media.uaudio.com/assetlibrary/b/l/blog_audio_compression_basics_feat_1_@2x_1.jpg width=360 height=240>

Code referenced in class: https://github.com/pdx-cs-sound/effects/blob/master/compressor.py

### 10/31/24 - _Notes_: Tone Control, More Effects

FFT is performed in chunks (windows), whereas filter is applied throughout all samples. Realize that when a filter is going,
it initially is given a block of all 0s, meaning the beginning may appear wonky. The filter needs to have a state of the
previous block saved as it goes through the remaining blocks. Calling scipy `sosfilt` requires context of the previous block.

**Implementing an Effect**: https://github.com/pdx-cs-sound/effects/blob/master/distortion.py

### 11/3/24 - Adaptive Tone Control

I merged the [`tone-control`](code/tone-control/) assignment branch into the main branch. The implementation is slightly
flawed due to my inexperience, but I feel the knowledge I gained and the resulting output is satisfactory. The dedicated
[`README`](code/tone-control/README.md) within the directory details my reflections and thought process about how
the code works, which were derived from the many things I researched and learned throughout implementing the objective.
Below is a summary of my takeaways:

- _Gain_ - The amplifier to adjust an audio signal. In this objective, gain determines the multiplier to adjust each frequency within
  the low/mid/high bands that would boost or attentuate the respective energies to the overall average.
- _Energy Calculation_ - Performing an FFT returns frequencies, which are complex values (real and imaginary) representing amplitude and phase. Calculating the **magnitude** can serve as the energy of a given frequency.
- _Filter Startup Transients_ - When applying a filter in window chunks, each call maintains an internal state about the previous samples to inform the next samples and produce a continuous response. Failing to remember past samples mean a filter starts fresh
  at every window, resulting in transients that cause distortions.
- _Combining Bands_ - Since the objective organizes band levels by frequency ranges, the low, mid, and high bands can be manipulated separately, then summed to reconstruct the windowed audio signal.
- _Minimal Energy Bands_ - When certain frequency bands have little to no energy (e.g. a sine wave would have power in one band), applying gain can disproportionately amplify noise or artifacts in those bands. This exaggerated adjustment can be solved by "turning off" bands, which an energy threshold can enforce on gain calculation.

## Week 6

### 11/4/24 - Project Ideas, Thought Process

I'm really fond of video game music, which extends to music made within the limitations of older consoles, such as the Nintendo 64 or
DS. I've enjoyed many covers online that take a song and "convert" it into the style of another video game or an 8/16-bit retro
rendition.

As such, my research for something feasible to do as a project centers around manipulating or producing "gamified" or retro
sounds. The following summarizes my research and help serve as context for what my eventual project will be:

- **_Soundfonts_** - Most song covers to a game's style use [soundfonts](https://en.wikipedia.org/wiki/SoundFont), a file format that
  provides a ton of samples from the source for playing MIDI sounds. This collection of samples is how an artist can take a song and
  make it sound like another game (e.g. Pokemon Black and White) by covering the song using audio samples from the game.

  - **Idea**: Take an input audio file and create a soundfont file for it.
    - _Practicality_: There are Python libraries ([`sf2_loader`](https://pypi.org/project/sf2-loader/)) to help with playing and rendering soundfonts. However, as someone inexperienced in music composition, it might not feel fulfilling to program a
      soundfont, then not actually knowing to use it to make music.
  - **Idea**: Apply an existing soundfont onto an input audio file, remixing the audio.
    - _Practicality_: Algorithmically applying a soundfont can be very error-prone. Musicians still need to compose how a song will sound like using the soundfont; running a program to substitute samples ignores musical intent, expression, and rhythmic content that make songs feel cohesive.
    - Moreover, decomposing a song into individual elements (e.g. melody, harmony, bass, percussion) will be very challenging due to the mix of sounds and likely requirement to use machine learning, which is out of scope.

- **_Retro Compression_** - Music from the early console era had many limitations due to the hardware that the sound was played on.

  - **Idea**: An audio compression program to make sounds more retro-esque. Ways that compression can be achieved:
    - [Bitcrushing](https://en.wikipedia.org/wiki/Bitcrusher): Reducing bit depth / resolution of the audio.
    - Sample Rate Reduction: Music from this era had a limited frequency range, so down-sampling can mimic these limits.
    - Filtering: Low/highpass to filter out frequencies older systems couldn't achieve, e.g. high frequencies weren't captured very well on such consoles.
  - _Practicality_: Compressing audio this way is feasible as a program, but the music won't necessarily sound "retro", rather just a low quality rendition.
    - The input audio needs to already sound like a song belonging to the older console era, otherwise the compressed music simply sounds muffled.
    - The musical expression and arrangement techniques composers did within their limitations would be missing in this program.

- :sparkles: **_Chiptune Synthesizer_** - From my research above on what makes music "retro", I discovered the term
  [chiptune](https://en.wikipedia.org/wiki/Chiptune) music, which is characterized by its use of simple waveforms, such as square, triangle, and sawtooth waves.
  - **Idea**: Take an input of musical key notes that form a melody, and synthesize those notes using a user-chosen basic wave,
    thus producing chiptune music. To allow music expression, each note can be accompanied by a duration and volume setter to affect how the wave plays the note.
  - _Practicality_: This project seems the most feasible to accomplish given my inexperience.
    - Key notes can be converted into frequencies through some dictionary.
    - Since chiptune music is characterized by basic waveforms, synthesizing each note involves applying the appropriate formula over a user supplied duration and volume.
  - _Stretch Goals_: The project has freedom for extension if time allows.
    - More input parts can be added besides the melody, such as a bassline or percussion, allowing for more musical expression.

I plan to play around with aspects related to the **Chiptune Synthesizer** as this project ultimately seems the most well-scoped and achievable.

### 11/5/24 - _Notes_: Delay and Modulation Effects

**Delay Effects** - store a signal and give back a delayed copy. Can organize audio samples into a queue as a
[ring buffer](https://en.wikipedia.org/wiki/Circular_buffer) and apply delay.  
The delay level intensity influence how the output sounds:

- Small delay (< 10ms): Phase cancellation, localization
- Moderate delay (10-100ms): "Ensemble" effect
- Moderate to long delay (50-500ms): Reverb and echo effects
- Other effects like filtering and damping the delay can give further depth (e.g. wet/dry modification).

Code referenced in class for reverb, vibrato, tremelo: https://github.com/pdx-cs-sound/effects/blob/master/

**Modulation Effects**

- **Vibrato**: For each sample of the output, the gain is multiplied by a low frequency oscillator to change the amplitude, changing the pitch subtly and quickly.

```python
t = np.linspace(0, len(channel) / float(rate), len(channel));
lfo = args.depth * np.sin(2 * np.pi * args.frequency * t)
channel *= 1.0 - args.depth + lfo / 2
```

- **Tremelo**: Similar to chorus effect, instead of changing amplitude, go back and forth of time. Uses entire sample as buffer. Code reference premise: speed up or slow down the playback rate.

- **Frequency Stretching / Pitch Shiftingt** - Lengthen or shorten a signal, but maintain the harmonic content. A fundamental by itself doesn't capture overtones / harmonics. Filter noise with amplitudes of output filter. _Example_: [Vocoder](https://github.com/pdx-cs-sound/vocoder)
