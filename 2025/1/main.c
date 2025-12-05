#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LINE_SIZE 1024
#define MAX_LINES 5000
typedef char lines_t[MAX_LINES][LINE_SIZE];

int solve1(lines_t lines) {
  int result = 0;
  int r = 50;

  for (int i = 0; lines[i][0] != '\0'; i++) {
    char* line = lines[i];
    const int mult = (line[0] == 'L') ? 1 : -1;
    const int turn = mult * atoi(&line[1]);
    r = (r + turn) % 100;
    if (r == 0) {
      result += 1;
    }
  }
  return result;
}

int solve2(lines_t lines) {
  int result = 0;
  int r = 50;

  for (int i = 0; lines[i][0] != '\0'; i++) {
    char* line = lines[i];
    const int mult = (line[0] == 'L') ? 1 : -1;
    int turn = mult * atoi(&line[1]);
    while (turn <= -100) {
      turn += 100;
      result += 1;
    }
    while (turn >= 100) {
      turn -= 100;
      result += 1;
    }
    if (r + turn >= 100) {
        result += 1;
    }
    else if (r > 0 && r + turn < 0) {
        result += 1;
    }
    if (r + turn == 0) {
        result += 1;
    }
    r = (r + turn) % 100;
    if (r < 0) {
      r += 100;
    }
  }
  return result;
}

int main () {
  lines_t lines;
  int i = 0;
  while (fgets(lines[i++], LINE_SIZE, stdin)) {
    // printf("%s", lines[i]);
  }
  const int solution1 = solve1(lines);
  if (solution1 != 0) {
    printf("Solution 1: %d\n", solution1);
  }
  const int solution2 = solve2(lines);
  if (solution2 != 0) {
    printf("Solution 2: %d\n", solution2);
  }
}
