# Adaptive Tone Control - Irvin Lu

This assignment project takes in a provided WAV file and arbitrarily divedes its audio frequencies into three arbitrary bands: low (0-300 Hz), mid (300-2000 Hz), and high (2000+ Hz). An FFT is used to calculate the sound energy within the three frequency bands across short time windows.

Tone filters are then applied to adjust the energy in each band, balancing them so that the energies of the three bands are roughly
equal. This process demonstrates **tone control** - adjusting the volume within specific frequency bands independently. Through
manipulating individual frequencies to be softer or louder by adjusting their energies, the original audio with its varied band
"levels" can sound more balanced or neutral in volume.
