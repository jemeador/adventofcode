#!/usr/bin/env python3
import fileinput
import pyperclip
import math
from collections import defaultdict

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def angle_wrap(angle):
    while angle < 0:
        angle += 360
    while angle > 360:
        angle -= 360
    return angle

def get_meteors(lines, station):
    meteors = defaultdict(list)
    sx, sy = station
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if (x, y) == station:
                continue
            if lines[y][x] == '#':
                dx = x - sx
                dy = y - sy
                angle = angle_wrap(90 - math.degrees(math.atan2(-dy,dx)))
                meteors[angle].append((x, y))
                meteors[angle].sort(key=lambda pos: math.pow(pos[0] - sx, 2) + math.pow(pos[1] - sy, 2))
    return meteors

def solve1(lines):
    most_visible_meteors = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] != '#':
                continue
            station = (x, y)
            meteors = get_meteors(lines, station)
            if most_visible_meteors < len(meteors):
                best_meteors = meteors
                best_position = station
                #dprint(station)
                #dprint(best_meteors)
                most_visible_meteors = len(meteors)

    blind_spots = []
    for angle, coord_list in best_meteors.items():
        # All but first visible meteor at the angle
        blind_spots += coord_list[1:]

    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if (x, y) == best_position:
                print('S', end=" ")
            elif (x, y) in blind_spots:
                print('X', end=" ")
            else:
                print(lines[y][x], end=" ")
        print()
    return most_visible_meteors

def solve2(lines):
    most_visible_meteors = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] != '#':
                continue
            station = (x, y)
            meteors = get_meteors(lines, station)
            if most_visible_meteors < len(meteors):
                best_meteors = meteors
                best_position = station
                #dprint(station)
                #dprint(best_meteors)
                most_visible_meteors = len(meteors)

    sorted_meteors = []
    for i in range(max([len(i) for i in best_meteors.values()])):
        for angle, coord_list in sorted(best_meteors.items()):
            if i < len(coord_list):
                sorted_meteors.append(coord_list[i])

    print(sorted_meteors)
    if 199 < len(sorted_meteors):
        coord = sorted_meteors[199]
        return coord[0] * 100 + coord[1]
    return 0

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
