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

def row_empty(grid, y):
    for i in range(grid_max_x(grid)+1):
        if grid[Coord(i, y)] != '.':
            return 0
    return 1
def col_empty(grid, x):
    for i in range(grid_max_y(grid)+1):
        if grid[Coord(x, i)] != '.':
            return 0
    return 1

def solve1(lines, expansion=1):
    r = 0
    grid = make_ascii_grid(lines)
    #graph = build_graph_from_ascii_grid(grid,
    #        is_node=lambda coord, cell: cell == '#' or cell == '.',
    #        is_passable=lambda coord, cell: cell == '#' or cell == '.',
    #        adjacency=adj_offsets,
    #        make_key=lambda coord, cell: coord,
    #        cost_func=lambda coord, cell: 1 + row_empty(grid, coord) + col_empty(grid, coord))
    print_grid(grid)
    pairs = {}
    galaxies = list(get_coords(grid, '#'))
    empty_rows = []
    empty_cols = []
    for x in range(len(lines)):
        if row_empty(grid, x):
            empty_rows.append(x)
    for y in range(len(lines[0])):
        if col_empty(grid, y):
            empty_cols.append(y)
    print(empty_rows, empty_cols)
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            src = galaxies[i]
            dest = galaxies[j]
            dist = manhatten(src, dest)
            minx = min(src.x,dest.x)
            miny = min(src.y,dest.y)
            maxx = max(src.x,dest.x)
            maxy = max(src.y,dest.y)
            print(i+1, j+1, "dist", dist)
            for x in range(minx+1, maxx):
                if x in empty_cols:
                    print("empty col", x)
                    dist += expansion
            for y in range(miny+1, maxy):
                if y in empty_rows:
                    print("empty row", y)
                    dist += expansion
            print(i+1, j+1, "dist", dist)
            pairs[(src,dest)] = dist
            r += dist
    print(len(pairs))
    return r

def solve2(lines):
    return solve1(lines, expansion=999999)

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
