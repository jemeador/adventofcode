#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    for line in lines:
        print(line)
    return 0

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
        print(p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print(p2)
        pyperclip.copy(p2)
