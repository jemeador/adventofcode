#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid, get_adj_items, add_coords
from py_utils.int_code import IntCodeProg
from py_utils.search import *

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

items_discovered = set()

def handle_output(prog):
    render = ''
    if prog.prog_out.empty():
        print('Program has no output?')
    while not prog.prog_out.empty():
        val = prog.prog_out.get()
        if 0 <= val < 256:
            render += chr(val)
    dir_list = False
    item_list = False
    inv_list = False
    cmds = []
    #cmds = ['north\n', 'south\n', 'east\n', 'west\n']
    room_name = ''
    for line in render.split('\n'):
        if line.startswith('=='):
            room_name = line.split(' ')[1]
        elif line.startswith('Items here:'):
            item_list = True
        elif line.startswith('Items in your inventory:'):
            inv_list = True
        elif line.startswith('Doors here lead:'):
            door_list = True
        elif len(line) < 1:
            item_list = False
            door_list = False
            inv_list = False
        elif item_list and line.startswith('-'):
            item = line[2:]
            items_discovered.add(item)
            if item not in ['infinite loop', 'escape pod', 'molten lava', 'photons']:
                cmds.append(f'take {item}\n')
        elif inv_list and line.startswith('-'):
            item = line[2:]
            cmds.append(f'drop {item}\n')
        elif door_list and line.startswith('-'):
            direction = line[2:]
            cmds.append(f'{direction}\n')
    print(render)
    if room_name.startswith('Pressure') and 'Alert' not in render:
        print('SOLVED')
        return {'ABORT'}

    return cmds

def send_ascii_input(prog, script=''):
    if script == '':
        str_input = input() + '\n'
    else:
        str_input = script
        print(str_input)
    if str_input.startswith('ABORT'):
        return False
    if str_input.startswith('exec'):
        if '1' in str_input:
            try_all_combinations(prog)
            return True
    for ch in str_input:
        prog.prog_in.put(ord(ch))
    return True

manual_mode = True

goal_state = (-1, -1, (0), '')

def try_all_combinations(prog):
    send_ascii_input(prog, 'inv\n')
    prog.process()
    inv = []
    for cmd in handle_output(prog):
        if cmd.startswith('drop'):
            inv.append(cmd[5:])
    for bitset in range(pow(2, len(inv))):
        for b in range(len(inv)):
            item = inv[b]
            if bitset & (1<<b):
                send_ascii_input(prog, f'take {item}\n')
            else:
                send_ascii_input(prog, f'drop {item}\n')
            prog.process()
            handle_output(prog)
        send_ascii_input(prog, 'south\n')
        prog.process()
        cmds = handle_output(prog)
        if 'ABORT' in cmds:
            return

class ShipGraph:
    def edges_from(self, src):
        prog = IntCodeProg()
        pos, relative_base, memory, cmd = src
        prog.pos = pos
        prog.relative_base = relative_base
        prog.ints = list(memory)
        if cmd != '':
            if not send_ascii_input(prog, cmd):
                yield goal_state, 1
        prog.process()
        cmds = handle_output(prog)
        new_pos = prog.pos
        new_relative_base = prog.relative_base
        new_memory = tuple(prog.ints)
        send_ascii_input(prog, 'inv\n')
        prog.process()
        handle_output(prog)
        for branch_cmd in cmds:
            cost = 10
            if branch_cmd.startswith('take'):
                cost = 1
            yield (new_pos, new_relative_base, new_memory, branch_cmd), 1

def solve(lines):
    ints = [int(s) for s in lines[0].split(',')]
    prog = IntCodeProg()
    prog.ints = ints.copy()
    prog.pos = 0
    prog.relative_base = 0
    if manual_mode:
        prog.process()
        handle_output(prog)
        while True:
            if not send_ascii_input(prog):
                break
            prog.process()
            handle_output(prog)
    else:
        find_path(ShipGraph(), (0, 0, tuple(prog.ints), ''), goal_state)
        print(items_discovered)

def solve1(lines):
    return solve(lines)
def solve2(lines):
    pass

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
