import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import pretty_midi # Currnetly incompatible with Python 3.12: https://github.com/craffel/pretty-midi/pull/252
import os

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
        self.instruments = self.data.instruments # Contains notes under each
        self.time_signatures = self.data.time_signature_changes
        self.key_signatures = self.data.key_signature_changes
    
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
            print(f"{instrument.name} has {len(instrument.notes)} notes")
        
        print("--------------------")

if __name__ == "__main__":
    synth = MidiToChiptune("Kirby's Return to Dreamland - Channel Menu.mid")
    synth.printMidiInfo()