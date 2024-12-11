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

    xmax = grid_max_x(g)
    ymax = grid_max_y(g)

    for y in range(ymax):
        for x in range(xmax):
            coord = Coord(x,y)
            cell = g[coord]
            if cell == 'O':
                swap_coord = coord
                next_coord = add_coords(swap_coord, Coord(0,-1))
                while next_coord in g and g[next_coord] == '.':
                    swap_coord = next_coord
                    next_coord = add_coords(swap_coord, Coord(0,-1))
                g[coord] = '.'
                g[swap_coord] = 'O'
    print()
    print_grid(g)
    print()
    print()
    print()
    for coord, cell in g.items():
        if cell == 'O':
            r += len(lines) - coord.y
    return r

def solve2(lines):
    r = 0
    g = make_ascii_grid(lines)
    print_grid(g)
    print()

    xmax = grid_max_x(g)
    ymax = grid_max_y(g)


    for i in range(500):
        offset = Coord(0,-1)
        for y in range(ymax+1):
            for x in range(xmax+1):
                coord = Coord(x,y)
                cell = g[coord]
                if cell == 'O':
                    swap_coord = coord
                    next_coord = add_coords(swap_coord, offset)
                    while next_coord in g and g[next_coord] == '.':
                        swap_coord = next_coord
                        next_coord = add_coords(swap_coord, offset)
                    g[coord] = '.'
                    g[swap_coord] = 'O'
        offset = Coord(-1,0)
        for x in range(xmax+1):
            for y in range(ymax+1):
                coord = Coord(x,y)
                cell = g[coord]
                if cell == 'O':
                    swap_coord = coord
                    next_coord = add_coords(swap_coord, offset)
                    while next_coord in g and g[next_coord] == '.':
                        swap_coord = next_coord
                        next_coord = add_coords(swap_coord, offset)
                    g[coord] = '.'
                    g[swap_coord] = 'O'
        offset = Coord(0,1)
        for y in range(ymax, -1, -1):
            for x in range(xmax+1):
                coord = Coord(x,y)
                cell = g[coord]
                if cell == 'O':
                    swap_coord = coord
                    next_coord = add_coords(swap_coord, offset)
                    while next_coord in g and g[next_coord] == '.':
                        swap_coord = next_coord
                        next_coord = add_coords(swap_coord, offset)
                    g[coord] = '.'
                    g[swap_coord] = 'O'
        offset = Coord(1,0)
        for x in range(xmax, -1, -1):
            for y in range(ymax+1):
                coord = Coord(x,y)
                cell = g[coord]
                if cell == 'O':
                    swap_coord = coord
                    next_coord = add_coords(swap_coord, offset)
                    while next_coord in g and g[next_coord] == '.':
                        swap_coord = next_coord
                        next_coord = add_coords(swap_coord, offset)
                    g[coord] = '.'
                    g[swap_coord] = 'O'
        for coord, cell in g.items():
            if cell == 'O':
                r += len(lines) - coord.y
        #print()
        #print_grid(g)
        print(i, r)
        r = 0
        # solved by analyzing output and finding any iteration in the cycle that has the same modulo
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
