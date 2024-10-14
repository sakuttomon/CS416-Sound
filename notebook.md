# Engineering Notebook - Irvin Lu

A document containing notes or reflections about the work and progress done throughout the course, organized by each week and
the estimated date where such activities occured or finished.

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

The [Nyquist Limit](https://www.slack.net/~ant/bl-synth/3.nyquist.html) expands on the intricacies of audio-to-digital conversion by
limiting the frequency to half the sample rate (conversely, the rate must be double the frequency) to prevent aliasing distortions.
A sample rate of 48,000 Hz is standard for movie and video audio.

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

**Musical Notes**  
_Note_ - Sound with a given fixed frequency "value". Starts at a time (_on time_) and ends at duration (_off time_). Notes can overlap (_polyphony_).  
_Octave_ - Frequency that is 2x some other frequency. **Divided into 12 parts**; since humans hear frequencies on a logarithmic scale, a given part looks like:

$$\textrm{note}_i(f) = f \cdot 2^{i/12}$$

_Ex_: The first note (i=0) simply equals `f`, whilst a note an octave up (i=12), which is the 13th note, equals `2f` since 12/12 = 1.

Base Frequency for a Note: 440 Hz _(Western Scale)_  
[MIDI Key Numbering](https://studiocode.dev/resources/midi-middle-c/) - Based on piano keys. _Ex_: 440Hz A = Key 69, A4, in Octave 4.  
Notes given letter names with **Sharp** (`#`) or **Flat** (`♭`) modifier.
