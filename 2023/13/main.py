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

def col(lines, n):
    ret = ''
    for line in lines:
        ret += line[n]
    return ret

def solve1(lines):
    groups = get_line_groups(lines)
    horizontal_score = 0
    vertical_score = 0
    for group in groups:
        lines = group.split('\n')
        for i in range(1, len(lines)):
            if lines[i] == lines[i-1]:
                mirror = True
                j = 0
                while i+j < len(lines) and i-1-j >= 0:
                    if lines[i+j] != lines[i-1-j]:
                        mirror = False
                        break
                    j += 1
                if mirror:
                    horizontal_score += i
        for i in range(1, len(lines[0])):
            if col(lines,i) == col(lines, i-1):
                mirror = True
                j = 0
                while i+j < len(lines[0]) and i-1-j >= 0:
                    if col(lines, i+j) != col(lines, i-1-j):
                        mirror = False
                        break
                    j += 1
                if mirror:
                    vertical_score += i
    return horizontal_score * 100 + vertical_score

def find_reflection(lines, presmudge):
    for i in range(1, len(lines)):
        if lines[i] == lines[i-1]:
            mirror = True
            j = 0
            while i+j < len(lines) and i-1-j >= 0:
                if lines[i+j] != lines[i-1-j]:
                    mirror = False
                    break
                j += 1
            if mirror and presmudge != (0, i):
                return (0, i)
    for i in range(1, len(lines[0])):
        if col(lines,i) == col(lines, i-1):
            mirror = True
            j = 0
            while i+j < len(lines[0]) and i-1-j >= 0:
                if col(lines, i+j) != col(lines, i-1-j):
                    mirror = False
                    break
                j += 1
            if mirror and presmudge != (i, 0):
                return (i, 0)
    return None

def solve2(lines):
    groups = get_line_groups(lines)
    horizontal_score = 0
    vertical_score = 0
    for group in groups:
        group_lines = group.split('\n')
        presmudge = find_reflection(group_lines, (-1,-1))
        #horizontal_score += presmudge[1]
        #vertical_score += presmudge[0]
        done = False
        copy_lines = []
        for y in range(0, len(group_lines)):
            if done:
                break
            for x in range(0, len(group_lines[0])):
                copy_lines = []
                for cpy in range(0, len(group_lines)):
                    copy_lines.append('')
                    for cpx in range(0, len(group_lines[0])):
                        if y == cpy and x == cpx:
                            if group_lines[y][x] == '.':
                                copy_lines[cpy] += '#'
                            else:
                                copy_lines[cpy] += '.'
                        else:
                            copy_lines[cpy] += group_lines[cpy][cpx]
                postsmudge = find_reflection(copy_lines, presmudge)
                if postsmudge and postsmudge != presmudge:
                    print(x, y, presmudge, postsmudge)
                    print('\n'.join(copy_lines))
                    print()
                    horizontal_score += postsmudge[1]
                    vertical_score += postsmudge[0]
                    done = True
                    break
        if not done:
            print('Found no reflection line for group')
            print(group)
    return horizontal_score * 100 + vertical_score

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
