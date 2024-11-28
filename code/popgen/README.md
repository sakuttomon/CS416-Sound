# Popgen: Play a Pop Music Loop - Irvin Lu

Bart Massey 2024, extended by Irvin Lu. This program is an extension of the [`pdx-cs-sound/popgen`](https://github.com/pdx-cs-sound/popgen) as part of the "Popgen" portfolio objective.

This Python program generates a pseudo-melody using chord and bass notes from the
[Axis Progression](https://en.wikipedia.org/wiki/axis_progression).

A sample is available in [`demo.wav`](demo.wav).

## Extensions / Changes Made

The portfolio objective instructions suggested various improvements to this `popgen` code that we were tasked to implement a couple of.
The following lists out the significant changes I made along with brief descriptions. Any additional thoughts or reflections of my code
implementations are documented in Week 9 within [**`notebook.md`**](../../notebook.md).

### Use a more interesting waveform than sine waves

Added a `waveform` parameter to the note creation function that determines whether a triangle, square, or sine (default) wave is generated for the given note. Applied square waves on the melody and triangle waves on the bass parts.

- _Generated result into [`more-waveforms.wav`](more-waveforms.wav)_

### Get rid of the note clicking by adding a bit of envelope

Added an `apply_envelope()` function to apply on a generated waveform to manipulate the sound dynamics of a given note. The ADSR parameters are fixed in the code, but different values are passed into the melody and bassline generation.

**Melody** is designed to sound "omnipresent" with a gradually ramping attack and high sustain level to keep these notes at the forefront. A shorter release is applied to make the melody sound precise and defining.

**Bass** is designed to "punch" with a short attack and decay, but with a longer release and lower sustain level to smoothly drift the bassline and give a complementary feel to the melody.

- _Square Wave Melody, Triangle Wave Bass generated into [`square-triangle-envelope.wav`](square-triangle-envelope.wav)_
- _Sine Wave Melody, Triangle Wave Bass generated into [`sine-triangle-envelope.wav`](sine-triangle-envelope.wav)_
