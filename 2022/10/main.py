#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid
from py_utils.fast_parse import get_ints, get_uints

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
    strength = 0
    cycle = 0
    register = 1
    next_cycle = 20
    for line in lines:
        if line.startswith('addx'):
            cycle += 2
        else:
            cycle += 1
        if cycle >= next_cycle:
            print(next_cycle, register, register * next_cycle)
            strength += next_cycle * register
            next_cycle += 40
        if line.startswith('addx'):
            num, = get_ints(line)
            register += int(num)
            print('reg', register)
    return strength

def draw(g, register, cycle):
    x = cycle % 40
    y = cycle // 40
    if x-1 <= register <= x+1:
        g[x,y] = '#'
    else:
        g[x,y] = '.'

def solve2(lines):
    strength = 0
    cycle = 0
    register = 1
    next_cycle = 20
    g = defaultdict(int)
    for line in lines:
        if line.startswith('addx'):
            draw(g, register, cycle)
            cycle += 1
            draw(g, register, cycle)
            cycle += 1
        else:
            draw(g, register, cycle)
            cycle += 1
        if line.startswith('addx'):
            num, = get_ints(line)
            register += int(num)
    print_grid(g)
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
