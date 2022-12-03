#!/usr/bin/env python3
import fileinput
import pyperclip
import re
from collections import defaultdict
from copy import deepcopy

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def solve1(lines):
# <x=-3, y=10, z=-1>
# <x=-12, y=-10, z=-5>
# <x=-9, y=0, z=10>
# <x=7, y=-5, z=-3>
    pp=defaultdict(list)
    pv=defaultdict(list)
    for line in lines:
        x, y, z = [int(s) for s in re.findall(r'-?\d+', line)]
        pp['x'].append(x)
        pp['y'].append(y)
        pp['z'].append(z)
        pv['x'].append(0)
        pv['y'].append(0)
        pv['z'].append(0)

    for i in range(0, 1000):
        dprint(f'After {i} steps')
        for index in range(4):
            dprint(f'pos=<', end="")
            for axis, pos_vals in pp.items():
                dprint(f'{axis}={pos_vals[index]}', end=",")
            dprint('>', end=",")
            dprint(f'vel=<', end="")
            for axis, vel_vals in pv.items():
                dprint(f'{axis}={vel_vals[index]}', end=",")
            dprint('>')
        for axis, pos_vals in pp.items():
            vel_vals = pv[axis]
            for index in range(len(pos_vals)):
                vel = pos_vals[index]
                for other_index in range(len(pos_vals)):
                    other_vel = pos_vals[other_index]
                    if vel > other_vel:
                        vel_vals[index] -= 1
                    elif vel < other_vel:
                        vel_vals[index] += 1
        for axis, vel_vals in pv.items():
            pos_vals = pp[axis]
            for index in range(len(pos_vals)):
                pos_vals[index] += vel_vals[index]
        dprint(f'After {i} steps')
    for index in range(4):
        dprint(f'pos=<', end="")
        for axis, pos_vals in pp.items():
            dprint(f'{axis}={pos_vals[index]}', end=",")
        dprint('>', end=",")
        dprint(f'vel=<', end="")
        for axis, vel_vals in pv.items():
            dprint(f'{axis}={vel_vals[index]}', end=",")
        dprint('>')

    te=[]
    for index in range(4):
        pe = 0
        ke = 0
        for axis, pos_vals in pp.items():
            pe += abs(pos_vals[index])
        for axis, vel_vals in pv.items():
            ke += abs(vel_vals[index])
        te.append(pe * ke)

    return sum(te)

def solve2(lines):
    pp=defaultdict(list)
    pv=defaultdict(list)
    for line in lines:
        x, y, z = [int(s) for s in re.findall(r'-?\d+', line)]
        pp['x'].append(x)
        pp['y'].append(y)
        pp['z'].append(z)
        pv['x'].append(0)
        pv['y'].append(0)
        pv['z'].append(0)


    cycles=[]
    for axis, pos_vals in pp.items():
        vel_vals = pv[axis]
        orig_pos_vals = deepcopy(pos_vals)
        orig_vel_vals = deepcopy(vel_vals)
        i = 0
        print(f'Calc {axis}')
        while orig_pos_vals != pos_vals or orig_vel_vals != vel_vals or i == 0:
            for index in range(len(pos_vals)):
                vel = pos_vals[index]
                for other_index in range(len(pos_vals)):
                    other_vel = pos_vals[other_index]
                    if vel > other_vel:
                        vel_vals[index] -= 1
                    elif vel < other_vel:
                        vel_vals[index] += 1
            for index in range(len(pos_vals)):
                pos_vals[index] += vel_vals[index]
            i+=1
        cycles.append(i)
    common_factors=defaultdict(int)
    for cycle in cycles:
        factors=defaultdict(int)
        for val in prime_factors(cycle):
            factors[val]+=1
        for val, count in factors.items():
            common_factors[val] = max(common_factors[val], factors[val])
    ret = 1;
    for val, n in common_factors.items():
        for _ in range(n):
            ret *= val

    return ret

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
