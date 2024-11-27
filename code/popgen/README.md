# Popgen: Play a Pop Music Loop - Irvin Lu

Bart Massey 2024, extended by Irvin Lu. This program is an extension of the [`pdx-cs-sound/popgen`](https://github.com/pdx-cs-sound/popgen) as part of the "Popgen" portfolio objective.

This Python program generates a pseudo-melody using chord and bass notes from the
[Axis Progression](https://en.wikipedia.org/wiki/axis_progression).

A sample is available in [`demo.wav`](demo.wav).

## Extensions / Changes Made

The portfolio objective instructions suggested various improvements to this `popgen` code that we were tasked to implement a couple of.
The following lists out the significant changes I made along with brief descriptions. Any additional thoughts or reflections of my code
implementations are documented in Week 9 of [**`notebook.md`**](../../notebook.md).

- **Use a more interesting waveform than sine waves** - Added a `waveform` parameter to the note creation function that determines whether a triangle, square, or sine (default) wave is generated for the given note. Applied square waves on the melody and triangle waves on the bass parts.
  - _Generated result into [`more-waveforms.wav`](more-waveforms.wav)_
