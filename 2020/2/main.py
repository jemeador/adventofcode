#!/usr/bin/env python3
import fileinput
import pyperclip

p1 = None
p2 = None

def solve1(lines):
    valid = 0
    for line in lines:
        r, letter, pw = line.split(' ')
        mini, maxi = r.split('-')
        minim = int(mini)
        maxim = int(maxi)
        letter = letter[0]
        count = 0
        for i in pw:
            if i == letter:
                count+=1
        if count >= minim and count <= maxim:
            valid+=1
    return valid


def solve2(lines):
    valid = 0
    for line in lines:
        r, letter, pw = line.split(' ')
        mini, maxi = r.split('-')
        pos1 = int(mini) - 1
        pos2 = int(maxi) - 1
        letter = letter[0]
        count = 0
        if pw[pos1] == letter:
            count+=1
        if pw[pos2] == letter:
            count+=1
        if count == 1:
            valid +=1
    return valid

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
