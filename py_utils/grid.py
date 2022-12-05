from collections import defaultdict

cell_with_spacing = (lambda d: str(d) + ' ')

adj_offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
diag_offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
king_offsets = adj_offsets + diag_offsets

def make_ascii_grid(lines):
    grid = defaultdict(str)
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            grid[x,y] = lines[y][x]
    return grid

def get_unique_pos(grid_dict, value):
    for coord, cell in grid_dict.items():
        if cell == value:
            return coord
    return None

def print_grid(grid_dict, painter_func=cell_with_spacing):
    cells = grid_dict.copy()
    x0 = min([c[0] for c in cells])
    xn = max([c[0] for c in cells])
    y0 = min([c[1] for c in cells])
    yn = max([c[1] for c in cells])
    for y in range(y0, yn + 1):
        line = []
        for x in range(x0, xn + 1):
            line.append(painter_func(cells[x, y]))
        print(''.join(line))

def add_coords(coord1, coord2):
    return tuple(map(lambda i, j: i + j, coord1, coord2)) 

def sub_coords(coord1, coord2):
    return tuple(map(lambda i, j: i - j, coord1, coord2)) 

def manhatten(coord1, coord2):
    return sum(tuple(map(lambda i, j: abs(i - j), coord1, coord2)))

def get_items_with_offsets(grid_dict, coord, d_offset):
    grid = grid_dict.copy()
    ret = {}
    for offset in d_offset:
        adj_coord = add_coords(coord, offset)
        ret[adj_coord] = grid[adj_coord]
    return ret.items()

def get_adj_items(grid_dict, coord):
    return get_items_with_offsets(grid_dict, coord, adj_offsets)

def get_diag_items(grid_dict, coord):
    return get_items_with_offsets(grid_dict, coord, diag_offsets)

def get_king_items(grid_dict, coord):
    return get_items_with_offsets(grid_dict, coord, king_offsets)

