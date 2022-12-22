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
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    r = 0
    nums = []
    indices = list(range(len(lines)))
    print(indices)
    for i in range(len(lines)):
        line = lines[i]
        val = int(line)
        old_index = indices.index(i)
        new_index = (old_index + val)
        while new_index >= len(lines):
            new_index += 1 - len(lines)
        while new_index < 1:
            new_index += len(lines) - 1
        indices.insert(new_index, indices.pop(old_index))
        dprint(old_index, new_index)
        for index in indices:
            dprint(int(lines[index]), end =', ')
        dprint()
    for index in indices:
        nums.append(int(lines[index]))
    zero_index = nums.index(0)
    return nums[(zero_index + 1000) % len(lines)] + nums[(zero_index + 2000) % len(lines)] + nums[(zero_index + 3000) % len(lines)]

def solve2(lines):
    r = 0
    nums = []
    indices = list(range(len(lines)))
    print(indices)
    for _ in range(10):
        for i in range(len(lines)):
            line = lines[i]
            val = int(line) * 811589153
            old_index = indices.index(i)
            new_index = (old_index + val)
            if new_index > 0:
                new_index %= (len(lines) - 1)
            if new_index < 0:
                new_index = int(math.copysign(abs(new_index) % (len(lines) - 1), new_index))
            indices.insert(new_index, indices.pop(old_index))
            dprint(old_index, new_index)
            for index in indices:
                dprint(int(lines[index]), end =', ')
            dprint()
    for index in indices:
        nums.append(int(lines[index]) * 811589153)
    zero_index = nums.index(0)
    return nums[(zero_index + 1000) % len(lines)] + nums[(zero_index + 2000) % len(lines)] + nums[(zero_index + 3000) % len(lines)]

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
