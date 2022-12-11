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

def make_network(lines):
    print('Make network')
    progs = []
    for addr in range(50):
        ints = [int(s) for s in lines[0].split(',')]
        prog = IntCodeProg()
        prog.ints = ints.copy()
        prog.pos = 0
        prog.prog_in.put(addr)
        progs.append(prog)
    return progs

def process(progs, part):
    print('Process')
    nat_x = 0
    nat_y = 0
    prev_nat_y = 0
    while True:
        idle = True
        for i in range(len(progs)):
            prog = progs[i]
            if prog.prog_in.empty():
                prog.prog_in.put(-1)
            else:
                idle = False
            prog.process()
            if prog.prog_out.empty():
                continue
            idle = False
            addr = prog.prog_out.get()
            x = prog.prog_out.get()
            y = prog.prog_out.get()
            print(addr, x, y)
            if addr == 255:
                if part == 1:
                    return y
                nat_x = x
                nat_y = y
            else:
                progs[addr].prog_in.put(x)
                progs[addr].prog_in.put(y)
        if idle:
            if part == 2 and prev_nat_y == nat_y:
                return nat_y
            progs[0].prog_in.put(nat_x)
            progs[0].prog_in.put(nat_y)
            prev_nat_y = nat_y

def solve1(lines):
    return process(make_network(lines), 1)
def solve2(lines):
    return process(make_network(lines), 2)

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
