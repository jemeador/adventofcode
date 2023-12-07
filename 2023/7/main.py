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

def tier(a, jokerswild=False):
    wild = 0
    if jokerswild:
        wild = a.count('J')
    best = 1
    cards = '23456789TJQKA'
    if jokerswild:
        cards = '23456789TQKA'
    for ch in cards:
        if a.count(ch) + wild == 5:
            best = max(best, 7)
        if a.count(ch) + wild == 4:
            best = max(best, 6)
        if a.count(ch) + wild == 3:
            for ch2 in cards:
                if ch != ch2 and a.count(ch2) == 2:
                    best = max(best, 5)
            best = max(best, 4)
        if a.count(ch) + wild == 2:
            for ch2 in cards:
                if ch != ch2 and a.count(ch2) == 2:
                    best = max(best, 3)
                if ch != ch2 and a.count(ch2) == 3:
                    best = max(best, 5)
            best = max(best, 2)
        print(wild, ch, best)
    return best

def rank(a, jokerswild=False):
    hand = a.split()[0]
    ta = tier(hand, jokerswild)
    r = pow(13, 7) * ta
    #print(hand, ta)
    for i in range(5):
        ch = hand[i]
        if jokerswild:
            r += pow(13, (6-i)) * 'J23456789TQKA'.find(ch)
        else:
            r += pow(13, (6-i)) * '23456789TJQKA'.find(ch)
        #print('23456789TJQKA'.find(ch))
    return r

def rank1(a):
    return rank(a, jokerswild=False)
def rank2(a):
    return rank(a, jokerswild=True)


def solve1(lines):
    r = 0
    lines.sort(key=rank1)
    #print(lines)
    for i in range(len(lines)):
        line = lines[i]
        r += (i+1) * int(line.split()[1])
        print(line, i+1, r)
    return r

def solve2(lines):
    r = 0
    lines.sort(key=rank2)
    #print(lines)
    for i in range(len(lines)):
        line = lines[i]
        r += (i+1) * int(line.split()[1])
        print(line, i+1, r)
    print('JJ355', tier('JJ355', jokerswild=True))
    print('JJ38T', tier('JJ38T', jokerswild=True))
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
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
