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
    r = 0
    mapping = {}
    seeds = []
    next_seeds = []
    for line in lines:
        if line == '':
            mapping = {}
            seeds = next_seeds.copy()
        elif line.startswith('seeds:'):
            _, nums_str = line.split(':')
            next_seeds = [int(v) for v in nums_str.strip().split(' ')]
        elif line[0].isdigit():
            dest, src, size = [int(v) for v in line.split(' ')]
            for i in range(len(seeds)):
                current_val = seeds[i]
                if current_val >= src and current_val < src + size:
                    next_seeds[i] = current_val - src + dest
                    if i == 1:
                        print(next_seeds[i], seeds[i])
    print(next_seeds)
    return min(next_seeds)

def solve2(lines):
    mapping_groups = []
    mapping_group = []
    for line in lines:
        if line == '':
            if len(mapping_group) > 0:
                mapping_groups.append(mapping_group)
            mapping_group = []
        elif line.startswith('seeds:'):
            _, nums_str = line.split(':')
            seed_ranges = [int(v) for v in nums_str.strip().split(' ')]
        elif line[0].isdigit():
            dest, src, size = [int(v) for v in line.split(' ')]
            mapping = (dest, src, size)
            mapping_group.append(mapping)
    mapping_groups.append(mapping_group)
    mapping_groups.reverse()
    for i in range(0, 999999999):
        val = i
        if i % 1000000 == 0:
            print(i)
        for mapping_group in mapping_groups:
            for mapping in mapping_group:
                dest, src, size = mapping
                if val >= dest and val < dest + size:
                    val = val - dest + src
                    break
        if (val >= seed_ranges[0] and val < seed_ranges[0] + seed_ranges[1]) or (val >= seed_ranges[2] and val < seed_ranges[2] + seed_ranges[3]):
            return i
    return 0

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1 = solve1(lines)
    print("")
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)

# 4 . . . . .
# 1 . . . . 4
# 5 . . . 1 4
# . . 5 . 1 4
# 1 4 5 . . 6
# 1 2 3 4 5 6
