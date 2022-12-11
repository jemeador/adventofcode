#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict, namedtuple

import fileinput
import itertools
import pyperclip
import queue
import re

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    deck_size = 10007
    deck = list(range(0, deck_size))
    for line in lines:
        if line.startswith('deal with'):
            increment, = get_ints(line)
            new_deck = list(range(0, deck_size))
            j = 0
            for i in range(0, deck_size):
                new_deck[j] = deck[i]
                j = (j + increment) % deck_size
            deck = new_deck
            print(deck[0])
        elif line.startswith('cut'):
            position, = get_ints(line)
            deck = list(deck[position:]) + list(deck[:position])
            print(deck[0])
        elif line.startswith('deal into'):
            deck.reverse()
            print(deck[0])
    return deck.index(2019)

def mod_inverse(i, deck_size):
    return pow(i, deck_size-2, deck_size)

def solve2(lines):
    #deck_size = 10007
    #times = 1
    deck_size = 119315717514047
    times = 101741582076661
    pos = 2020
    offset_diff = 0
    increment_mul = 1
    for line in lines:
        if line.startswith('deal with'):
            i, = get_ints(line)
            increment_mul *= mod_inverse(i, deck_size)
            increment_mul %= deck_size
        elif line.startswith('cut'):
            position, = get_ints(line)
            offset_diff += increment_mul * position
            offset_diff %= deck_size
        elif line.startswith('deal into'):
            increment_mul *= -1
            increment_mul %= deck_size
            offset_diff += increment_mul
            offset_diff %= deck_size
    increment = pow(increment_mul, times, deck_size)
    offset = offset_diff * (1 - pow(increment_mul, times, deck_size)) * mod_inverse(1 - increment_mul, deck_size)

    deck = []
    for i in range(pos):
        offset += increment
        offset %= deck_size

    return offset

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1 = solve1(lines)
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
