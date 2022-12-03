#!/usr/bin/env python3
import fileinput
import pyperclip

def dprint(*args, **kwargs):
    if True:
        return print(*args, **kwargs)

p1 = None
p2 = None

def solve1(lines):
    data = lines[0]
    w = 25
    h = 6
    layer_counts = {}
    l = 0
    while l*w*h < len(data):
        counts = [0, 0, 0]
        for y in range(0,h):
            for x in range(0,w):
                cell = int(data[l*h*w + y*w + x])
                counts[cell]+=1
        layer_counts[l] = counts
        print(counts)
        l+=1
    index, counts = min(layer_counts.items(), key = lambda x: x[1][0])
    print(len(layer_counts))
    return counts[1] * counts[2]

def solve2(lines):
    data = lines[0]
    w = 25
    h = 6
    l = 0
    image = [' '] * w * h
    for l in reversed(range(100)):
        for c in range(h*w):
            color = data[l*w*h + c]
            if color == '1':
                image[c] = '#'
            elif color == '0':
                image[c] = ' '
    image = ''.join(image)
    for y in range(h):
        print(image[y*w:(y+1)*w])
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
        print(p1)
        pyperclip.copy(p1)
    if p2 is not None:
        print(p2)
        pyperclip.copy(p2)
