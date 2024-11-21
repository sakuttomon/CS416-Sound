import numpy as np
import os
import pretty_midi # 0.2.10 release incompatible with Python 3.12: https://github.com/craffel/pretty-midi/pull/252
import sounddevice as sd
from scipy import signal
from scipy.io.wavfile import write
from typing import List

# The sample rate to produce chiptune audio with.
SAMPLE_RATE = 44100

# Currently supported drum sounds for chiptune synthesis, following the percussion key map from:
# https://en.wikipedia.org/wiki/General_MIDI#Percussion
DRUM_KEY_MAP = {
    # Acoustic Bass Drum
    35: {"type": "wave", "frequency": 50, "waveform": "sine", "base_volume": 0.9},
    # Electric Bass Drum
    36: {"type": "wave", "frequency": 50, "waveform": "sine", "base_volume": 0.85},
    38: {"type": "noise", "base_volume": 0.75}, # Acoustic Snare
    40: {"type": "noise", "base_volume": 0.75}, # Electric Snare
    42: {"type": "noise", "base_volume": 0.6}, # Closed Hi-Hat
    44: {"type": "noise", "base_volume": 0.6}, # Pedal Hi-Hat
    46: {"type": "noise", "base_volume": 0.6}, # Open Hi-Hat
}

class MidiToChiptune:
    def __init__(self, file):
        """
        Extracts the MIDI data from a given `.mid` file to prepare for applying chiptune waveforms on each note.

        Args:
            file (str): The MIDI file to process, parsed using the `pretty_midi` library.
        """
        self.filename, file_extension = os.path.splitext(file)
        
        if not file_extension == '.mid':
            raise OSError('File must be a MIDI file (.mid)')
        
        # Get all the information pretty_midi parses
        self.data = pretty_midi.PrettyMIDI(file)
        self.instruments: List[pretty_midi.Instrument] = self.data.instruments # Contains notes under each
        self.time_signatures = self.data.time_signature_changes
        self.key_signatures = self.data.key_signature_changes
        self.track_length = self.calculateTrackLength()

        # Waveforms to construct chiptune tunes with
        self.melody_wave = np.zeros(self.track_length)
        self.bass_wave = np.zeros(self.track_length)
        self.percussion_wave = np.zeros(self.track_length)

        self.full_wave = np.zeros(self.track_length)
    
    def calculateTrackLength(self):
        """
        Calculates the total duration of the input MIDI track in samples. Necessary for constructing the
        chiptune waveform arrays so that waves can be placed between where a given note starts and ends.

        Returns:
            int: The highest end time of a note among all instruments multiplied by `SAMPLE_RATE`, 
            indicating total duration.
        
        Raises:
            Exception: If there are no instruments, there is no note data and thus nothing to calculate length for.
        """
        if self.instruments:
            max_end_time = max(max(note.end for note in instrument.notes) for instrument in self.instruments)
            return int(max_end_time * SAMPLE_RATE)

        raise Exception("Input MIDI has no instruments and thus no note data.")
    
    def midiNoteToFrequency(self, midi_note):
        """
        Converts a MIDI note number to its corresponding frequency value.

        Args:
            midi_note (int): The pitch from a MIDI note to calculate a frequency from.
        
        Returns:
            float: The corresponding frequency to the MIDI note number.
        """
        # Baseline key A4 is represented as MIDI note 69
        return 440.0 * (2 ** ((midi_note - 69) / 12))
    
    def printMidiInfo(self):
        """
        Prints all the MIDI information, listing all instruments involved with the number of notes in each.
        If the MIDI file contained any key or time signatures, also display the number of changes.
        """
        print("--------------------")
        print(self.filename)

        if self.time_signatures:
            print(f"{len(self.time_signatures)} time signature change{'s' if len(self.time_signatures) > 1 else ''}")
        if self.key_signatures:
            print(f"{len(self.key_signatures)} key signature change{'s' if len(self.key_signatures) > 1 else ''}")

        print('\nInstruments:')
        for instrument in self.instruments:
            is_drum = ", is a drum" if instrument.is_drum else ''
            print(f"{instrument.name} has {len(instrument.notes)} notes, Program {instrument.program}{is_drum}")
            # for note in instrument.notes:
            #     print(note.pitch)
            #     print(f"{self.midiNoteToFrequency(note.pitch)}")
        
        print("--------------------")
    
    def generateWave(self, frequency, duration, waveform='square', volume=0.5):
        """
        Generates a waveform of the specified type for a given frequency. This generation imitates the
        chiptune effect by synthesizing a basic waveform using a note's pitch from the input MIDI.

        Args:
            frequency (float): Frequency (Hz) of a note pitch to generate a waveform with.
            duration (float): Duration of the waveform in seconds. Determined by the note's start and end times.
            waveform (str): The type of basic waveform to generate for a chiptune effect.
            volume (float): Volume scaling factor (0.0 to 1.0).

        Returns:
            np.ndarray: The generated waveform as a numpy array.

        Raises:
            Exception: If the specified waveform type is unsupported.
        """
        time = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)

        if waveform == 'square':
            # Defined as sign function of sinusoid: https://en.wikipedia.org/wiki/Square_wave
            return volume * np.sign(np.sin(2 * np.pi * frequency * time)) 
        
        elif waveform == 'sawtooth':
            return volume * signal.sawtooth(2 * np.pi * frequency * time)
        
        elif waveform == 'triangle':
            # Width of 0.5 gives a a triangle wave:
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sawtooth.html
            return volume * signal.sawtooth(2 * np.pi * frequency * time, width=0.5) 
        
        elif waveform == 'sine':
            return volume * np.sin(2 * np.pi * frequency * time)

        raise Exception(f"{waveform} is not a supported waveform to generate.")
    
    def generateNoise(self, duration, volume):
        """
        Generates white noise for percussion sounds.
        
        Args:
            duration (float): Duration to play the noise in seconds.
            volume (float): Volume to scale noise (0 to 1).
        """
        # Random values to simulate noise, stay within -1 to 1 amplitude to align with normalization
        return volume * np.random.uniform(-1, 1, int(SAMPLE_RATE * duration))
    
    def generateMelodyOrBassline(self, notes: List[pretty_midi.Note], program):
        """
        Given all notes from an instrument in the input MIDI, generates waves to add to the melody and
        bassline tracks. Whether a melody or bassline is generated depends on instrument's program number.
        Populates the `melody_wave` and `bass_wave` class variables.

        Args:
            notes (List[Note]): Array of notes to derive information from for generating a chiptune wave.
            program (int): The program number of the MIDI instrument.
        """
        melody_parts = np.zeros(self.track_length)
        bass_parts = np.zeros(self.track_length)

        for note in notes:
            frequency = self.midiNoteToFrequency(note.pitch)
            duration = note.end - note.start
            # Normalize velocity, MIDI considers 127 the maximum strength a note was hit
            velocity = note.velocity / 127.0

            # General MIDI Program Numbers: https://en.wikipedia.org/wiki/General_MIDI#Program_change_events
            # Bass instruments from 33-40, -1 to account for zero indexing 
            if program in range(32, 40):
                # Triangle waves are softer, more fit for bassline
                # https://soundation.com/music-genres/how-to-make-chiptunes
                wave = self.generateWave(frequency, duration, waveform='triangle', volume=velocity)

                # Add part to bass track during its timeslot
                start_sample = int(note.start * SAMPLE_RATE)
                end_sample = start_sample + len(wave)
                bass_parts[start_sample:end_sample] += wave[:len(bass_parts) - start_sample]
            
            # Strings, Ensemble, Brass, Reed, and Pipe range from 41-80, -1 to account for zero indexing 
            elif program in range(40, 80):
                wave = self.generateWave(frequency, duration, waveform='sawtooth', volume=velocity)

                # Add part to melody track during its timeslot
                start_sample = int(note.start * SAMPLE_RATE)
                end_sample = start_sample + len(wave)
                melody_parts[start_sample:end_sample] += wave[:len(melody_parts) - start_sample]

            # All other instruments used for melody (piano, etc.)
            else:
                # Square waves make sharp distinct sounds fitting for a melody
                wave = self.generateWave(frequency, duration, waveform='square', volume=velocity)

                # Add part to melody track during its timeslot
                start_sample = int(note.start * SAMPLE_RATE)
                end_sample = start_sample + len(wave)
                melody_parts[start_sample:end_sample] += wave[:len(melody_parts) - start_sample]
        
        self.melody_wave += melody_parts
        self.bass_wave += bass_parts

    def generatePercussion(self, notes: List[pretty_midi.Note]):
        """
        Given all notes from an instrument in the input MIDI, generates a percussion waveform by combining
        each drum noise. Populates the `percussion_wave` class variable.

        Args:
            notes (List[Note]): Array of notes to derive information from for generating chiptune noises.
        """
        percussion_parts = np.zeros(self.track_length)

        for note in notes:
            duration = note.end - note.start
            velocity = note.velocity / 127.0

            # Determine the drum sound based on pitch, default to a quieter sound for unsupported drum types
            drum_config = DRUM_KEY_MAP.get(note.pitch, {"type": "unsupported", "base_volume": 0.3})
            volume = velocity * drum_config["base_volume"]

            # For bass drums, sine waves in sub 100Hz range simulate the low-pitched thump of a kick drum
            # https://www.musicguymixing.com/sine-wave-kick-drum/
            if drum_config["type"] == "wave":
                wave = self.generateWave(drum_config["frequency"], duration, waveform=drum_config["waveform"], volume=volume)
            else:
               # Simulate the short bursts of noise-based drum sounds. Unsupported drum pitches sound quieter.
                wave = self.generateNoise(duration, volume=volume)
            
            # Add part to percussion track during its timeslot
            start_sample = int(note.start * SAMPLE_RATE)
            end_sample = start_sample + len(wave)
            percussion_parts[start_sample:end_sample] += wave[:len(percussion_parts) - start_sample]
        
        # Combine waves into a single waveform
        self.percussion_wave += percussion_parts

    def midiToChiptune(self):
        """
        The process to generate a chiptune track for an input MIDI file. For every instrument from the MIDI, 
        populates melody, bassline, and percussion tracks with basic waveforms based on each note's pitch, velocity, 
        and duration. Then, combines each part to construct the complete chiptune wave resembling the input MIDI.

        Returns:
            np.ndarray: Combined waveform of melody, bassline, and percussion constructed using chiptune waveforms. 
        """        
        for instrument in self.instruments:
             # Drums don't use frequency / note pitch, generate a percussive noise based on note pitch
             if instrument.is_drum:
                self.generatePercussion(instrument.notes)
             else:
                # Melodic and bassline notes, determine which part based on MIDI program
                self.generateMelodyOrBassline(instrument.notes, instrument.program)
        
        self.full_wave = self.melody_wave + self.bass_wave + self.percussion_wave
        # Due to additive synthesis (overlaying waves on top of each other), normalize to prevent clipping
        self.full_wave = self.full_wave / np.max(np.abs(self.full_wave))

if __name__ == "__main__":
    synth = MidiToChiptune("midi-assets/Kirby's Return to Dreamland - Channel Menu.mid")
    synth.printMidiInfo()
    synth.midiToChiptune()
    sd.play(synth.full_wave, samplerate=SAMPLE_RATE)
    sd.wait()