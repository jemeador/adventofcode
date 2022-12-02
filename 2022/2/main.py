#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def score(them, you):
    if them == you:
        return 3 + you + 1
    if them == (you + 1) % 3:
        return 0 + you + 1
    else:
        return 6 + you + 1

def solve1(lines):
    s = 0
    for line in lines:
        a, b = line.split(' ')
        if a == 'A':
            them = 0
        if a == 'B':
            them = 1
        if a == 'C':
            them = 2
        if b == 'X':
            you = 0
        if b == 'Y':
            you = 1
        if b == 'Z':
            you = 2
        s += score(them, you)
    return s


def solve2(lines):
    s = 0
    for line in lines:
        a, b = line.split(' ')
        if a == 'A':
            them = 0
        if a == 'B':
            them = 1
        if a == 'C':
            them = 2
        if b == 'X':
            you = (them -1) % 3
        if b == 'Y':
            you = them
        if b == 'Z':
            you = (them + 1) % 3
        s += score(them, you)
    return s

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
