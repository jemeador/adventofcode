#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid, get_adj_items, add_coords
from py_utils.int_code import IntCodeProg

import time
import fileinput
import pyperclip
import itertools
import queue
import os
from collections import defaultdict

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def get_pixel(ints, x, y):
    prog = IntCodeProg()
    prog.ints = ints.copy()
    prog.pos = 0
    prog.prog_in.put(x)
    prog.prog_in.put(y)
    prog.process()
    ret = prog.prog_out.get()
    dprint('Checking',x,y,ret)
    return ret

def solve1(lines):
    ints = [int(s) for s in lines[0].split(',')]
    g = defaultdict(int)
    c, d = 0, 0
    for x in range(c, c+50):
        for y in range(d, d+50):
            g[x, y] = get_pixel(ints, x, y)
    print_grid(g, lambda x: '#' if x else '.')
    return list(g.values()).count(1)

def solve2(lines):
    ints = [int(s) for s in lines[0].split(',')]
    x, y = 7, 8 # first pixel where the beam takes shape and is contiguous
    size = 100
    while True:
        bot_corner = get_pixel(ints, x, y)
        top_corner = y >= size and get_pixel(ints, x+size-1, y-size+1)
        if bot_corner and top_corner:
            print('Found square',x,y)
            g = defaultdict(str)
            c, d = x, y-size+1
            print('Solution:',c,d)
            return c * 10000 + d
        if bot_corner:
            y+=1
        else:
            x+=1
            y-=1

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        lines.append(line)
    p1 = solve1(lines)
    p2 = solve2(lines)
    if p1 is not None:
        print(p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print(p2)
        pyperclip.copy(p2)
