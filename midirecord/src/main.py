#!/usr/bin/env env/bin/python

import argparse
import mido
from timeit import default_timer as timer

PROG_NAME = 'rmidi'
PROG_DESCRIP = 'record midi data from given input to given file'
DEFAULT_INPUT = 'KeyLab mkII 61:KeyLab mkII 61 MIDI'
DEFAULT_BPM = 120
SECONDS_PER_MIN = 60


def get_cmd_args():
    parser = argparse.ArgumentParser(prog=PROG_NAME, description=PROG_DESCRIP)
    parser.add_argument('-b', '--bpm', default=DEFAULT_BPM)
    parser.add_argument('-i', '--input')
    parser.add_argument('-f', '--file')
    parser.add_argument('-s', '--silence', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

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

def get_appending_handler(appendable, ticks_per_second, print_msgs):
    def full(x):
        appendable.append(x)
        print(x)

    def append_only(x):
        appendable.append(x)

    if print_msgs:
        return full

    return append_only

def print_input(midi_in):
    process_msgs(lambda x: print(x))

def accumulate_input(midi_in, appendable, ticks_per_second, print_msgs=True):
    handler = get_appending_handler(appendable, ticks_per_second, print_msgs)
    process_msgs(handler, ticks_per_second=ticks_per_second)

def process_msgs(handler, ticks_per_second=0):
    last_time = timer()

    try:
        with mido.open_input(midi_in) as inport:
            for msg in inport:

                end = timer()
                seconds = end - last_time
                last_time = end
                msg.time = round(ticks_per_second * seconds)

                handler(msg)
    except KeyboardInterrupt:
        if print_msgs:
            print() # Just so the "^C" ends up on a separate line from prompt on exit
        pass

def record_to_file(midi_in, filename, bpm, print_msgs, trim_init_silence):
    mid = mido.MidiFile(type=0)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    ticks_per_second = bpm * mid.ticks_per_beat / SECONDS_PER_MIN

    accumulate_input(midi_in, track, ticks_per_second, print_msgs)

    if trim_init_silence:
        track[0].time = 0

    mid.save(filename)

    print('MIDI data written to', filename)


if __name__ == '__main__':
    args = get_cmd_args()
    midi_in = args.input
    filename = args.file
    bpm = args.bpm
    print_msgs = args.verbose
    trim_init_silence = not args.silence

    if not midi_in:
        midi_in = get_midi_in()

    print('Receiving from "%s"' % midi_in)

    if filename:
        record_to_file(midi_in, filename, bpm, print_msgs, trim_init_silence)
    elif print_msgs:
        print_input(midi_in)
