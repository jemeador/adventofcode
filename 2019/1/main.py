#!/usr/bin/env python3
import fileinput
import pyperclip

p1 = None
p2 = None


def fuel_req_rec(mass):
    if mass <= 0:
        return 0
    return mass + fuel_req_rec(int(mass / 3) - 2)

def fuel_req(mass):
    if mass <= 0:
        return 0
    return fuel_req_rec(int(mass / 3) - 2)

def solve1(lines):
    fuel = 0
    for line in lines:
        fuel += int(int(line) / 3 ) - 2
    return fuel

def solve2(lines):
    fuel = 0
    for line in lines:
        fuel += fuel_req(int(line))
    return fuel

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
