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
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def size(rect):
    x1, y1, x2, y2 = rect
    return (1 + abs(x2 - x1)) * (1 + abs(y2 - y1))

def solve1(lines):
    r = 0
    tiles = []
    for line in lines:
        x, y = map(int, line.split(','))
        tiles.append((x, y))
    max_rect = 0
    for x1, y1 in tiles:
        for x2, y2 in tiles:
            max_rect = max(max_rect, (1 + abs(x2 - x1)) * (1 + abs(y2 - y1)))
    return max_rect

def solve2(lines):
    r = 0
    tiles = []
    for line in lines:
        x, y = map(int, line.split(','))
        tiles.append((x, y))
    rectangles = set()
    for x1, y1 in tiles:
        for x2, y2 in tiles:
            rectangles.add((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
    sorted_rectangles = sorted(rectangles, key=size, reverse=True)
    for rectangle in sorted_rectangles:
        dprint(rectangle)

    for rectangle in sorted_rectangles:
        x1, y1, x2, y2 = rectangle
        invalid = False
        for i in range(0, len(tiles)):
            sx, sy = tiles[i]
            if i + 1 < len(tiles):
                ex, ey = tiles[i+1]
            else:
                ex, ey = tiles[0]
            dprint("Checking rectangle ", rectangle, " of size ", size(rectangle), " against ", (sx, sy), (ex, ey))
            start_left = sx <= x1
            start_right = x2 <= ex
            end_left = ex <= x1
            end_right = x2 <= ex
            start_x_center = x1 < sx < x2
            start_y_center = y1 < sy < y2
            end_x_center = x1 < ex < x2
            end_y_center = y1 < ey < y2
            start_up = sy <= y1
            start_down = y2 <= sy
            end_up = ey <= y1
            end_down = y2 <= ey

            if (start_x_center and start_y_center):
                dprint("Invalid due to start inside")
                invalid = True
                break
            if (end_x_center and end_y_center):
                dprint("Invalid due to end inside")
                invalid = True
                break
            if start_x_center and (start_up != end_up or start_down != end_down):
                dprint("Invalid due to vertical edge crossint a line")
                invalid = True
                break
            if start_y_center and (start_left != end_left or start_right != end_right):
                dprint("Invalid due to horizontal edge crossing a line")
                invalid = True
                break

        if not invalid:
            return size(rectangle)
    return 0

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
