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

# 6510000
# 5973431

#  536569

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def expanded_pattern(digits, pattern, pos):
    pos += 1
    expanded_pattern = []
    for d in pattern:
        for _ in range(pos):
            expanded_pattern.append(d)
    while len(expanded_pattern) < len(digits) + pos:
        expanded_pattern.extend(expanded_pattern)
    return expanded_pattern[1:len(digits) + 1]

def apply_pattern(digits, pattern):
    assert(len(digits) == len(pattern))
    val = 0
    for i in range(len(digits)):
        dprint(f'{digits[i]} * {pattern[i]} + ', end='')
        val += digits[i] * pattern[i]
    val = int(str(val)[-1:])
    assert(val < 10)
    dprint(f'= {val}')
    return val

def next_phase(digits, pos):
    partial_sum = sum(digits[start:])
    repeated_sum = sum(digits)
    digit_count = len(digits) * 10000
    val = partial_sum + multiplier * repeated_sum
    return int(str(val)[-1:])

def solve1(lines):
    pattern = [0, 1, 0, -1]
    digits = []
    for line in lines:
        for c in line:
            digits.append(int(c))
    for phase in range(100):
        new_digits = []
        for pos in range(len(digits)):
            new_digits.append(apply_pattern(digits, expanded_pattern(digits, pattern, pos)))
        dprint(f'After {phase} phase:', ''.join([str(d) for d in new_digits[:8]]))
        digits = new_digits.copy()
    return ''.join([str(d) for d in new_digits[:8]])

def solve2(lines):
    digits = []
    for line in lines:
        for c in line:
            digits.append(int(c))
    pos = int(''.join([str(d) for d in digits[:7]]))
    start = pos % len(digits)
    truncated_digits = digits[start:]
    relevant_signal_length = len(digits) * 10000 - pos
    while len(truncated_digits) < relevant_signal_length:
        truncated_digits.extend(digits)
    truncated_digits = truncated_digits[:relevant_signal_length]
    for phase in range(100):
        print(phase)
        digit_to_add = sum(truncated_digits) % 10
        for i in range(len(truncated_digits)):
            irrelevant_digit = truncated_digits[i]
            truncated_digits[i] = digit_to_add
            digit_to_add = (digit_to_add - irrelevant_digit) % 10
    return ''.join([str(d) for d in truncated_digits[:8]])

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
