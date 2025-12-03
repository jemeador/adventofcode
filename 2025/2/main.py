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
    total = 0
    line = ''.join(lines)
    for r in line.split(','):
        lo,hi = r.split('-')
        lo = int(lo)
        hi = int(hi)
        for i in range(lo, hi+1):
            as_str = str(i)
            for len_segment in range(1, 1 + len(as_str) // 2):
                if len(as_str) % len_segment != 0:
                    continue
                segment = as_str[0:len_segment]
                next_segment = segment
                k = 0
                valid = False
                while k + len_segment <= len(as_str):
                    next_segment = as_str[k:k+len_segment]
                    if next_segment != segment:
                        valid = True
                        break
                    k += len_segment
                if not valid:
                    total += i
                    # print(i)
                    break
    return total

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
    if p2 is not None:
        + print("Solution 2:", p2)
