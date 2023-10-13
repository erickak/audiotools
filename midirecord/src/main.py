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
    parser.add_argument('-f', '--file')

    return parser.parse_args()

def get_msg_handler(appendable, print_msgs):
    def full(x):
        appendable.append(x)
        print(x)

    def append_only(x):
        appendable.append(x)

    def print_only(x):
        print(x)

    if appendable is None:
        if print_msgs:
            return print_only
        else:
            return lambda *args: None
    else:
        if print_msgs:
            return full
        else:
            return append_only

def accumulate_input(midi_in, appendable=None, print_msgs=True):
    handler = get_msg_handler(appendable, print_msgs)
    try:
        with mido.open_input(midi_in) as inport:
            for msg in inport:
                handler(msg)
    except KeyboardInterrupt:
        print() # Just so the ^C ends up on a separate line from prompt on exit
        pass


if __name__ == '__main__':
    args = get_cmd_args()
    midi_in = args.input
    filename = args.file

    if not midi_in:
        midi_in = get_midi_in()

    print('Recording from "%s"' % midi_in)

    if filename:
        mid = mido.MidiFile(type=0)
        track = mido.MidiTrack()
        mid.tracks.append(track)
        accumulate_input(midi_in, appendable=track)
        mid.save(filename)
    else:
        accumulate_input(midi_in)
