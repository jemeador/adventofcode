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
    s = 0
    for line in lines:
        first = None
        last = None
        for c in line:
            if c.isdigit():
                if not first:
                    first = c
                last = c
        s += int(first + last)
    return s

def solve2(lines):
    words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    s = 0
    for line in lines:
        first = None
        last = None
        digitword = ''
        for c in line:
            if c.isdigit():
                first = c
            else:
                print(digitword)
                digitword += c
                for i in range(len(words)):
                    word = words[i]
                    if word in digitword:
                        first = str(i+1)
            print(first)
            if first:
                break
        digitword = ''
        for c in line[::-1]:
            if c.isdigit():
                last = c
            else:
                print(digitword)
                digitword = c + digitword
                for i in range(len(words)):
                    word = words[i]
                    if word in digitword:
                        last = str(i+1)
            print(last)
            if last:
                break
        s += int(first + last)
    return s

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1 = None#solve1(lines)
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
