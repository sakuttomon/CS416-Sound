# Popgen: Play a Pop Music Loop - Irvin Lu

Bart Massey 2024, extended by Irvin Lu. This program is an extension of [`pdx-cs-sound/popgen`](https://github.com/pdx-cs-sound/popgen) as part of the _Popgen_ portfolio objective.

This Python program generates a pseudo-melody using chord and bass notes from the
[Axis Progression](https://en.wikipedia.org/wiki/axis_progression).

A sample is available in [`demo.wav`](demo.wav).

## Extensions / Changes Made

The portfolio objective instructions suggested various improvements to this `popgen` code that we were tasked to implement a couple of.
The following lists out the significant changes I made along with brief descriptions. Any additional thoughts or reflections of my code
implementations are documented in Week 9 within [**`notebook.md`**](../../notebook.md#week-9).

### Use a more interesting waveform than sine waves

Added a `waveform` parameter to the note creation function that determines whether a triangle, square, or sine (default) wave is generated for the given note. Applied square waves on the melody and triangle waves on the bass parts.

- _Generated result into [`more-waveforms.wav`](more-waveforms.wav)_

### Get rid of the note clicking by adding a bit of envelope

Added an `apply_envelope()` function to apply on a generated waveform, manipulating the sound dynamics of a given note. The ADSR parameters are fixed in the code, but different values are passed into the melody and bassline generation.

**Melody** is designed to sound "omnipresent" with a gradually ramping attack and high sustain level to keep these notes at the forefront. A shorter release is applied to make the melody sound precise and defining.

**Bass** is designed to "punch" with a short attack and decay, but with a longer release and lower sustain level to smoothly drift the bassline and give a complementary feel to the melody.

- _Square Wave Melody, Triangle Wave Bass generated into [`square-triangle-envelope.wav`](square-triangle-envelope.wav)_
- _Sine Wave Melody, Triangle Wave Bass generated into [`sine-triangle-envelope.wav`](sine-triangle-envelope.wav)_

Four beats are used per measure as before, but `rhythm_pattern` can supply varied note
durations per beat (e.g. [1, 0.5, 0.5, 2])

### Allow rhythm patterns for the melody other than one note per beat

The `pick_notes()` function was reworked into `pick_notes_rhythm()`. The `n` parameter was replaced with `rhythm_pattern`, which
expects a list of note durations to create chord notes with. The return of `notes` was updated to return a list of tuples,
each tuple containing the chord note number and corresponding duration.

When creating melody notes, these durations determine how many samples of the beat a given note takes up. For example, for a tuple
`(60, 0.5)`, `make_note()` will generate a note at approximately half the length of a beat. Thus, melody notes are no longer
constrained to one note per beat.

The rhythm pattern argument supplied to `pick_notes_rhythm` is defined as `[1, 0.5, 0.5, 2]`, syncing each measure to the rhythm of a
quarter note, eighth note, eigth note again, followed by a half note. Melodies now play at a "moderate, short, short, long" rhythm!

- _Square Melody, Triangle Bass, Fixed Rhythm Pattern generated into [`square-triangle-fixed-rhythm.wav`](square-triangle-fixed-rhythm.wav)_

An additional command line argument `--shuffle-rhythm` was added. If this flag is set when running `popgen.py`, the program shuffles
the rhythm pattern order (`[1, 0.5, 0.5, 2]`) for each chord instead of staying fixed. This shuffle results in "randomly" dynamic
rhythms for each measure while still maintaining the axis progression of 4 beats per measure.

- _Square Melody, Triangle Bass, Shuffled Rhythm Pattern generated into [`square-triangle-shuffle-rhythm.wav`](square-triangle-shuffle-rhythm.wav)_
