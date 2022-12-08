#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import get_ints, get_uints
from py_utils.search import *

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

debug_mode = False
def dprint(*args, **kwargs):
    if debug_mode:
        return print(*args, **kwargs)

p1 = None
p2 = None

State = namedtuple('State', 'nodes keys_remaining')

def is_bit_set(bitset, b):
    return bitset & (1<<b)

def keys_from_bits(n):
    return [chr(o + ord('a')) for o in range(26) if is_bit_set(n, o)]

def keys_to_bitset(keys):
    bitset = 0
    for key in keys:
        k = ord(key) - ord('a')
        bitset |= (1<<k)
    return bitset

#def playback(g, moves):
#    os.system('clear')
#    print_grid(g)
#    mutable_g = g.copy()
#    coords = get_coords(g, '@')
#    for coord in coords:
#        mutable_g[coord] = '.'
#    for i in range(len(moves)):
#        m = moves[i]
#        coord = get_unique_pos(g, m)
#        mutable_g[coord] = '@'
#        time.sleep(0.1)
#        os.system('clear')
#        print_grid(mutable_g)
#        mutable_g[coord] = '.'

def is_connected(edges, start_node, end_node, memo):
    return math.isfinite(BFS(edges, start_node, end_node, 0, memo))

def BFS(edges, start_node, end_node, keys_remaining, memo):
    class Graph:
        def __init__(self, edges):
            self.edges = edges
        def edges(self, src):
            src_cell, keys = src
            for dest_cell, cost in self.edges[src]:
                matches_unowned_key = dest_cell.isalpha() and keys & (1 << (ord(dest_cell.lower()) - ord('a')))
                # Locked door
                if dest_cell.isupper() and matches_unowned_key:
                    continue
                new_keys = keys
                if dest_cell.islower() and matches_unowned_key:
                    new_keys = new_keys & ~(1<<(ord(key_to_obtain) - ord('a')))
                yield (dest_cell, new_keys), cost

    graph = Graph(edges)
    find_path()
    if start_node == end_node:
        return 0
    args = (start_node, end_node, keys_remaining)
    if args in memo:
        return memo[args]
    cost = 0
    visited = set()
    q = []
    heapq.heappush(q, (0, start_node))
    while q:
        cost, src = heapq.heappop(q)
        visited.add(src)
        for dest, added_cost in edges[src].items():
            new_cost = cost + added_cost
            if dest == end_node:
                # Perfectly bi-direction graph, cache both directions
                memo[(start_node, dest, keys_remaining)] = new_cost
                memo[(dest, start_node, keys_remaining)] = new_cost
                return new_cost
            # A key we aren't looking for and haven't collected. An unowned key
            # would change the keys_remaining (and the 'Z' dimension of the
            # graph)
            if matches_unowned_key:
                continue
            # This is a starting node (numeric), an opened door, or collected key
            heapq.heappush(q, (new_cost, dest))
    return math.inf

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
    next_start_node_id = 1
    for coord, cell in g.items():
        if is_poi(cell):
            if cell == '@':
                cell = str(next_start_node_id)
                next_start_node_id += 1
                g[coord] = cell
            node_coords[cell] = coord
    edges = {}
    for node, coord in node_coords.items():
        edges[node] = find_edges(g, node_coords[node])

    return node_coords.keys(), edges

def collect_keys(g):
    nodes, edges = build_graph(g)
    start_nodes = ''.join([n for n in nodes if n.isnumeric()])
    keys = [n for n in nodes if n.islower()]
    dfs_memo = {}
    print('Keys:', sorted(keys))
    print('Edges:', sorted(edges.items()))

    visited_states = defaultdict(lambda: math.inf)
    start_state = State(nodes=start_nodes, keys_remaining=keys_to_bitset(keys))

    q = []
    PqElement = namedtuple('PqElement', 'cost entry_count state moves')
    entry_count = 0
    heapq.heappush(q, PqElement(0, entry_count, start_state, ''))
    iteration = 0
    best = math.inf
    while q:
        cost, _, state, moves = heapq.heappop(q)

        if moves == 'acd':
            dprint(f'Debug print')
        debug_mode = (moves != 'acd')

        if cost >= visited_states[state]:
            dprint(f'state {moves} ({cost}) already visited with cost {visited_states[state]}' )
            continue
        if cost >= best:
            dprint(f'state {moves} cannot beat {best} starting from {cost}')
            continue

        visited_states[state] = cost
        nodes, keys_remaining = state

        if keys_remaining == 0:
            #playback(g, moves)
            print(f'Found solution {cost} with {moves}')
            best = cost

        if iteration % 1000 == 0:
            print(f'g={cost}, nodes={nodes}, moves={moves}')

        for i in range(0, 26):
            if not keys_remaining & (1<<i):
                continue
            key_to_obtain = chr(ord('a') + i)
            new_keys_remaining = keys_remaining & ~(1<<(ord(key_to_obtain) - ord('a')))

            for from_node in nodes:
                if not is_connected(edges, from_node, key_to_obtain, dfs_memo):
                    dprint(f'{from_node} not connected')
                    continue
                new_nodes = nodes.replace(from_node, key_to_obtain)
                new_state = State(nodes=new_nodes, keys_remaining=new_keys_remaining)

                if (from_node, key_to_obtain, keys_remaining) in dfs_memo:
                    added_cost = dfs_memo[(from_node, key_to_obtain, keys_remaining)]
                    dprint(f'cost {from_node} to {key_to_obtain} {added_cost} from memo')
                else:
                    added_cost = BFS(edges, from_node, key_to_obtain, keys_remaining, dfs_memo)
                    dprint(f'cost {from_node} to {key_to_obtain} {added_cost} calculated from BFS')
                if added_cost == math.inf:
                    continue
                new_cost = cost + added_cost
                if new_cost < visited_states[new_state]:
                    entry_count += 1
                    if new_cost < best:
                        dprint(f'adding {moves + key_to_obtain} {new_cost}')
                        heapq.heappush(q, PqElement(new_cost, entry_count, new_state, moves + key_to_obtain))
                    else:
                        dprint(f'Not adding child {moves + key_to_obtain}, {visited_states[new_state]} is better than {new_cost}')
                    # If this robot found a path, then the others should not be on this grid
                    continue
                else:
                    dprint(f'{visited_states[new_state]} is better than {new_cost}')
        iteration += 1
    print(f'Explored {iteration} states')
    return best

def solve1(lines):
    g = make_ascii_grid(lines)
    print_grid(g, str)
    return collect_keys(g)

def solve2(lines):
    g = make_ascii_grid(lines)

    before = make_ascii_grid([
        "...",
        ".@.",
        "...",
    ])
    after = make_ascii_grid([
        "@#@",
        "###",
        "@#@",
    ])

    count = find_and_replace_pattern(g, before, after)
    print_grid(g, str)
    return collect_keys(g)

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    #p1 = solve1(lines)
    #cProfile.run('p1 = solve1(lines)')
    p2 = solve2(lines)
    #cProfile.run('p2 = solve2(lines)')
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
