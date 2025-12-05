#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LINE_SIZE 1024
#define MAX_LINES 5000
typedef char lines_t[MAX_LINES][LINE_SIZE];

long long solve(int line_count, lines_t lines, int battery_count) {
  long long result = 0;
  for (int line_index = 0; line_index < line_count; line_index++) {
      char num_str[LINE_SIZE] = "";
      char *line = lines[line_index];
      if (strlen(line) < battery_count) {
          continue;
      }
      int start = 0;
      for (int battery_n = 0; battery_n < battery_count; battery_n++) {
          char largest_digit = line[start];
          assert(start < (int)strlen(line));
          start += 1;
          int end = (int)strlen(line) - battery_count + battery_n;
          if (end > (int)strlen(line)) {
              end = (int)strlen(line);
          }
          for (int i = start; i < end; i++) {
              char c = line[i];
              if (c > largest_digit) {
                  largest_digit = c;
                  start = i + 1;
              }
          }
          num_str[battery_n] = largest_digit;
      }
      num_str[battery_count] = '\0';
      result += atoll(num_str);
  }
  return result;
}

long long solve1(int line_count, lines_t lines) {
  return solve(line_count, lines, 2);
}

long long solve2(int line_count, lines_t lines) {
  return solve(line_count, lines, 12);
}

int main () {
  lines_t lines;
  int i = 0;
  while (fgets(lines[i++], LINE_SIZE, stdin)) {
    // printf("%s", lines[i-1]);
  }
  const long long solution1 = solve1(i, lines);
  if (solution1 != 0) {
    printf("Solution 1: %lld\n", solution1);
  }
  const long long solution2 = solve2(i, lines);
  if (solution2 != 0) {
    printf("Solution 2: %lld\n", solution2);
  }
}
