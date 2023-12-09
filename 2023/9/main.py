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

def extrapolate(d):
    if d.count(0) == len(d):
        return 0
    e = []
    for i in range(len(d) - 1):
        e.append(d[i+1] - d[i])
    print(e)
    return d[-1] + extrapolate(e)

def extrapolate2(d):
    if d.count(0) == len(d):
        return 0
    e = []
    for i in range(len(d) - 1):
        e.append(d[i+1] - d[i])
    print(e)
    return d[0] - extrapolate2(e)

def solve1(lines):
    r = 0
    for line in lines:
        nums = get_ints(line)
        d = nums.copy()
        r += extrapolate(d)
    return r

def solve2(lines):
    r = 0
    for line in lines:
        nums = get_ints(line)
        d = nums.copy()
        r += extrapolate2(d)
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
