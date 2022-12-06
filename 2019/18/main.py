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
import math
import heapq

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

State = namedtuple('State', 'node keys_remaining')

def key_for_bit(n):
    return chr(ord('a') + n)

def keys_from_bits(n):
    return [chr(o + ord('a')) for o in range(26) if is_bit_set(n, o)]

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
        time.sleep(0.1)
        os.system('clear')
        print_grid(mutable_g)
        mutable_g[coord] = '.'

def DFS(edges, start_node, end_node, keys_remaining, visited, memo):
    if start_node == end_node:
        return 0
    args = (start_node, end_node, keys_remaining)
    if args in memo:
        return memo[args]
    new_visited = visited.copy()
    new_visited.add(start_node)
    best = math.inf
    for dest, cost in edges[start_node].items():
        if dest in visited:
            continue
        # Locked door
        if dest.isupper() and key_in_bitset(keys_remaining, dest.lower()):
            continue
        if dest == end_node:
            memo[args] = cost
            return cost
        # Collecting another key would change the keys_remaining
        if dest.islower() and key_in_bitset(keys_remaining, dest):
            continue
        total_cost = cost + DFS(edges, dest, end_node, keys_remaining, new_visited, memo)
        if total_cost < best:
            best = total_cost
    memo[args] = best
    return best

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
                    ret[cell] = cost
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
        edges[node] = find_edges(g, node_coords[node])

    return node_coords.keys(), edges

def collect_keys(g):
    nodes, edges = build_graph(g)
    keys = [n for n in nodes if n.islower()]
    dfs_memo = {}
    dprint('Keys:', sorted(keys))
    dprint('Edges:', sorted(edges))

    visited_states = defaultdict(int)
    start_state = State(node='@', keys_remaining=keys_to_bitset(keys))

    q = []
    PqElement = namedtuple('PqElement', 'cost entry_count state moves')
    entry_count = 0
    heapq.heappush(q, PqElement(0, entry_count, start_state, ''))
    iteration = 0
    while q:
        cost, _, state, moves = heapq.heappop(q)
        visited_states[state] = cost
        node, keys_remaining = state

        if keys_remaining == 0:
            playback(g, moves)
            print(f'Explorerd {iteration} states')
            return cost

        if iteration % 10000 == 0:
            print(f'g={cost}, keys_remaining={bin(keys_remaining)}({len(keys_from_bits(keys_remaining))})')

        for i in range(0, 26):
            if not is_bit_set(keys_remaining, i):
                continue
            new_node = key_for_bit(i)
            new_keys_remaining = without_key(keys_remaining, new_node)
            new_state = State(node=new_node, keys_remaining=new_keys_remaining)
            if new_state in visited_states and visited_states[new_state] <= cost:
                continue

            if (node, new_node, keys_remaining) in dfs_memo:
                added_cost = dfs_memo[(node, new_node, keys_remaining)]
            else:
                added_cost = DFS(edges, node, new_node, keys_remaining, set(), dfs_memo)
            if added_cost == math.inf:
                continue
            new_cost = cost + added_cost
            if new_state not in visited_states or new_cost < visited_states[state]:
                entry_count += 1
                heapq.heappush(q, PqElement(new_cost, entry_count, new_state, moves + new_node))
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
    cProfile.run('p1 = solve1(lines)')
    #p1 = solve1(lines)
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
