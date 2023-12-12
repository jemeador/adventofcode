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
    #if True:
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def fit(possibility, template):
    for i in range(len(possibility)):
        if template[i] != '?' and possibility[i] != template[i]:
            dprint('nofit', possibility, template)
            return False
    dprint('fits', possibility, template)
    return True

def recursive_combos(springs, runs, memo):
    key = (springs,tuple(runs))
    if key in memo:
        return memo[key]
    dprint(springs, runs, 'consider')
    if len(runs) == 0:
        dprint(springs, runs, 0, 'len(runs) == 0')
        memo[(springs, runs)] = 0
        return 0
    if len(runs) == 1:
        run = runs[0]
        if run > len(springs):
            dprint(springs, runs, 0, 'run < len(springs)')
            memo[key] = 0
            return 0
        ret = 0
        for i in range(len(springs)+1-run):
            possibility = ''
            for j in range(len(springs)):
                if j < i or j >= i + run:
                    possibility += '.'
                else:
                    possibility += '#'
            if fit(possibility, springs):
                ret += 1
        dprint(springs, runs, ret, 'final')
        memo[key] = ret
        return ret
    run = runs[0]
    run_start_max = run
    for rr in runs[1:]:
        run_start_max += rr + 1
    combos = 0
    for i in range(0, len(springs)+1 - run_start_max):
        left_springs = springs[0:i+run+1]
        possibility = ''
        for j in range(len(left_springs)):
            if j < i or j >= i + run:
                possibility += '.'
            else:
                possibility += '#'
        if fit(possibility, left_springs):
            right_springs = springs[i+run+1:]
            combos += recursive_combos(right_springs, runs[1:], memo)
        if i == run_start_max-1:
            dprint(left_springs, springs[i+run+1:], 'out of room')
    dprint(springs, runs, combos, 'main')
    memo[key] = combos
    return combos


def solve1(lines):
    r = 0
    #for line in lines[0:1]:
    for line in lines:
        springs, runs_str = line.split()
        runs = get_uints(runs_str)
        memo = {}
        combos = recursive_combos(springs, runs, memo)
        r += combos
        print(springs, runs, combos)
    return r

def solve2(lines):
    r = 0
    #for line in lines[0:1]:
    for line in lines:
        springs, runs_str = line.split()
        new_springs = ''
        new_runs_str = ''
        for i in range(5):
            new_springs += springs + '?'
            new_runs_str += runs_str + ','
        springs = new_springs[:-1]
        runs_str = new_runs_str
        runs = get_uints(runs_str)
        memo = {}
        combos = recursive_combos(springs, runs, memo)
        r += combos
        print(springs, runs, combos)
    return r

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1 = solve1(lines)
    print()
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
