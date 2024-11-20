import numpy as np
import os
import pretty_midi # 0.2.10 release incompatible with Python 3.12: https://github.com/craffel/pretty-midi/pull/252
import sounddevice as sd
from scipy import signal
from scipy.io.wavfile import write
from typing import List

SAMPLE_RATE = 44100

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

        # Waveforms to construct chiptune tunes with
        self.melody_wave, self.bass_wave, self.percussion_wave = [], [], []
    
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
    
    def generateMelodyOrBassline(self, notes: List[pretty_midi.Note], program):
        """
        Given all notes from an instrument in the input MIDI, generate a wave to add to the melody
        or bassline tracks. Whether a melody or bassline is generated depends on instrument's program number.
        """
        for note in notes:
            frequency = self.midiNoteToFrequency(note.pitch)
            duration = note.end - note.start
            # Normalize velocity, MIDI considers 127 the maximum strength a note was hit
            velocity = note.velocity / 127.0

            # General MIDI format states bass instruments from 33-40, -1 to account for zero indexing 
            if program in range(32, 40):
                # Triangle waves are softer, more fit for bassline
                # https://soundation.com/music-genres/how-to-make-chiptunes
                wave = self.generateWave(frequency, duration, waveform='triangle', volume=velocity)
                self.bass_wave.append(wave)
            
            # All other instruments used for melody (piano, orchestra, non-bass guitars, etc.)
            else:
                # Square waves make sharp distinct sounds fitting for a melody
                wave = self.generateWave(frequency, duration, waveform='square', volume=velocity)
                self.melody_wave.append(wave)

    def generatePercussion(self):
        pass

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
                pass
             
             # Melodic and bassline notes, determine which part based on MIDI program
             else:
                self.generateMelodyOrBassline(instrument.notes, instrument.program)

if __name__ == "__main__":
    synth = MidiToChiptune("midi-assets/Kirby's Return to Dreamland - Channel Menu.mid")
    synth.printMidiInfo()