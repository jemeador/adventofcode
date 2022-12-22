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

def pixel(cell):
    if cell == 0:
        return '.'
    if cell == 1:
        return '#'
    if cell == 2:
        return 'o'
    if cell == 3:
        return '+'

def sim_sand(grid):
    count = 0
    spawn = get_unique_pos(grid, 3)
    max_y = grid_max_y(grid)
    print('Spawn:', spawn)
    while True:
        coord = spawn
        while True:
            if grid[coord] == 2:
                return count
            if coord.y == max_y + 1:
                break
            elif grid[add_coords(coord, Coord(0, 1))] == 0:
                coord = add_coords(coord, Coord(0, 1))
            elif grid[add_coords(coord, Coord(-1, 1))] == 0:
                coord = add_coords(coord, Coord(-1, 1))
            elif grid[add_coords(coord, Coord(1, 1))] == 0:
                coord = add_coords(coord, Coord(1, 1))
            else:
                break
        grid[coord] = 2
        count += 1
    return -1

def solve1(lines):
    r = 0
    grid = defaultdict(int)
    grid[Coord(500, 0)] = 3
    for line in lines:
        coords = line.split(' -> ')
        prev_coord = None
        for c in coords:
            x, y = c.split(',')
            coord = Coord(int(x),int(y))
            grid[coord] = 1
            if prev_coord:
                if prev_coord.x == coord.x:
                    for yi in range(0, coord.y - prev_coord.y, int(math.copysign(1, coord.y - prev_coord.y))):
                        iter_coord = add_coords(prev_coord, Coord(0, yi))
                        grid[iter_coord] = 1
                elif prev_coord.y == coord.y:
                    for xi in range(0, coord.x - prev_coord.x, int(math.copysign(1, coord.x - prev_coord.x))):
                        iter_coord = add_coords(prev_coord, Coord(xi, 0))
                        grid[iter_coord] = 1
            prev_coord = coord
    print_grid(grid, pixel)
    r = sim_sand(grid)
    print_grid(grid, pixel)
    return r

def solve2(lines):
    pass

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
