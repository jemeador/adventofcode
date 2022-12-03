#!/usr/bin/env python3
import fileinput
import pyperclip
import itertools
import queue

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
    prog_in: queue.Queue
    prog_out: int
    is_halted: bool

    def __init__(self):
        self.prog_in = queue.SimpleQueue()
        self.pos = 0
        self.is_halted = False
        self.prog_out = None

    def __str__(self):
        out = str(self.ints)
        delimiter_positions = [pos for pos, char in enumerate(out) if char == ' ' or char == '[']
        carat_pos = delimiter_positions[self.pos] + 1
        out += '\n'
        for _ in range(carat_pos):
            out += ' '
        out += '^'
        #out = 'I/O:' + str(self.prog_in) + ',' + str(self.prog_out) + out
        return out

    def get(self, arg, mode) -> int:
        if mode == 0:
            return self.ints[arg]
        elif mode == 1:
            return arg
        dprint(f'ERROR mode == {mode}')

    def add(self):
        argc = 4
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2, ret = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        dprint(f'ADD: ints[{ret}] = {self.get(a1, m1)} + {self.get(a2, m2)}')
        self.ints[ret] = self.get(a1, m1) + self.get(a2, m2)
        self.pos += argc

    def mult(self):
        argc = 4
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2, ret = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        dprint(f'MUL: ints[{ret}] = {self.get(a1, m1)} * {self.get(a2, m2)}')
        self.ints[ret] = self.get(a1, m1) * self.get(a2, m2)
        self.pos += argc

    def input(self):
        argc = 2
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, ret = self.ints[self.pos:self.pos+argc]
        next_input = self.prog_in.get()
        dprint(f'INP: ints[{ret}] = {next_input}')
        self.ints[ret] = next_input
        self.pos += argc

    def output(self):
        argc = 2
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        dprint(f'OUT: prog_out = {self.get(a1, m1)}')
        self.prog_out = self.get(a1, m1)
        self.pos += argc

    def jump_if_true(self):
        argc = 3
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) != 0:
            dprint(f'IFJ: {self.get(a1, m1)} != 0, pos = {self.get(a2, m2)}')
            self.pos = self.get(a2, m2)
        else:
            dprint(f'IFJ: {self.get(a1, m1)} == 0')
            self.pos += argc

    def jump_if_false(self):
        argc = 3
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) == 0:
            dprint(f'ELJ: {self.get(a1, m1)} == 0, pos = {self.get(a2, m2)}')
            self.pos = self.get(a2, m2)
        else:
            dprint(f'ELJ: {self.get(a1, m1)} != 0')
            self.pos += argc

    def less_than(self):
        argc = 4
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2, a3 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) < self.get(a2, m2):
            dprint(f'LTH: {self.get(a1, m1)} < {self.get(a2, m2)}, self.ints[{a3}] = 1')
            self.ints[a3] = 1
        else:
            dprint(f'LTH: {self.get(a1, m1)} >= {self.get(a2, m2)}, self.ints[{a3}] = 0')
            self.ints[a3] = 0
        self.pos += argc

    def equals(self):
        argc = 4
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2, a3 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) == self.get(a2, m2):
            dprint(f'EQS: {self.get(a1, m1)} == {self.get(a2, m2)}, self.ints[{a3}] = 1')
            self.ints[a3] = 1
        else:
            dprint(f'EQS: {self.get(a1, m1)} != {self.get(a2, m2)}, self.ints[{a3}] = 0')
            self.ints[a3] = 0
        self.pos += argc

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
            elif opcode == 99:
                dprint('HALT')
                self.is_halted = True
                return self.prog_out
            else:
                return None

def solve1(lines):
    ints = [int(s) for s in lines[0].split(',')]
    inputs = range(1,5)
    permutations = itertools.permutations(inputs)
    solutions = []
    for p in permutations:
        next_input = 0
        for prog_in in p:
            prog = IntCodeProg()
            prog.ints = ints
            prog.pos = 0
            prog.prog_in.put(prog_in)
            prog.prog_in.put(next_input)
            prog.process()
            next_input = prog.prog_out
        solutions.append(next_input)
    return max(solutions)

def solve2(lines):
    ints = [int(s) for s in lines[0].split(',')]
    inputs = range(5,10)
    ids = ['A','B','C','D','E']
    permutations = itertools.permutations(inputs)
    solutions = []
    for p in permutations:
        progs = []
        for i in range(0, 5):
            progs.append(IntCodeProg())
            progs[i].prog_in.put(p[i])
            progs[i].ints = ints.copy()
        next_input = 0
        iters = 0
        while True:
            iters+=1
            for i in range(0, 5):
                progs[i].prog_in.put(next_input)
                dprint(f"=== Processing {ids[i]} ===")
                progs[i].process()
                next_input = progs[i].prog_out
            if progs[4].is_halted:
                solutions.append(next_input)
                dprint(f'Ran {iters} times')
                break
    return max(solutions)

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
