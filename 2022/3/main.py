#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid

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
    p = 0
    for line in lines:
        l = int(len(line) / 2)
        first = line[:l]
        second = line[l:]
        for c in first:
            if c in second:
                v = ord(c)
                if v in range(ord('A'), ord('Z') + 1):
                    v -= ord('A')
                    v += 27
                else:
                    v -= ord('a')
                    v += 1
                print(v)
                p += v
                break
                #print(v + 1)
    return p

def solve2(lines):
    p = 0
    g = 0
    for i in range(0, len(lines), 3):
        group = lines[i:i+3]
        for c in group[0]:
            if c in group[1] and c in group[2]:
                v = ord(c)
                if v in range(ord('A'), ord('Z') + 1):
                    v -= ord('A')
                    v += 27
                else:
                    v -= ord('a')
                    v += 1
                print(v)
                p += v
                break
    return p

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
