#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import *
from py_utils.search import *

from collections import defaultdict

import ast
import fileinput
import itertools
import math
import os
import pyperclip
import queue
import re
import json
import functools

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None


def ordered(p1, p2):
    if not isinstance(p1, list) and not isinstance(p2, list):
        dprint(f'Compare {p1} vs {p2}')
        return p2 - p1
    p1 = p1 if isinstance(p1, list) else [p1]
    p2 = p2 if isinstance(p2, list) else [p2]
    for i in range(len(p1)):
        if i >= len(p2):
            dprint(f'Right ran out of items')
            return -1
        diff = ordered(p1[i], p2[i])
        if diff != 0:
            return diff
    if len(p1) != len(p2):
        return 1
        dprint(f'Left ran out of items')
    return 0

def solve1(lines):
    score = 0
    for l in range(0, len(lines), 3):
        line1 = lines[l]
        line2 = lines[l+1]
        p1, p2 = eval(line1), eval(line2)
        right_order = ordered(p1, p2) > 0
        if right_order:
            dprint(f'Left side is smaller')
            print(f'{l//3 + 1}')
            score += l//3 + 1
        else:
            dprint(f'Right side is smaller')
            print('Wrong order')
    return score

def solve2(lines):
    score = 0
    packets = []
    for line in lines:
        if len(line) == 0:
            continue
        p1 = eval(line)
        packets.append(p1)
    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=functools.cmp_to_key(ordered))
    packets.reverse()
    i1 = packets.index([[2]]) + 1
    i2 = packets.index([[6]]) + 1
    print (i1, i2)
    print(packets)
    return i1 * i2

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
