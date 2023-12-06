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
    count2 = 0
    count3 = 0
    for line in lines:
        counted2 = False
        counted3 = False
        l = defaultdict(int)
        print(line)
        for c in line:
            l[c] += 1
        for key, a in l.items():
            if not counted2 and a == 2:
                count2 += 1
                print('2', line, key)
                counted2 = True
            if not counted3 and a == 3:
                count3 += 1
                print('3', line, key)
                counted3 = True
    print(count2, count3)
    return count2*count3

def solve2(lines):
    r = 0
    for line in lines:
        for line2 in lines:
            count = 0
            pos = 0
            for i in range(len(line)):
                if line[i] != line2[i]:
                    count += 1
                    pos = i
            if count == 1:
                print(line)
                print(line2)
                return ''
    return ''

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
