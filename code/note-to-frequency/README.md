# Note to Frequency - Irvin Lu

A program I wrote to learn how to convert notes into frequencies to apply basic waveforms over. Intended for reuse for my overall chiptune synthesizer project.

[`note-to-frequency.py`](note-to-frequency.py) takes a note string (e.g. "A#4", "C5", "G7", etc.) defined in the main routine and
converts it into a frequency to play a sine wave over. The main routine also has freely modifiable duration and volume variables
to allow experimentation with playing single notes.

The Wikipedia article for piano key frequencies was referenced for formulas on how to obtain the frequency (Hz) of the $n^{th}$ key,
which often matches the standard piano key. The only inaccuracies between $n$ and the standard piano key are for notes at C#8 and
above, or at G#0 and below. The program will still calculate the frequency, albeit with an incorrect key number printed.

https://en.wikipedia.org/wiki/Piano_key_frequencies
