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

def handle_output(prog):
    render = ''
    while not prog.prog_out.empty():
        val = prog.prog_out.get()
        if val > 255:
            return val
        render += chr(val)
    for line in render.split('\n'):
        if len(line) == 0:
            time.sleep(0.5)
            os.system('clear')
        print(line)

def send_ascii_input(prog, script=''):
    done = False
    if script == '':
        while not done:
            str_input = input()
            if str_input == 'WALK':
                done = True
            str_input += '\n'
    else:
        str_input = script
    for ch in str_input:
        prog.prog_in.put(ord(ch))


def solve(lines, springscript):
    ints = [int(s) for s in lines[0].split(',')]
    prog = IntCodeProg()
    prog.ints = ints.copy()
    prog.pos = 0
    prog.process()
    handle_output(prog)
    send_ascii_input(prog, springscript)
    prog.process()
    return handle_output(prog)

springscript1 = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

springscript2 = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT D T
OR E T
OR H T
AND T J
RUN
"""

def solve1(lines):
    return solve(lines, springscript1)
def solve2(lines):
    return solve(lines, springscript2)

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
