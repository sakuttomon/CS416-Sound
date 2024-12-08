# Chiptune Synthesizer Course Project - Irvin Lu

This program takes in a MIDI file, parses note information, and creates a chiptune-style audio track by synthesizing basic waveforms
(e.g. square, triangle, sawtooth) based on each instrument and their notes, obtained from the MIDI parsing. The purpose of this project
is to demonstrate my learnings of sound synthesis while celebrating the retro audio genre I enjoy.

Additional thoughts and reflections learned from working on this project is documented in [`notebook.md`](../../notebook.md) with the
**Chiptune Synthesizer** header. See the conclusion post examining the resulting chiptune outputs in the notebook's
[final entry](../../notebook.md/#12724---chiptune-synthesizer-conclusions).

**_Notice_**: The [`pretty_midi`](https://craffel.github.io/pretty-midi/) library used to parse MIDI files' current release (`0.2.10`)
is incompatible with Python 3.12. This [PR](https://github.com/craffel/pretty-midi/pull/252) addresses the issue, but a new version to
contain this update has yet to be released. Please keep this inconvenience in mind. I currently run this project in **Python 3.9**.

## Build and Run Instructions

Tested on Mac OS, Python 3.9

1. Create a virtual environment if desired: `python3 -m venv env`
2. Activate the env: `source env/bin/activate`
3. Install required dependencies: `pip install -r requirements.txt`
4. Run the program with an input MIDI file path (`.mid`). See [_Arguments_](#arguments) for additional command line flags.

```python
python3 chiptune-synthesizer.py "{file_path}"

# For Example:
# python3 chiptune-synthesizer.py "midi-assets/Mario Kart 8 - Wild Woods.mid"
```

5. The program should generate a chiptunified WAV file in the specified output path and/or play the track to computer audio output.

### Arguments

Since this chiptune synthesizer relies on an input MIDI, the file path to a MIDI file is a required positional argument when running `chiptune-synthesizer.py`.

| Flag              | Type   | Default       | Description                                     |
| ----------------- | ------ | ------------- | ----------------------------------------------- |
| input_midi        | string |               | **Required**: File path to the input MIDI file. |
| --output {OUTPUT} | string | "output-wavs" | Directory to generate the chiptune WAV into.    |
| --no-play         | bool   | `false`       | Do not play the chiptune wave to audio output.  |
| --disable-adsr    | bool   | `false`       | Disable applying an ADSR envelope.              |
| -h, --help        |        |               | Show help message and exit.                     |

```python
# For Example, to generate a chiptune wave without ADSR and prevent playing audio to speakers:
python3 chiptune-synthesizer.py "midi-assets/Mario Kart 8 - Wild Woods.mid" --disable-adsr --no-play --output "output-wavs"
```

## MIDI Assets

All MIDI files used for this project were downloaded from [Online Sequencer](https://onlinesequencer.net/), a community web-based
music sequencer where users create music and and share it with other users.

Songs I used to synthesize chiptune tracks for is contained in the [`midi-assets`](midi-assets) directory. The MIDIs contained in
[`midi-assets/instruments`](midi-assets/instruments) are note sequences that I constructed myself to test each instrument offered by
Online Sequencer, with conclusions written in [`program-info.md`](midi-assets/instruments/program-info.md).

This chiptune synthesizer applies different waveforms based on the instrument. The MIDI assets use a variety of instrument type
combinations to test the capabilities of the chiptune synthesizer. The following list of emojis reveals the mapping between
supported instrument types and the corresponding basic waveforms that generates. These emojis are prepended to each song in the credits list to indicate what the chiptune synthesizer operated with for the given song.

- 🎸: Bassline Instruments --> Triangle Waves
- 🎺: Orchestral Instruments --> Sawtooth Waves
- 🥁: Drum Instruments --> Sine Waves or White Noise
- 🎹: Keyboard + All Unsupported Instruments --> Square Waves

_Please see the [**Credits**](#credits) for songs I did not make myself._

## Demo WAVs

This program defaults to saving the generated chiptune WAV files to an existing directory [`output-wavs`](output-wavs/).
This directory contains reference WAVs to demonstrate the chiptune synthesizer's output for various tracks. Each WAV file's name
matches the corresponding song name in [`midi-assets`](midi-assets/).

All current demo audio files in `output-wavs` were generated with the **ADSR Envelope** enabled.

## Credits

Many of the songs listed below are remixes or renditions of official soundtracks that Online Sequencer community members sequenced and
shared within the tool. Credit to all of these tracks go to the original composers and franchises, along with the users who sequenced
these tracks in Online Sequencer.

- 🎹 _Bright Sandstorm - Fire Emblem Engage_, by Anonymous:
  - https://onlinesequencer.net/3657022
- 🎹 _Kirby's Return to Dreamland - Channel Menu_, by theoneguy:
  - https://onlinesequencer.net/2071395
- 🎸 _Oops, all Bass Guitar!_, by Buzzpip:
  - https://onlinesequencer.net/3988662
- 🎺 _Super Mario Galaxy - To the Gateway_, by Anonymous:
  - https://onlinesequencer.net/4289654
- 🎹🎺 _Overture - Super Mario Galaxy OST_, by Firebolt391d:
  - https://onlinesequencer.net/1134773
- 🎹🥁🎺 _Raise (One Piece ED 19) Ringtone_, by Wacky:
  - https://onlinesequencer.net/3580111
- 🎹🥁🎺 _Super Mario Wonder--- Snow theme_, by Anonymous:
  - https://onlinesequencer.net/3774579
- 🎹🎸🥁🎺 _Mario Kart 8 Deluxe - Animal Crossing (Autumn)_, by hoppingicon:
  - https://onlinesequencer.net/3966328
- 🎹🎸🥁🎺 _Mario Kart 8 - Wild Woods_, by Anonymous:
  - https://onlinesequencer.net/132432
- 🎹🎸🥁🎺 - _Sonic Unleashed - Endless Possibility_, by Anonymous:
  - https://onlinesequencer.net/3966329
