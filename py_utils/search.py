from collections import defaultdict, namedtuple
from heapq import heappop, heappush
from functools import lru_cache

from py_utils.grid import *
import math

class StaticGraph:
    def __init__(self):
        self.edges = defaultdict(lambda: defaultdict(int))
    def add_edge(self, src, dest, cost):
        self.edges[src][dest] = cost
    # Implement this for find_path
    def edges_from(self, src):
        for dest, cost in self.edges[src].items():
            yield dest, cost

def build_graph_from_ascii_grid(grid_dict,
        is_node=lambda coord, cell: cell.isalpha(),
        is_passable=lambda coord, cell: cell == '.',
        adjacency=adj_offsets,
        make_key=lambda coord, cell: cell
        ):
    graph = StaticGraph()
    nodes = [coord for coord, cell in grid_dict.items() if is_node(coord=coord, cell=cell)]
    for src_coord in nodes:
        src_node = make_key(coord=src_coord,cell=grid_dict[src_coord])
        visited = set([src_coord])
        frontier = [src_coord]
        start_node = grid_dict[src_coord]
        cost = 0
        while frontier:
            cost += 1
            new_frontier = []
            for coord in frontier:
                for adj_coord in get_coords_with_offsets(coord, adjacency):
                    if adj_coord in visited:
                        continue
                    adj_cell = grid_dict[adj_coord]
                    if adj_coord in nodes:
                        dest_node = make_key(coord=adj_coord,cell=adj_cell)
                        graph.add_edge(src_node, dest_node, cost)
                    if is_passable(coord=adj_coord, cell=adj_cell):
                        new_frontier.append(adj_coord)
                    visited.add(adj_coord)
            frontier = new_frontier.copy()
    return graph

PathResult = namedtuple('PathResult', 'score cost_so_far path')

@lru_cache(maxsize=None)
def find_path(graph, start_node, end_node=None, is_end_node=None, calc_heuristic=None, maximize=False):
    if start_node == end_node or (is_end_node is not None and is_end_node(start_node)):
        return 0
    visited = set()
    q = []
    h = 0
    if calc_heuristic:
        h += calc_heuristic(start_node, end_node)
    start_h = h
    heappush(q, PathResult(h, 0, [start_node]))
    while q:
        state = heappop(q)
        score, cost_so_far, path = state
        src = path[-1]
        if src in visited:
            continue
        visited.add(src)
        if len(visited) % 1000 == 0:
            print(f'Explored {len(visited)} states')
        if src == end_node or (is_end_node is not None and is_end_node(src)):
            print(f'Explored {len(visited)} states')
            return state
        for dest, edge_cost in graph.edges_from(src):
            if dest in visited:
                continue
            h = 0
            if calc_heuristic:
                h += calc_heuristic(dest, end_node)
            new_cost = cost_so_far + edge_cost
            priority = start_h - (new_cost+h) if maximize else new_cost + h
            state = PathResult(priority, new_cost, path + [dest])
            heappush(q, state)
    print(f'Failed to find a single path in {len(visited)} states')
    return PathResult(math.inf, 0, [])
