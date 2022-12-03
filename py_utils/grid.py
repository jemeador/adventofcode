from collections import defaultdict

__print_cell = (lambda d: str(d) + ' ')

def print_grid(grid_dict, painter_func=__print_cell):
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
