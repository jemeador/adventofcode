#!/usr/bin/env python3
import fileinput
import pyperclip

p1 = None
p2 = None

def solve(lines, x_step, y_step):
    x = 0
    y = 0
    count = 0
    while y+y_step < len(lines):
        y+=y_step
        x+=x_step
        x %= len(lines[0]) - 1
        if lines[y][x] == '#':
            count+=1
    return count

def solve1(lines):
    return solve(lines, 3, 1)

def solve2(lines):
    count = 1
    count *= solve(lines, 1, 1)
    count *= solve(lines, 3, 1)
    count *= solve(lines, 5, 1)
    count *= solve(lines, 7, 1)
    count *= solve(lines, 1, 2)
    return count

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
