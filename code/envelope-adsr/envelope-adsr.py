
import numpy as np
import sounddevice as sd

VOLUME = 0.5
SAMPLE_RATE = 44100

def apply_envelope(original_wave, tAttack, tDecay, tRelease, peak_level, sustain_level):
    """
    Applies an envelope over a supplied wave using expected seconds for each ADSR parameter.

    Args:
        original_wave (np.array): Audio wave function to apply ADSR over.
        tAttack (float): Time for **attack** - the time from silence to reach peak amplitude.
        tDecay (float): Time for **decay** - the time from peak amplitude to reach sustain amplitude.
        tSustain (float): Time for **sustain** - the time period for the sound to rest / maintain.
        tRelease (float): Time for **release** - the time from sustain amplitude to reach silence.
    
    Returns:
        envelope_wave (np.array): A copy of the original wave but with the ADSR applied.
    """
    wave = np.copy(original_wave)

    # Samples lengths for each ADSR parameter
    attack_samples = int(tAttack * SAMPLE_RATE)
    decay_samples = int(tDecay * SAMPLE_RATE)
    release_samples = int(tRelease * SAMPLE_RATE)
    sustain_samples = len(wave) - (attack_samples + decay_samples + release_samples)

    # np.linspace is used for gradual increases/decreases of amplitude to mimic natural sound
    envelope = np.concatenate([
        np.linspace(0, peak_level, attack_samples), # Attack
        np.linspace(peak_level, sustain_level, decay_samples), # Decay
        # np.full is used to create a constant level of amplitude to "rest" on
        np.full(sustain_samples, sustain_level), # Sustain
        np.linspace(sustain_level, 0, release_samples) # Release
    ])

    # Apply envelope to wave, ensure envelope matches wave length in case of int rounding
    envelope_wave = wave * envelope[:len(wave)]
    return envelope_wave

if __name__ == "__main__":
    # Wave Audio
    duration = 1.0
    frequency = 440 # A4 Note
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # Using sine wave as example, can apply other waves here
    wave = VOLUME * np.sin(2 * np.pi * frequency * t)
   
    # Steady smooth wave that builds up to peak amplitude and drifts off
    melody = apply_envelope(wave, tAttack=0.2, tDecay=0.15, tRelease=0.03, peak_level=0.9, sustain_level=0.6)
    print("Playing Wave 1")
    sd.play(melody, samplerate=SAMPLE_RATE)
    sd.wait()

    # More rhythmic if repeated, quick to reach peak and lower sustain to feel like background complement  
    punchy = apply_envelope(wave, tAttack=0.01, tDecay=0.25, tRelease=0.02, peak_level=0.8, sustain_level=0.3)
    print("Playing Wave 2")
    sd.play(punchy, samplerate=SAMPLE_RATE)
    sd.wait()

    # Sharp and quick burst attempt, maximum peak and no sustain to avoid lingering
    percussive = apply_envelope(wave, tAttack=0.01, tDecay=0.1, tRelease=0.1, peak_level=1.0, sustain_level=0.0)
    print("Playing Wave 3")
    sd.play(percussive, samplerate=SAMPLE_RATE)
    sd.wait()
