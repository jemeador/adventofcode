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

def solve1(lines):
    r = 0
    g = make_ascii_grid(lines)
    gc = g.copy()

    good_cells = []
    for c in g:
        val = g[c]
        if val != '.' and not val.isdigit():
            for coord, symbol in get_king_items(g, c):
                good_cells.append(coord)
                gc[coord] = 'x'
    for y in range(len(lines)):
        line = lines[y]
        x = 0
        while x < len(line):
            coord = Coord(x, y)
            char = g[coord]
            if char.isdigit():
                num_str = ''
                part_num = coord in good_cells
                while char.isdigit():
                    num_str += char
                    coord = add_coords(coord, Coord(1, 0))
                    x += 1
                    if coord in g:
                        char = g[coord]
                        if char.isdigit() and coord in good_cells:
                            part_num = True
                    else:
                        break
                if part_num:
                    r += int(num_str)
                else:
                    print(num_str)
            else:
                x += 1
    print_grid(gc, lambda d: str(d))
    return r

def solve2(lines):
    r = 0
    g = make_ascii_grid(lines)
    gc = g.copy()

    gears_cells = []
    for c in g:
        val = g[c]
        if val == '*':
            cells = []
            for coord, symbol in get_king_items(g, c):
                cells.append(coord)
                gc[coord] = 'x'
            gears_cells.append(cells.copy())

    for gear_i in range(len(gears_cells)):
        gear_cells = gears_cells[gear_i]
        gear_values = []
        for y in range(len(lines)):
            line = lines[y]
            x = 0
            while x < len(line):
                coord = Coord(x, y)
                char = g[coord]
                if char.isdigit():
                    num_str = ''
                    part_num = coord in gear_cells
                    while char.isdigit():
                        num_str += char
                        coord = add_coords(coord, Coord(1, 0))
                        x += 1
                        if coord in g:
                            char = g[coord]
                            if char.isdigit() and coord in gear_cells:
                                part_num = True
                        else:
                            break
                    if part_num:
                        gear_values.append(int(num_str))
                else:
                    x += 1
        if len(gear_values) == 2:
            r += gear_values[0] * gear_values[1]
            print(gear_values[0], gear_values[1])
    print_grid(gc, lambda d: str(d))
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
