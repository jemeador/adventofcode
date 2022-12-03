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
        them = ord(a) - ord('A')
        you = ord(b) - ord('X')
        s += score(them, you)
    return s


def solve2(lines):
    s = 0
    for line in lines:
        a, b = line.split(' ')
        them = ord(a) - ord('A')
        if b == 'X':
            you = (them -1) % 3
        elif b == 'Y':
            you = them
        else:
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
