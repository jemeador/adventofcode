import re

def get_uints(line):
    return [int(s) for s in re.findall(r'\d+', line)]

def get_ints(line):
    return [int(s) for s in re.findall(r'-?\d+', line)]

def get_line_groups(lines):
    return '\n'.join(lines).split('\n\n')

