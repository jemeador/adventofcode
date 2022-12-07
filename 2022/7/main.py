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

def solve(lines):
    fs = defaultdict(int)
    cd = ''
    for line in lines:
        if line.startswith('$ cd '):
            dir_cmd = line[5:]
            if dir_cmd.startswith('/'):
                cd = dir_cmd
            elif dir_cmd.startswith('..'):
                cd = cd[:cd.rindex('/')]
            else:
                cd = cd + dir_cmd + '/'
            dprint(cd)
        elif line.startswith('$ ls'):
            pass
        elif line.startswith('dir '):
            pass
        else:
            size, filename = line.split(' ')
            path = cd + filename
            fs[path] = size
    dir_sizes = defaultdict(int)
    print()
    for key, s in fs.items():
        print(key, s)
        size = int(s)
        full_dir_name = '/'
        dir_sizes[full_dir_name] += size
        for base_name in key.split('/')[:-1]:
            full_dir_name += base_name + '/'
            dir_sizes[full_dir_name] += size
    print()
    count = 0
    for key, s in dir_sizes.items():
        print(key, size)
        if s <= 100000:
            count += s
    p1 = count
    files = []
    for key, s in dir_sizes.items():
        files.append((s, key))
    files.sort()
    files.reverse()

    free = 70000000 - dir_sizes['/']
    required = 30000000 - free
    for size, d in files:
        if size >= required:
            to_delete = d
    p2 = dir_sizes[to_delete]
    return p1, p2

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    p1, p2 = solve(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
