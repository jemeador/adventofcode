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

def dist(j1, j2):
    return (j1[0] - j2[0]) ** 2 + (j1[1] - j2[1]) ** 2 + (j1[2] - j2[2]) ** 2


def get_zone(j):
    # Heuristic for making buckets (cheated a bit by knowing the final
    # distance) Make buckets where junctions boxes in adjacent buckets are
    # never more than 15000 units apart
    M = 15000

    return (j[0] // M, j[1] // M, j[2] // M)

def adj_zones(zone):
    ret = []
    for x in range(zone[0] - 1, zone[0] + 2):
        for y in range(zone[1] - 1, zone[1] + 2):
            for z in range(zone[2] - 1, zone[2] + 2):
                ret.append((x, y , z))
    return ret

def solve(lines):
    junctions = []
    buckets = defaultdict(list)
    for i, line in enumerate(lines):
        j = tuple([int(x) for x in line.split(',')])
        junctions.append(j)
        buckets[get_zone(j)].append(i)

    distances = {}
    dprint("Bucket count: ", len(buckets))

    # This part is entirely optional, the program runs fast enough at ~1s, but
    # this makes it about 10x faster
    optimize = True
    if optimize:
        for a, j1 in enumerate(junctions):
            for adj_zone in adj_zones(get_zone(j1)):
                bucket = buckets[adj_zone]
                for b in bucket:
                    if a < b:
                        j2 = junctions[b]
                        distances[(a,b)] = dist(j1, j2)
    else:
        for a, j1 in enumerate(junctions):
            for b in range(a+1, len(junctions)):
                j2 = junctions[b]
                distances[(a,b)] = dist(j1, j2)

    distances_sorted = sorted(distances.items(), key=lambda x: x[1])

    grouping = {}
    circuits = {}

    for j in range(len(junctions)):
        # Each junction box is in its own circuit to start
        grouping[j] = j
        circuits[j] = set([j])

    connections_to_make = 1000
    if len(lines) == 20:
        connections_to_make = 10

    n = 0
    last_connection = (0, 0)

    while len(circuits[grouping[0]]) < len(junctions):
        if n >= len(distances_sorted):
            print("Exhausted list of distances at ", n-1,
                  math.sqrt(distances_sorted[n-1][1]))
            exit(1)
        item = distances_sorted[n]
        pair = item[0]
        (a, b) = pair
        last_connection = pair
        if grouping[a] != grouping[b]:
            b_circuit = circuits[grouping[b]].copy()
            # Move all junction boxes from b's group into a's group
            for j in b_circuit:
                circuits[grouping[a]].update(circuits[grouping[j]])
                circuits[grouping[j]].clear()
                grouping[j] = grouping[a]
        n += 1
        if n == connections_to_make:
            solution1 = 1
            sorted_circuits = sorted(circuits.items(),
                                     key=lambda x: len(x[1]), reverse=True)
            for i in range(3):
                solution1 *= len(sorted_circuits[i][1])


    dprint("Max distance: ", math.sqrt(distances[last_connection]))

    solution2 = junctions[last_connection[0]][0] * junctions[last_connection[1]][0]
    return solution1, solution2


if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1, p2 = solve(lines)
    print("Solution 1:", p1)
    print("Solution 2:", p2)
