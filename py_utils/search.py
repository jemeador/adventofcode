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

PathResult = namedtuple('PathResult', 'cost path')

@lru_cache(maxsize=None)
def find_path(graph, start_node, end_node, calc_heuristic=None):
    if start_node == end_node:
        return 0
    visited = set()
    q = []
    heappush(q, PathResult(0, [start_node]))
    while q:
        state = heappop(q)
        total_cost, path = state
        src = path[-1]
        if src in visited:
            continue
        visited.add(src)
        if src == end_node:
            print(f'Explored {len(visited)} states')
            return state
        for dest, edge_cost in graph.edges_from(src):
            if dest in visited:
                continue
            cost = total_cost + edge_cost
            if calc_heuristic:
                cost += calc_heuristic(src, dest)
            state = PathResult(cost, path + [dest])
            heappush(q, state)
    print(f'Failed to find a single path in {len(visited)} states')
    return PathResult(math.inf, [])
