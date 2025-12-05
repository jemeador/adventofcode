#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LINE_SIZE 1024
#define MAX_LINES 5000
typedef char lines_t[MAX_LINES][LINE_SIZE];


long long solve1(lines_t lines) {
  long long result = 0;
  return result;
}

long long solve2(lines_t lines) {
  long long result = 0;
  return result;
}

int main () {
  lines_t lines;
  int i = 0;
  while (fgets(lines[i++], LINE_SIZE, stdin)) {
    printf("%s", lines[i-1]);
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
