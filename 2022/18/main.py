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

Cube = namedtuple('Cube', 'x y z')

def add_cubes(a, b):
    return Cube(a.x + b.x, a.y + b.y, a.z + b.z)

def negative_cube(a):
    return Cube(-a.x, -a.y, -a.z)

def abs_cube(a):
    return Cube(abs(a.x), abs(a.y), abs(a.z))

def solve1(lines):
    r = 0
    cubes = []
    pockets = defaultdict(int)
    for line in lines:
        x, y, z = get_ints(line)
        coord = Cube(x, y, z)
        cubes.append(coord)
        r += 6
    for a in cubes:
        for b in cubes:
            dx, dy, dz = abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z)
            if sorted([dx, dy, dz]) == [0, 0, 1]:
                r -= 1
    return r

def solve2(lines):
    r = 0
    cubes_map = defaultdict(int)
    for line in lines:
        x, y, z = get_ints(line)
        coord = Cube(x, y, z)
        cubes_map[coord] = 1
    frontier = []
    for coord, cube in cubes_map.items():
        must_be_outside = True
        for x in range(1,20):
            new_coord = add_cubes(coord, Cube(x, 0, 0))
            if new_coord in cubes_map and cubes_map[new_coord] == 1:
                must_be_outside = False
                break
        if must_be_outside:
            frontier.append((coord, Cube(1, 0, 0)))
    visited = set()
    for item in frontier:
        dprint(item)
    while frontier:
        new_frontier = []
        for coord, side in frontier:
            if (coord, side) in visited:
                continue
            visited.add((coord, side))
            for spin in [Cube(1, 0, 0), Cube(0, 1, 0), Cube(0, 0, 1), Cube(-1, 0, 0), Cube(0, -1, 0), Cube(0, 0, -1)]:
                if abs_cube(spin) == abs_cube(side):
                    continue
                corner_coord = add_cubes(side, add_cubes(coord, spin))
                adj_coord = add_cubes(coord, spin)
                if cubes_map[corner_coord] == 1:
                    new_frontier.append((corner_coord, negative_cube(spin)))
                    dprint(f"Corner cube, following concave side from {(coord, side)} to {(adj_coord, side)}")
                elif cubes_map[adj_coord] == 1:
                    new_frontier.append((adj_coord, side))
                    dprint(f"Adj cube, sliding from {(coord, side)} to {(adj_coord, side)}")
                else:
                    new_frontier.append((coord, spin))
                    dprint(f"No adj, following convex side from {(coord, side)} to {(coord, spin)}")
        frontier = new_frontier
    return len(visited)

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
