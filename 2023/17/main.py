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
import time

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

class CrucibleGraph:
    def __init__(self, grid_dict, min_straight, max_straight):
        self.grid_dict = grid_dict
        self.min_straight = min_straight
        self.max_straight = max_straight
    # Implement this for find_path
    def edges_from(self, src):
        location, direction, moves_until_turn = src
        for dest_direction in adj_offsets:
            # Reverse is not allowed
            if add_coords(dest_direction, direction) == Coord(0,0):
                continue
            is_turn = (dest_direction != direction)
            dest_location = add_coords(location, dest_direction)
            if is_turn:
                if location != Coord(0,0) and moves_until_turn > self.max_straight - self.min_straight:
                    continue
                dest_moves_until_turn = self.max_straight - 1
            else:
                dest_moves_until_turn = moves_until_turn - 1
            # Moving too many blocks in one direction is not allowed
            if dest_moves_until_turn < 0:
                continue
            if dest_moves_until_turn < 0:
                continue
            # Off the map
            if dest_location not in self.grid_dict:
                continue
            cost = int(self.grid_dict[dest_location])
            yield (dest_location, dest_direction, dest_moves_until_turn), cost

def print_path(path_result, grid_dict):
    priority, cost, path = path_result
    for node in path:
        location, direction, moves_until_turn = node
        if direction == Coord(0,1):
            grid_dict[location] = 'v'
        elif direction == Coord(0,-1):
            grid_dict[location] = '^'
        elif direction == Coord(1,0):
            grid_dict[location] = '>'
        elif direction == Coord(-1,0):
            grid_dict[location] = '<'
    print_grid(grid_dict, lambda c: c)

def solve(lines, grid_dict, graph, is_end, max_straight):
    r = 0
    print_grid(grid_dict)

    visited = set()
    q = []
    # location, direction, moves until turn
    start_node = (Coord(0,0), Coord(1,0), max_straight)
    heappush(q, PathResult(0, 0, [start_node]))
    while q:
        state = heappop(q)
        score, cost_so_far, path = state
        src = path[-1]
        if src in visited:
            continue
        visited.add(src)
        location, direction, moves_until_turn = src
        if len(visited) % 1000 == 0:
            print(f'Explored {len(visited)} states. Current cost: ', cost_so_far)
        if is_end(src):
            print(f'Explored {len(visited)} states')
            print_path(state, grid_dict.copy())
            return state[1]
        for dest, edge_cost in graph.edges_from(src):
            if dest in visited:
                continue
            dest_location, dest_direction, dest_moves_until_turn = dest
            h = 0
            #if calc_heuristic:
                #h += calc_heuristic(dest, end_node)
            new_cost = cost_so_far + edge_cost
            priority = new_cost
            state = PathResult(priority, new_cost, path + [dest])
            heappush(q, state)
    print(f'Failed to find a single path in {len(visited)} states')
    return -1

def solve1(lines):
    grid_dict = make_ascii_grid(lines)
    graph = CrucibleGraph(grid_dict, min_straight=0, max_straight=3)
    return solve(lines, grid_dict, graph,
                 is_end=lambda node: node[0] == Coord(len(lines[0])-1, len(lines)-1), max_straight=3)

def solve2(lines):
    grid_dict = make_ascii_grid(lines)
    graph = CrucibleGraph(grid_dict, min_straight=4, max_straight=10)
    return solve(lines, grid_dict, graph,
                 is_end=lambda node: (node[0] == Coord(len(lines[0])-1, len(lines)-1)) and node[2] <= 6, max_straight=10)

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
