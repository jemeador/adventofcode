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
import queue
import re

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve(lines, battery_count):
    r = 0
    for line in lines:
        num_str = ""
        start = 0
        for num in range(0, battery_count):
            largest_digit = line[start]
            start += 1
            end = min(len(line), num + len(line) - battery_count  + 1)
            for i in range(start, end):
                c = line[i]
                if c > largest_digit:
                    largest_digit = c
                    start = i+1
            num_str += largest_digit
        print(num_str)
        r += int(num_str)
    return r

def solve1(lines):
    return solve(lines, 2)

def solve2(lines):
    return solve(lines, 12)

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
    if p2 is not None:
        print("Solution 2:", p2)
