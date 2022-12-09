#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict

import os
import fileinput
import itertools
import pyperclip
import queue
import re
import math
import time

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

offsets = {}
offsets['R'] = (1, 0)
offsets['L'] = (-1, 0)
offsets['U'] = (0, -1)
offsets['D'] = (0, 1)

def solve1(lines):
    tail_positions = set()
    head = (0, 0)
    tail = (0, 0)
    tail_positions.add(tail)
    for line in lines:
        o, n = line.split(' ')
        offset = offsets[o]
        dist = int(n)
        for i in range(dist):
            head = add_coords(head, offset)
            diff = sub_coords(head, tail)
            if abs(diff[0]) > 1 or abs(diff[1]) > 1:
                if diff[0] == 0:
                    diff = (diff[0], diff[1] // 2)
                elif diff[1] == 0:
                    diff = (diff[0] // 2, diff[1])
                else:
                    diff = (int(math.copysign(1, diff[0])), int(math.copysign(1, diff[1])))
                tail = add_coords(tail, diff)
                tail_positions.add(tail)
            assert(abs(diff[0])<=1 or abs(diff[1]) <= 1)
            #grid = defaultdict(lambda: '.')
            #grid[-10, -10] = '.'
            #grid[10, 10] = '.'
            #grid[tail] = 'T'
            #grid[head] = 'H'
            #grid[(0,0)] = 's'
            #os.system('clear')
            #print_grid(grid, str)
    return len(tail_positions)

def solve2(lines):
    tail_positions = set()
    knots = []
    for i in range(10):
        knots.append((0,0))
    tail_positions.add((0,0))
    for line in lines:
        o, n = line.split(' ')
        offset = offsets[o]
        dist = int(n)
        for i in range(dist):
            knots[0] = add_coords(knots[0], offset)
            grid = defaultdict(lambda: '.')
            grid[(0,0)] = 's'
            grid[-10, -10] = '.'
            grid[10, 10] = '.'
            grid[knots[0]] = 'H'
            for j in range(len(knots) - 1):
                head = knots[j]
                tail = knots[j+1]
                diff = sub_coords(head, tail)
                if abs(diff[0]) > 1 or abs(diff[1]) > 1:
                    if diff[0] == 0:
                        diff = (diff[0], diff[1] // 2)
                    elif diff[1] == 0:
                        diff = (diff[0] // 2, diff[1])
                    else:
                        diff = (int(math.copysign(1, diff[0])), int(math.copysign(1, diff[1])))
                    knots[j+1] = add_coords(tail, diff)
            for k in range(1,len(knots)):
                grid[knots[k]] = str(k)
            tail_positions.add(knots[9])
            #os.system('clear')
            #print_grid(grid, str)
            #time.sleep(0.1)
    return len(tail_positions)

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
