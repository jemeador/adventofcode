#!/usr/bin/env python3
import sys
sys.path.append('../..')
from py_utils.grid import print_grid

import fileinput
import pyperclip
import itertools
import queue
from collections import defaultdict

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

def nth_digit(val, n):
    return val // 10**n % 10

class IntCodeProg:
    ints: list
    pos: int
    relative_base: int
    prog_in: queue.Queue
    prog_out: queue.Queue
    is_halted: bool

    def __init__(self):
        self.prog_in = queue.SimpleQueue()
        self.pos = 0
        self.relative_base = 0
        self.is_halted = False
        self.prog_out = queue.SimpleQueue()

    def __str__(self):
        out = str(self.ints)
        delimiter_positions = [pos for pos, char in enumerate(out) if char == ' ' or char == '[']
        carat_pos = delimiter_positions[self.pos] + 1
        out += '\n'
        for _ in range(carat_pos):
            out += ' '
        out += '^'
        return out

    def get_params(self, argc):
        dprint(self, self.ints[self.pos:self.pos+argc+1])
        opcode = self.ints[self.pos]
        params = []
        for i in range(argc):
            arg = self.ints[self.pos + 1 + i]
            mode = nth_digit(opcode, 2 + i)
            params.append((arg, mode))
        self.pos += argc + 1
        return params

    def read(self, param) -> int:
        arg, mode = param
        addr = None
        if mode == 0:
            addr = arg
        elif mode == 1:
            return arg
        elif mode == 2:
            addr = self.relative_base + arg
        else:
            dprint(f'ERROR mode == {mode}')
            return None
        while addr and addr >= len(self.ints):
            self.ints.append(0)
        return self.ints[addr]

    def write(self, param, val) -> int:
        arg, mode = param
        addr = None
        if mode == 0:
            addr = arg
        elif mode == 2:
            addr = self.relative_base + arg
        else:
            dprint(f'ERROR mode == {mode}')
            return None
        while addr and addr >= len(self.ints):
            self.ints.append(0)
        self.ints[addr] = val

    def add(self):
        a1, a2, a3 = self.get_params(3)
        dprint(f'ADD: self.write({a3}, {self.read(a1)} + {self.read(a2)}')
        self.write(a3, self.read(a1) + self.read(a2))

    def mult(self):
        a1, a2, a3 = self.get_params(3)
        dprint(f'MUL: self.write({a3}, {self.read(a1)} * {self.read(a2)}')
        self.write(a3, self.read(a1) * self.read(a2))

    def input(self):
        a1, = self.get_params(1)
        next_input = self.prog_in.get()
        dprint(f'INP: self.write({a1}, {next_input})')
        self.write(a1, next_input)

    def output(self):
        a1, = self.get_params(1)
        dprint(f'OUT: prog_out.put({self.read(a1)})')
        self.prog_out.put(self.read(a1))

    def jump_if_true(self):
        a1, a2 = self.get_params(2)
        if self.read(a1) != 0:
            dprint(f'IFJ: {self.read(a1)} != 0, pos = {self.read(a2)}')
            self.pos = self.read(a2)
        else:
            dprint(f'IFJ: {self.read(a1)} == 0')

    def jump_if_false(self):
        a1, a2 = self.get_params(2)
        if self.read(a1) == 0:
            dprint(f'ELJ: {self.read(a1)} == 0, pos = {self.read(a2)}')
            self.pos = self.read(a2)
        else:
            dprint(f'ELJ: {self.read(a1)} != 0')

    def less_than(self):
        a1, a2, a3 = self.get_params(3)
        if self.read(a1) < self.read(a2):
            dprint(f'LTH: {self.read(a1)} < {self.read(a2)}, self.write({a3}, 1)')
            self.write(a3, 1)
        else:
            dprint(f'LTH: {self.read(a1)} >= {self.read(a2)}, self.write({a3}, 0)')
            self.write(a3, 0)

    def equals(self):
        a1, a2, a3 = self.get_params(3)
        if self.read(a1) == self.read(a2):
            dprint(f'EQS: {self.read(a1)} == {self.read(a2)}, self.write({a3}, 1)')
            self.write(a3, 1)
        else:
            dprint(f'EQS: {self.read(a1)} != {self.read(a2)}, self.write({a3}, 0)')
            self.write(a3, 0)

    def relative_base_offset(self):
        a1, = self.get_params(1)
        dprint(f'RBO: relative_base += {self.read(a1)}; now: {self.relative_base + self.read(a1)}')
        self.relative_base += self.read(a1)

    def process(self):
        while True:
            dprint(self)
            opcode = self.ints[self.pos] % 100
            if opcode == 1:
                self.add()
            elif opcode == 2:
                self.mult()
            elif opcode == 3:
                if self.prog_in.empty():
                    dprint(f'WAIT')
                    return None
                self.input()
            elif opcode == 4:
                self.output()
            elif opcode == 5:
                self.jump_if_true()
            elif opcode == 6:
                self.jump_if_false()
            elif opcode == 7:
                self.less_than()
            elif opcode == 8:
                self.equals()
            elif opcode == 9:
                self.relative_base_offset()
            elif opcode == 99:
                dprint('HALT')
                self.is_halted = True
                return self.prog_out
            else:
                return None

def paint(lines, start):
    ints = [int(s) for s in lines[0].split(',')]
    prog = IntCodeProg()
    prog.ints = ints
    prog.pos = 0
    cells = defaultdict(int)
    pos = (0, 0)
    di = 0
    d_map = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    cells[pos] = start
    while not prog.is_halted:
        prog.prog_in.put(cells[pos])
        prog.process()
        new_color = prog.prog_out.get()
        turn_right = prog.prog_out.get()
        cells[pos] = new_color
        if turn_right:
            di = (di + 1) % 4
        else:
            di = (di - 1) % 4
        dx, dy = d_map[di]
        pos = (pos[0] + dx, pos[1] + dy)

    def print_cell(c):
        if c:
            return '# '
        else:
            return '  '

    print_grid(cells, print_cell)

    return len(cells)

def solve1(lines):
    return paint(lines, 0)

def solve2(lines):
    return paint(lines, 1)

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
