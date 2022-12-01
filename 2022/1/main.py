#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    elfs = []
    elf = 0
    for line in lines:
        dprint(line)
        if len(line) == 1:
            elfs.append(elf)
            elf = 0
        else:
            elf += int(line)
    elfs.append(elf)
    elf = 0
    elfs.sort(reverse=True)
    return elfs[0]

def solve2(lines):
    elfs = []
    elf = 0
    for line in lines:
        dprint(line)
        if len(line) == 1:
            elfs.append(elf)
            elf = 0
        else:
            elf += int(line)
    elfs.append(elf)
    elf = 0
    elfs.sort(reverse=True)
    return sum(elfs[0:3])

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        lines.append(line)
    p1 = solve1(lines)
    p2 = solve2(lines)
    if p1 is not None:
        print(p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print(p2)
        pyperclip.copy(p2)
