import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

# Tuple of the 12 musical notes
NOTES = ('A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#')

def note_to_frequency(note):
    """
    Converts a supplied note to its corresponding frequency value. Expected format is
    either "pitchoctave" for natural notes, or "pitch#octave" for flat notes.
    """
    # Octave should be on far right of input (e.g. A#4 or A4)
    octave = int(note[-1])

    # Calculate piano key number, as according to https://en.wikipedia.org/wiki/Piano_key_frequencies#List
    key_position = NOTES.index(note[:-1])
    # Standard piano starts at (C -> G -> A, B), so A and B notes need to shift up an octave.
    adjustment = 12 if key_position < 3 else 0
    key_number = key_position + adjustment + ((octave - 1) * 12) + 1

    # Applying formula to get frequency given a piano key number
    # https://en.wikipedia.org/wiki/Piano_key_frequencies
    frequency = 440 * (2 ** ((key_number - 49) / 12))

    print(f"Note {note}:")
    print(f"\tPiano Key Number: {key_number}")
    print(f"\tFrequency: {frequency}")

    return frequency

def generate_note_wave(note, duration=1.0, volume=0.5, sample_rate=44100):
    """
    Generate a wave for a supplied note to demonstrate how synthesizing notes should feel.
    """
    frequency = note_to_frequency(note)

    # Time array at specified sample rate
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Using sine wave as example, can apply other waves here
    wave = volume * np.sin(2 * np.pi * frequency * t)
    
    return wave

if __name__ == "__main__":
    note = "A#4"
    duration = 2.0
    volume = 0.4
    sample_rate = 44100

    wave_data = generate_note_wave(note, duration, volume, sample_rate)

    sd.play(wave_data, samplerate=sample_rate)
    sd.wait()

    write(f"note_{note}.wav", sample_rate, (wave_data * 32767).astype(np.int16))


