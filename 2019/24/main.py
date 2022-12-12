#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict

import time
import os
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

def calc_bio_score(g):
    score = 0
    for coord, cell in g.items():
        if cell == '#':
            score += pow(2, coord.x + coord.y * 5)
    return score


def solve1(lines):
    g = make_ascii_grid(lines)
    next_g = g.copy()
    scores = set()
    while True:
        score = calc_bio_score(g)
        if score in scores:
            return score
        scores.add(score)
        for coord, cell in g.items():
            bug_count = 0
            for adj_coord in get_adj_coords(coord):
                if adj_coord in g and g[adj_coord] == '#':
                    bug_count += 1
            if cell == '#' and bug_count != 1:
                next_g[coord] = '.'
            elif cell == '.' and 1 <= bug_count <= 2:
                next_g[coord] = '#'
            else:
                next_g[coord] = cell
        #time.sleep(1)
        #os.system('clear')
        #print_grid(g)
        next_g, g = g, next_g

def empty_grid():
    ret = defaultdict(int)
    for x in range(5):
        for y in range(5):
            ret[Coord(x,y)] = '.'
    ret[Coord(2,2)] = '?'
    return ret

def nested_adj_coords(level, coord):
    ret = []
    coord = Coord(x=coord[0], y=coord[1])

    # Up
    if coord.y == 0:
        ret.append((level-1, Coord(2, 1)))
    elif coord == Coord(2, 3):
        for x in range(5):
            ret.append((level+1, Coord(x, 4)))
    else:
        ret.append((level, add_coords(coord, Coord(0,-1))))

    # Left
    if coord.x == 0:
        ret.append((level-1, Coord(1, 2)))
    elif coord == Coord(3, 2):
        for y in range(5):
            ret.append((level+1, Coord(4, y)))
    else:
        ret.append((level, add_coords(coord, Coord(-1,0))))

    # Down
    if coord.y == 4:
        ret.append((level-1, Coord(2, 3)))
    elif coord == Coord(2, 1):
        for x in range(5):
            ret.append((level+1, Coord(x, 0)))
    else:
        ret.append((level, add_coords(coord, Coord(0,1))))

    # Right
    if coord.x == 4:
        ret.append((level-1, Coord(3, 2)))
    elif coord == Coord(1, 2):
        for y in range(5):
            ret.append((level+1, Coord(0, y)))
    else:
        ret.append((level, add_coords(coord, Coord(1,0))))

    return ret

def recur_step(level, layers, next_layers):
    g = layers[level]
    levels_to_recur = set()
    # If layers above or below this have any bugs at all, we must process them
    if level-1 in layers and level <= 0:
        #print(f"Processing {level-1} because it was processed before")
        levels_to_recur.add(level-1)
    if level+1 in layers and level >= 0:
        #print(f"Processing {level+1} because it was processed before")
        levels_to_recur.add(level+1)
    for coord, cell in g.items():
        if coord == Coord(2,2):
            continue
        #print(f"Level:{level} {coord}")
        bug_count = 0
        for adj_level, adj_coord in nested_adj_coords(level, coord):
            if level == 0 and coord == Coord(1, 0):
                if adj_level in layers and layers[adj_level][adj_coord] == '#':
                    print('Adj ', adj_level, adj_coord)
            #print(f"Adj: level:{adj_level} {adj_coord}")
            if cell == '#' and adj_level != level:
                if level <= 0 and adj_level < level or level >= 0 and adj_level > level:
                    #if adj_level not in levels_to_recur:
                        #print(f"Including {adj_level} in this cycle due to {level},{coord} having a bug")
                    # If a bug is adjacent to another level, we have to process the adjacent level
                    levels_to_recur.add(adj_level)
            if adj_level in layers and layers[adj_level][adj_coord] == '#':
                bug_count += 1
        if cell == '#' and bug_count != 1:
            next_layers[level][coord] = '.'
        elif cell == '.' and 1 <= bug_count <= 2:
            next_layers[level][coord] = '#'
        else:
            next_layers[level][coord] = cell
    for l in levels_to_recur:
        recur_step(l, layers, next_layers)

def solve2(lines):
    layers = defaultdict(empty_grid)
    layers[0] = make_ascii_grid(lines)
    for n in range(200):
        print("Minute:", n)
        next_layers = defaultdict(empty_grid)
        recur_step(0, layers, next_layers)
        next_layers, layers = layers, next_layers
        for level, layer in layers.items():
            print(level)
            print_grid(layer)
    ret = 0
    for level, layer in layers.items():
        ret += len(list(get_coords(layer, '#')))
    return ret

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
