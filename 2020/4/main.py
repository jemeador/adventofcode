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
    count = 0
    for passport in get_line_groups(lines):
        valid = True
        for s in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
            if s + ':' not in passport:
                dprint(passport, 'is not valid')
                valid = False
                break
        if valid:
            dprint(passport, 'is valid')
            count += 1
    return count

def solve2(lines):
    count = 0
    for passport in get_line_groups(lines):
        valid = True
        dprint("======")
        dprint(passport)
        dprint("------")

        for s in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
            if s + ':' not in passport:
                dprint(s, 'is missing')
                valid = False
                continue
            regex = re.compile(r'' + re.escape(s) + r':(\S+)')
            for match in regex.finditer(passport):
                dprint(s, match.groups()[0])
                if s == 'byr':
                    val = int(match.groups()[0])
                    if not 1920 <= val <= 2002:
                        dprint(s, "is invalid")
                        valid = False
                if s == 'iyr':
                    val = int(match.groups()[0])
                    if not 2010 <= val <= 2020:
                        dprint(s, "is invalid")
                        valid = False
                if s == 'eyr':
                    val = int(match.groups()[0])
                    if not 2020 <= val <= 2030:
                        dprint(s, "is invalid")
                        valid = False
                if s == 'hgt':
                    field = match.groups()[0]
                    try:
                        val = int(field[:-2])
                        if field[-2:] == 'cm':
                           if 150 < val and val > 193:
                               dprint(s, " is invalid")
                               valid = False
                        elif field[-2:] == 'in':
                           if 59 < val and val > 76:
                               dprint(s, " is invalid")
                               valid = False
                        else:
                            dprint(s, " is invalid")
                            valid = False
                    except:
                        valid = False
                if s == 'hcl':
                    field = match.groups()[0]
                    if re.search(r'^#[0-9a-f]{6}$', field) is None:
                        dprint(s, "is invalid")
                        valid = False
                if s == 'ecl':
                    f = match.groups()[0]
                    if f not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                        valid = False
                if s == 'pid':
                    field = match.groups()[0]
                    if re.search(r'^[0-9]{9}$', field) is None:
                        dprint(s, "is invalid")
                        valid = False
        if valid:
            dprint("==VALID==")
            count += 1
        else:
            dprint("==INVALID==")
    return count

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
