#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def add(ints, i):
    assert(ints[i] == 1)
    a1 = ints[i+1]
    a2 = ints[i+2]
    ret = ints[i+3]
    ints[ret] = ints[a1] + ints[a2]
    dprint('add', a1, a2)
    return ints, i+4

def mult(ints, i):
    assert(ints[i] == 2)
    a1 = ints[i+1]
    a2 = ints[i+2]
    ret = ints[i+3]
    ints[ret] = ints[a1] * ints[a2]
    dprint('mult', a1, a2)
    return ints, i+4

def process(ints, i):
    while True:
        dprint(ints)
        code = ints[i]
        if code == 1:
            ints, i = add(ints.copy(), i)
        elif code == 2:
            ints, i = mult(ints.copy(), i)
        elif code == 99:
            return ints
        else:
            return None

def solve1(lines):
    ints=[int(s) for s in lines[0].split(',')]
    ints[1] = 12
    ints[2] = 2
    ints = process(ints, 0)
    return ints[0]

def solve2(lines):
    prog=[int(s) for s in lines[0].split(',')]
    for noun in range(1, 99):
        for verb in range(1, 99):
            prog[1] = noun
            prog[2] = verb
            ints = process(prog, 0)
            if ints is not None and ints[0] == 19690720:
                return 100 * noun + verb
    return -1

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
