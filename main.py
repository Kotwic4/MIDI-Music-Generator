from miditime.miditime import MIDITime
import argparse


class Pitch:
    octave_min = 1
    octave_max = 7
    pitch_start = 24  # value of C1
    sound_map = {'C': 0,
                 'CIS': 1,
                 'D': 2,
                 'DIS': 3,
                 'E': 4,
                 'F': 5,
                 'FIS': 6,
                 'G': 7,
                 'GIS': 8,
                 'A': 9,
                 'AIS': 10,
                 'H': 11}  # B is AIS or H!

    def __init__(self, sound, offset=0, octave=4):
        self.value = self.sound_map[sound] + (octave + offset-1) * 12 + self.pitch_start


class Scale:
    scale_map = {'A-moll': [('A', 0), ('H', 0), ('C', 1), ('D', 1), ('E', 1), ('F', 1), ('G', 1), ('A', 1)],
                 'C-dur': [('C', 0), ('D', 0), ('E', 0), ('F', 0), ('G', 0), ('A', 0), ('H', 0), ('C', 1)],
                 'C-moll': [('C', 0), ('D', 0), ('DIS', 0), ('F', 0), ('G', 0), ('GIS', 0), ('AIS', 0), ('C', 1)]}

    def __init__(self, scale_name='C-dur'):
        self.pitch_list = self.scale_map[scale_name]

    def test(self, midi_helper):
        for pitch_tuple in self.pitch_list:
            pitch = Pitch(pitch_tuple[0], pitch_tuple[1])
            midi_helper.add_pith(pitch)
        for pitch_tuple in reversed(self.pitch_list):
            pitch = Pitch(pitch_tuple[0], pitch_tuple[1])
            midi_helper.add_pith(pitch)


class MidiHelper:
    def __init__(self, filename, bpm):
        # Instantiate the class with a tempo (120bpm is the default) and an output file destination.
        self.my_midi = MIDITime(bpm, filename)
        # Create a list of notes. Each note is a list: [time, pitch, velocity, duration]
        self.midi_notes = []
        self.i = 0

    def add_pith(self, pitch, d=2, volume=127):
        self.midi_notes.append([self.i, pitch.value, volume, d])
        self.i += d

    def save(self):
        # Add a track with those notes
        self.my_midi.add_track(self.midi_notes)
        # Output the .mid file
        self.my_midi.save_midi()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-bpm', type=int, default=120, help='BPM', dest='bmp')
parser.add_argument('-f', type=str, default='myfile.mid', help='FILENAME', dest='filename')
args = parser.parse_args()
midi_helper = MidiHelper(args.filename, args.bmp)
scale = Scale('A-moll')
scale.test(midi_helper)
midi_helper.save()
