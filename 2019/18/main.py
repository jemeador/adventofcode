#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict, deque

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

def key_positions(g):
    ret = {}
    for coord, cell in g.items():
        if cell.islower():
            ret[cell] = coord
    return ret

def heuristic(state, key_pos):
    h = 0
    coord, keys_collected = state
    for cell, key_coord in key_pos.items():
        if cell not in keys_collected:
            h += manhatten(coord, key_coord)
    return h

def priority(steps, state, key_pos):
    g = steps
    h = heuristic(state, key_pos)
    return g + h

def collect_keys(g):
    # Create a queue to store the coordinates of the starting position.
    key_pos = key_positions(g)
    start = get_unique_pos(g, '@')
    assert(start != None)
    visited_states = defaultdict(int)
    start_state = (start, frozenset())
    q = queue.PriorityQueue()
    q.put((0, 0, start_state))

    # While the queue is not empty, do the following:
    iteration = 0
    while not q.empty():
        _, steps, state = q.get()
        visited_states[state] = steps
        coord, keys_collected = state

        if len(keys_collected) == len(key_pos):
            return steps

        if iteration % 1000 == 0:
            print(steps, keys_collected, coord)

        # Step 5d: Explore the 4 adjacent positions (up, down, left, right) by adding their coordinates to the queue
        # if they are traversable paths and not walls.
        for new_coord, cell in get_adj_items(g, coord):
            if cell == '#':
                continue
            elif cell.isupper() and cell.lower() not in keys_collected:
                continue
            else:
                new_keys_collected = set(keys_collected)
                if cell.islower():
                    new_keys_collected.add(cell)
                new_state = (new_coord, frozenset(new_keys_collected))
                if new_state not in visited_states or steps < visited_states[state]:
                    q.put((priority(steps, new_state, key_pos), steps+1, new_state))
        iteration += 1
    return -1

def solve1(lines):
    g = make_ascii_grid(lines)
    print_grid(g, str)
    return collect_keys(g)

def solve2(lines):
    pass

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
