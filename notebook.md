# Engineering Notebook - Irvin Lu

A document containing notes or reflections about the work and progress done throughout the course, organized by each week and
the estimated date where such activities occured or finished.

| Table of Contents |
| ----------------- |
| [Week 1](#week-1) |
| [Week 2](#week-2) |
| [Week 3](#week-3) |
| [Week 4](#week-4) |

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

## Week 3

### 10/14/24 - Saying Hi in Zulip

Wrote an introduction of myself to share in the course [Zulip](https://zulip.com/). In this introduction, I expressed my inexperience
with sound and digital audio concepts, so the course appealed to me as a way to start establishing the basics. I mentioned interests
in "behind-the-scenes" content of media, but sound and music is a field I've yet to dive deep in. So, this class focused on the
interactions between computers and audio seemed like a perfect motive to start learning this hobby topic and make some fun projects,
while also feeling relevant to my field of study.

### 10/18/24 - Notes: Understanding Frequency

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

### 10/22/24 - Review of DFT

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

### 10/24/22 - Filter Design

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
