from miditime.miditime import MIDITime
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-bpm', type=int, default=120, help='BPM', dest='bmp')
parser.add_argument('-f', type=str, default='myfile.mid', help='FILENAME', dest='filename')


class MidiHelper:
    pitch_map = {'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71, 'C5': 72}

    def __init__(self, filename, bpm):
        # Instantiate the class with a tempo (120bpm is the default) and an output file destination.
        self.my_midi = MIDITime(bpm, filename)
        # Create a list of notes. Each note is a list: [time, pitch, velocity, duration]
        self.midi_notes = []
        self.i = 0

    def add_pith(self, pitch_b, d=2, volume=127):
        self.midi_notes.append([self.i, self.pitch_map[pitch_b], volume, d])
        self.i += d

    def save(self):
        # Add a track with those notes
        self.my_midi.add_track(self.midi_notes)
        # Output the .mid file
        self.my_midi.save_midi()

args = parser.parse_args()
midi_helper = MidiHelper(args.filename,args.bmp)
pitch_list = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
for pitch in pitch_list:
    midi_helper.add_pith(pitch)
for pitch in reversed(pitch_list):
    midi_helper.add_pith(pitch)
midi_helper.save()
