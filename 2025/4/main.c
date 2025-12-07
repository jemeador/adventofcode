#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define DIM 150
typedef char grid_t[DIM][DIM];

struct Coord {
  int x;
  int y;
};

struct Coord adj_offsets[8] = {
  {-1, -1},
  {-1, 0},
  {-1, 1},
  {0, -1},
  {0, 1},
  {1, -1},
  {1, 0},
  {1, 1},
};

struct Coord add_coords(struct Coord left, struct Coord right) {
  const struct Coord ret = {left.x + right.x, left.y + right.y};
  return ret;
}

char item_at(grid_t grid, struct Coord coord) {
  if (coord.x < 0 || coord.x >= DIM || coord.y < 0 || coord.y >= DIM) {
    return '.';
  }
  return grid[coord.y][coord.x];
}

void set_item_at(grid_t grid, struct Coord coord, char item) {
  if (coord.x < 0 || coord.x >= DIM || coord.y < 0 || coord.y >= DIM) {
    return;
  }
  grid[coord.y][coord.x] = item;
}

long long solve1(grid_t grid) {
  long long result = 0;
  for (int y = 0; y < DIM; ++y) {
    for (int x = 0; x < DIM; ++x) {
      const struct Coord coord = {x, y};
      if (item_at(grid, coord) != '@') {
        continue;
      }
      int count = 0;
      for (int c = 0; c < 8; ++c) {
        const struct Coord adj_coord = add_coords(coord, adj_offsets[c]);
        const char value = item_at(grid, adj_coord);
        if (value == '@') {
          count += 1;
        }
      }
      if (count < 4) {
          result += 1;
      }
    }
  }
  return result;
}

long long solve2(grid_t grid) {
  long long result = 0;
  int removals = -1;
  while (removals != 0) {
    removals = 0;
    for (int y = 0; y < DIM; ++y) {
      for (int x = 0; x < DIM; ++x) {
        const struct Coord coord = {x, y};
        if (item_at(grid, coord) != '@') {
          continue;
        }
        int count = 0;
        for (int c = 0; c < 8; ++c) {
          const struct Coord adj_coord = add_coords(coord, adj_offsets[c]);
          const char value = item_at(grid, adj_coord);
          if (value == '@') {
            count += 1;
          }
        }
        if (count < 4) {
          set_item_at(grid, coord, '.');
          removals += 1;
        }
      }
    }
    result += removals;
  }
  return result;
}

int main () {
  grid_t grid;
  for (int y = 0; y < DIM; ++y) {
    for (int x = 0; x < DIM; ++x) {
      struct Coord coord = {x, y};
      set_item_at(grid, coord, '.');
    }
  }
  int i = 0;
  while (fgets(grid[i++], DIM, stdin)) {
    // printf("%s", grid[i-1]);
  }
  const long long solution1 = solve1(grid);
  if (solution1 != 0) {
    printf("Solution 1: %lld\n", solution1);
  }
  const long long solution2 = solve2(grid);
  if (solution2 != 0) {
    printf("Solution 2: %lld\n", solution2);
  }
}
