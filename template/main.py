#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict

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
    for line in lines:
        print(line)
    return 0

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
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
