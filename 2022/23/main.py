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

dirs = [Coord(0, -1), Coord(0, 1), Coord(-1, 0), Coord(1, 0)]

def solve(lines, level):
    r = 0
    grid = make_ascii_grid(lines)
    print_grid(grid, lambda x: '.' if x != '#' else '#')
    print()
    i = 0
    while (level == 1 and i < 10) or level == 2:
        proposals = defaultdict(set)
        for coord in get_coords(grid, '#'):
            need_to_move = False
            for adj_coord in get_king_coords(coord):
                if adj_coord in grid and grid[adj_coord] == '#':
                    need_to_move = True
                    break
            if not need_to_move:
                continue
            for d in range(len(dirs)):
                direction = dirs[(d+i) % len(dirs)]
                proposed_move = add_coords(coord, direction)
                clear = True
                for scan_adjust in [0, -1, 1]:
                    scan_coord = proposed_move
                    if direction.x == 0: # North or south
                        scan_coord = add_coords(scan_coord, Coord(scan_adjust, 0))
                    else: # East or west
                        scan_coord = add_coords(scan_coord, Coord(0, scan_adjust))
                    if scan_coord in grid and grid[scan_coord] == '#':
                        clear = False
                if clear:
                    proposals[proposed_move].add(coord)
                    break
        if len(proposals) == 0:
            return i + 1
        for dest, srcs in proposals.items():
            if len(srcs) == 1:
                src = next(iter(srcs))
                grid[src], grid[dest] = grid[dest], grid[src]
        print_grid(grid, lambda x: '.' if x != '#' else '#')
        print()
        i += 1

    erase_me = set()
    for coord, cell in grid.items():
        if cell != '#':
            erase_me.add(coord)
    for coord in erase_me:
        del grid[coord]
    print_grid(grid, lambda x: '.' if x != '#' else '#')
    print()
    min_x = grid_min_x(grid)
    max_x = grid_max_x(grid)
    min_y = grid_min_y(grid)
    max_y = grid_max_y(grid)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    r = width * height - len(list(get_coords(grid, '#')))
    return r

def solve1(lines):
    return solve(lines, 1)

def solve2(lines):
    return solve(lines, 2)

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
