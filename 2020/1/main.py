#!/usr/bin/env python3
import fileinput
import pyperclip

p1 = None
p2 = None

def solve1(lines):
    for a in range(len(lines)):
        num1 =  int(lines[a])
        for b in range(a+1, len(lines)):
            num2 =  int(lines[b])
            if num1 + num2 == 2020:
                return num1 * num2

def solve2(lines):
    for a in range(len(lines)):
        num1 =  int(lines[a])
        for b in range(a+1, len(lines)):
            num2 =  int(lines[b])
            for c in range(b+1, len(lines)):
                num3 =  int(lines[c])
                if num1 + num2 + num3 == 2020:
                    return num1 * num2 * num3


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

