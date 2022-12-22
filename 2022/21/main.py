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

def resolve_op(a, op, b, mapping):
    print(a, op, b)
    val_a = resolve(a, mapping)
    val_b = resolve(b, mapping)

    if op == '+':
        return val_a + val_b
    if op == '-':
        return val_a - val_b
    if op == '*':
        return val_a * val_b
    if op == '/':
        return val_a // val_b
    if op == '=':
        return val_a == val_b

def resolve(monkey_name, mapping):
    say = mapping[monkey_name]
    if say.isnumeric():
        return int(say)
    return resolve_op(*say.split(' '), mapping)

def solve1(lines):
    r = 0
    mapping = {}
    for line in lines:
        key, say = line.split(':')
        mapping[key] = say.strip()
    print(mapping)
    return resolve('root', mapping)

def make_tree(monkey_name, mapping):
    if monkey_name == 'humn':
        return 'you'
    say = mapping[monkey_name]
    if say.isnumeric():
        return int(say)

    a, op, b = say.split(' ')
    return (make_tree(a, mapping), op, make_tree(b, mapping))

def has_you(node):
    if node == 'you':
        return True
    if type(node) == int:
        return False
    return has_you(node[0]) or has_you(node[2])

def apply_inverse(node, op, moved_node):
    if op == '+':
        return (node, '-', moved_node)
    if op == '-':
        return (node, '+', moved_node)
    if op == '*':
        return (node, '/', moved_node)
    if op == '/':
        return (node, '*', moved_node)

def resolve_tree(node):
    assert(node != 'you')
    if type(node) == int:
        return node
    lhs, op, rhs = node
    a = resolve_tree(lhs)
    b = resolve_tree(rhs)
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a // b
    assert(False)

def solve_tree(node):
    lhs, op, rhs = node
    assert(op == '=')
    for side, opp_side in [(lhs, rhs), (rhs, lhs)]:
        if has_you(side):
            if side == 'you':
                print(node)
                return resolve_tree(opp_side)
            side_lhs, side_op, side_rhs = side
            if side_op == '-' or side_op == '/' or has_you(side_lhs):
                new_rhs = side_lhs
                new_lhs = apply_inverse(opp_side, side_op, side_rhs)
            else:
                new_rhs = side_rhs
                new_lhs = apply_inverse(opp_side, side_op, side_lhs)
            new_tree = (new_lhs, '=', new_rhs)
            return solve_tree(new_tree)

def solve2(lines):
    r = 0
    mapping = {}
    for line in lines:
        key, say = line.split(':')
        mapping[key] = say.strip()
    new_root = mapping['root'].split(' ')
    mapping['root'] = ' '.join([new_root[0], '=', new_root[2]])
    tree = make_tree('root', mapping)
    print(tree)
    return solve_tree(tree)

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
