#!/usr/bin/env env/bin/python

import argparse
import mido

DEFAULT_INPUT = 'KeyLab mkII 61:KeyLab mkII 61 MIDI'

def get_midi_in():
    inputs = mido.get_input_names()
    default_i = 0
    entry = -1

    while(entry < 0 or entry >= len(inputs)):
        for i, name in enumerate(inputs):
            if DEFAULT_INPUT in name:
                default_i = i
            print('%d: %s' % (i, name))

        raw_entry = input('Input (default: %d): ' % default_i)

        try:
            entry = int(raw_entry)
        except ValueError:
            entry = default_i

    return inputs[entry]

def get_cmd_args():
    parser = argparse.ArgumentParser(
        prog='rmidi',
        description='record midi data from given input to given file')

    parser.add_argument('-i', '--input')
    parser.add_argument('-f', '--file', required=True)

    return parser.parse_args()

def read_input(midi_in):
    try:
        with mido.open_input(midi_in) as inport:
            for msg in inport:
                print(msg)
    except KeyboardInterrupt:
        print()
        pass


if __name__ == '__main__':
    args = get_cmd_args()
    midi_in = args.input
    filename = args.file

    if not midi_in:
        midi_in = get_midi_in()

    print('Recording from "%s"' % midi_in)
    read_input(midi_in)
