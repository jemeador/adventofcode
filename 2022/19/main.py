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

Resources = namedtuple('Resources', 'ore clay obsidian geode')
RobotNode = namedtuple('RobotNode', 'robots resources time_remaining')

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

type_map = {'ore': ORE, 'clay': CLAY, 'obsidian': OBSIDIAN, 'geode': GEODE }

def accumulate(starting_resources, robots, time):
    new_resources = list(starting_resources)
    for _, resource_type in type_map.items():
        new_resources[resource_type] += robots[resource_type] * time
    return Resources(*new_resources)

def time_required(starting_resources, robots, recipe):
    time = 0
    for count, resource_type in recipe:
        resource_req = count - starting_resources[resource_type]
        if resource_req > 0 and robots[resource_type] == 0:
            return math.inf
        time_req = resource_req // robots[resource_type]
        if resource_req % robots[resource_type] > 0:
            time_req += 1
        time = max(time_req, time)
    return time

def pay_cost(starting_resources, recipe):
    new_resources = list(starting_resources)
    for count, resource_type in recipe:
        new_resources[resource_type] -= count
    return Resources(*new_resources)

def add_robot(starting_robots, robot_type):
    new_robots = list(starting_robots)
    new_robots[robot_type] += 1
    return Resources(*new_robots)

class RobotGraph:
    def __init__(self, recipes):
        self.recipes = recipes

    def is_end_node(self, node):
        return node.time_remaining <= 0

    def calc_heuristic(self, node):
        score = 0
        for t in range(node.time_remaining):
            score += t + node.robots.geode
        return score

    def edges_from(self, src):
        for robot_type, recipe in self.recipes.items():
            if robot_type == GEODE and src.time_remaining <= 1:
                break
            if robot_type != GEODE and src.time_remaining <= 2:
                continue
            if robot_type == ORE and src.robots.ore >= 4:
                continue
            dt = time_required(src.resources, src.robots, recipe) + 1
            if math.isinf(dt):
                continue
            new_time_remaining = src.time_remaining - dt
            if new_time_remaining < 0:
                continue
            dprint(f"Expanding build {robot_type} from {src}")
            new_resources = pay_cost(accumulate(src.resources, src.robots, dt), recipe)
            new_robots = add_robot(src.robots, robot_type)
            new_node = RobotNode(new_robots, new_resources, new_time_remaining)
            yield new_node, dt * src.robots.geode
        dprint(f"Expanding do nothing from {src}")
        dt = src.time_remaining
        new_resources = accumulate(src.resources, src.robots, dt)
        new_node = RobotNode(src.robots, new_resources, 0)
        yield new_node, dt * src.robots.geode

def solve1(lines):
    r = 0
    blueprint_id = 1
    for line in lines:
        recipes = defaultdict(list)
        for recipe in line.split('Each')[1:]:
            robot_type, ingredients = recipe.split(' robot costs ')
            robot_type = type_map[robot_type.strip()]
            for ingredient in ingredients.split('and'):
                ingredient = ingredient.strip()
                ingredient = ingredient.replace('.', '')
                count, type_str = ingredient.split(' ')
                recipes[robot_type].append((int(count), type_map[type_str]))
        print(recipes)
        starting_robots = Resources(1, 0, 0, 0)
        starting_resources = Resources(0, 0, 0, 0)
        graph = RobotGraph(recipes)
        _, score, path = find_path(graph, RobotNode(starting_robots, starting_resources, 24),
                is_end_node=lambda n: RobotGraph.is_end_node(graph, n),
                calc_heuristic=lambda n, _: RobotGraph.calc_heuristic(graph, n), maximize=True)
        #for p in path:
            #print(p)
        r += blueprint_id * path[-1].resources.geode
        print (blueprint_id, path[-1].resources.geode)
        blueprint_id += 1
    return r

def solve2(lines):
    r = 1
    blueprint_id = 1
    for line in lines[:3]:
        recipes = defaultdict(list)
        for recipe in line.split('Each')[1:]:
            robot_type, ingredients = recipe.split(' robot costs ')
            robot_type = type_map[robot_type.strip()]
            for ingredient in ingredients.split('and'):
                ingredient = ingredient.strip()
                ingredient = ingredient.replace('.', '')
                count, type_str = ingredient.split(' ')
                recipes[robot_type].append((int(count), type_map[type_str]))
        print(recipes)
        starting_robots = Resources(1, 0, 0, 0)
        starting_resources = Resources(0, 0, 0, 0)
        graph = RobotGraph(recipes)
        _, score, path = find_path(graph, RobotNode(starting_robots, starting_resources, 32),
                is_end_node=lambda n: RobotGraph.is_end_node(graph, n),
                calc_heuristic=lambda n, _: RobotGraph.calc_heuristic(graph, n), maximize=True)
        #for p in path:
            #print(p)
        r *= path[-1].resources.geode
        print (blueprint_id, path[-1].resources.geode)
        blueprint_id += 1
    return r

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
