# "Pop Music Generator"
# Bart Massey 2024, extended by Irvin Lu
#
# This script puts out four bars in the "Axis Progression" chord loop, with a melody and bass line.
# The following extensions were added:
#   - Use a more interesting waveform than sine waves.
#   - Get rid of the note clicking by adding a bit of envelope.
#   - Allow rhythm patterns for the melody other than one note per beat.

import argparse, random, re, wave
import numpy as np
import sounddevice as sd

# 11 canonical note names.
names = [ "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", ]
note_names = { s : i for i, s in enumerate(names) }

# Turn a note name into a corresponding MIDI key number.
# Format is name with optional bracketed octave, for example
# "D" or "Eb[5]". Default is octave 4 if no octave is
# specified.
note_name_re = re.compile(r"([A-G]b?)(\[([0-8])\])?")
def parse_note(s):
    m = note_name_re.fullmatch(s)
    if m is None:
        raise ValueError
    s = m[1]
    s = s[0].upper() + s[1:]
    q = 4
    if m[3] is not None:
        q = int(m[3])
    return note_names[s] + 12 * q

# Given a string representing a knob setting between 0 and
# 10 inclusive, return a linear gain value between 0 and 1
# inclusive. The input is treated as decibels, with 10 being
# 0dB and 0 being the specified `db_at_zero` decibels.
def parse_log_knob(k, db_at_zero=-40):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    if v < 0.1:
        return 0
    if v > 9.9:
        return 10
    return 10**(-db_at_zero * (v - 10) / 200)

# Given a string representing a knob setting between 0 and
# 10 inclusive, return a linear gain value between 0 and 1
# inclusive.
def parse_linear_knob(k):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    return v / 10

# Given a string representing an gain in decibels, return a
# linear gain value in the interval (0,1]. The input gain
# must be negative.
def parse_db(d):
    v = float(d)
    if v > 0:
        raise ValueError
    return 10**(v / 20)

ap = argparse.ArgumentParser()
ap.add_argument('--bpm', type=int, default=90)
ap.add_argument('--samplerate', type=int, default=48_000)
ap.add_argument('--root', type=parse_note, default="C[5]")
ap.add_argument('--bass-octave', type=int, default=2)
ap.add_argument('--balance', type=parse_linear_knob, default="5")
ap.add_argument('--gain', type=parse_db, default="-20") # Made default gain quieter for more (personally) bearable volume
ap.add_argument('--output')
ap.add_argument('--shuffle-rhythm', action="store_true")
ap.add_argument("--test", action="store_true", help=argparse.SUPPRESS)
args = ap.parse_args()

# Tempo in beats per minute.
bpm = args.bpm

# Audio sample rate in samples per second.
samplerate = args.samplerate

# Samples per beat.
beat_samples = int(np.round(samplerate / (bpm / 60)))

# Relative notes of a major scale.
major_scale = [0, 2, 4, 5, 7, 9, 11]

# Major chord scale tones — one-based.
major_chord = [1, 3, 5]

# Given a scale note with root note 0, return a key offset
# from the corresponding root MIDI key.
def note_to_key_offset(note):
    scale_degree = note % 7
    return note // 7 * 12 + major_scale[scale_degree]

# Given a position within a chord, return a scale note
# offset — zero-based.
def chord_to_note_offset(posn):
    chord_posn = posn % 3
    return posn // 3 * 7 + major_chord[chord_posn] - 1

# MIDI key where melody goes.
melody_root = args.root

# Bass MIDI key is below melody root.
bass_root = melody_root - 12 * args.bass_octave

# Root note offset for each chord in scale tones — one-based.
chord_loop = [8, 5, 6, 4]

position = 0
def pick_notes_rhythm(chord_root, rhythm_pattern):
    """
    Extensions: 
    - Allow rhythm patterns for the melody other than one note per beat, determined by a sequence of note durations 
    defined in `rhythm_pattern`. 
    - Return of `notes` now is a list of tuples containing (chord_note, duration). Duration is used in `make_note()` 
    to enforce the rhythmic pattern of each note within a measure.
    - Removed `n=4` parameter due to supporting rhythmic variety.
    """
    global position
    p = position

    notes = []
    for duration in rhythm_pattern:
        chord_note_offset = chord_to_note_offset(p)
        chord_note = note_to_key_offset(chord_root + chord_note_offset)
        notes.append((chord_note, duration))

        if random.random() > 0.5:
            p = p + 1
        else:
            p = p - 1

    position = p
    return notes # Tuples of (note, duration), e.g. (60, 0.5)

