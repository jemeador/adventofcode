#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid

from collections import defaultdict

import fileinput
import itertools
import pyperclip
import pprint
import queue
import re

pp = pprint.PrettyPrinter(indent=4)

debug_mode = False

def dpprint(*args, **kwargs):
    if debug_mode:
        return pp.pprint(*args, **kwargs)
def dprint(*args, **kwargs):
    if debug_mode:
        return print(*args, **kwargs)

p1 = None
p2 = None

def read_reactions(lines):
    reactions = {}
    for line in lines:
        inputs, outputs = line.split(' => ')
        output_count, output_chemical = outputs.split(' ')
        reactions[output_chemical] = (int(output_count), [])
        for input_chemical in inputs.split(', '):
            count, chemical = input_chemical.split(' ')
            reactions[output_chemical][1].append((int(count), chemical))
    return reactions

def solve_for_n_fuel(reactions, n):
    required_chemicals = defaultdict(int)
    required_chemicals['FUEL'] = n

    while True:
        dpprint(required_chemicals)
        done = True
        for rch, rco in required_chemicals.items():
            if rch != "ORE" and rco > 0:
                done = False
                required_chemical = rch
                required_count = rco
                break
        if done:
            return required_chemicals["ORE"]

        output_count, ingredients = reactions[required_chemical]
        m = required_count // output_count
        if required_count % output_count:
            m += 1
        dprint('Consume  ', end="")
        for input_count, chemical in ingredients:
            required_chemicals[chemical] += input_count * m
            dprint(f'{input_count} {chemical}', end=",")
        dprint(f' to produce {output_count} {required_chemical}')
        required_chemicals[required_chemical] -= output_count * m

def solve1(lines):
    return solve_for_n_fuel(read_reactions(lines), 1)

def solve2(lines):
    reactions = read_reactions(lines)
    lower_bound = 1
    upper_bound = 1e12
    while upper_bound != lower_bound:
        n = (upper_bound + lower_bound + 1) // 2
        ore_required = solve_for_n_fuel(reactions, n)
        print(n, ore_required)
        if ore_required < 1e12:
            lower_bound = n
        elif ore_required > 1e12:
            upper_bound = n-1
        else:
            return int(n)
    return int(lower_bound)


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
