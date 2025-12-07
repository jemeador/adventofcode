#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LINE_SIZE 1024
#define MAX_RANGES 200
#define MAX_INGREDIENTS 1000
typedef long long IngredientId;

typedef struct{
    IngredientId start;
    IngredientId end;
} Range;
typedef Range Ranges[MAX_RANGES];

int valid(Range* range) {
  return range->start != -1 && range->end != -1;
}

int compare_ranges(const void *lhs, const void *rhs) {
  Range* lhs_range = (Range *)lhs;
  Range* rhs_range = (Range *)rhs;
  const int lhs_valid = valid(lhs_range);
  const int rhs_valid = valid(rhs_range);

  // Put invalid ranges at the end
  if (! lhs_valid && ! rhs_valid) {
    return 0;
  }
  if (! lhs_valid) {
    return 1;
  }
  if (! rhs_valid) {
    return -1;
  }

  if (lhs_range->start < rhs_range->start) {
    return -1;
  }
  if (lhs_range->start > rhs_range->start) {
    return 1;
  }
  return 0;
}

long long solve1(Ranges ranges, IngredientId ingredients[MAX_INGREDIENTS]) {
  long long result = 0;
  int fresh_lines = 1;
  for (int i = 0; i < MAX_INGREDIENTS; i++) {
    IngredientId ingredient_id = ingredients[i];
    if (ingredient_id == -1) {
      break;
    }
    for (int i = 0; i < MAX_RANGES; i++) {
      Range range = ranges[i];
      if (range.start <= ingredient_id && ingredient_id <= range.end) {
        result += 1;
        break;
      }
    }
  }
  return result;
}

long long solve2(Ranges ranges) {
  long long result = 0;
  Ranges normal_ranges;
  for (int i = 0; i < MAX_RANGES; i++) {
      normal_ranges[i].start = -1;
      normal_ranges[i].end = -1;
  }
  for (int i = 0; i < MAX_RANGES; i++) {
    Range range = ranges[i];
    IngredientId start = range.start;
    IngredientId end = range.end;
    if (! valid(&range)) {
      break;
    }
    int start_included_in = -1;
    int end_included_in = -1;
    for (int n = 0; valid(&normal_ranges[n]); n++) {
      Range range_j = normal_ranges[n];
      IngredientId normal_start = range_j.start;
      IngredientId normal_end = range_j.end;
      if (normal_start <= start && start <= normal_end + 1) {
        start_included_in = n;
      }
      if (normal_start - 1 <= end && end <= normal_end) {
        end_included_in = n;
      }
      if (start_included_in >= 0 && start_included_in == end_included_in) {
        break;
      }
      if (start < normal_start && normal_end < end) {
        normal_ranges[n].start = -1;
        normal_ranges[n].end = -1;
      }
      if (start_included_in >= 0 && end_included_in >= 0) {
        break;
      }
      if (start < normal_end && end < normal_end) {
        break;
      }
    }
    if (start_included_in == -1 && end_included_in == -1) {
      int first_invalid_index = 0;
      while (valid(&normal_ranges[first_invalid_index])) {
        first_invalid_index++;
      };
      normal_ranges[first_invalid_index].start = start;
      normal_ranges[first_invalid_index].end = end;
      // print(f"Range {start}-{end} intersects nothing")
      printf("Range %lld-%lld intersects nothing\n",
          start,
          end);
    }
    else if (start_included_in == end_included_in) {
      printf("Range %lld-%lld is eclipsed by %lld-%lld\n",
          start,
          end,
          normal_ranges[start_included_in].start,
          normal_ranges[start_included_in].end);
      continue;
    }
    else if (start_included_in != -1 && end_included_in == -1) {
      printf("Range %lld-%lld intersects %lld-%lld at start\n",
          start,
          end,
          normal_ranges[start_included_in].start,
          normal_ranges[start_included_in].end);
      normal_ranges[start_included_in].end = end;
      printf("Extending to %lld-%lld\n",
          normal_ranges[start_included_in].start,
          normal_ranges[start_included_in].end);
    }
    else if (start_included_in == -1 && end_included_in != -1) {
      printf("Range %lld-%lld intersects %lld-%lld at end\n",
          start,
          end,
          normal_ranges[end_included_in].start,
          normal_ranges[end_included_in].end);
      normal_ranges[end_included_in].start = start;
      printf("Extending to %lld-%lld\n",
          normal_ranges[end_included_in].start,
          normal_ranges[end_included_in].end);
    }
    else {
        printf("Range %lld-%lld intersects %lld-%lld and %lld-%lld\n",
          start,
          end,
          normal_ranges[start_included_in].start,
          normal_ranges[start_included_in].end,
          normal_ranges[end_included_in].start,
          normal_ranges[end_included_in].end);
        normal_ranges[start_included_in].end = normal_ranges[end_included_in].end;
        normal_ranges[end_included_in].start = -1;
    }
    qsort(normal_ranges, MAX_RANGES, sizeof(Range), compare_ranges);
    for (int n = 0; valid(&normal_ranges[n]); ++n) {
      Range range_j = normal_ranges[n];
    }
  }

  for (int i = 0; valid(&normal_ranges[i]); ++i) {
    Range normal_range = normal_ranges[i];
    printf("  Normal range %d: %lld-%lld\n", i, normal_range.start, normal_range.end);
    result += normal_range.end - normal_range.start + 1;
  }
  return result;
}

int main () {
  Ranges fresh_ranges;
  for (int i = 0; i < MAX_RANGES; i++) {
      fresh_ranges[i].start = -1;
      fresh_ranges[i].end = -1;
  }
  char buffer[LINE_SIZE];
  IngredientId ingredients[MAX_INGREDIENTS];
  for (int i = 0; i < MAX_INGREDIENTS; i++) {
    ingredients[i] = -1;
  }
  int fresh_lines = 1;
  int i = 0;
  while (fgets(buffer, LINE_SIZE, stdin)) {
    if (strlen(buffer) <= 1) {
      fresh_lines = 0;
      i = 0;
      continue;
    }
    if (fresh_lines) {
      sscanf(buffer, "%lld-%lld", &fresh_ranges[i].start, &fresh_ranges[i].end);
      i++;
    }
    else {
      ingredients[i] = atoll(buffer);
      i++;
    }
  }
  const long long solution1 = solve1(fresh_ranges, ingredients);
  if (solution1 != 0) {
    printf("Solution 1: %lld\n", solution1);
  }
  const long long solution2 = solve2(fresh_ranges);
  if (solution2 != 0) {
    printf("Solution 2: %lld\n", solution2);
  }
}
