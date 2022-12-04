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
    count = 0
    for line in lines:
        elf1, elf2 = line.split(',')
        i, j = [int(x) for x in elf1.split('-')]
        k, l = [int(x) for x in elf2.split('-')]

        a = range(i, j+1)
        b = range(k, l+1)

        both = set()
        for i in a:
            both.add(i)
        for i in b:
            both.add(i)
        if len(both) == len(a) or len(both) == len(b):
            count+=1

    return count

def solve2(lines):
    count = 0
    for line in lines:
        elf1, elf2 = line.split(',')
        i, j = [int(x) for x in elf1.split('-')]
        k, l = [int(x) for x in elf2.split('-')]

        a = range(i, j+1)
        b = range(k, l+1)

        both = set()
        for i in a:
            both.add(i)
        for i in b:
            both.add(i)
        if len(both) < len(a) + len(b):
            count+=1
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
