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

def dprint(*args, **kwargs):
    if False:
        return print(*args, **kwargs)

p1 = None
p2 = None

block_text = [
['@@@@'],

['.@.',
 '@@@',
 '.@.'],

['..@',
 '..@',
 '@@@'],

['@',
 '@',
 '@',
 '@'],

['@@',
 '@@'],
]

class Tetris:
    def __init__(self, line):
        self.b = 0
        self.j = 0
        self.g = defaultdict(str)
        self.g[Coord(0,0)] = '.'
        self.blocks = []
        self.block_coords = []
        self.jets = line
        self.min_y = 0
        for text in block_text:
            block = make_ascii_grid(text)
            self.blocks.append(block)

    def top_rock(self):
        for y in range(self.min_y, 1):
            for x in range(0, 7):
                if self.g[Coord(x, y)] == '#':
                    return y
        return 0

    def start_y(self, block):
        return (self.top_rock() - 1) - (grid_max_y(block) + 3)

    def add_block(self):
        block = self.blocks[self.b % len(self.blocks)]
        start = Coord(2, self.start_y(block))
        for y in range(self.start_y(block) - grid_max_y(block), self.start_y(block) + 4):
            for x in range(0, 7):
                self.g[Coord(x, y)] = '.'
        self.block_coords = []
        for coord, cell in block.items():
            grid_coord = add_coords(coord, start)
            if cell == '@':
                self.block_coords.append(grid_coord)
        self.b += 1

    def move(self, offset):
        for coord in self.block_coords:
            dest_coord = add_coords(coord, offset)
            dprint(f'Trying {coord}->{dest_coord}')
            if self.g[dest_coord] == '#':
                dprint(f'Failed to move {coord}->{dest_coord} (block)')
                return False
            if dest_coord.x < 0 or dest_coord.x >= 7:
                dprint(f'Failed to move {coord}->{dest_coord} (out of x range)')
                return False
            if dest_coord.y >= 0:
                dprint(f'Failed to move {coord}->{dest_coord} (out of y range)')
                return False
        new_coords = []
        for coord in self.block_coords:
            new_coord = add_coords(coord, offset)
            self.min_y = min(self.min_y, new_coord.y)
            new_coords.append(new_coord)
        self.block_coords = new_coords
        return True

    def land_block(self):
        for coord in self.block_coords:
            self.g[coord] = '#'

    def iterate(self):
        dir_ch = self.jets[self.j % len(self.jets)]
        offset = Coord(0,0)
        if dir_ch == '<':
            offset = Coord(-1,0)
        if dir_ch == '>':
            offset = Coord(1,0)
        self.move(offset)
        self.j += 1
        if not self.move(Coord(0,1)):
            self.land_block()
            self.add_block()

    def solution1(self):
        return -1 * self.top_rock()

    def print(self):
        lines = []
        for y in range(self.min_y, self.min_y + 10):
            line = []
            for x in range(0, 7):
                line.append(self.g[x, y])
            txt = ''.join(line)
            lines.append(txt)
        return '\n'.join(lines)

def solve1(lines):
    r = 0

    tetris = Tetris(lines[0])
    tetris.add_block()

    while tetris.b <= 2022:
        print(tetris.b)
        tetris.iterate()

    return tetris.solution1()

def solve2(lines):
    r = 0

    tetris = Tetris(lines[0])
    tetris.add_block()

    head_height = None
    head_blocks = None
    pattern_height = None
    num_patterns = None
    prev_lines = None
    period = None
    while tetris.b <= 1e12:
        if tetris.j % (len(tetris.jets) * 5) == 0:
            blocks_placed = tetris.b - 1
            print(blocks_placed)
            lines = tetris.print()
            print(lines)
            if not head_height and tetris.j != 0:
                head_height = tetris.solution1()
                head_blocks = blocks_placed
                print('head_height=', head_height)
            elif head_height and not pattern_height:
                pattern_height = tetris.solution1() - head_height
                pattern_blocks = blocks_placed - head_blocks
                remaining_blocks = (1000000000000 - head_blocks) % pattern_blocks
                num_patterns =     (1000000000000 - head_blocks) // pattern_blocks
                tetris.b =         (1000000000000 - remaining_blocks) + 1
                print('pattern_height=', head_height)
                print('num_patterns=', num_patterns)
            prev_lines = lines
        tetris.iterate()
    tail_height = tetris.solution1() - pattern_height - head_height
    print('tail_height=', tail_height)
    r = head_height + pattern_height * num_patterns + tail_height
    print(f'{head_height} + {pattern_height} * {num_patterns} + {tail_height}')
    print('total blocks', head_blocks + pattern_blocks * num_patterns + remaining_blocks)
    assert(head_blocks + pattern_blocks * num_patterns + remaining_blocks == 1000000000000)
    print(f'{head_blocks} + {pattern_height} * {num_patterns} + {tail_height}')
    return r

if __name__ == "__main__":
    f = fileinput.input()
    lines = []
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        lines.append(line)
    ##p1 = solve1(lines)
    p2 = solve2(lines)
    if p1 is not None:
        print("Solution 1:", p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print("Solution 2:", p2)
        pyperclip.copy(p2)
