# Envelope ADSR - Irvin Lu

A program I wrote to experiment with applying attack, decay, sustain, and release (ADSR) on a single frequency
applied over a sine wave. This [**envelope generator**](<https://en.wikipedia.org/wiki/Envelope_(music)>) controls
the amplitude of a sound and how it changes over its duration, allowing for imaginative musical expression.

[`envelope-adsr.py`](envelope-adsr.py) defines a sine wave audio array in the main routine to apply ADSR over, allowing the routine
to supply the times for playing attack, decay, and release. The amplitude to "attack up to" and "decay away from" is defined as the
`peak_level`. Lastly, since sustain is the sound level to rest on for the remainder of time not covered by attack, decay, and release,
the main routine only needs to pass in the amplitude `sustain_level` it wants the note to "sustain" at.

The purpose of the program is to play around with various ADSR values to imitate different musical arrangement parts, such as melody,
bassline, harmony, etc. This program helps me judge the feasibility and noticeable effect of integrating the stretch goal of my
chiptune synthesizer project, which aims to nurture musical expression through multiple instrumental parts or lines, despite the
limitations of imitating retro music using basic waveforms.

Reference for learning ADSR: https://blog.native-instruments.com/adsr-explained/
