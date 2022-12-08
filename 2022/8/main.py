#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict

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

def solve1(lines):
    count = 0
    g = make_ascii_grid(lines)
    h = make_ascii_grid(lines)
    print_grid(g)
    for coord, cell in g.items():
        tree = int(g[coord])
        visible = False
        for offset in adj_offsets:
            from_tree_coord = add_coords(coord, offset)
            if from_tree_coord not in g:
                visible = True
            while not visible:
                next_tree = int(g[from_tree_coord])
                if next_tree >= tree:
                    break
                from_tree_coord = add_coords(from_tree_coord, offset)
                if from_tree_coord not in g:
                    visible = True
            if visible:
                break
        if visible:
            h[coord] = '.'
            count += 1
    print_grid(h)
    return count

def solve2(lines):
    count = 0
    g = make_ascii_grid(lines)
    print_grid(g)
    best = 0
    for coord, cell in g.items():
        tree = int(g[coord])
        score = 1
        for offset in adj_offsets:
            visible_trees = 0
            from_tree_coord = add_coords(coord, offset)
            while from_tree_coord in g:
                visible_trees += 1
                next_tree = int(g[from_tree_coord])
                if next_tree >= tree:
                    break
                from_tree_coord = add_coords(from_tree_coord, offset)
            score *= visible_trees
        best = max(score, best)
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
