import argparse
import numpy as np
import os
import pretty_midi # 0.2.10 release incompatible with Python 3.12: https://github.com/craffel/pretty-midi/pull/252
import sounddevice as sd
from scipy import signal
from scipy.io.wavfile import write
from typing import List

# The sample rate to produce chiptune audio with.
SAMPLE_RATE = 44100

# The multiplier to apply to the resulting chiptune track, for reducing overall volume if too loud.
LOUDNESS = 0.40

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
    def __init__(self, input_midi, disable_adsr):
        """
        Extracts the MIDI data from a given `.mid` file to prepare for applying chiptune waveforms on each note.

        Args:
            input_midi (str): The MIDI file path to process, parsed using the `pretty_midi` library.
            disable_adsr (bool): Whether to apply an ADSR envelope on the melody, bassline, and percussion waves.
        """
        # Arguments from Command Line
        self.file_path, file_extension = os.path.splitext(input_midi)
        self.track_name = os.path.basename(self.file_path)
        self.adsr = not disable_adsr
        
        if not file_extension == '.mid':
            raise OSError('File must be a MIDI file (.mid)')
        
        # Get all the information pretty_midi parses
        self.data = pretty_midi.PrettyMIDI(input_midi)
        self.instruments: List[pretty_midi.Instrument] = self.data.instruments # Contains notes under each
        self.time_signatures = self.data.time_signature_changes
        self.key_signatures = self.data.key_signature_changes
        self.track_length = self.calculateTrackLength()

        # Waveforms to construct chiptune tunes with
        self.melody_wave = np.zeros(self.track_length)
        self.bass_wave = np.zeros(self.track_length)
        self.percussion_wave = np.zeros(self.track_length)

        # Final wave to sum above musical parts into
        self.chiptune_wave = np.zeros(self.track_length)

        # Perform the chiptune synthesis, storing result in chiptune_wave
        self.midiToChiptune()
    
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
        print(self.track_name)

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
    
    def applyEnvelope(self, original_wave, tAttack, tDecay, tRelease, sustain_level, velocity):
        """
        Applies an ADSR envelope to a waveform with velocity dynamics.

        Args:
            original_wave (np.ndarray): The waveform to apply the envelope to.
            tAttack (float): Attack time in seconds.
            tDecay (float): Decay time in seconds.
            tRelease (float): Release time in seconds.
            sustain_level (float): Base sustain level (scaled by velocity).
            velocity (float): MIDI velocity normalized to 0.0–1.0.

        Returns:
            np.ndarray: A copy of the original waveform with the ADSR envelope applied.
        """
        wave = np.copy(original_wave)

        # Convert time parameters to sample counts
        attack_samples = int(tAttack * SAMPLE_RATE)
        decay_samples = int(tDecay * SAMPLE_RATE)
        release_samples = int(tRelease * SAMPLE_RATE)
        sustain_samples = max(0, len(wave) - (attack_samples + decay_samples + release_samples))

        # Scale sustain level and peak amplitude by velocity
        peak_amplitude = velocity
        scaled_sustain = sustain_level * velocity

        envelope = np.concatenate([
            np.linspace(0, peak_amplitude, attack_samples), # Attack
            np.linspace(peak_amplitude, scaled_sustain, decay_samples), # Decay
            np.full(sustain_samples, scaled_sustain), # Sustain
            np.linspace(scaled_sustain, 0, release_samples) # Release
        ])

        # Apply envelope to wave, ensure envelope matches wave length in case of int rounding
        return wave * envelope[:len(wave)]
    
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
    
    def generateDrumSound(self, pitch, duration, velocity):
        """
        Generates a drum effect based on the percussive sound determined by an input note's pitch.
        References the `DRUM_KEY_MAP` for supported note numbers / drum types.

        Args:
            pitch (int): The MIDI note pitch to determine which type of drum sound is generated.
            duration (float): Duration of the input note in seconds. 
            velocity (int): The strength the input note, used to determine volume multiplier.

        Returns:
            wave (np.ndarray): A sine wave or noise wave array to use as the drum sound for the notes 
            of a percussion instrument.
        """
        # Determine the drum sound based on pitch, default to a quieter sound for unsupported drum types
        drum_config = DRUM_KEY_MAP.get(pitch, {"type": "unsupported", "base_volume": 0.3})
        volume = velocity * drum_config["base_volume"]

        # For bass drums, sine waves in sub 100Hz range simulate the low-pitched thump of a kick drum
        # https://www.musicguymixing.com/sine-wave-kick-drum/
        if drum_config["type"] == "wave":
            wave = self.generateWave(drum_config["frequency"], duration, drum_config["waveform"], volume)
        else:
            # Simulate the short bursts of noise-based drum sounds. Unsupported drum pitches sound quieter.
            wave = self.generateNoise(duration, volume)
        
        return wave
    
    def generatePercussion(self, notes: List[pretty_midi.Note]):
        """
        Given all notes from an instrument in the input MIDI, generates a percussion waveform or noise wave.
        The type and base volume of the drum sound to generate depends on the a given note's pitch / key number, 
        in addition to whether the note key is supported in `DRUM_KEY_MAP`.

        Args:
            notes (List[Note]): Array of notes to derive information from for generating chiptune noises.
        
        Returns:
            percussion_parts: Audio data containing the generated percussive waveform or noises.
        """
        percussion_parts = np.zeros(self.track_length)

        for note in notes:
            duration = note.end - note.start
            velocity = note.velocity / 127.0
            
            # Obtain either a waveform (bass drums) or noise wave (other drums).
            wave = self.generateDrumSound(note.pitch, duration, velocity)
            if self.adsr:
                # Percussion sounds naturally short, should not sustain a sound
                wave = self.applyEnvelope(wave, tAttack=0.01, tDecay=0.05, tRelease=0.05, sustain_level=0.0, velocity=velocity)

            # Add part to percussion track during its timeslot
            start_sample = int(note.start * SAMPLE_RATE)
            end_sample = start_sample + len(wave)
            
            percussion_parts[start_sample:end_sample] += wave[:len(percussion_parts) - start_sample]
        
        # Contains chiptune audio data for percussive instruments
        return percussion_parts

    def generateMelodyOrBassline(self, notes: List[pretty_midi.Note], program):
        """
        Given all notes from an instrument in the input MIDI, generates a basic waveform to serve as the melody
        or bassline for this instrument of the chiptune synthesis. Whether a melody or bassline is generated depends 
        on the instrument's program number.

        Args:
            notes (List[Note]): Array of notes to derive information from for generating a chiptune wave.
            program (int): The program number of the MIDI instrument.
        
        Returns:
            tuple (melody_parts, bass_parts): Audio data containing the generated waveform for either the melody 
            or bassline.
        """
        melody_parts = np.zeros(self.track_length)
        bass_parts = np.zeros(self.track_length)

        # General MIDI Program Numbers: https://en.wikipedia.org/wiki/General_MIDI#Program_change_events
        waveform = None
        if program in range(32, 40): # Bass instruments from 33-40, -1 to account for zero indexing 
            # Triangle waves softer, fit for bassline: https://soundation.com/music-genres/how-to-make-chiptunes
            waveform = "triangle"
        elif program in range(40, 80): # Strings, Ensemble, Brass, Reed, and Pipe labeled 41-80, -1 for zero indexing
            # Sawtooth best for bowed instruments: https://en.wikipedia.org/wiki/Sawtooth_wave
            waveform = "sawtooth"
        else: # All other instruments used for melody (piano, etc.)
            waveform = "square" # Square waves make sharp distinct sounds fitting for a melody

        # Apply waveform on each note played by the instrument
        for note in notes:
            frequency = self.midiNoteToFrequency(note.pitch)
            duration = note.end - note.start
            # Normalize velocity, MIDI considers 127 the maximum strength a note was hit
            velocity = note.velocity / 127.0

            # Construct waveform data
            wave = self.generateWave(frequency, duration, waveform, volume=velocity)

            # Place waveforms in the appropriate track timeslot
            start_sample = int(note.start * SAMPLE_RATE)
            end_sample = start_sample + len(wave)
            
            if waveform == "triangle": # Bass
                if self.adsr:
                    wave = self.applyEnvelope(wave, tAttack=0.01, tDecay=0.1, tRelease=0.1, sustain_level=0.65, velocity=velocity)
                bass_parts[start_sample:end_sample] += wave[:len(bass_parts) - start_sample]

            else: # Melody (square or sawtooth)
                if self.adsr:
                    wave = self.applyEnvelope(wave, tAttack=0.05, tDecay=0.15, tRelease=0.2, sustain_level=0.75, velocity=velocity)
                melody_parts[start_sample:end_sample] += wave[:len(melody_parts) - start_sample]
        
        # Contains chiptune audio data for melody and bassline instruments
        return melody_parts, bass_parts

    def midiToChiptune(self):
        """
        The process to generate a chiptune track for an input MIDI file. For every instrument from the MIDI, 
        populates melody, bassline, and percussion tracks with basic waveforms based on each note's pitch, velocity, 
        and duration. Then, combines each part to construct the complete chiptune wave resembling the input MIDI.
        
        Populates the `melody_wave`, `bass_wave` and `percussion_wave` class variables to sum into the overall 
        `chiptune_wave`, the final synthesized audio data.
        """        
        for instrument in self.instruments:
             if instrument.is_drum:
                # Drums don't use frequency / note pitch, generate a percussive noise based on note pitch
                self.percussion_wave += self.generatePercussion(instrument.notes)
             else:
                # Melodic and bassline notes, determine which part based on MIDI program
                melody_parts, bass_parts = self.generateMelodyOrBassline(instrument.notes, instrument.program)
                self.melody_wave += melody_parts
                self.bass_wave += bass_parts
        
        # Construct final wave, combine all instruments back together
        self.chiptune_wave = self.melody_wave + self.bass_wave + self.percussion_wave

        # Due to additive synthesis (overlaying waves on top of each other), normalize to prevent clipping
        self.chiptune_wave = self.chiptune_wave / np.max(np.abs(self.chiptune_wave))
        self.chiptune_wave = np.tanh(self.chiptune_wave) # Softly limit range to prevent peaks
        self.chiptune_wave *= LOUDNESS      

    def saveWAV(self, output_dir="output-wavs"):
        """
        Saves the `chiptune_wave` audio data array to a WAV file. The saved filename matches the original 
        input MIDI's track name.

        Args:
            output_dir (str): The directory name to save the WAV file to. Defaults to `output-wavs`
        
        Raises:
            Exception: If `chiptune_wave` is not populated yet, inform user to run converter first.
        """ 
        # Convert to expected format WAV files expect
        if self.chiptune_wave.any(): 
            wav_chiptune_wave = (self.chiptune_wave * 32767).astype(np.int16)
            write(f"{output_dir}/{self.track_name}.wav", SAMPLE_RATE, wav_chiptune_wave)
        else:
            raise Exception("No chiptune audio to save. Please call midiToChiptune() before saving audio.")
    
    def playChiptune(self):
        """
        Plays the `chiptune_wave` to computer audio output using the `sounddevice` library.

        Raises:
            Exception: If `chiptune_wave` is not populated yet, inform user to run converter first.
        """
        if self.chiptune_wave.any():
            print(f"♪♪♪\tPlaying {self.track_name}\t♪♪♪")
            sd.play(synth.chiptune_wave, samplerate=SAMPLE_RATE)
            sd.wait()
            print(f"---\tFinished {self.track_name}\t---")

        else:
            raise Exception("No chiptune audio to play. Please call midiToChiptune() before playing audio.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Chiptune Synthesizer")
    
    # Required Argument, path to MIDI file to synthesize chiptune waves with:
    ap.add_argument("input_midi", help="File path to the input MIDI file.")

    # Optional Arguments
    ap.add_argument('--output', default="output-wavs", help="Directory to generate the chiptune WAV into. Defaults to `output-wavs`.")
    ap.add_argument('--no-play', action="store_true", help="Do not play the chiptune wave to audio output.")
    ap.add_argument('--disable-adsr', action="store_true", help="Disable applying an ADSR envelope.")
    args = ap.parse_args()

    # Construct the Chiptune Wave
    synth = MidiToChiptune(args.input_midi, args.disable_adsr)

    # Show the Results
    synth.printMidiInfo()
    synth.saveWAV(args.output)
    
    if not args.no_play:
        print()
        synth.playChiptune()