def apply_envelope(original_wave, tAttack, tDecay, tRelease, peak_level, sustain_level):
    """
    New Addition:
    - Get rid of note clicking by adding an envelope. Uses an ADSR envelope to apply over the waveform.
      Lengths of attack, decay, and release are fixed based on the function call. The amplitude to attack 
      up to (peak_level) and sustain at after the decay are also fixed according to the parameters.
    """
    wave = np.copy(original_wave)
    # Samples lengths for each ADSR parameter
    attack_samples = int(tAttack * samplerate)
    decay_samples = int(tDecay * samplerate)
    release_samples = int(tRelease * samplerate)
    sustain_samples = len(wave) - (attack_samples + decay_samples + release_samples)

    envelope = np.concatenate([
        np.linspace(0, peak_level, attack_samples), # Attack
        np.linspace(peak_level, sustain_level, decay_samples), # Decay
        np.full(sustain_samples, sustain_level), # Sustain
        np.linspace(sustain_level, 0, release_samples) # Release
    ])

    return wave * envelope[:len(wave)]

# Given a MIDI key number and an optional number of beats of
# note duration, return a sine wave for that note.
def make_note(key, n=1, waveform='sine', tAttack=0.01, tDecay=0.1, tRelease=0.2, peak_level=1.0, sustain_level=0.7):
    """
    Extensions:
    - Used more interesting waveforms than purely sine waves
    - Applied fixed ADSR envelope to generated waves to reduce clicking
    """
    f = 440 * 2 ** ((key - 69) / 12)
    b = round(beat_samples * n)
    cycles = 2 * np.pi * f * b / samplerate
    t = np.linspace(0, cycles, b)

    if waveform == 'triangle':
        # Triangle Wave Formula: https://en.wikipedia.org/wiki/Triangle_wave
        # x(t) = 2 | 2(t/p - floor(t/p + 1/2) | - 1
        wave = 2 * np.abs(2 * ((t / (2 * np.pi)) % 1) - 1) - 1
    
    elif waveform == 'square':
        wave = np.sign(np.sin(t))
    
    else: # Default to sine wave
        wave = np.sin(t)
    
    # Apply ADSR envelope
    return apply_envelope(wave, tAttack, tDecay, tRelease, peak_level, sustain_level)

# Play the given sound waveform using `sounddevice`.
def play(sound):
    sd.play(sound, samplerate=samplerate, blocking=True)
        
# Unit tests, driven by hidden `--test` argument.
if args.test:
    note_tests = [
        (-9, -15),
        (-8, -13),
        (-7, -12),
        (-6, -10),
        (-2, -3),
        (-1, -1),
        (0, 0),
        (6, 11),
        (7, 12),
        (8, 14),
        (9, 16),
    ]

    for n, k in note_tests:
        k0 = note_to_key_offset(n)
        assert k0 == k, f"{n} {k} {k0}"

    chord_tests = [
        (-3, -7),
        (-2, -5),
        (-1, -3),
        (0, 0),
        (1, 2),
        (2, 4),
        (3, 7),
        (4, 9),
    ]

    for n, c in chord_tests:
        c0 = chord_to_note_offset(n)
        assert c0 == c, f"{n} {c} {c0}"

    exit(0)
    
# Quarter, Eighth, Eighth, Half
rhythm_pattern = [1, 0.5, 0.5, 2]
# Stitch together a waveform for the desired music.
sound = np.array([], dtype=np.float64)
for c in chord_loop:

    if args.shuffle_rhythm:
        # Randomize order of note durations for different rhythms per chord
        np.random.shuffle(rhythm_pattern)

    notes = pick_notes_rhythm(c - 1, rhythm_pattern)
    melody = np.concatenate(list(make_note(note + melody_root, 
                                           n=duration, waveform='square', 
                                           tAttack=0.15, tDecay=0.02, tRelease=0.03, 
                                           peak_level=1.0, sustain_level=0.9) 
                                           for note, duration in notes))

    bass_note = note_to_key_offset(c - 1)
    bass = make_note(bass_note + bass_root, n=4, waveform='triangle', 
                     tAttack=0.05, tDecay=0.03, tRelease=0.1, peak_level=0.9, sustain_level=0.7)

    melody_gain = args.balance
    bass_gain = 1 - melody_gain

    sound = np.append(sound, melody_gain * melody + bass_gain * bass)

# Save or play the generated "music".
if args.output:
    output = wave.open(args.output, "wb")
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(samplerate)
    output.setnframes(len(sound))

    data = args.gain * 32767 * sound.clip(-1, 1)
    output.writeframesraw(data.astype(np.int16))

    output.close()
else:
    play(args.gain * sound)