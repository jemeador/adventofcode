#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid
from py_utils.fast_parse import get_ints, get_uints

from collections import defaultdict, namedtuple

import fileinput
import itertools
import pyperclip
import queue
import re

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None


Monkey = namedtuple('Monkey', 'items inspect test toss')
sample = False

def monkey_primes():
    if sample:
        return (19 * 23 * 13  * 17)
    else:
        return (2 * 17 * 7 * 11 * 19 * 5 * 13 * 3)

def eval_monkey(i, monkeys, tally, level):
    m = monkeys[i]
    for item in m.items:
        dprint(f'  Monkey inspects an item with a worry level of {item}.')
        item = m.inspect(item)
        if level != 2:
            dprint(f'  {item} becomes boring {item // 3}')
            item //= 3
        else:
            item %= monkey_primes()
        if m.test(item):
            dprint(f'  {item} is tossed to {m.toss[0]}')
            monkeys[m.toss[0]].items.append(item)
        else:
            dprint(f'  {item} is tossed to {m.toss[1]}')
            monkeys[m.toss[1]].items.append(item)
    tally[i] += len(m.items)
    m.items.clear()

def solve(lines, level):
    monkey = {}

    #for l in range(0, len(lines), step=7):
    #    m = get_ints(lines[l+0])
    #    items = get_ints(lines[l+1])
    #    words = line[l+2].split(' ')[-2:]
    #    if words[0] == add
    #    if words[1] == 'old':
    #    monkey[m] = Monkey(
    #      items=[79, 98],
    #      inspect=lambda x: x * 19,
    #      test=lambda x: x % 23 == 0,
    #      toss=(2, 3),
    #      )

    if sample:
        monkey[0] = Monkey(
          items=[79, 98],
          inspect=lambda x: x * 19,
          test=lambda x: x % 23 == 0,
          toss=(2, 3),
          )

        monkey[1] = Monkey(
          items=[54, 65, 75, 74],
          inspect=lambda x: x + 6,
          test=lambda x: x % 19 == 0,
          toss=(2, 0),
          )

        monkey[2] = Monkey(
          items=[79, 60, 97],
          inspect=lambda x: x * x,
          test=lambda x: x % 13 == 0,
          toss=(1, 3),
          )

        monkey[3] = Monkey(
          items=[74],
          inspect=lambda x: x + 3,
          test=lambda x: x % 17 == 0,
          toss=(0, 1),
          )

    else:
        monkey[0] = Monkey(
          items=[99, 63, 76, 93, 54, 73],
          inspect=lambda x: x * 11,
          test=lambda x: x % 2 == 0,
          toss=(7, 1),
          )

        monkey[1] = Monkey(
          items=[91, 60, 97, 54],
          inspect=lambda x: x + 1,
          test=lambda x: x % 17 == 0,
          toss=(3, 2),
          )

        monkey[2] = Monkey(
          items=[65],
          inspect=lambda x: x + 7,
          test=lambda x: x % 7 == 0,
          toss=(6, 5),
          )

        monkey[3] = Monkey(
          items=[84, 55],
          inspect=lambda x: x + 3,
          test=lambda x: x % 11 == 0,
          toss=(2, 6),
          )

        monkey[4] = Monkey(
          items=[86, 63, 79, 54, 83],
          inspect=lambda x: x * x,
          test=lambda x: x % 19 == 0,
          toss=(7, 0),
          )

        monkey[5] = Monkey(
          items=[96, 67, 56, 95, 64, 69, 96],
          inspect=lambda x: x + 4,
          test=lambda x: x % 5 == 0,
          toss=(4, 0),
          )

        monkey[6] = Monkey(
          items=[66, 94, 70, 93, 72, 67, 88, 51],
          inspect=lambda x: x * 5,
          test=lambda x: x % 13 == 0,
          toss=(4, 5),
          )

        monkey[7] = Monkey(
          items=[59, 59, 74],
          inspect=lambda x: x + 8,
          test=lambda x: x % 3 == 0,
          toss=(1, 3),
          )

    tally = defaultdict(int)
    rounds = 20
    if level == 2:
        rounds = 10000
    for i in range(rounds):
        dprint('Iteration', i)
        for j in range(len(monkey)):
            dprint(f'Monkey {j}:')
            eval_monkey(j, monkey, tally, level)
    score = 1
    items = list(tally.values())
    dprint (items)
    items = sorted(items)[-2:]
    dprint (items)
    for item in items:
        score *= item
    return score

def solve1(lines):
    return solve(lines, 1)

def solve2(lines):
    return solve(lines, 2)

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
