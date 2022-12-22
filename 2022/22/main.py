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
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def solve1(lines):
    r = 0
    grid = make_ascii_grid(lines[:-2])
    print_grid(grid)
    path = lines[-1]
    num_token = ''
    seq = []
    for i in range(len(path)):
        ch = path[i]
        if ch.isnumeric():
            num_token += ch
        else:
            seq.append(num_token)
            num_token = ''
            seq.append(ch)
    seq.append(num_token)
    print(seq)

    for coord in get_coords(grid, '.'):
        pos = coord
        break
    facing = 0

    print(pos)
    path_grid = grid.copy()
    max_x = grid_max_x(grid)
    max_y = grid_max_y(grid)
    path_ch = ['>', 'v', '<', '^']

    for item in seq:
        #print('Processing', item)
        if item.isnumeric():
            count = int(item)
            for i in range(count):
                #print(i)
                next_pos = add_coords(pos, dirs[facing])
                #print(next_pos)
                if next_pos not in grid or grid[next_pos] == ' ':
                    if facing == 0:
                        next_pos = Coord(0, next_pos[1])
                    elif facing == 1:
                        next_pos = Coord(next_pos[0], 0)
                    elif facing == 2:
                        next_pos = Coord(max_x, next_pos[1])
                    elif facing == 3:
                        next_pos = Coord(next_pos[0], max_y)
                    if next_pos[0] > max_x:
                        next_pos = Coord(max_x, next_pos[1])
                    elif next_pos[1] > max_y:
                        next_pos = Coord(next_pos[0], max_y)
                    while next_pos not in grid or grid[next_pos] == ' ':
                        next_pos = add_coords(next_pos, dirs[facing])
                if grid[next_pos] == '.':
                    pos = next_pos
                    path_grid[pos] = path_ch[facing]
                elif grid[next_pos] == '#':
                    break
            #print_grid(path_grid)
        else:
            if item == 'R':
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4
    print(pos)
    print_grid(path_grid, str)
    print(pos, facing)
    return 1000 * (pos[1]+1) + 4 * (pos[0]+1) + facing

# AUGH globals
side_len = None

