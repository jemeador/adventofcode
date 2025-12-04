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
    debug_grid = make_ascii_grid(lines)
    for coord in grid:
        if grid[coord] != '@':
            continue
        count = 0
        for adj_coord, value in get_items_with_offsets(grid, coord, king_offsets):
            if value == '@':
                count += 1
        if count < 4:
            debug_grid[coord] = 'x'
            r += 1
    print_grid(debug_grid)
    return r

def solve2(lines):
    total_removed = 0
    removed = None
    grid = make_ascii_grid(lines)
    new_grid = make_ascii_grid(lines)
    while removed != 0:
        removed = 0
        for coord in grid:
            if grid[coord] != '@':
                continue
            count = 0
            for adj_coord, value in get_items_with_offsets(grid, coord, king_offsets):
                if value == '@':
                    count += 1
            if count < 4:
                new_grid[coord] = '.'
                removed += 1
        grid = new_grid
        total_removed += removed
        print_grid(grid)
    return total_removed

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
    if p2 is not None:
        print("Solution 2:", p2)
