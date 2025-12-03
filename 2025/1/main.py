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
# import pyperclip
import queue
import re

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    r = 50
    sol = 0
    for line in lines:
        if line.startswith('L'):
            turn = -1 * int(line[1:])
        if line.startswith('R'):
            turn = 1 * int(line[1:])
        while turn <= -100:
            turn += 100
            sol += 1
        while turn >= 100:
            turn -= 100
            sol += 1

        if r + turn >= 100:
            sol += 1
            print(line)
        elif r > 0 and r + turn < 0:
            sol += 1
            print(line)
        if r + turn == 0:
            sol += 1
            print(line)

        r = (r + turn) % 100
        print(r)
    return sol

def solve2(lines):
    pass

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
        # pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        # pyperclip.copy(p2)
