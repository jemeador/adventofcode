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

def add_range(ranges, a):
    for b in ranges:
        if min(a[1] + 1, b[1] + 1) >= max(a[0], b[0]):
            ranges.remove(b)
            b = (min(a[0], b[0]), max(a[1], b[1]))
            add_range(ranges, b)
            return
    ranges.append(a)

def solve1(lines):
    r = 0
    loi = 2000000
    ranges = []
    beacons = set()
    for line in lines:
        sx, sy, bx, by = get_ints(line)
        s = Coord(sx, sy)
        b = Coord(bx, by)
        max_dist = manhatten(s, b)
        dx = max_dist - abs(sy - loi)
        if dx > 0:
            x0 = sx - dx
            x1 = sx + dx
            add_range(ranges, (x0, x1))
        beacons.add(b)
    for beacon in beacons:
        if b.y == loi:
            r -= 1
    for ra in ranges:
        r += ra[1] - ra[0]
    return r

def find_gap(ranges, loi):
    a = (0, 4000000)
    for b in ranges:
        if a[0] >= b[0] and a[1] <= b[1]:
            return None
    return (1 + min([b[1] for b in ranges if b[1] >= 0 and b[1] <= 4000000]), loi)

def solve2(lines):
    ranges_by_y = defaultdict(list)
    beacons = set()
    for line in lines:
        print(line)
        sx, sy, bx, by = get_ints(line)
        s = Coord(sx, sy)
        b = Coord(bx, by)
        max_dist = manhatten(s, b)
        for loi in range(4000000):
            dx = max_dist - abs(sy - loi)
            if dx > 0:
                x0 = sx - dx
                x1 = sx + dx
                add_range(ranges_by_y[loi], (x0, x1))
        beacons.add(b)
    for loi in range(4000000):
        gap = find_gap(ranges_by_y[loi], loi)
        if gap:
            return gap[0] * 4000000 + gap[1]

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
