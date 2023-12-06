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
    max_x = 1001
    max_y = 1001
    cells = [0] * (max_x * max_y)
    print(len(cells))
    for line in lines:
        claim_id, rect = line.split('@')
        claim_id = claim_id[1:]
        coord, size = rect.split(':')
        x, y = coord.split(',')
        width, height = size.split('x')
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        for i in range(x,x+width):
            for j in range(y,y+height):
                n = i + j*1000
                cells[n] += 1
    count = 0
    for n in range(max_x * max_y):
        if cells[n] > 1:
            count += 1
    return count

def solve2(lines):
    max_x = 1001
    max_y = 1001
    cells = [0] * (max_x * max_y)
    print(len(cells))
    for line in lines:
        claim_id, rect = line.split('@')
        claim_id = claim_id[1:]
        coord, size = rect.split(':')
        x, y = coord.split(',')
        width, height = size.split('x')
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        for i in range(x,x+width):
            for j in range(y,y+height):
                n = i + j*1000
                cells[n] += 1
    for line in lines:
        claim_id, rect = line.split('@')
        claim_id = claim_id[1:]
        coord, size = rect.split(':')
        x, y = coord.split(',')
        width, height = size.split('x')
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        clean = True
        for i in range(x,x+width):
            for j in range(y,y+height):
                print(x, y, cells[n])
                if cells[n] > 1:
                    clean = False
        if clean:
            return claim_id
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
