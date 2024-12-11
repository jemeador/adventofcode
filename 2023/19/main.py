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
import inspect

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def eval(predicate, part):
    var, symbol, val = predicate
    print(var, symbol,val)
    if symbol == '<':
        return part[var] < val
    elif symbol == '>':
        return part[var] > val
    return True

def process(part, workflows, label):
    print(label)
    if label == 'A':
        return True
    if label == 'R':
        return False
    for step in workflows[label]:
        predicate, jump_label = step
        if eval(predicate,part):
            return process(part, workflows, jump_label)
    assert(False)

def solve1(lines):
    workflow_strs, part_strs = get_line_groups(lines)
    workflows = defaultdict(list)
    for workflow_str in workflow_strs.split('\n'):
        label, instructions_str = workflow_str.split('{')
        instructions_str  = instructions_str[:-1]
        instructions_str = instructions_str.split(',')
        for i in range(len(instructions_str)):
            instruction_str = instructions_str[i]
            if ':' in instruction_str:
                condition, jump_label = instruction_str.split(':')
                if '>' in condition:
                    var, rhs = condition.split('>')
                    val = int(rhs)
                    predicate = (var, '>', val)
                    workflows[label].append((predicate, jump_label))
                elif '<' in condition:
                    var, rhs = condition.split('<')
                    val = int(rhs)
                    predicate = (var, '<', val)
                    workflows[label].append((predicate, jump_label))
            else:
                workflows[label].append((('Fallthrough','...',0), instruction_str))
    parts = []
    for line in part_strs.split('\n'):
        line = line[1:-1]
        part = {}
        for init in line.split(','):
            var, val = init.split('=')
            part[var] = int(val)
        parts.append(part)
    r = 0
    for part in parts:
        print('Eval', part)
        if (process(part, workflows, 'in')):
            print('Accepted')
            for key, val in part.items():
                r += val
        else:
            print('Rejected')
    return r

def combinations(workflows, labels, min_part, max_part):
    label = labels[-1]
    if label == 'A':
        combos = 1
        for var in 'xmas':
            combos *= max(0, max_part[var]-min_part[var] + 1)
        print(labels, combos, min_part, max_part)
        return combos
    if label == 'R':
        return 0
    combos = 0
    for step in workflows[label]:
        predicate, jump_label = step
        var, symbol, val = predicate
        cp_labels = labels.copy()
        cp_labels.append(jump_label)
        if symbol == '<':
            cp_max_part = max_part.copy()
            cp_max_part[var] = val - 1
            combos += combinations(workflows, cp_labels, min_part.copy(), cp_max_part)
            min_part[var] = val
        elif symbol == '>':
            cp_min_part = min_part.copy()
            cp_min_part[var] = val + 1
            combos += combinations(workflows, cp_labels, cp_min_part, max_part.copy())
            max_part[var] = val
        else:
            combos += combinations(workflows, cp_labels, min_part.copy(), max_part.copy())
    return combos

def solve2(lines):
    workflow_strs, part_strs = get_line_groups(lines)
    workflows = defaultdict(list)
    for workflow_str in workflow_strs.split('\n'):
        label, instructions_str = workflow_str.split('{')
        instructions_str  = instructions_str[:-1]
        instructions_str = instructions_str.split(',')
        for i in range(len(instructions_str)):
            instruction_str = instructions_str[i]
            if ':' in instruction_str:
                condition, jump_label = instruction_str.split(':')
                if '>' in condition:
                    var, rhs = condition.split('>')
                    val = int(rhs)
                    predicate = (var, '>', val)
                    workflows[label].append((predicate, jump_label))
                elif '<' in condition:
                    var, rhs = condition.split('<')
                    val = int(rhs)
                    predicate = (var, '<', val)
                    workflows[label].append((predicate, jump_label))
            else:
                workflows[label].append((('Fallthrough','...',0), instruction_str))
    min_part = {'x':1, 'm':1,'a':1,'s':1}
    max_part = {'x':4000, 'm':4000,'a':4000,'s':4000}
    # 167409079868000
    # 79000692663011
    # 79000692663000
    return combinations(workflows, ['in'], min_part, max_part)

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
