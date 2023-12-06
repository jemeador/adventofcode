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

def from_snafu(snafu):
    dec = 0
    r_snafu = snafu[::-1]
    for i in range(len(snafu)):
        ch = r_snafu[i]
        multi = pow(5, i)
        if ch == '2':
            dec += multi * 2
        elif ch == '1':
            dec += multi * 1
        elif ch == '-':
            dec += multi * -1
        elif ch == '=':
            dec += multi * -2
    print(snafu, dec)
    return dec

def to_snafu(dec):
    print(dec)
    remainder = dec
    digits = []
    i = 0
    while remainder != 0 and i < 30:
        next_multi = pow(5, i+1)
        multi = pow(5, i)
        m = remainder % next_multi
        if m == multi * 0:
            digits.append('0')
            dec_digit = 0
        elif m == multi * 1:
            digits.append('1')
            dec_digit = 1
        elif m == multi * 2:
            digits.append('2')
            dec_digit = 2
        elif m == multi * 3:
            digits.append('=')
            dec_digit = -2
        elif m == multi * 4:
            digits.append('-')
            dec_digit = -1
        remainder -= dec_digit * multi
        i += 1
    return ''.join(digits[::-1])

def solve1(lines):
    dec = sum([from_snafu(line) for line in lines])
    snafu =  to_snafu(dec)
    print(snafu, dec, from_snafu(snafu))
    assert(from_snafu(snafu) == dec)
    return snafu

def solve2(lines):
    pass

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
