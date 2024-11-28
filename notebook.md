# Engineering Notebook - Irvin Lu

A document containing notes or reflections about the work and progress done throughout the course, organized by each week and the
estimated date where such activities occured or finished. Notes taken from lectures are contained in the [`lectures.md`](lectures.md) file.

Ideas for my overall course project were conjectured in this [entry](#11424---project-ideas-thought-process). The project is a
**Chiptune Synthesizer** that will take a MIDI file as input, and for each instrument, generate basic waveforms referring to the
original note data. Combining the waveforms together results in a chiptune wave, containing synthesized notes that sounds like the
input MIDI, but with a retro-esque touch.

| Table of Contents | Projects                                                                |
| ----------------- | ----------------------------------------------------------------------- |
| [Week 1](#week-1) |                                                                         |
| [Week 2](#week-2) | [Clipped Sine Waves](#101124---clipping-portfolio-objective)            |
| [Week 3](#week-3) |                                                                         |
| [Week 4](#week-4) | [FFT & Spectrogram](#102524---playing-around-with-fft-and-spectrograms) |
| [Week 5](#week-5) | [Adaptive Tone Control](#11324---adaptive-tone-control)                 |
| [Week 6](#week-6) | [Note to Frequency](#11924---note-to-frequency-program)                 |
| [Week 7](#week-7) | [Envelope ADSR](#111324---envelope-adsr-program)                        |
| [Week 8](#week-8) | [Chiptune Synthesizer](#111624---chiptune-synthesizer-midi-parsing)     |
| [Week 9](#week-9) | [Popgen](#112624---popgen-triangle-waves)                               |

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

I merged the [`clipped`](code/clipped/) assignment branch into the main branch. The dedicated [`README`](code/clipped/README.md) within the directory contains my reflections and lessons learned on how I approached the objective.

## Week 3

### 10/14/24 - Saying Hi in Zulip

Wrote an introduction of myself to share in the course [Zulip](https://zulip.com/). In this introduction, I expressed my inexperience
with sound and digital audio concepts, so the course appealed to me as a way to start establishing the basics. I mentioned interests
in "behind-the-scenes" content of media, but sound and music is a field I've yet to dive deep in. So, this class focused on the
interactions between computers and audio seemed like a perfect motive to start learning this hobby topic and make some fun projects,
while also feeling relevant to my field of study.

## Week 4

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

### 11/9/24 - Note to Frequency Program

To start on my chiptune synthesizer project, I wrote a program within the [`note-to-frequency`](code/note-to-frequency/) directory to
learn how I will take note inputs from the user and convert them to interactable frequencies. More details on how the program works in
its dedicated [`README`](code/note-to-frequency/README.md). The calculation and frequency validation follows the Wikipedia article
"[Piano key frequencies](https://en.wikipedia.org/wiki/Piano_key_frequencies)". Some lessons I learned:

- In Western music notation, the note sequence in each octave progresses from C to B. This means pitches A to B need to be shifted up an octave when calculating frequency to account for this order.
- There are multiple methods to represent flat notes, either with the flat symbol with the subsequent pitch, or the sharp (♯) modifier
  with the current pitch (e.g. D♭ = C♯). For the project, I will likely adhere to the sharp pattern to stay consistent with managing an
  octave of 12 musical notes.

## Week 7

### 11/13/24 - Envelope ADSR Program

This is another program I wrote in the [`envelope-adsr`](code/envelope-adsr/) directory, inspired off the chiptune synthesizer project
I want to do. This time, I aimed to learn the significance of attack, decay, sustain, and release (ADSR) for manipulating audio
through an [envelope](<https://en.wikipedia.org/wiki/Envelope_(music)>). Details on how the program works and the reference I used to
understand the role of each ADSR parameter is located in the dedicated [`README`](code/envelope-adsr/README.md). Below are my
inferences on how adjusting the times of ADSR affect the music:

- **Attack**
  - _Short_ - Reaches peak amplitude quicker, resulting in notes sounding more crisp, fit for defining parts like a melody.
  - _Long_ - Slower ascend to peak amplitude, fit for smoother, more atmospheric sounds.
- **Decay**
  - _Short_ - Sound fades quicker, meaning peak its decaying from sounds sharper and more pronounced.
  - _Long_ - Peak fades more slowly, smoother transition to sustain level.
- **Sustain**
  - _Level_ - The amplitude volume to "hold down" at for the remaining time not covered by the other parameters.
  - Minimal sustain means the sound will be close to or silent after decay, fit for drum hits and punchy sounds not meant to rest or smoothly fade out.
  - Max sustain means the sound continues at the same peak volume achieved by the attack stage. Useful for notes that want to stay at the same amplitude for as long as "the key is held down".
- **Release**
  - _Short_ - Sound ends abruptly after "key is released", due to little time allocated for sound to fade to silence.
  - _Long_ - Sound flows gracefully into silence, fit for notes intended to complement others as it drifts off.
  - Not necessary if sustain is already set to minimum since sound would have already reached silence.

### 11/14/24 - MIDI Input for Chiptune Project

I was given the suggestion to instead rely on MIDI files as my input rather than manual note strings typed in by a user. Since MIDI
files often offer multiple channels with detailed note information, I would be given more freedom to focus on the chiptune sound generation.

The libraries [`mido`](https://github.com/mido/mido) or [`pretty_midi`](https://github.com/craffel/pretty-midi) will parse notes, and
I will ideally need to extract the start time, end time, and note pitches to correspond to frequences. The velocity will indicate
the intensity or volume for each note, which can be mapped to ADSR parameters.

To further emphasize the chiptune aesthetic, I was suggested to add "chiptune noise" alongside the MIDI note conversion. I took this
as perhaps adding a layer of noise percussion (e.g. white noise) to mimic sharp snares that retro music tend to express due to limited
sound output systems.

## Week 8

### 11/16/24 - Chiptune Synthesizer: MIDI Parsing

With a background established from my previous programs, I decided to start my overall course project, located in the
[`chiptune-synthesizer`](code/chiptune-synthesizer/) directory. After being suggested to take MIDI inputs, I started with figuring out
how to process these MIDIs and extract note information.

The `pretty_midi` library mentioned in the last entry seems promising due to its ability to organize notes together by the instrument
that played them. The notes themselves contain pitch, velocity, start and end times I was looking for to eventually create chiptune
waveforms with. This separation by instrument should make it simpler to apply different waveforms based on type, e.g. square waves for
bass instruments.

Currently, the program parses MIDI files and displays the properties that the `pretty_midi` library finds relevant, such as the
instrument list and if any time/key signature changes are present. This print display was a test to ensure that the MIDI files
I am providing were properly parsed. More info and credits on the MIDIs I am using is outlined in the project's
[`README`](code/chiptune-synthesizer/README.md).

### 11/17/24 - Online Sequencer Note Naming Convention

The MIDI files I've been using for testing have all come from [Online Sequencer](https://onlinesequencer.net/). Thanks to its
piano roll-style interface, it also serves as a good reference for comparing my note-to-frequency conversions and other modifications
against each note from the input MIDI track.

Something I noticed when parsing MIDI files is that the notes in the actual MIDI file appear to be one octave higher than the note
displays in Online Sequencer's interface. For example, for the note `C5` on the web interface, the actual MIDI file data claims the note is `C4` (MIDI note number 60), meaning my frequency conversion would calculate the frequency at note `C4` instead.

After browsing the [Online Sequencer Wiki](https://onlinesequencer.net/wiki/Online_Sequencer), I found its main article confirm that
the sequencer tool is labeled "with 72 notes from C2-B7 (labelled differently from a piano, **C2 on the sequencer corresponds to C1**
on a piano)". This statement confirms that the one octave difference in their web interface is simply a naming convention
that doesn't affect the underlying frequency values since a note like `C2` in Online Sequencer corresponds to piano key `C1`.

Online Sequencer labels notes one octave higher than the standard piano labeling that this Chiptune Synthesizer project follows. This
entry serves as a reminder that the frequencies calculated from the MIDI file notes are accurate, and the notes being an octave higher
on the Online Sequencer web interface is just a slightly different visualization of mapping frequencies to note numbers.

### 11/19/24 - MIDI Program Numbers

Today, I began the functionality in my **Chiptune Synthesizer** project to generate basic waveforms based on the information of each
note per MIDI instrument. As mentioned in earlier entries, I wanted to incorporate multiple musical parts, such as a melody, bassline,
and percussion for greater musical expression and allow me to use different waveforms for each part.

The `pretty_midi` library I'm using fortunately provides an `is_drum` boolean for each instrument, allowing me to easily
determine which instrument notes will go under the percussion wave track. For non-drum instruments, I had to figure out which
ones become a melody or bassline. This is where the `program` of an instrument comes in.

[General MIDI](https://en.wikipedia.org/wiki/General_MIDI) (GM) is a format many electronic musical tools adhere to. Within these
conventions, there are 128 instrument sound programs organized by type, e.g. piano, organ, guitar, bass, etc. As such, I can apply
specific waveforms depending on the program number of the instrument as I increment through each one from the input MIDI.

To make the bassline part I wanted to do, I would determine which instruments contain a program number between 32-39 (GM states bass
is 33-40, we're accounting for zero indexing), then apply a basic waveform exclusive to that set of instruments. This
[Soundation article](https://soundation.com/music-genres/how-to-make-chiptunes) on how to make chiptune music reinforces my idea
that triangle waves' more rounded and softer nature fits with the backline complementary role that bassline instruments often serve.

### 11/19/24 - Online Sequencer MIDI Export Shenanigans

With my research towards MIDI program numbers in the previous entry, I wanted to confirm if Online Sequencer, the tool where I've
retrieved all of my input MIDIs to test the chiptune synthesizer, followed the General MIDI (GM) requirements. I ended up sequencing
singular notes for every instrument Online Sequencer offered, then ran those exported MIDIs through my project, logging the program
number for each instrument.

The exported MIDIs I sequenced are contained in the [`midi-assets/instruments`](code/chiptune-synthesizer/midi-assets/instruments/)
directory of the project, while the results of my testing is outlined in [`program-info.md`](code/chiptune-synthesizer/midi-assets/instruments/program-info.md) within the same folder. Although Online Sequencer names its instruments differently, there's a
noticeable correlation with the GM program numbers.

For instance, Online Sequencer's _Acoustic Guitar Classic_ instrument has a program number of 24, which seemingly aligns with GM's _Acoustic Guitar (nylon)_ of program 25 (difference by 1 due to zero indexing). So it is safe to say that Online Sequencer
sufficiently adheres to the GM specifications despite their deviated naming conventions.

However, I found an issue with 1 of Online Sequencer's [58 instruments](https://onlinesequencer.net/wiki/Instruments), specifically
the **synthesizer** instrument in the electronic category. The libraries I use to parse MIDIs (`pretty_midi` and `mido`) are unable to
process MIDIs that contain this instrument, raising the error:

```python
OSError: data byte must be in range 0..127
```

Some [discussions](https://github.com/mido/mido/issues/63#issuecomment-253860552) explain that MIDI data bytes should never be larger
than 127, so it appears that this synthesizer instrument isn't properly transcripted when exporting an Online Sequencer track to a
MIDI file.

Given the popularity of the `mido` library and that this problem only occurs with a singular instrument, I'm inclined to agree that
this particular instrument causes corruption that is more the fault of the Online Sequencer tool's export abilities than this
project's MIDI processing library. With this error acknowledged, I believe my chiptune synthesizer program behaves as expected,
properly throwing an error when encountering corrupt MIDIs.

### 11/21/24 - Percussion Key Map

With the knowledge of MIDI program numbers from the prior entries, I configured my chiptune synthesizer to apply triangle waves
for bass instruments, sawtooth waves for orchestral instruments, and square waves for others. Triangle waves would construct the
bassline audio, while sawtooth and square waves compose the melody.

An instrument unlike the others is the drum, which is where a percussion wave comes in. Percussion instruments are "noise-based",
meaning we do not necessarily need to rely on a note's frequency to generate a basic waveform with. Instead, the General MIDI standard
determines the type of drum sound from the incoming note number: https://en.wikipedia.org/wiki/General_MIDI#Percussion

Based on the note number of a given drum, I would then generate a wave of fixed frequency, or create a noise array of uniformly
distributed points. There are a lot of different drums from the list above, so I chose to support **bass/kick**, **snare**,
and **hi-hat** drums. These instruments appear to be more fundamental sounds when beginning to learn drums, as indicated by this
[interactive tutorial](https://learningmusic.ableton.com/make-beats/what-are-these-sounds.html) from [Ableton](https://www.ableton.com/)
about learning music beats.

Bass drums produce a "thump" sound, so I chose to imitate this by generating a fixed low frequency sine wave, supported by this
[article](https://www.musicguymixing.com/sine-wave-kick-drum/) explaining how sub 100Hz sine waves sounds like the thud you would hear
from hitting a bass drum. For the snare and hi-hat drums, I opted to generate random white noise signals since short instances of this
energetic buzz fit the sharp and bright crackle effect of these drums.

I accomplished which drum sound to generate through a `DRUM_KEY_MAP` dictionary that maps note numbers to a configuration indicating
the generation type (wave or noise) and a base volume multiplier. For example, for a MIDI input with an _Acoustic Bass Drum_ instrument
(_808 Drum Kit_ in Online Sequencer), the note's pitch of `35` would map to the fixed low frequency sine wave that I employ for
kick drum sounds.

If a note pitch isn't supported in the chiptune synthesizer's `DRUM_KEY_MAP`, I chose to fallback to random noise, but with a miniscule
base volume multiplier so that unsupported drum types have a subtler effect on the chiptune audio.

### 11/22/24 - Generating Chiptune Waves, Playing & Writing Audio

This [**PR**](https://github.com/sakuttomon/CS416-Sound/pull/3) contains most of the code changes described throughout this week's
entries. With constructed melody, bassline, and percussion waves, the overall chiptune wave would sum the three parts, combining every
instrument back together. To prevent clipping from summing values, I normalized the audio data by dividing each element by the maximum.
I noticed the resulting waves were very loud, so I applied a `LOUDNESS` multiplier to soften the output.

Users can listen to the chiptunified track using either an audio player or save to WAV file function. Saved WAVs are stored in the
[`output-wavs`](code/chiptune-synthesizer/output-wavs/) directory. The output files share the same song name from the input MIDI.

The output audio sounds pretty satisfying! The audio feels very retro-esque, and I haven't found any obvious cases of clipping. I have
noticed that when an input MIDI plays a lot of notes during the same timeframe, the chiptune version sounds amplified, likely due to the
layering of basic waveforms - especially for square waves and their "beeping" characteristic. This is moreso an effect of translating
more complex songs to a limited set of "chiptune instruments".

Nonetheless, it undeniably sounds like chiptune music, so the minimum requirements I set for this project are accompished. With the
foundations of a chiptune synthesizer established, I intend to look into further improvements or additions to enhance the musical depth
or project structure.

## Week 9

### 11/24/24 - Moving lecture notes to dedicated document

To reduce the complexity of interleaving lecture notes with project diary entries, I chose to move all of my _Notes_ from class lectures
to [`lectures.md`](lectures.md). This notebook is now dedicated to documenting experiences from code projects and portolio objectives.

### 11/26/24 - Popgen: Triangle Waves

I started the Popgen portfolio objective, contained in the [**`popgen`**](code/popgen/) code directory. Due to its similarities with
my _Chiptune Synthesizer_ course project in terms of note manipulation, I wanted to bring over some techniques to see how the code would
operate in a slightly different environment of generated chords versus processing an input MIDI.

One of the tasks is to "Use a more interesting waveform than sine waves", which aligns with how I used triangle waves for basslines and
square waves for melodies in my chiptune synthesizer. I incorporated this logic into the `popgen` code, but this time I wanted to try
calculating the triangle wave purely through `numpy` instead of relying on `scipy.signal`.

The [formula](https://en.wikipedia.org/wiki/Triangle_wave) for a triangle wave of period $p$ and time $t$ spanning the range [-1, 1]
is as follows:

$$
x(t) = 2 * | 2 * (t/p - \lfloor t/p + 1/2 \rfloor) | - 1
$$

$t/p$ divides time by the period, resulting in cycles that `popgen` already calculates and accounts for in the time array `t`.
The sub-equation $t/p - \lfloor t/p + 1/2 \rfloor$ generates a [sawtooth wave](https://en.wikipedia.org/wiki/Sawtooth_wave)
in the range [-0.5, 0.5]. Multiplying by 2 then stretches the range to [-1, 1]. The absoulate value operation restricts the range
to [0, 1], but creates the upward and downward slopes of a traingle, as an [absoulte value function](https://en.wikipedia.org/wiki/Absolute_value#/media/File:Absolute_value.svg) normally does when plotted.
Finally, the outer multiplication by $2$ changes the range to [0, 2], and the $-1$ brings the range back to [-1, 1] to fit within
normalized amplitude.

Translating this into code, the $t/p - \lfloor t/p + 1/2 \rfloor$ retrieves the fractional parts of the signal. An equivalent to achieve this is to **modulo** $t/p$ by $1$. `mod 1` will reset time $t$ back to period $p$ once time exceeds the period, ensuring the waveform resets every $p$ seconds, creating the repeating triangle pattern over time.

```python
2 * np.abs(2 * ((t / (2 * np.pi)) % 1) - 1) - 1
```

### 11/27/24 - Popgen: ADSR Envelope

I originally planned to implement an ADSR envelope into my chiptune synthesizer, so I figured I'd prove out the concept in this popgen
portfolio objective and satisfy the task to "Get rid of the note clicking by adding a bit of envelope." Most of the code is repurposed
from my approach in [`envelope-adsr`](code/envelope-adsr/), so I mainly played around with ADSR values until the output sounded enjoyable.

I decided to code two sets of fixed values, one for the melody and another for the bass, to try and produce different feelings of music. More details of the ADSR design is described in the code directory [`README`](code/popgen/README.md).

Since I already implemented support for other waveforms, I experimented with how a given set of ADSR parameters affect different
combinations of waveforms on the melody and bassline. I ended up really liking the soothing feeling of a sine wave melody and triangle
wave bass, so I pushed up [`sine-triangle-envelope.wav`](code/popgen/sine-triangle-envelope.wav) to demonstrate how this set of ADSR
especially improves more clean and smoother tracks.

To maintain the previous improvement of using more interesting waveforms than sine waves, I also generated
[`square-triangle-envelope.wav`](code/popgen/square-triangle-envelope.wav), which definitely imitates the retro vibe I aimed to
achieve in my chiptune synthesizer project. The "binary" style of square waves applied on the melody, along with an ADSR envelope to
smooth out the sound reduces clicking noises as intended, but introduces a feeling I can only describe as "playing from a limited
sound system".

Based off my learnings from applying an ADSR envelope in this `popgen` objective, I'm planning to implement a similar system into my
chiptune synthesizer for that additional layer of musical depth and alleviate the notion of each note sounding "flat" due to staying
at a constant amplitude.
