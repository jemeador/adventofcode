#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict, deque

import cProfile
import fileinput
import itertools
import pyperclip
import queue
import re
import os
import time

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

State = namedtuple('State', 'node keys_remaining')
Edge = namedtuple('Edge', 'start end')

def keys_from_bits(n):
    keys = []
    for o in range(0,26):
        if is_bit_set(n, o):
            keys.append(chr(o + ord('a')))
    return keys

def keys_to_bitset(keys):
    bitset = 0
    for key in keys:
        k = ord(key) - ord('a')
        bitset |= (1<<k)
    return bitset

def key_in_bitset(bitset, key):
    return is_bit_set(bitset, ord(key) - ord('a'))

def is_bit_set(bitset, b):
    return bitset & (1<<b)

def without_key(bitset, key):
    k = ord(key) - ord('a')
    return bitset & ~(1<<k)

def playback(g, moves):
    os.system('clear')
    print_grid(g)
    mutable_g = g.copy()
    coord = get_unique_pos(g, '@')
    mutable_g[coord] = '.'
    for i in range(len(moves)):
        m = moves[i]
        coord = get_unique_pos(g, m)
        mutable_g[coord] = '@'
        time.sleep(0.01)
        os.system('clear')
        print_grid(mutable_g)
        mutable_g[coord] = '.'

def BFS(g, edges, start_key, end_key):
    if start_key == end_key:
        return 0
    visited = {}
    visited[start_key] = 0
    q = queue.PriorityQueue()
    q.put((0, start_key))
    while not q.empty():
        cost, node = q.get()
        for edge, added_cost in edges.items():
            if edge.start != node:
                continue
            new_cost = cost + added_cost
            if edge.end == end_key:
                return new_cost
            if edge.end not in visited or new_cost < visited[edge.end]:
                visited[edge.end] = new_cost
                q.put((new_cost, edge.end))
    print(f'Failed to find min dist! {start_key}, {end_key}')
    assert(False)
    return None

def build_min_dists(g, edges):
    dists = {}
    node_coords = {}
    for coord, cell in g.items():
        if is_poi(cell):
            node_coords[cell] = coord
    for start_key, start_coord in node_coords.items():
        for end_key, end_coord in node_coords.items():
            min_dist = BFS(g, edges, start_key, end_key)
            assert(min_dist is not None)
            dists[start_key, end_key] = min_dist
    return dists

def heuristic(state, min_distances):
    keys = keys_from_bits(state.keys_remaining)
    return max([min_distances[state.node, key] for key in keys] + [0])

def is_poi(cell):
    return cell != '.' and cell != '#'

def find_edges(g, start_coord):
    ret = {}
    visited = set([start_coord])
    frontier = [start_coord]
    start_node = g[start_coord]
    cost = 0
    while frontier:
        cost += 1
        new_frontier = []
        for coord in frontier:
            for adj_coord in get_adj_coords(coord):
                cell = g[adj_coord]
                if cell == '#':
                    continue
                if adj_coord in visited:
                    continue
                visited.add(adj_coord)
                if is_poi(cell):
                    ret[Edge(start_node, cell)] = cost
                else:
                    new_frontier.append(adj_coord)
        frontier = new_frontier.copy()
    return ret

def build_graph(g):
    node_coords = {}
    for coord, cell in g.items():
        if is_poi(cell):
            node_coords[cell] = coord
    edges = {}
    for node, coord in node_coords.items():
        edges.update(find_edges(g, node_coords[node]))

    return node_coords.keys(), edges

def collect_keys(g):
    nodes, edges = build_graph(g)
    min_distances = build_min_dists(g, edges)
    keys = [n for n in nodes if n.islower()]
    print(keys)
    print(edges)
    print(min_distances)

    visited_states = defaultdict(int)
    start_state = State(node='@', keys_remaining=keys_to_bitset(keys))

    q = queue.PriorityQueue()
    PqElement = namedtuple('PqElement', 'priority cost state moves')
    q.put(PqElement(0, 0, start_state, ''))

    iteration = 0
    while not q.empty():
        priority, cost, state, moves = q.get()
        visited_states[state] = cost
        node, keys_remaining = state

        if keys_remaining == 0:
            playback(g, moves)
            return cost

        if iteration % 1000 == 0:
            print(f'Priority: {priority}, g={cost}, h={priority-cost}, keys_remaining={bin(keys_remaining)}({len(keys_from_bits(keys_remaining))})')

        for edge, added_cost in edges.items():
            if edge.start != node:
                continue
            if edge.end.isupper() and key_in_bitset(keys_remaining, edge.end.lower()):
                continue
            new_node = edge.end
            new_cost = cost + added_cost
            new_keys_remaining = keys_remaining
            if edge.end.islower():
                new_keys_remaining = without_key(keys_remaining, edge.end)
            new_state = State(node=new_node, keys_remaining=new_keys_remaining)
            if new_state not in visited_states or new_cost < visited_states[state]:
                q.put((new_cost + heuristic(new_state, min_distances), new_cost, new_state, moves + edge.end))
        iteration += 1
    return -1

def solve1(lines):
    assert(key_in_bitset(1, 'a'))
    assert(key_in_bitset(2, 'b'))
    assert(key_in_bitset(4, 'c'))
    assert(without_key(11, 'a') == 10)
    assert(without_key(7, 'c') == 3)
    _bitset = keys_to_bitset(['a', 'b', 'c', 'f'])
    assert(keys_from_bits(_bitset) == ['a', 'b', 'c', 'f'])
    assert(keys_from_bits(5) == ['a', 'c'])
    assert(keys_from_bits(5) == ['a', 'c'])
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
    #cProfile.run('p1 = solve1(lines)')
    p1 = solve1(lines)
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
