#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import get_ints, get_uints
from py_utils.search import *

from collections import defaultdict

import math
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

class MountainGraph:
    def __init__(self, grid):
        self.grid = grid
    def edges_from(self, src):
        coord = src
        cell = self.grid[coord]
        if cell == 'S':
            cell = 'a'
        height = ord(cell)
        for adj_coord in get_adj_coords(coord):
            if adj_coord in self.grid:
                adj_cell = self.grid[adj_coord]
                if adj_cell == 'E':
                    adj_cell = 'z'
                adj_height = ord(adj_cell)
                if adj_height <= height + 1:
                    yield adj_coord, 1

def solve1(lines):
    grid = make_ascii_grid(lines)
    print_grid(grid)
    cost, path = find_path(MountainGraph(grid), get_unique_pos(grid, 'S'), get_unique_pos(grid, 'E'))
    debug = grid.copy()
    for coord in path:
        debug[coord] = '.'
    print_grid(debug, str)
    return cost

def solve2(lines):
    grid = make_ascii_grid(lines)
    print_grid(grid)
    best = math.inf
    for coord in get_coords(grid, 'a'):
        cost, path = find_path(MountainGraph(grid), coord, get_unique_pos(grid, 'E'))
        if cost < best:
            best = cost
            debug = grid.copy()
            for coord in path:
                debug[coord] = '.'
            print_grid(debug, str)
    return best

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
