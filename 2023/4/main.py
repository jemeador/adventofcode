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
    r = 0
    for line in lines:
        cards = set()
        wins = set()
        left, right = line.split('|')
        _, nums_str = left.split(':')
        print(nums_str)
        for num in nums_str.strip().split(' '):
            if num != '':
                cards.add(int(num))
        for num in right.strip().split(' '):
            if num != '':
                wins.add(int(num))
        exp = 0
        for num in cards:
            if num in wins:
                exp += 1
        if exp > 0:
            r += pow(2, exp-1)
    return r

def process(i, cards, win_nums, memo):
    if i in memo:
        print(i, 'memoized', memo[i])
        return memo[i]
    nums = cards[i]
    wins = win_nums[i]
    score = 0
    print(nums, wins)
    for num in nums:
        if num in wins:
            score += 1
    print(i, score)
    if score == 0:
        memo[i] = 1
        print(i, 'gains', 0)
        return memo[i]
    card_count = 0
    for j in range(i+1, i+1+score):
        card_count += process(j, cards, win_nums, memo)
    memo[i] = 1 + card_count
    print(i, 'gains', card_count)
    return memo[i]

def solve2(lines):
    r = 0
    all_cards = []
    all_wins = []
    for i in range(len(lines)):
        line = lines[i]
        cards = set()
        wins = set()
        left, right = line.split('|')
        _, nums_str = left.split(':')
        print(nums_str)
        for num in nums_str.strip().split(' '):
            if num != '':
                cards.add(int(num))
        for num in right.strip().split(' '):
            if num != '':
                wins.add(int(num))
        all_cards.append(cards)
        all_wins.append(wins)
    memo = defaultdict(int)
    counts = 0
    for i in range(len(lines)):
        counts += process(i, all_cards, all_wins, memo)
    return counts

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
