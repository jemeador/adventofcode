#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def count(orbits, body):
    if body in orbits:
        return 1 + count(orbits, orbits[body])
    return 0

def chain(orbits, body):
    if body in orbits:
        return chain(orbits, orbits[body]) + [body]
    return []

def solve1(lines):
    orbits = {}
    for line in lines:
        body, sat = line.split(')')
        orbits[sat] = body
    return sum([count(orbits, body) for body in orbits])

def solve2(lines):
    orbits = {}
    for line in lines:
        body, sat = line.split(')')
        orbits[sat] = body
    you_chain = chain(orbits, 'YOU')
    san_chain = chain(orbits, 'SAN')
    dprint("You:", you_chain)
    dprint("Santa:", san_chain)
    i = 0
    while you_chain[i] == san_chain[i]:
        i+=1
    return len(you_chain) + len(san_chain) - (i+1)*2

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
