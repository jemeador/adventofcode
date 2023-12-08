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
    count = 0
    g= defaultdict(list)
    instructions = lines[0]
    for line in lines[2:]:
        src, dests = line.split('=')
        src = src.strip()
        l, r = dests[2:-1].split(', ')
        g[src].append(l)
        g[src].append(r)
    node = 'AAA'
    while True:
        direction = instructions[count%len(instructions)]
        if direction == 'L':
            node = g[node][0]
        if direction == 'R':
            node = g[node][1]
        count += 1
        if node == 'ZZZ':
            return count
    return 0

def solve2(lines):
    count = 0
    g= defaultdict(list)
    instructions = lines[0]
    starts = []
    nodes = []
    seen = defaultdict(list)
    offsets = []
    cycles = []
    for line in lines[2:]:
        src, dests = line.split('=')
        src = src.strip()
        l, r = dests[2:-1].split(', ')
        g[src].append(l)
        g[src].append(r)
        if src.endswith('A'):
            starts.append(src)
            nodes.append(src)
            offsets.append(0)
            cycles.append(0)
    done = False
    cycle_count = 0
    print(len(instructions))
    while True:
        ii = count%len(instructions)
        for i in range(len(nodes)):
            node = nodes[i]
            direction = instructions[ii]
            if direction == 'L':
                nodes[i] = g[node][0]
            if direction == 'R':
                nodes[i] = g[node][1]
            if nodes[i].endswith('Z'):
                print(cycle_count, i, starts[i], nodes[i])
                cycles[i] = cycle_count
            if cycles.count(0) == 0:
                print(cycles)
                solution = len(instructions)
                for j in cycles:
                    solution *= j
                return solution
        count +=1
        if ii == 0:
            cycle_count += 1
    return 0

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
