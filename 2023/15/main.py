#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import *
from py_utils.search import *

from collections import defaultdict

import fileinput
import itertools
import math
import os
import pyperclip
import queue
import re

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

# Determine the ASCII code for the current character of the string.
# Increase the current value by the ASCII code you just determined.
# Set the current value to itself multiplied by 17.
# Set the current value to the remainder of dividing itself by 256.
def hash(instruction_str):
    current = 0
    skip = 0
    codes = [ord(c) for c in instruction_str]
    for code in codes:
        current += code
        current *= 17
        current %= 256
    return current

def hash_label(instruction_str):
    current = 0
    skip = 0
    codes = [ord(c) for c in instruction_str]
    for code in codes:
        if not (code >= ord('a') and code <= ord('z')):
            break
        current += code
        current *= 17
        current %= 256
    return current

def solve1(lines):
    r = 0
    instructions = lines[0].split(',')
    for instr in instructions:
        print(hash(instr))
        r += hash(instr)
    print()
    return r


#If the operation character is an equals sign (=), it will be followed by a
# number indicating the focal length of the lens that needs to go into the
# relevant box; be sure to use the label maker to mark the lens with the label
# given in the beginning of the step so you can find it later. There are two
# possible situations:

# One plus the box number of the lens in question.
# The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
# The focal length of the lens.

def process(hashmap, lensmap, instr):
    if '=' in instr:
        label, lens = instr.split('=')
        box_id = hash(label)
        if not label in hashmap[box_id]:
            hashmap[box_id].append(label)
        lensmap[label] = int(lens)
    if '-' in instr:
        label = instr.split('-')[0]
        box_id = hash(label)
        if label in hashmap[box_id]:
            hashmap[box_id].remove(label)

def solve2(lines):
    r = 0
    instructions = lines[0].split(',')
    hashmap = defaultdict(list)
    lensmap = {}
    for instr in instructions:
        process(hashmap, lensmap, instr)
    for box_id, lenses in hashmap.items():
        for i in range(len(lenses)):
            label = lenses[i]
            focal_len = lensmap[label]
            power = (1 + box_id) * (1 + i) * focal_len
            print(label, power)
            r += power
    return r

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
