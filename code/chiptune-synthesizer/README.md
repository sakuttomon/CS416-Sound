# Chiptune Synthesizer Course Project - Irvin Lu

This program takes in a MIDI file, parses note information, and creates a chiptune-style audio track by synthesizing basic waveforms
(e.g. square, triangle, sawtooth) based on the notes from each instrument obtained from the MIDI parsing. The purpose of this project
is to demonstrate my learnings of sound synthesis while celebrating the retro audio genre I enjoy.

**_Notice_**: The library used to parse MIDI files, [`pretty_midi`](https://craffel.github.io/pretty-midi/), is currently incompatible
with Python 3.12, and is currently being addressed in this [PR](https://github.com/craffel/pretty-midi/pull/252). Please keep this inconvenience in mind. I currently run this project in Python 3.9.

## Credits

All MIDI files used for this project were downloaded from [Online Sequencer](https://onlinesequencer.net/), a community web-based
music sequencer where users create music and and share it with other users. Credit to all of these tracks go to the original composers and franchises, along with the users who sequenced these tracks in Online Sequencer.

- _Kirby's Return to Dreamland - Channel Menu_, by theoneguy: https://onlinesequencer.net/2071395
