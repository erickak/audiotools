#!/usr/bin/env env/bin/python

import argparse
import mido
from timeit import default_timer as timer

PROG_NAME = 'pmidi'
PROG_DESCRIP = 'play midi data from given file to given output'
DEFAULT_OUTPUT = 'fluidsynth 1'
SECONDS_PER_MIN = 60


def get_cmd_args():
    parser = argparse.ArgumentParser(prog=PROG_NAME, description=PROG_DESCRIP)
    parser.add_argument('file')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def get_midi_out():
    outputs = mido.get_output_names()
    default_i = 0
    entry = -1

    while(entry < 0 or entry >= len(outputs)):
        for i, name in enumerate(outputs):
            if DEFAULT_OUTPUT in name:
                default_i = i
            print('%d: %s' % (i, name))

        raw_entry = input('Output (default: %d): ' % default_i)

        try:
            entry = int(raw_entry)
        except ValueError:
            entry = default_i

    return outputs[entry]

def play_file(filename, midi_out, print_msgs=False):
    with mido.open_output(midi_out, autoreset=True) as midi_out:
        midifile = mido.MidiFile(filename)
        for msg in midifile.play():
            print(msg)
            midi_out.send(msg)


if __name__ == '__main__':
    args = get_cmd_args()
    midi_out = args.output
    filename = args.file
    print_msgs = args.verbose

    if not midi_out:
        midi_out = get_midi_out()

    print('Sending to "%s"' % midi_out)

    try:
        play_file(filename, midi_out, print_msgs=print_msgs)
    except KeyboardInterrupt:
        print('')
