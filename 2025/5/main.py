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
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    r = 0
    fresh_lines = True;
    fresh_ranges = []
    ingredient_ids = []
    for line in lines:
        if line == '':
            fresh_lines = False
            continue
        if fresh_lines:
            start, end = line.split('-')
            fresh_ranges.append((start, end))
        else:
            ingredient_ids.append(int(line))
    for ingredient_id in ingredient_ids:
        for start, end in fresh_ranges:
            if int(start) <= ingredient_id <= int(end):
                r += 1
                break
    return r

def solve2(lines):
    r = 0
    fresh_ranges = []
    ingredient_ids = []
    for line in lines:
        if line == '':
            break
        start, end = [int(num) for num in line.split('-')]
        assert(start <= end)
        fresh_ranges.append((start, end))
    normal_ranges = []
    for start, end in fresh_ranges:
        start_included_in = None
        end_included_in = None
        for i in range(len(normal_ranges)):
            range_i = normal_ranges[i]
            normal_start, normal_end = range_i
            if normal_start <= start <= normal_end + 1:
                start_included_in = i
                dprint(f"{start} is in {normal_start}-{normal_end}")
            else:
                dprint(f"{start} not in {normal_start}-{normal_end}")
            if normal_start - 1 <= end <= normal_end:
                dprint(f"{end} is in {normal_start}-{normal_end}")
                end_included_in = i
            else:
                dprint(f"{end} not in {normal_start}-{normal_end}")
            if start_included_in is not None and start_included_in == end_included_in:
                dprint(f"Range {start}-{end} is fully included in {normal_ranges[i]}")
                break
            if start < normal_start and normal_end < end:
                dprint("Removing", normal_ranges[i])
                normal_ranges[i] = (0, 0)
            if start_included_in is not None and end_included_in is not None:
                break
            if start < normal_end and end < normal_end:
                break
        if start_included_in is None and end_included_in is None:
            dprint(f"Range {start}-{end} intersects nothing")
            normal_ranges.append((start, end))
        elif start_included_in == end_included_in:
            dprint(f"Range {start}-{end} is eclipsed by {normal_ranges[start_included_in]}")
            continue
        elif start_included_in is not None and end_included_in is None:
            dprint(f"Range {start}-{end} intersects {normal_ranges[start_included_in]}")
            normal_ranges[start_included_in] = (
                normal_ranges[start_included_in][0],
                end
            )
            dprint(f"Extending existing range to {normal_ranges[start_included_in]}")
        elif start_included_in is None and end_included_in is not None:
            dprint(f"Range {start}-{end} intersects {normal_ranges[end_included_in]}")
            normal_ranges[end_included_in] = (
                start,
                normal_ranges[end_included_in][1]
            )
            dprint(f"Extending existing range to {normal_ranges[end_included_in]}")
        else:
            dprint(f"Range {start}-{end} intersects {normal_ranges[start_included_in]} and {normal_ranges[end_included_in]}")
            normal_ranges[start_included_in] = (
                normal_ranges[start_included_in][0],
                normal_ranges[end_included_in][1]
            )
            dprint(f"Removing {normal_ranges[end_included_in]}")
            normal_ranges[end_included_in] = (0, 0)
        normal_ranges = [r for r in normal_ranges if r != (0, 0)]
        for normal_range in normal_ranges:
            assert(start <= end)
        normal_ranges = sorted(normal_ranges)
    prev_num = 0
    dprint(normal_ranges)
    for index, normal_range in enumerate(normal_ranges):
        r += normal_range[1] - normal_range[0] + 1
        print(f"  Normal range {index}: {normal_range[0]}-{normal_range[1]}");
        if normal_range[0] <= prev_num:
            dprint("Overlap!", normal_range[0])
        if normal_range[1] <= prev_num:
            dprint("Overlap!", normal_range[1])
        prev_num = normal_range[1]
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

   # generate a simplified input
   # for line in lines:
   #     factor = 1000000000000
   #     if line == '':
   #         print(line)
   #         continue
   #     if '-' not in line:
   #         print(int(line) // factor)
   #     else:
   #         start, end = line.split('-')
   #         print(f'{int(start) // factor}-{int(end) // factor}')
