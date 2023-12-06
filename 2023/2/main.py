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

def solve1(lines):
    r = 12
    g = 13
    b = 14
    c = 0
    for i in range(len(lines)):
        line = lines[i]
        possible = True
        _, games_str = line.split(':')
        games = games_str.split(';')
        for game in games:
            colors = game.split(',')
            for s in colors:
                s = s.strip()
                count, color = s.split(' ')
                print(count, color)
                if color == 'red' and int(count) > r:
                    possible = False
                if color == 'blue' and int(count) > b:
                    possible = False
                if color == 'green' and int(count) > g:
                    possible = False
        if possible:
            print(i+1, 'is possible')
            c += (i+1)

    return c

def solve2(lines):
    c = 0
    for i in range(len(lines)):
        r = 0
        g = 0
        b = 0
        line = lines[i]
        possible = True
        _, games_str = line.split(':')
        games = games_str.split(';')
        for game in games:
            colors = game.split(',')
            for s in colors:
                s = s.strip()
                count, color = s.split(' ')
                print(count, color)
                if color == 'red':
                    r = max(r, int(count))
                if color == 'blue' and int(count) > b:
                    b = max(b, int(count))
                if color == 'green' and int(count) > g:
                    g = max(g, int(count))
        if possible:
            power = r * g * b
            print(power)
            c += power

    return c

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
