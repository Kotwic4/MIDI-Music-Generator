from miditime.miditime import MIDITime

# Instantiate the class with a tempo (120bpm is the default) and an output file destination.
mymidi = MIDITime(240, 'myfile.mid')

# Create a list of notes. Each note is a list: [time, pitch, velocity, duration]
midi_notes = [
    [0, 60, 127, 4],   # C4
    [4, 62, 127, 4],   # D4
    [8, 64, 127, 4],   # E4
    [12, 65, 127, 4],  # F4
    [16, 67, 127, 4],  # G4
    [20, 69, 127, 4],  # A4
    [24, 71, 127, 4],  # B4
    [28, 72, 127, 4],  # C5
]

# Add a track with those notes
mymidi.add_track(midi_notes)

# Output the .mid file
mymidi.save_midi()
