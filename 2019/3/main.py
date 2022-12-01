#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def intersection(ray1, ray2):
    p11, p12 = ray1
    p21, p22 = ray2

    ray1_is_vert = p11[0] == p12[0]
    ray2_is_vert = p21[0] == p22[0]

    if ray1_is_vert == ray2_is_vert:
        return None

    if ray2_is_vert:
        return intersection(ray2, ray1)

    x = p11[0]
    y = p21[1]
    print(x, y)
    ix = x >= min(p21[0], p22[0]) and x <= max(p21[0], p22[0])
    iy = y >= min(p11[1], p12[1]) and y <= max(p11[1], p12[1])
    if ix and iy:
        if x != 0 and y != 0:
            print("Intersection found")
            return x, y
    return None

def solve1(lines):
    intersections = []
    first_wire_rays = []
    for i in range(0,2):
        line = lines[i]
        rays = []
        spans = line.split(',')
        p1 = (0, 0)
        for span in spans:
            direction = span[0]
            val = int(span[1:])
            dprint(direction, val)
            p2 = p1
            if direction == 'R':
                p2 = (p2[0] + val, p2[1])
            if direction == 'L':
                p2 = (p2[0] - val, p2[1])
            if direction == 'D':
                p2 = (p2[0], p2[1] + val)
            if direction == 'U':
                p2 = (p2[0], p2[1] - val)
            new_ray = (p1, p2)
            if i == 0:
                first_wire_rays.append(new_ray)
            elif i == 1:
                for ray in first_wire_rays:
                    inter = intersection(new_ray, ray)
                    if inter:
                        intersections.append(inter)
            p1 = p2
    dists = [abs(x) + abs(y) for x, y in intersections]
    return min(dists)

def get_steps(rays, x, y):
    steps = 0
    for ray in rays:
        p1, p2 = ray
        is_vert = p1[0] == p2[0]
        if is_vert:
            if x == p1[0]:
                iy = y >= min(p1[1], p2[1]) and y <= max(p1[1], p2[1])
                steps += abs(p1[1] - y)
                return steps
            steps += abs(p2[1] - p1[1])
        else:
            if y == p1[1]:
                ix = x >= min(p1[0], p2[0]) and x <= max(p1[0], p2[0])
                steps += abs(p1[0] - x)
                return steps
            steps += abs(p2[0] - p1[0])

def solve2(lines):
    intersections = []
    first_wire_rays = []
    second_wire_rays = []
    for i in range(0,2):
        line = lines[i]
        rays = []
        spans = line.split(',')
        p1 = (0, 0)
        for span in spans:
            direction = span[0]
            val = int(span[1:])
            dprint(direction, val)
            p2 = p1
            if direction == 'R':
                p2 = (p2[0] + val, p2[1])
            if direction == 'L':
                p2 = (p2[0] - val, p2[1])
            if direction == 'D':
                p2 = (p2[0], p2[1] + val)
            if direction == 'U':
                p2 = (p2[0], p2[1] - val)
            new_ray = (p1, p2)
            if i == 0:
                first_wire_rays.append(new_ray)
            elif i == 1:
                second_wire_rays.append(new_ray)
                for ray in first_wire_rays:
                    inter = intersection(new_ray, ray)
                    if inter:
                        intersections.append(inter)
            p1 = p2
    steps = [get_steps(first_wire_rays, x, y) + get_steps(second_wire_rays, x, y) for x, y in intersections]
    return min(steps)

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
