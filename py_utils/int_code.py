import queue

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
        opcode = self.ints[self.pos]
        params = []
        for i in range(argc):
            arg = self.ints[self.pos + 1 + i]
            mode = opcode // 10**(2+i) % 10 # 2+ith digit from right
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
            return None
        while addr and addr >= len(self.ints):
            self.ints.append(0)
        self.ints[addr] = val

    def add(self):
        a1, a2, a3 = self.get_params(3)
        self.write(a3, self.read(a1) + self.read(a2))

    def mult(self):
        a1, a2, a3 = self.get_params(3)
        self.write(a3, self.read(a1) * self.read(a2))

    def input(self):
        a1, = self.get_params(1)
        next_input = self.prog_in.get()
        self.write(a1, next_input)

    def output(self):
        a1, = self.get_params(1)
        self.prog_out.put(self.read(a1))

    def jump_if_true(self):
        a1, a2 = self.get_params(2)
        if self.read(a1) != 0:
            self.pos = self.read(a2)

    def jump_if_false(self):
        a1, a2 = self.get_params(2)
        if self.read(a1) == 0:
            self.pos = self.read(a2)

    def less_than(self):
        a1, a2, a3 = self.get_params(3)
        if self.read(a1) < self.read(a2):
            self.write(a3, 1)
        else:
            self.write(a3, 0)

    def equals(self):
        a1, a2, a3 = self.get_params(3)
        if self.read(a1) == self.read(a2):
            self.write(a3, 1)
        else:
            self.write(a3, 0)

    def relative_base_offset(self):
        a1, = self.get_params(1)
        self.relative_base += self.read(a1)

    def process(self):
        while True:
            opcode = self.ints[self.pos] % 100
            if opcode == 1:
                self.add()
            elif opcode == 2:
                self.mult()
            elif opcode == 3:
                if self.prog_in.empty():
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
                self.is_halted = True
                return self.prog_out
            else:
                return None
