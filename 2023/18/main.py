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

def clockwise(triangle):
    p1, p2, p3 = triangle
    side_sum = 0
    side_sum += (p2.x - p1.x)*(p2.y + p1.y)
    side_sum += (p3.x - p2.x)*(p3.y + p2.y)
    side_sum += (p1.x - p3.x)*(p1.y + p3.y)
    return side_sum < 0

def solve(polygon):
    r = 0
    offset_i = 0
    offsets = [Coord(0,0), Coord(1,0), Coord(1,1), Coord(0,1)]
    is_clockwise = True
    for i in range(0, len(polygon)-2):
        p1 = polygon[i]
        p2 = polygon[(i+1) % len(polygon)]
        p3 = polygon[(i+2) % len(polygon)]
        prev_is_clockwise = is_clockwise
        is_clockwise = clockwise([p1,p2,p3])
        if is_clockwise and prev_is_clockwise:
            offset_i += 1
        elif not is_clockwise and not prev_is_clockwise:
            offset_i += 3
        offset_i %= 4
        polygon[(i+1) % len(polygon)] = add_coords(polygon[(i+1) % len(polygon)], offsets[offset_i])
    i = 0
    while len(polygon) > 2:
        p1 = polygon[i]
        p2 = polygon[(i+1) % len(polygon)]
        p3 = polygon[(i+2) % len(polygon)]
        a_vector = sub_coords(p2, p1)
        b_vector = sub_coords(p3, p2)
        c_vector = sub_coords(p1, p3)
        a = math.sqrt(pow(a_vector.x, 2) + pow(a_vector.y, 2))
        b = math.sqrt(pow(b_vector.x, 2) + pow(b_vector.y, 2))
        c = math.sqrt(pow(c_vector.x, 2) + pow(c_vector.y, 2))
        s = (a + b + c) / 2
        is_clockwise = clockwise([p1,p2,p3])
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        print(area)
        if is_clockwise:
            r += area
        else:
            r -= area
        del polygon[(i+1) % len(polygon)]
        i+=2
        i%=len(polygon)
    return round(r)


def solve1(lines):
    r = 0
    coord = Coord(0,0)
    grid_dict = defaultdict(str)
    grid_dict[coord] = '#'
    for line in lines:
        dir_ch, dist_str, color = line.split()
        if dir_ch == 'R':
            direction = Coord(1,0)
        elif dir_ch == 'L':
            direction = Coord(-1,0)
        elif dir_ch == 'U':
            direction = Coord(0,-1)
        elif dir_ch == 'D':
            direction = Coord(0,1)
        distance = int(dist_str)
        for i in range(distance):
            coord = add_coords(coord, direction)
            grid_dict[coord] = '#'

    frontier = []
    frontier.append(Coord(1,1))
    while len(frontier) > 0:
        coord = frontier.pop()
        if grid_dict[coord] == '':
            grid_dict[coord] = '#'
            for offset in adj_offsets:
                frontier.append(add_coords(coord, offset))
    #print_grid(grid_dict, lambda c: '.' if c == '' else c)

    return len(list(get_coords(grid_dict, '#')))

def solve2(lines):
    r = 0
    coords = [Coord(0,0)]
    for line in lines:
        _, _, hexcode = line.split()
        hexcode = hexcode[2:-1]
        distance = int(hexcode[:-1], 16)
        dir_ch = hexcode[-1]
        if dir_ch == '0':
            direction = Coord(1,0)
        elif dir_ch == '1':
            direction = Coord(0,1)
        elif dir_ch == '2':
            direction = Coord(-1,0)
        elif dir_ch == '3':
            direction = Coord(0,-1)
        new_coord = add_coords(coords[-1], mult_coord(direction, distance))
        coords.append(new_coord)
    print(coords)
    return solve(coords)

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1 = solve1(lines)
    print()
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
