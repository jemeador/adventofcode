#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    count=0
    lo, hi = lines[0].split('-')
    for i in range(int(lo), int(hi)):
        adj = False
        asc = True
        pw = str(i)
        for i in range(0, len(pw)-1):
            if pw[i] == pw[i+1]:
                adj = True
            if pw[i] > pw[i+1]:
                asc = False
        if adj and asc:
            count+=1
    return count


def solve2(lines):
    count=0
    lo, hi = lines[0].split('-')
    for i in range(int(lo), int(hi)):
        group = 1
        adj = False
        asc = True
        pw = str(i)
        for i in range(0, len(pw)-1):
            if pw[i] == pw[i+1]:
                group+=1
            else:
                if group == 2:
                    adj = True
                group=1
            if pw[i] > pw[i+1]:
                asc = False
        if group == 2:
            adj = True
        if adj and asc:
            count+=1
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
