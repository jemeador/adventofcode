#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid
from py_utils.fast_parse import get_ints, get_uints
from py_utils.search import *

from collections import defaultdict

import functools
import fileinput
import itertools
import pyperclip
import queue
import re
import json

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def __make_key(grid_dict, coord, cell):
    """
    Identify a unique node in a pluto graph, we only care about the cells adjacent to warps (two letters)
    Distinguish between inner and outer cells for warping
    """
    for adj_coord, adj_cell in get_adj_items(grid_dict, coord):
        if adj_cell.isalpha():
            label1 = adj_cell
            for double_adj_coord, double_adj_cell in get_adj_items(grid_dict, adj_coord):
                if double_adj_cell.isalpha():
                    label2 = double_adj_cell
                    # Pairs of letters are unique, they won't be in a different order to identiify a different warp
                    if label2 < label1:
                        label1, label2 = label2, label1
                    is_outer = (coord.x == grid_min_x(grid_dict) + 2 or
                        coord.y == grid_min_y(grid_dict) + 2 or
                        coord.x == grid_max_x(grid_dict) - 2 or
                        coord.y == grid_max_y(grid_dict) - 2)
                    return (label1+label2, is_outer)
    return None

def __is_node(grid_dict, coord, cell):
    return cell == '.' and __make_key(grid_dict, coord, cell) is not None

def build_pluto_graph(lines):
    g = make_ascii_grid(lines)
    print_grid(g)
    is_node = functools.partial(__is_node, grid_dict=g)
    make_key = functools.partial(__make_key, grid_dict=g)
    graph = build_graph_from_ascii_grid(g, is_node=is_node, make_key=make_key)
    nodes = set(graph.edges.keys())
    # Add the warps
    for node1 in nodes:
        label1, is_outer1 = node1
        for node2 in nodes:
            label2, is_outer2 = node2
            if label1 == label2 and is_outer1 != is_outer2:
                graph.add_edge(node1, node2, 1)
    return graph

class RecursiveGraph:
    def __init__(self, normal_graph):
        self.graph = normal_graph
    def edges_from(self, src):
        src_label, src_is_outer, src_layer = src
        for dest, cost in self.graph.edges[src_label,src_is_outer].items():
            dest_label, dest_is_outer = dest
            dest_layer = src_layer
            if dest_label == src_label:
                if dest_is_outer:
                    dest_layer += + 1
                else:
                    dest_layer += - 1
            is_endpoint = dest_label == 'AA' or dest_label == 'ZZ'
            if dest_is_outer:
                if dest_layer == 0 and not is_endpoint:
                    continue
                elif dest_layer > 0 and is_endpoint:
                    continue
            yield (dest_label, dest_is_outer, dest_layer), cost

def solve1(lines):
    graph = build_pluto_graph(lines)
    cost, path = find_path(graph, ('AA', True), ('ZZ', True))
    print(path)
    return cost

def solve2(lines):
    graph = RecursiveGraph(build_pluto_graph(lines))
    cost, path = find_path(graph, ('AA', True, 0), ('ZZ', True, 0))
    print(path)
    return cost

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
