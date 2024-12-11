#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import *
from py_utils.fast_parse import *
from py_utils.search import *

from collections import defaultdict

import fileinput
import itertools
import math
import os
import pyperclip
import queue
import re
import time

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def normalize(module_name):
    module_name = module_name.strip()
    if module_name.startswith('%') or module_name.startswith('&'):
        return module_name[1:]
    return module_name

def solve1(lines, need_rx = False):
    r = 0
    modules = {}
    flip_flop_states = defaultdict(int)
    conjunction_states = defaultdict(dict)

    signal_queue = []
    signal_count = defaultdict(int)
    found_rx = False

    def send_signal(src, dest, signal):
        signal_queue.append((src, dest, signal))
        signal_str = 'low'
        if signal == 1:
            signal_str = 'high'
        signal_count[signal] += 1
        if need_rx and dest == 'rx':
            found_rx = True

    for line in lines:
        line = line.strip()
        src,_ = line.split('->')
        if src.startswith('&'):
            conjunction_states[normalize(src)] = {}
        if src.startswith('%'):
            flip_flop_states[normalize(src)] = 0

    for line in lines:
        line = line.strip()
        src,dests_str = line.split('->')
        dests = [normalize(dest.strip()) for dest in dests_str.split(',')]
        modules[normalize(src.strip())] = dests
        for dest in dests:
            if dest in conjunction_states:
                conjunction_states[normalize(dest)][normalize(src)] = 0

    cycles = {}
    prev = {}
    presses = 1000
    if need_rx:
        presses = 10000000000000000000000
    for n in range(presses):
        send_signal('button', 'broadcaster', 0)
        while len(signal_queue) > 0:
            sender,module,signal = signal_queue.pop(0)
            if module not in modules:
                continue
            dests = modules[module]
            if module in flip_flop_states:
                if signal == 0:
                    flip_flop_states[module] += 1
                    flip_flop_states[module] %= 2
                    for dest in dests:
                        send_signal(module, dest, flip_flop_states[module])
            elif module in conjunction_states:
                conjunction_states[module][sender] = signal
                pulse = 0
                for dest, signal in conjunction_states[module].items():
                    if signal == 0:
                        pulse = 1
                        break
                for dest in dests:
                    send_signal(module, dest, pulse)
            else:
                for dest in dests:
                    send_signal(module, dest, signal)
        if need_rx and found_rx:
            return n
        for module, memory in conjunction_states.items():
            reset = True
            for val in memory.values():
                if val == 1:
                    reset = False
            if module in prev and reset != prev[module] and module not in cycles:
                cycles[module] = n
                print(module, ' cycle = ', n)
            prev[module] = reset
        for module, memory in flip_flop_states.items():
            if memory and module not in cycles:
                cycles[module] = n
                print(module, ' cycle = ', n)
    print('low', signal_count[0], 'high', signal_count[1])
    return signal_count[0] * signal_count[1]

def solve2(lines):
    return solve1(lines, need_rx=True)

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
