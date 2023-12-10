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

def pipe_adjacent_coords(g, coord):
    cell = g[coord]
    if cell == '.':
        return []
    if cell == 'S':
        return get_coords_with_offsets(coord, adj_offsets)
    if cell == '|':
        return get_coords_with_offsets(coord, [(0, 1), (0, -1)])
    if cell == '-':
        return get_coords_with_offsets(coord, [(1, 0), (-1, 0)])
    if cell == 'L':
        return get_coords_with_offsets(coord, [(1, 0), (0, -1)])
    if cell == 'J':
        return get_coords_with_offsets(coord, [(0, -1), (-1, 0)])
    if cell == '7':
        return get_coords_with_offsets(coord, [(0, 1), (-1, 0)])
    if cell == 'F':
        return get_coords_with_offsets(coord, [(0, 1), (1, 0)])
    return []

def solve1(lines):
    r = 0
    g = make_ascii_grid(lines)
    path = g.copy()
    #print_grid(g)
    graph = StaticGraph()
    for coord, cell in g.items():
        if cell == 'S':
            start_coord = coord
            break
    src_node = start_coord
    visited = set([start_coord])
    frontier = [start_coord]
    start_node = g[start_coord]
    cost = 0
    while frontier:
        cost += 1
        new_frontier = []
        for coord in frontier:
            visited_count = 0
            for adj_coord in pipe_adjacent_coords(g, coord):
                if coord not in g:
                    continue
                if coord not in pipe_adjacent_coords(g, adj_coord):
                    continue
                if adj_coord in visited:
                    visited_count += 1
                    continue
                dest_node = adj_coord
                graph.add_edge(src_node, dest_node, cost)
                new_frontier.append(adj_coord)
                visited.add(adj_coord)
                path[adj_coord] = 'X'
            if visited_count == 2:
                #print_grid(path)
                return cost
        frontier = new_frontier.copy()
    return r

def solve2(lines):
    r = 0
    g = make_ascii_grid(lines)
    path = g.copy()
    #print_grid(g)
    print()
    graph = StaticGraph()
    for coord, cell in g.items():
        if cell == 'S':
            start_coord = coord
            path[start_coord] = 'X'
            break
    src_node = start_coord
    visited = set([start_coord])
    frontier = [start_coord]
    start_node = g[start_coord]
    cost = 0
    while frontier:
        cost += 1
        new_frontier = []
        for coord in frontier:
            visited_count = 0
            for adj_coord in pipe_adjacent_coords(g, coord):
                if coord not in g:
                    continue
                if coord not in pipe_adjacent_coords(g, adj_coord):
                    continue
                if adj_coord in visited:
                    visited_count += 1
                    continue
                dest_node = adj_coord
                graph.add_edge(src_node, dest_node, cost)
                new_frontier.append(adj_coord)
                visited.add(adj_coord)
                path[adj_coord] = 'X'
            if visited_count == 2:
                #print_grid(path)
                #print()
                frontier = []
                break
        frontier = new_frontier.copy()
    enclosed = g.copy()
    max_x = grid_max_x(g)
    for coord, cell in path.items():
        if cell != 'X':
            # Count the number of "vertical" walls made of main-loop pipe pieces
            wall_count = 0
            ray_coord = coord
            spin = 0
            while ray_coord.x < max_x:
                # Only need to count in one direction. Because the pipe makes a
                # perfect cycle, anything on the inside will see an odd number
                # of walls in any direction
                ray_coord = add_coords(ray_coord, (1,0))
                # S is an F in my puzzle
                if g[ray_coord] in ['F','J','S'] and path[ray_coord] == 'X':
                    # F and J together make a 1 vertical pipe
                    wall_count += 0.5
                if g[ray_coord] in ['L','7'] and path[ray_coord] == 'X':
                    # L and 7 together make 1 vertical pipe
                    # ... but F and 7 balance out to be a 0 vertical pipes
                    # Example: this is a non-intersecting surface; we count
                    # it as 0 walls on both rows
                    # --->LJ----> 0
                    # --->F7----> 0
                    wall_count -= 0.5
                if g[ray_coord] in ['|'] and path[ray_coord] == 'X':
                    wall_count += 1
            if int(wall_count) % 2 == 1:
                enclosed[coord] = 'X'
                r += 1
            else:
                enclosed[coord] = 'O'
    #print_grid(path)
    #print_grid(enclosed)
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
