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

Valve = namedtuple("Valve", "rate id")
Node = namedtuple("Node", "valves_opened valves_opened2")
Graph = namedtuple("Graph", "edges valves valve_rates_by_id")
PqElement = namedtuple("PqElement", "score node")

def branch(valves, node, participants):
    for rate, valve_id in valves:
        if valve_id not in node.valves_opened and valve_id not in node.valves_opened2:
            valves_opened = set(node.valves_opened)
            valves_opened2 = set(node.valves_opened2)
            valves_opened.add(valve_id)
            yield Node(valves_opened + [valve_id], valves_opened2)
            # Once we start adding to the first list, stop adding to the second to avoid duplicate nodej
            if participants == 2 and len(valves_opened) == 1:
                valves_opened2.add(valve_id)
                yield Node(valves_opened, frozenset(valves_opened2))

def bound(graph, node, time_limit, participants):
    score, times_remaining = calc_score(graph, node, time_limit, participants)
    for rate, valve_id in graph.valves:
        if valve_id not in node.valves_opened and valve_id not in node.valves_opened2:
            times_remaining[0] -= 2 # min cost to go to the room and open the valve
            if times_remaining[0] > 0:
                score += rate * times_remaining[0]
    return score

def calc_score(graph, node, time_limit, participants):
    score = 0
    p_list = [node.valves_opened]
    if participants == 2:
        p_list.append(node.valves_opened2)
    times_remaining = []
    for valves_opened in p_list:
        time_remaining = time_limit
        for i in range(1, len(valves_opened)):
            src_valve_id = valves_opened[i-1]
            dest_valve_id = valves_opened[i]
            dist = dist_to_valve(graph.edges, src_valve_id, dest_valve_id)
            rate = graph.valve_rates_by_id[dest_valve_id]
            time_remaining -= (dist + 1) # 1 minute to turn the valve
            if time_remaining > 0:
                score += rate * time_remaining
            if time_remaining <= 2: # can't possibly increase score
                break
        times_remaining.append(time_remaining)
    return score, times_remaining

def find_best_score(graph, time_limit, participants=1):
    greedy_route1 = ['AA']
    greedy_route2 = ['AA']
    for i in range(len(graph.valves)):
        if participants == 1 or i % 2 == 0:
            greedy_route1.append(graph.valves[i].id)
        else:
            greedy_route2.append(graph.valves[i].id)
    best_node = Node(greedy_route1, greedy_route2)
    start_node = Node(['AA'], ['AA'])
    greedy_score, _ = calc_score(graph, best_node, time_limit, participants)
    best = PqElement(greedy_score, start_node)
    q = []
    q.append(PqElement(0, start_node))
    visited = 0
    while q:
        visited += 1
        if visited % 1000 == 0:
            print(f'{participants} Explored {visited} states')
        state = q.pop()
        score, node = state
        max_possible_score = bound(graph, node, time_limit, participants)
        if score == max_possible_score and score > best.score:
            print(f'Updating best with {node} {score} > {best.score}')
            best = state
            continue
        for branch_node in branch(graph.valves, node, participants):
            max_possible_branch_score = bound(graph, branch_node, time_limit, participants)
            if max_possible_branch_score <= best.score:
                dprint(f'Pruning {branch_node} {max_possible_branch_score} <= {best.score}')
                continue
            branch_score, _ = calc_score(graph, branch_node, time_limit, participants)
            q.append(PqElement(branch_score, branch_node))
    print(f'Explored {visited} states')
    return best

ValveNode = namedtuple('ValveNode', 'current_room valves_opened time_remaining')

class ValveGraph:
    def __init__(self, lines):
        edges = {}
        self.valves = []
        self.valve_rates_by_id = {}
        self.dist_to_valve = {}
        for line in lines:
            first, second = line.split(';')
            valve_id = first.split(' ')[1]
            rate, adj_rooms = get_ints(first)[0], [name[-2:] for name in second.split(',')]
            edges[valve_id] = adj_rooms
            if rate > 0:
                self.valves.append(Valve(rate, valve_id))
                self.valve_rates_by_id[valve_id] = rate

        self.valves.sort(reverse=True)
        self.allowed_rooms = frozenset([v.id for v in self.valves])

        for _, src_valve in self.valves + [Valve(0, 'AA')]:
            for _, dest_valve in self.valves:
                visited = set()
                frontier = [(src_valve, 0)]
                while frontier:
                    new_frontier = []
                    for current_valve, cost in frontier:
                        if current_valve in visited:
                            continue
                        visited.add(current_valve)
                        if current_valve == dest_valve:
                            self.dist_to_valve[src_valve, dest_valve] = cost + 1
                        for next_valve in edges[current_valve]:
                            if next_valve in visited:
                                continue
                            new_frontier.append((next_valve, cost + 1))
                    frontier = new_frontier

    def set_constraint(self, allowed_rooms):
        self.allowed_rooms = allowed_rooms

    def is_end_node(self, node):
        return node.time_remaining <= 2 or len(node.valves_opened) - 1 == len(self.allowed_rooms)

    def calc_heuristic(self, node):
        score = 0
        time_remaining = node.time_remaining
        for rate, valve_id in self.valves:
            if valve_id not in node.valves_opened and valve_id in self.allowed_rooms:
                time_remaining -= 2
                if time_remaining > 0:
                    score += rate * time_remaining
        return score

    def edges_from(self, src):
        for rate, valve_id in self.valves:
            if valve_id not in src.valves_opened and valve_id in self.allowed_rooms:
                valves_opened = set(src.valves_opened)
                valves_opened.add(valve_id)
                time_remaining = max(0, src.time_remaining - self.dist_to_valve[src.current_room, valve_id])
                flow_gained = time_remaining * rate
                yield ValveNode(valve_id, frozenset(valves_opened), time_remaining), flow_gained

def solve1(lines):
    graph = ValveGraph(lines)
    _, cost, path = find_path(graph, ValveNode('AA', frozenset({'AA'}), 26),
            is_end_node=lambda n: ValveGraph.is_end_node(graph, n),
            calc_heuristic=lambda n, _: ValveGraph.calc_heuristic(graph, n), maximize=True)
    for p in path:
        print(p)
    return cost

def solve2(lines):
    graph = ValveGraph(lines)
    best_score = 0
    best_scores = []
    best_paths = []
    valve_ids = [v.id for v in graph.valves]
    memo = {}
    for k in range(1, len(graph.valves) // 2 + 1):
        for set1 in itertools.combinations(valve_ids, k):
            set1 = frozenset(set1)
            set2 = frozenset([v.id for v in graph.valves if v.id not in set1])
            graph.set_constraint(set1)
            _, score1, path1 = find_path(graph, ValveNode('AA', frozenset({'AA'}), 26),
                    is_end_node=lambda n: ValveGraph.is_end_node(graph, n),
                    calc_heuristic=lambda n, _: ValveGraph.calc_heuristic(graph, n), maximize=True)
            graph.set_constraint(set2)
            _, score2, path2 = find_path(graph, ValveNode('AA', frozenset({'AA'}), 26),
                    is_end_node=lambda n: ValveGraph.is_end_node(graph, n),
                    calc_heuristic=lambda n, _: ValveGraph.calc_heuristic(graph, n), maximize=True)
            print(set1, set2)
            print(score1, score2, score1 + score2)
            if score1 + score2 > best_score:
                best_score = score1 + score2
                best_paths = [path1, path2]
                best_scores = [score1, score2]
    for i in range(0,2):
        for p in best_paths[i]:
            print(p)
        print(best_scores[i])
    return best_score

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
