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

def solve(lines):
    junctions = []
    for line in lines:
        j = [int(x) for x in line.split(',')]
        junctions.append(j)

    distances = {}


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
            for i in range(3):
                sorted_circuits = sorted(circuits.items(),
                                         key=lambda x: len(x[1]), reverse=True)
                solution1 *= len(sorted_circuits[i][1])


    print("Max distance: ", distances[last_connection])

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
