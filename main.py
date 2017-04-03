from miditime.miditime import MIDITime
import random
import argparse


class Pitch:
    octave_min = 1
    octave_max = 6
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
                 'H': 11}

    def __init__(self, sound, offset, octave):
        if octave < self.octave_min:
            octave = self.octave_min
        if octave > self.octave_max:
            octave = self.octave_max
        self.value = self.sound_map[sound] + (octave + offset-1) * 12 + self.pitch_start

    @classmethod
    def create_sound_list(cls, scale):
        sound_list = []
        offset = 0
        previous_sound_value = 0
        for sound in scale:
            if cls.sound_map[sound] < previous_sound_value:
                offset += 1
            sound_list.append([sound, offset])
            previous_sound_value = cls.sound_map[sound]
        return sound_list


class Chord:
    chord_map = {'C': ['C', 'E', 'G'],
                 'c': ['C', 'DIS', 'G'],
                 'C#': ['CIS', 'F', 'GIS'],
                 'c#': ['CIS', 'E', 'GIS'],
                 'D': ['D', 'FIS', 'A'],
                 'd': ['D', 'F', 'A'],
                 'D#': ['DIS', 'G', 'AIS'],
                 'd#': ['DIS', 'FIS', 'AIS'],
                 'E': ['E', 'GIS', 'H'],
                 'e': ['E', 'G', 'H'],
                 'F': ['F', 'A', 'C'],
                 'f': ['F', 'GIS', 'C'],
                 'F#': ['FIS', 'AIS', 'CIS'],
                 'f#': ['FIS', 'A', 'CIS'],
                 'G': ['G', 'H', 'D'],
                 'g': ['G', 'AIS', 'D'],
                 'G#': ['GIS', 'C', 'DIS'],
                 'g#': ['GIS', 'H', 'DIS'],
                 'A': ['A', 'CIS', 'E'],
                 'a': ['A', 'C', 'E'],
                 'A#': ['AIS', 'D', 'F'],
                 'a#': ['AIS', 'CIS', 'F'],
                 'a7': ['A', 'C', 'E', 'G']}

    def __init__(self, chord_name, octave):
        chord = self.chord_map[chord_name]
        self.pitch_list = []
        self.sound_list = Pitch.create_sound_list(chord)
        for sound in self.sound_list:
            pitch = Pitch(sound[0], sound[1], octave)
            self.pitch_list.append(pitch)

    @classmethod
    def get_chords_for_scale(cls, scale):
        chords = []
        for chord_name, chord in cls.chord_map.items():
            if cls.chord_in_scale(chord,scale):
                chords.append(chord_name)
        return chords

    @staticmethod
    def chord_in_scale(chord, scale):
        i = 0
        for e in scale:
            if chord[i] == e:
                i += 1
            if i == len(chord)-1:
                return True
        return False


class Scale:
    scale_map = {'A-moll': ['A', 'H', 'C', 'D', 'E', 'F', 'G', 'A'],
                 'C-dur': ['C', 'D', 'E', 'F', 'G', 'A', 'H', 'C'],
                 'C-moll': ['C', 'D', 'DIS', 'F', 'G', 'GIS', 'AIS', 'C']}

    pitch_d_list = [0.25, 0.5, 1]
    chord_d_list = [1, 2, 4]

    def __init__(self, scale_name, bass_octave, melody_octave):
        self.scale = self.scale_map[scale_name]
        self.bass_octave = bass_octave
        self.melody_octave = melody_octave
        self.sound_list = Pitch.create_sound_list(self.scale)

    def hello_word(self, midi_helper):
        for sound in self.sound_list:
            midi_helper.add_pith(Pitch(sound[0], sound[1], self.melody_octave))
        for sound in reversed(self.sound_list):
            midi_helper.add_pith(Pitch(sound[0], sound[1], self.melody_octave))

    @classmethod
    def random_scale_name(cls):
        return random.choice(list(cls.scale_map.keys()))

    def random_chord_music(self, midi_helper):
        chord_list = Chord.get_chords_for_scale(self.scale)
        for j in range(0, 3):
            i = 0
            while i < 4:
                chord_name = random.choice(chord_list)
                chord = Chord(chord_name, self.bass_octave)
                chord_d = random.choice(self.chord_d_list)
                if chord_d > 4 - i:
                    available_d = list(filter(lambda x: x <= 4 - i, self.chord_d_list))
                    chord_d = min(available_d, key=lambda x: abs(chord_d-x))
                midi_helper.add_chord(chord, chord_d, 100)
                i += chord_d
                j = 0
                while j < chord_d:
                    chord_sound = random.choice(chord.sound_list)[0]
                    pitch_tuple = list(filter(lambda x: x[0] == chord_sound, self.sound_list))[0]
                    pitch = Pitch(pitch_tuple[0], pitch_tuple[1], self.melody_octave)
                    pitch_d = random.choice(self.pitch_d_list)
                    if pitch_d > chord_d - j:
                        available_d = list(filter(lambda x: x <= chord_d - j, self.pitch_d_list))
                        pitch_d = min(available_d, key=lambda x: abs(pitch_d - x))
                    midi_helper.add_pith(pitch, pitch_d)
                    j += pitch_d


class MidiHelper:
    def __init__(self, filename, bpm, bass_volume, melody_volume):
        # Instantiate the class with a tempo (120bpm is the default) and an output file destination.
        self.my_midi = MIDITime(bpm, filename)
        # Create a list of notes. Each note is a list: [time, pitch, velocity, duration]
        self.midi_notes = []
        self.midi_final_notes = []
        self.duration = 0
        self.bass_track = 0
        self.melody_track = 0
        self.bass_volume = bass_volume
        self.melody_volume = melody_volume

    def add_pith(self, pitch, d, volume=None):
        if volume is None:
            volume = self.melody_volume
        self.midi_notes.append([self.melody_track, pitch.value, volume, d])
        self.melody_track += d

    def add_chord(self, chord, d, volume=None):
        if volume is None:
            volume = self.bass_volume
        for pitch in chord.pitch_list:
            self.midi_notes.append([self.bass_track, pitch.value, volume, d])
        self.bass_track += d

    def loop_music(self, max_duration):
        self.midi_final_notes = []
        self.midi_notes.sort(key=lambda x: x[0])
        offset = 0
        self.duration = max(self.bass_track, self.melody_track)
        while self.duration < max_duration:
            previous_start = self.duration
            for note in self.midi_notes:
                new_note = note[:]
                new_note[0] += offset
                if (new_note[0] != previous_start) and (self.duration >= max_duration):
                    break
                self.midi_final_notes.append(new_note)
                self.duration = new_note[0] + new_note[3]
                previous_start = new_note[0]
            offset = self.duration

    def save(self):
        # Add a track with those notes
        if not self.midi_final_notes:
            for e in self.midi_notes:
                note = e[:]
                self.midi_final_notes.append(note)
        self.my_midi.add_track(self.midi_final_notes)
        # Output the .mid file
        self.my_midi.save_midi()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-bpm', type=int, default=120, help='BPM', dest='bmp')
    parser.add_argument('-f', type=str, default='myfile.mid', help='FILENAME', dest='filename')
    random_scale = False
    args = parser.parse_args()
    midi_helper = MidiHelper(args.filename, args.bmp, 60, 120)
    scale_name = 'A-moll'
    if random_scale:
        scale_name = Scale.random_scale_name()
    scale = Scale(scale_name, 2, 5)
    scale.random_chord_music(midi_helper)
    midi_helper.loop_music(4*4*4)
    midi_helper.save()

if __name__ == '__main__':
    main()
