#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def nth_digit(val, n):
    return val // 10**n % 10

class IntCodeProg:
    ints: list
    pos: int
    prog_in: int
    prog_out: int

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
        self.ints[ret] = self.get(a1, m1) + self.get(a2, m2)
        dprint('add', self.get(a1, m1), self.get(a2, m2))
        self.pos += argc

    def mult(self):
        argc = 4
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2, ret = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        self.ints[ret] = self.get(a1, m1) * self.get(a2, m2)
        dprint('mult', self.get(a1, m1), self.get(a2, m2))
        self.pos += argc

    def input(self):
        argc = 2
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, ret = self.ints[self.pos:self.pos+argc]
        self.ints[ret] = self.prog_in
        self.pos += argc

    def output(self):
        argc = 2
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        self.prog_out = self.get(a1, m1)
        self.pos += argc

    def jump_if_true(self):
        argc = 3
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) != 0:
            self.pos = self.get(a2, m2)
        else:
            self.pos += argc

    def jump_if_false(self):
        argc = 3
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) == 0:
            self.pos = self.get(a2, m2)
        else:
            self.pos += argc

    def less_than(self):
        argc = 4
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2, a3 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) < self.get(a2, m2):
            self.ints[a3] = 1
        else:
            self.ints[a3] = 0
        self.pos += argc

    def equals(self):
        argc = 4
        dprint(self.ints[self.pos:self.pos+argc])
        opcode, a1, a2, a3 = self.ints[self.pos:self.pos+argc]
        m1 = nth_digit(opcode, 2)
        m2 = nth_digit(opcode, 3)
        if self.get(a1, m1) == self.get(a2, m2):
            self.ints[a3] = 1
        else:
            self.ints[a3] = 0
        self.pos += argc

    def process(self):
        while True:
            opcode = self.ints[self.pos] % 100
            if opcode == 1:
                self.add()
            elif opcode == 2:
                self.mult()
            elif opcode == 3:
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
                return self.prog_out
            else:
                return None

def solve1(lines):
    prog = IntCodeProg()
    prog.ints = [int(s) for s in lines[0].split(',')]
    prog.pos = 0
    prog.prog_in = 1
    return prog.process()

def solve2(lines):
    prog = IntCodeProg()
    prog.ints = [int(s) for s in lines[0].split(',')]
    prog.pos = 0
    prog.prog_in = 5
    return prog.process()

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
