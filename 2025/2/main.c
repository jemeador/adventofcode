#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFFER_MAX 1024
typedef char Buffer[BUFFER_MAX];

struct Range {
  long long start;
  long long end;
};

typedef struct Range Ranges[100];

long long solve2(int size, struct Range ranges[size], int only_halves) {
  long long result = 0;
  for (int r = 0; r < size; r++) {
    struct Range range = ranges[r];
    for (long long i = range.start; i <= range.end; i++) {
      char as_str[20];
      sprintf(as_str, "%lld", i);
      const int digit_count = strlen(as_str);
      for (int len_segment = 1; len_segment < digit_count / 2 + 1; len_segment++) {
        if (digit_count % len_segment != 0) {
          continue;
        }
        if (only_halves && len_segment != digit_count / 2) {
          continue;
        }
        const int parts = digit_count / len_segment;
        int valid = 0;
        for (int j = 0; j < len_segment; j++) {
          char c = as_str[j];
          for (int segment_i = 1; segment_i < parts; segment_i++) {
            if (as_str[j + segment_i * len_segment] != c) {
              valid = 1;
              break;
            }
          }
        }
        if (! valid) {
          //printf("In range %d-%d: ", range.start, range.end);
          //printf("Found invalid number: %lld\n", i);
          result += i;
          break;
        }
      }
    }
  }
  return result;
}

long long solve1(int size, struct Range ranges[size]) {
  return solve2(size, ranges, 1);
}

int main () {
  Ranges ranges;
  int i = 0;
  int b = 0;
  char c;
  // Scan as a signed value %d and you get negative numbers! Scan as an
  // unsigned and you get overflow!
  while (scanf("%llu-%llu,", &ranges[i].start, &ranges[i].end) != EOF) {
    i++;
  }
  const long long solution1 = solve1(i, ranges);
  if (solution1 != 0) {
    printf("Solution 1: %lld\n", solution1);
  }
  const long long solution2 = solve2(i, ranges, 0);
  if (solution2 != 0) {
    printf("Solution 2: %lld\n", solution2);
  }
}
