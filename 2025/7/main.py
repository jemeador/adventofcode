#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import *
from py_utils.search import *

from collections import defaultdict

import functools
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

def solve1(lines):
    r = 0
    grid = make_ascii_grid(lines)
    start = get_unique_pos(grid, 'S')
    beams = set()
    beams.add(start.x)
    for y in range(start.y + 1, grid_max_y(grid) + 1):
        next_beams = set()
        for beam in beams:
            next_coord = Coord(beam, y)
            if grid[next_coord] == '^':
                next_beams.add(beam - 1)
                next_beams.add(beam + 1)
                grid[Coord(beam-1, y)] = '|'
                grid[Coord(beam+1, y)] = '|'
                r += 1
            else:
                next_beams.add(beam)
                grid[next_coord] = '|'
        beams = next_beams
        print_grid(grid)
    return r

grid = None

@functools.cache
def solve2(start=None):
    y = start.y + 1
    if y > grid_max_y(grid):
        return 1
    next_coord = Coord(start.x, y)
    if grid[next_coord] == '^':
        return solve2(Coord(start.x-1, y)) + solve2(Coord(start.x+1, y))
    return solve2(Coord(start.x, y))

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1 = solve1(lines)
    grid = make_ascii_grid(lines)
    start = get_unique_pos(grid, 'S')
    p2 = solve2(start)
    if p1 is not None:
        print("Solution 1:", p1)
    if p2 is not None:
        print("Solution 2:", p2)