def get_macro_coord(side_len, coord):
    return Coord(coord.x // side_len, coord.y // side_len)

def get_relative_coord(side_len, coord):
    print('Macro/side', get_macro_coord(side_len, coord), side_len)
    origin = mult_coord(get_macro_coord(side_len, coord), side_len)
    print('Origin', origin)
    return sub_coords(coord, origin)

def make_cube(grid, side_len):
    side_grid = grid.copy()
    side_map = {}
    rotation_map = {}
    if side_len == 4: # sample
        side_map[Coord(2, 0)] = 1
        side_map[Coord(0, 1)] = 2
        side_map[Coord(1, 1)] = 3
        side_map[Coord(2, 1)] = 4
        side_map[Coord(2, 2)] = 5
        side_map[Coord(3, 2)] = 6

        side_map[1] = Coord(2, 0)
        side_map[2] = Coord(0, 1)
        side_map[3] = Coord(1, 1)
        side_map[4] = Coord(2, 1)
        side_map[5] = Coord(2, 2)
        side_map[6] = Coord(3, 2)
        # side, facing = new_side, new_facing
        rotation_map[1, 0] = (6, 2)
        rotation_map[1, 1] = None
        rotation_map[1, 2] = (3, 1)
        rotation_map[1, 3] = (2, 1)
        rotation_map[2, 0] = None
        rotation_map[2, 1] = (5, 3)
        rotation_map[2, 2] = (6, 2)
        rotation_map[2, 3] = (1, 1)
        rotation_map[3, 0] = None
        rotation_map[3, 1] = (5, 1)
        rotation_map[3, 2] = None
        rotation_map[3, 3] = (1, 0)
        rotation_map[4, 0] = (6, 1)
        rotation_map[4, 1] = None
        rotation_map[4, 2] = None
        rotation_map[4, 3] = None
        rotation_map[5, 0] = None
        rotation_map[5, 1] = (2, 3)
        rotation_map[5, 2] = (3, 3)
        rotation_map[5, 3] = None
        rotation_map[6, 0] = (1, 2)
        rotation_map[6, 1] = (2, 0)
        rotation_map[6, 2] = None
        rotation_map[6, 3] = (4, 2)
    else:
        side_map[Coord(1, 0)] = 1
        side_map[Coord(2, 0)] = 2
        side_map[Coord(1, 1)] = 3
        side_map[Coord(0, 2)] = 4
        side_map[Coord(1, 2)] = 5
        side_map[Coord(0, 3)] = 6

        side_map[1] = Coord(1, 0)
        side_map[2] = Coord(2, 0)
        side_map[3] = Coord(1, 1)
        side_map[4] = Coord(0, 2)
        side_map[5] = Coord(1, 2)
        side_map[6] = Coord(0, 3)
        # side, facing = new_side, new_facing
        rotation_map[1, 0] = None
        rotation_map[1, 1] = None
        rotation_map[1, 2] = (4, 0)
        rotation_map[1, 3] = (6, 0)
        rotation_map[2, 0] = (5, 2)
        rotation_map[2, 1] = (3, 2)
        rotation_map[2, 2] = None
        rotation_map[2, 3] = (6, 3)
        rotation_map[3, 0] = (2, 3)
        rotation_map[3, 1] = None
        rotation_map[3, 2] = (4, 1)
        rotation_map[3, 3] = None
        rotation_map[4, 0] = None
        rotation_map[4, 1] = None
        rotation_map[4, 2] = (1, 0)
        rotation_map[4, 3] = (3, 0)
        rotation_map[5, 0] = (2, 2)
        rotation_map[5, 1] = (6, 2)
        rotation_map[5, 2] = None
        rotation_map[5, 3] = None
        rotation_map[6, 0] = (5, 3)
        rotation_map[6, 1] = (2, 1)
        rotation_map[6, 2] = (1, 1)
        rotation_map[6, 3] = None
    for coord, cell in grid.items():
        macro_coord = get_macro_coord(side_len, coord)
        if cell != ' ':
            side_grid[coord] = str(side_map[macro_coord])
    return (side_map, rotation_map)

def apply_spin(coord, spin, side_len):
    s = side_len - 1
    x, y = coord
    if spin == 0:
        return Coord(x, y)
    if spin == 1:
        return Coord(s-y, x)
    if spin == 2:
        return Coord(s-x, s-y)
    if spin == 3:
        return Coord(y, s-x)
    assert(False)

def wrap_offset(grid, cube, side_len, pos, facing):
    side_map, rotation_map = cube
    new_pos = add_coords(pos, dirs[facing])
    new_facing = facing
    if new_pos not in grid or grid[new_pos] == ' ':
        side = side_map[get_macro_coord(side_len, pos)]
        rotation = rotation_map[side, facing]
        print('Side/Facing', side, facing)
        assert(rotation is not None)
        new_side, new_facing = rotation
        print('New Side/Facing', new_side, new_facing)
        spin = (new_facing - facing) % 4
        print('Spin', spin)
        relative_pos = get_relative_coord(side_len, pos)
        print('Relative[0]', relative_pos)
        relative_next_pos = add_coords(relative_pos, dirs[facing])
        print('Relative[1]', relative_next_pos)
        relative_next_pos = apply_spin(relative_next_pos, spin, side_len)
        print('Relative[2]', relative_next_pos)
        if relative_next_pos.x >= side_len:
            relative_next_pos = Coord(0, relative_next_pos.y)
        elif relative_next_pos.y >= side_len:
            relative_next_pos = Coord(relative_next_pos.x, 0)
        elif relative_next_pos.x < 0:
            relative_next_pos = Coord(side_len - 1, relative_next_pos.y)
        elif relative_next_pos.y < 0:
            relative_next_pos = Coord(relative_next_pos.x, side_len - 1)
        print('Relative wrapped', relative_next_pos)
        macro_next_pos = side_map[new_side]
        new_pos = Coord(macro_next_pos.x * side_len, macro_next_pos.y * side_len)
        print('New pos(0)', new_pos)
        new_pos = add_coords(new_pos, relative_next_pos)
        print('New pos(1)', new_pos)
    if grid[new_pos] == '.':
        return new_pos, new_facing
    elif grid[new_pos] == '#':
        return None, None
    assert(False)

def solve2(lines):
    r = 0
    grid = make_ascii_grid(lines[:-2])
    print_grid(grid)
    side_len = int((max(grid_max_x(grid), grid_max_y(grid)) + 1) // 4)
    cube = make_cube(grid, side_len)
    path = lines[-1]
    num_token = ''
    seq = []
    for i in range(len(path)):
        ch = path[i]
        if ch.isnumeric():
            num_token += ch
        else:
            seq.append(num_token)
            num_token = ''
            seq.append(ch)
    seq.append(num_token)

    for coord in get_coords(grid, '.'):
        pos = coord
        break
    facing = 0

    path_grid = grid.copy()
    max_x = grid_max_x(grid)
    max_y = grid_max_y(grid)
    path_ch = ['>', 'v', '<', '^']

    for item in seq:
        #print('Processing', item)
        if item.isnumeric():
            count = int(item)
            for i in range(count):
                next_pos, next_facing = wrap_offset(grid, cube, side_len, pos, facing)
                if not next_pos:
                    break
                pos, facing = next_pos, next_facing
                path_grid[pos] = path_ch[facing]
                print(pos, facing)
        else:
            if item == 'R':
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4
            print(pos, facing)
    print_grid(path_grid, str)
    print(pos, facing)
    return 1000 * (pos[1]+1) + 4 * (pos[0]+1) + facing

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
