#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict

import fileinput
import itertools
import pyperclip
import queue
import re

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    stacks = defaultdict(queue.LifoQueue)
    stack_lines = []
    for line in lines:
        if line.startswith(' 1'):
            print(line)
            break
        else:
            print(line)
            stack_lines.append(line)
    print(stack_lines)
    stack_lines.reverse()
    for line in stack_lines:
        for i in range(0, len(line)//4 + 1):
            index = i*4 + 1
            if line[index] != ' ':
                stacks[i].put(line[index])

    for line in lines[len(stack_lines) + 2:]:
        count, from_s, to_s = get_ints(line)
        print(count, from_s, to_s)
        for _ in range(0, count):
            top = stacks[from_s-1].get()
            print(top)
            stacks[to_s-1].put(top)

    ret = ''
    for s in range(0, len(stacks)):
        ret += stacks[s].get()
    return ret

def solve2(lines):
    stacks = defaultdict(queue.LifoQueue)
    stack_lines = []
    for line in lines:
        if line.startswith(' 1'):
            print(line)
            break
        else:
            print(line)
            stack_lines.append(line)
    print(stack_lines)
    stack_lines.reverse()
    for line in stack_lines:
        for i in range(0, len(line)//4 + 1):
            index = i*4 + 1
            if line[index] != ' ':
                stacks[i].put(line[index])

    for line in lines[len(stack_lines) + 2:]:
        count, from_s, to_s = get_ints(line)
        print(count, from_s, to_s)
        group = []
        for _ in range(0, count):
            group.append(stacks[from_s-1].get())
        group.reverse()
        for item in group:
            stacks[to_s-1].put(item)

    ret = ''
    for s in range(0, len(stacks)):
        ret += stacks[s].get()
    return ret

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
