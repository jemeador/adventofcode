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

Node = namedtuple('Node', 'coord step')

dirs = [Coord(0, -1), Coord(0, 1), Coord(1, 0), Coord(-1, 0)]
chrs = ['^', 'v', '>', '<']

class Graph:
    def __init__(self, grid):
        self.grid = grid
        self.init_blizzards = defaultdict(list)
        self.hazards_by_step = defaultdict(set)
        self.width = grid_max_x(self.grid) - 1
        self.height = grid_max_y(self.grid) - 1
        for i in range(len(dirs)):
            d = dirs[i]
            c = chrs[i]
            for coord in get_coords(grid, c):
                self.init_blizzards[c].append(coord)

    def has_blizzard(self, coord, step):
        return coord in self.project_blizzard(step)

    def project_blizzard(self, step):
        if step in self.hazards_by_step:
            return self.hazards_by_step[step]
        for i in range(len(dirs)):
            d = dirs[i]
            c = chrs[i]
            blizz_offset = mult_coord(d, step)
            for orig_blizz_coord in self.init_blizzards[c]:
                blizz_coord = add_coords(orig_blizz_coord, blizz_offset)
                blizz_coord = Coord(((blizz_coord.x-1) % self.width) + 1, ((blizz_coord.y-1) % self.height) + 1)
                self.hazards_by_step[step].add(blizz_coord)
        return self.hazards_by_step[step]

    def edges_from(self, src):
        coord, step = src
        new_step = (step+1) % (300)
        for adj_coord in get_adj_coords(coord):
            if not self.has_blizzard(adj_coord, new_step) and adj_coord in self.grid and self.grid[adj_coord] != '#':
                yield Node(adj_coord, new_step), 1
        if not self.has_blizzard(coord, new_step):
            yield Node(coord, new_step), 1

    def calc_heuristic(self, s):
        return manhatten(s.coord, Coord(self.width, self.height+1))
    def calc_heuristic_to_start(self, s):
        return manhatten(s.coord, Coord(1, 0))

def is_end_node(graph, node):
    return node.coord == Coord(graph.width, graph.height+1)
def is_start_node(graph, node):
    return node.coord == Coord(1, 0)

def solve1(lines):
    grid = make_ascii_grid(lines)
    print_grid(grid)
    graph = Graph(grid)
    print(graph.width, graph.height)
    score, cost, path = find_path(graph,
            start_node=Node(Coord(1, 0),0),
            is_end_node=lambda n: is_end_node(graph, n),
            calc_heuristic=lambda s, e: Graph.calc_heuristic(graph, s)
            )
    for p in path:
        g = grid.copy()
        for coord in g:
            if g[coord] != '#':
                g[coord] = '.'
        g[p.coord] = 'E'
        for c in graph.project_blizzard(p.step):
            g[c] = 'o'
        print(p.step)
        print_grid(g)
    return cost

def solve2(lines):
    grid = make_ascii_grid(lines)
    print_grid(grid)
    graph = Graph(grid)
    _, cost1, _ = find_path(graph,
            start_node=Node(Coord(1, 0),0),
            is_end_node=lambda n: is_end_node(graph, n),
            calc_heuristic=lambda s, e: Graph.calc_heuristic(graph, s)
            )
    _, cost2, _ = find_path(graph,
            start_node=Node(Coord(graph.width, graph.height+1), cost1 % 300),
            is_end_node=lambda n: is_start_node(graph, n),
            calc_heuristic=lambda s, e: Graph.calc_heuristic_to_start(graph, s)
            )
    _, cost3, _ = find_path(graph,
            start_node=Node(Coord(1, 0),(cost1+cost2) % 300),
            is_end_node=lambda n: is_end_node(graph, n),
            calc_heuristic=lambda s, e: Graph.calc_heuristic(graph, s)
            )
    print(cost1,cost2,cost3)
    return cost1 + cost2 + cost3

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
