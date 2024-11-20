# Every Online Sequencer Instrument - Program Results

Since the input MIDIs I've chosen to test the Chiptune Synthesizer have all been from [Online Sequencer](https://onlinesequencer.net/), I decided to test every instrument the tool provides to get more information on what programs each instrument relates to when
transcripted into a MIDI. Program numbers indicate the type of instrument and generally go from 1 to 128, based on this standardized
[parameter list](https://en.wikipedia.org/wiki/General_MIDI#Parameter_interpretations) from Wikipedia.

A numbering system 0 to 127 is usually used internally by the synthesizer, which Online Sequencer seems to also follow. For example,
_Acoustic Guitar Classic_ is program 24, whereas the Wikipedia list says the likely corresponding _Acoustic Guitar (nylon)_ is 25.
The program results here will follow the zero indexing pattern.

Online Sequencer divides its instruments into several categories. Within the tool, I created music that is simply a single note
of every instrument listed under a given category, played sequentially. I exported these sequences as MIDI files, and named them
according to the instrument category. I then processed these MIDI files in [`chiptune-synthesizer.py`](../../chiptune-synthesizer.py),
and used the `printMidiInfo` function to obtain the results below:

## Piano

[`pianos.mid`](pianos.mid)

```python
    Electric Piano has 1 notes, Program 0
    Grand Piano has 1 notes, Program 0
    Harpsichord has 1 notes, Program 6
    Ragtime Piano has 1 notes, Program 3
    Music Box has 1 notes, Program 10
    Elec. Piano (Classic) has 1 notes, Program 0
    Grand Piano (Classic) has 1 notes, Program 0
```

## Percussion (MIDI)

[`percussion-midi.mid`](percussion-midi.mid)

```python
    Drum Kit has 1 notes, Program 0, is a drum
    Electric Drum Kit has 1 notes, Program 0, is a drum
    Xylophone has 1 notes, Program 13
    Vibraphone has 1 notes, Program 11
    Steel Drums has 1 notes, Program 114
```

## Percussion (Classic)

[`percussion-classic.mid`](percussion-classic.mid)

```python
    2013 Drum Kit has 1 notes, Program 0, is a drum
    808 Drum Kit has 1 notes, Program 0, is a drum
    909 Drum Kit has 1 notes, Program 0, is a drum
    2023 Drum Kit has 1 notes, Program 0, is a drum
    EDM Kit (E) has 1 notes, Program 0, is a drum
    8-Bit Drum Kit has 1 notes, Program 0, is a drum
```

## Guitar

[`guitars.mid`](guitars.mid):

```python
    Acoustic Guitar has 1 notes, Program 27
    Electric Guitar has 1 notes, Program 29
    Bass has 1 notes, Program 32
    Bass Guitar has 1 notes, Program 32
    Slap Bass has 1 notes, Program 36
    Jazz Guitar has 1 notes, Program 26
    Muted E-Guitar has 1 notes, Program 28
    Distortion Guitar has 1 notes, Program 42
    Clean Guitar has 1 notes, Program 27
    Sitar has 1 notes, Program 104
    Koto has 1 notes, Program 107
    Acoustic Gtr (Classic) has 1 notes, Program 24
    Bass Guitar (Classic) has 1 notes, Program 32
    Dist. Guitar (Classic) has 1 notes, Program 30
```

## Electronic

Any Online Sequencer songs using the **Synthesizer** instrument, when exported as a MIDI file, would fail MIDI processing
in `chiptune-synthesizer.py`. This issue stems from the `pretty_midi` and `mido` libraries used to parse MIDI files, which enforces
that input data bytes must range from 0-127.

The [`electronics.mid`](electronics.mid) example contains the synthesizer instrument, and running the chiptune program results in the error:

```python
OSError: data byte must be in range 0..127
```

This [GitHub discussion](https://github.com/mido/mido/issues/63#issuecomment-253860552) explains that bytes outside of this expected
range indicate a courrpted MIDI file. As a result, use of the synthesizer instrument in Online Sequencer likely corrupts the export
to MIDI file, and thus songs using this instrument cannot be used in my chiptune synthesizer project.

The MIDI file below is the same note sequence but excluding the **Synthesizer** instrument and was successfully processed in the
chiptune program. More discoveries about my discoveries and choice to move forward without worry is documented in [`notebook.md`](../../../../notebook.md).

[`electronics-without-synthesizer.mid`](electronics-without-synthesizer.mid)

```python
    Synth Bass (Classic) has 1 notes, Program 38
    Pop Synth (Classic) has 1 notes, Program 50
    808 Bass has 1 notes, Program 0
    Synth Bass has 1 notes, Program 38
    Pop Synth has 1 notes, Program 50
    8-Bit Triangle has 1 notes, Program 87
    8-Bit Sawtooth has 1 notes, Program 81
    8-Bit Square has 1 notes, Program 80
    8-Bit Sine has 1 notes, Program 82
    Scifi has 1 notes, Program 99
    Synth Pluck has 1 notes, Program 87
    Smooth Synth has 1 notes, Program 80
```

## Orchestra

[`orchestra.mid`](orchestra.mid):

```python
    Trombone has 1 notes, Program 57
    French Horn has 1 notes, Program 60
    Cello has 1 notes, Program 42
    Violin has 1 notes, Program 40
    Concert Harp has 1 notes, Program 45
    Pizzicato has 1 notes, Program 45
    Flute has 1 notes, Program 73
    Strings has 1 notes, Program 43
    Saxophone has 1 notes, Program 64
    Church Organ has 1 notes, Program 19
    French Horn (Classic) has 1 notes, Program 60
    Trombone (Classic) has 1 notes, Program 57
    Violin (Classic) has 1 notes, Program 40
    Cello (Classic) has 1 notes, Program 42
    Lucent Choir has 1 notes, Program 0
```
