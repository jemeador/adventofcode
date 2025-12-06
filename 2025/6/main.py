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
import queue
import re

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    r = 0
    cols = []
    ops = []
    l = lines[0].split()
    for i in range(len(l)):
        cols.append([])
    for line in lines:
        nums = line.split()
        for i in range(len(nums)):
            if nums[i] != '*' and nums[i] != '+':
                cols[i].append(nums[i])
            else:
                ops.append(nums[i])
    for i in range(len(cols)):
        problem = 0
        if ops[i] == '+':
            for item in cols[i]:
                problem += int(item)
        if ops[i] == '*':
            problem = 1
            for item in cols[i]:
                problem *= int(item)
        r += problem
    return r

def solve2(lines):
    r = 0
    num_strs = []
    operator = '?'
    for i in range(len(lines[0]) + 1):
        num_str = ' '
        if i < len(lines[0]):
            for j in range(len(lines)):
                num_str += lines[j][i]
            if '+' in num_str:
                operator = '+'
                num_str = num_str.replace('+', '')
            if '*' in num_str:
                operator = '*'
                num_str = num_str.replace('*', '')
        if set(num_str).issubset(' '):
            if operator == '+':
                problem = 0
                for num in num_strs:
                    problem += int(num)
                r += problem
            if operator == '*':
                problem = 1
                for num in num_strs:
                    problem *= int(num)
                r += problem
            print(num_strs, operator, problem)
            num_strs.clear()
        else:
            num_strs.append(num_str)
    return r

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
    if p2 is not None:
        print("Solution 2:", p2)
