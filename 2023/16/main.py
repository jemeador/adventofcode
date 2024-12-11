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

def solve1(lines, start = None):
    grid_dict = make_ascii_grid(lines)
    r = 0
    print_grid(grid_dict, lambda c: c)
    coverage = grid_dict.copy()

    frontier = set()
    visited_splitters = set()
    if start == None:
        frontier.add((Coord(-1,0),Coord(1,0)))
    else:
        frontier.add(start)

    while len(frontier) > 0:
        coord, direction = frontier.pop()
        next_coord = add_coords(coord, direction)
        if next_coord not in grid_dict or next_coord in visited_splitters:
            continue
        coverage[next_coord] ='X'
        cell = grid_dict[next_coord]
        if cell == '.':
            frontier.add((next_coord, direction))
        elif cell == '|':
            if direction.y == 0:
                visited_splitters.add(next_coord)
                frontier.add((next_coord, Coord(0,-1)))
                frontier.add((next_coord, Coord(0,1)))
            else:
                frontier.add((next_coord, direction))
        elif cell == '-':
            if direction.x == 0:
                visited_splitters.add(next_coord)
                frontier.add((next_coord, Coord(-1,0)))
                frontier.add((next_coord, Coord(1,0)))
            else:
                frontier.add((next_coord, direction))
        elif cell == '/':
            if direction == Coord(1, 0):
                frontier.add((next_coord, Coord(0,-1)))
            elif direction == Coord(0, -1):
                frontier.add((next_coord, Coord(1,0)))
            elif direction == Coord(-1, 0):
                frontier.add((next_coord, Coord(0,1)))
            elif direction == Coord(0, 1):
                frontier.add((next_coord, Coord(-1,0)))
        elif cell == '\\':
            if direction == Coord(1, 0):
                frontier.add((next_coord, Coord(0,1)))
            elif direction == Coord(0, -1):
                frontier.add((next_coord, Coord(-1,0)))
            elif direction == Coord(-1, 0):
                frontier.add((next_coord, Coord(0,-1)))
            elif direction == Coord(0, 1):
                frontier.add((next_coord, Coord(1,0)))
    #print_grid(coverage, lambda c: c)
    for coord, cell in coverage.items():
        if cell == 'X':
            r += 1
    return r

def solve2(lines):
    r = 0
    for i in range(len(lines[0])):
        r = max(r, solve1(lines, (Coord(i, -1), Coord(0,1))))
        r = max(r, solve1(lines, (Coord(i, len(lines)), Coord(0,-1))))
    for i in range(len(lines)):
        r = max(r, solve1(lines, (Coord(-1, i), Coord(1,0))))
        r = max(r, solve1(lines, (Coord(len(lines), i), Coord(-1,0))))
    return r

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
