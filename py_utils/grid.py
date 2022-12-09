from collections import defaultdict
from collections import namedtuple

cell_with_spacing = (lambda d: str(d) + ' ')

adj_offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
diag_offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
king_offsets = adj_offsets + diag_offsets

Coord = namedtuple('Coord', 'x y')

def make_ascii_grid(lines):
    grid = defaultdict(str)
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            grid[Coord(x,y)] = lines[y][x]
    return grid

def grid_min_x(grid_dict):
    return min([c[0] for c in grid_dict])
def grid_min_y(grid_dict):
    return min([c[1] for c in grid_dict])
def grid_max_x(grid_dict):
    return max([c[0] for c in grid_dict])
def grid_max_y(grid_dict):
    return max([c[1] for c in grid_dict])

def get_unique_pos(grid_dict, value):
    for coord, cell in grid_dict.items():
        if cell == value:
            return coord
    return None

def get_coords(grid_dict, value):
    for coord, cell in grid_dict.items():
        if cell == value:
            yield coord

def find_and_replace_pattern(grid_dict, before, after):
    for coord in grid_dict.keys():
        if all(grid_dict[add_coords(coord, pattern_coord)] == pattern_cell for pattern_coord, pattern_cell in before.items()):
            for pattern_coord, pattern_cell in before.items():
                replace_coord = add_coords(coord, pattern_coord)
                grid_dict[replace_coord] = after[pattern_coord]

def print_grid(grid_dict, painter_func=cell_with_spacing):
    x0 = grid_min_x(grid_dict)
    xn = grid_max_x(grid_dict)
    y0 = grid_min_y(grid_dict)
    yn = grid_max_y(grid_dict)
    cells = grid_dict.copy()
    for y in range(y0, yn + 1):
        line = []
        for x in range(x0, xn + 1):
            line.append(painter_func(cells[x, y]))
        print(''.join(line))

def add_coords(coord1, coord2):
    return Coord(coord1[0] + coord2[0], coord1[1] + coord2[1])

def sub_coords(coord1, coord2):
    return Coord(coord1[0] - coord2[0], coord1[1] - coord2[1])

def manhatten(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def get_coords_with_offsets(coord, d_offset):
    for offset in d_offset:
        yield add_coords(coord, offset)

def get_adj_coords(coord):
    return get_coords_with_offsets(coord, adj_offsets)

def get_diag_coords(coord):
    return get_coords_with_offsets(coord, diag_offsets)

def get_king_coords(coord):
    return get_coords_with_offsets(coord, king_offsets)

def get_items_with_offsets(grid_dict, coord, d_offset):
    for offset in d_offset:
        adj_coord = add_coords(coord, offset)
        if adj_coord in grid_dict:
            yield adj_coord, grid_dict[adj_coord]

def get_adj_items(grid_dict, coord):
    return get_items_with_offsets(grid_dict, coord, adj_offsets)

def get_diag_items(grid_dict, coord):
    return get_items_with_offsets(grid_dict, coord, diag_offsets)

def get_king_items(grid_dict, coord):
    return get_items_with_offsets(grid_dict, coord, king_offsets)

