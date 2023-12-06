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

def solve1(lines):
    r = 1
    times = [int(i) for i in lines[0].split(':')[1].split()]
    dists = [int(i) for i in lines[1].split(':')[1].split()]
    print(times)
    print(dists)
    for i in range(len(dists)):
        count = 0
        time = times[i]
        dist = dists[i]
        for j in range(1, time):
            a = j
            b = time - j
            if a*b > dist:
                count += 1
        print(count)
        r *= count
    return r

def solve2(lines):
    r = 1
    time = 53837288
    dist = 333163512891532
    count = 0
    for j in range(1, time):
        a = j
        b = time - j
        if a*b > dist:
            count += 1
    return count

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
