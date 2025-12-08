#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LINE_SIZE 4000
#define MAX_LINES 10
typedef char lines_t[MAX_LINES][LINE_SIZE];
typedef long long Num;


long long solve1(lines_t lines) {
  long long result = 0;
  int nums[1000][MAX_LINES];
  int ops[1000];
  int col = 0;
  int number_started = 0;
  int y;
  int max_col = 0;
  for (y = 0; y < MAX_LINES; ++y) {
    char buffer[10];
    if (strlen(lines[y]) <= 1) {
      printf("Done parsing\n");
      break;
    }
    int i = 0;
    for (int x = 0; x < LINE_SIZE; ++x) {
      const char c = lines[y][x];
      const int is_digit = ('0' <= c && c <= '9');
      if (c == '+' || c == '*') {
        printf("Found op %d %c\n" ,col, c);
        ops[col] = c;
        col += 1;
      }
      else if (is_digit) {
        buffer[i] = c;
        number_started = 1;
        ++i;
      }
      else if (number_started) {
        buffer[i] = '\0';
        nums[col][y] = atoi(buffer);
        printf("Found num %d\n" ,nums[col][y]);
        number_started = 0;
        col += 1;
        max_col = col;
        i = 0;
      }
      if (c == '\n' || c == '\0') {
        printf("End of line\n");
        break;
      }
    }
    col = 0;
  }
  y -= 1;
  for (int c = 0; c < max_col; ++c) {
    if (ops[c] == '*') {
      int total = 1;
      for (int j = 0; j < y; ++j) {
        printf("nums[%d][%d] = %d\n", c, j,  nums[c][j]);
        total *= nums[c][j];
      }
      printf("Total: %d\n", total);
      result += total;
    }
    else if (ops[c] == '+') {
      int total = 0;
      for (int j = 0; j < y; ++j) {
        printf("nums[%d][%d] = %d\n", c, j,  nums[c][j]);
        total += nums[c][j];
      }
      printf("Total: %d\n", total);
      result += total;
    }
    else {
      assert(0);
    }
  }
  return result;
}

long long solve2(lines_t lines) {
  long long result = 0;
  int nums[1000][MAX_LINES];
  int ops[1000];
  int col = 0;
  int max_col = 0;
  for (int x = 0; x < LINE_SIZE; ++x) {
    char buffer[10];
    int i = 0;
    for (int y = 0; y < MAX_LINES; ++y) {
      if (strlen(lines[y]) <= 1) {
        buffer[i] = '\0';
        nums[x][y] = atoi(buffer);
        printf("Found num %d\n" ,nums[x][y]);
        i = 0;
        break;
      }
      const char c = lines[y][x];
      const int is_digit = ('0' <= c && c <= '9');
      if (c == '+' || c == '*') {
        printf("Found op %d %c\n" ,col, c);
        ops[col] = c;
        col += 1;
        max_col += 1;
      }
      else if (is_digit) {
        buffer[i] = c;
        ++i;
      }
      if (c == '\n' || c == '\0') {
        printf("End of line\n");
        break;
      }
    }
  }
  for (int c = 0; c < max_col; ++c) {
    if (ops[c] == '*') {
      int total = 1;
      for (int j = 0; j < y; ++j) {
        printf("nums[%d][%d] = %d\n", c, j,  nums[c][j]);
        total *= nums[c][j];
      }
      printf("Total: %d\n", total);
      result += total;
    }
    else if (ops[c] == '+') {
      int total = 0;
      for (int j = 0; j < y; ++j) {
        printf("nums[%d][%d] = %d\n", c, j,  nums[c][j]);
        total += nums[c][j];
      }
      printf("Total: %d\n", total);
      result += total;
    }
    else {
      assert(0);
    }
  }
  return result;
}

int main () {
  lines_t lines;
  int i = 0;
  while (fgets(lines[i++], LINE_SIZE, stdin)) {
    //printf("%s", lines[i-1]);
  }
  const long long solution1 = solve1(lines);
  if (solution1 != 0) {
    printf("Solution 1: %lld\n", solution1);
  }
  const long long solution2 = solve2(lines);
  if (solution2 != 0) {
    printf("Solution 2: %lld\n", solution2);
  }
}
