# 2352\. Equal Row and Column Pairs - Solution Explanation

## Problem Overview

You are given an `n x n` integer grid. The task is to find the total number of pairs `(row, column)` where the sequence of numbers in the row is identical to the sequence of numbers in the column.

**Key Definitions:**

  - **Pair `(ri, cj)`**: A combination of a row (at index `ri`) and a column (at index `cj`).
  - **Equal**: The row and column are considered equal if they contain the exact same elements in the exact same order.

**Examples:**

```python
Input: grid = [[3,2,1],[1,7,6],[2,7,7]]
Output: 1
Explanation:
Row 2 is [2,7,7].
Column 1 is [2,7,7].
This is one equal pair: (Row 2, Column 1).

Input: grid = [[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]
Output: 3
Explanation:
- (Row 0, Column 0) are both [3,1,2,2].
- (Row 2, Column 2) are both [2,4,2,2].
- (Row 3, Column 2) are both [2,4,2,2]. (Note that one column can match multiple rows).
```

## Key Insights

### The Inefficient Brute-Force Approach

The most direct way to think about this is to compare every row with every column. You could write a loop to pick a row, then an inner loop to pick a column, and a third loop to compare them element by element. This `O(n³)` approach is very slow and would likely time out on larger grids.

### Pre-computation with a Hash Map

The key to an efficient `O(n²)` solution is to **pre-process** the grid. Instead of rebuilding and re-scanning for every comparison, we can first create an "inventory" of all the unique row patterns and how many times each one appears. A **hash map** (like Python's `collections.Counter`) is the perfect tool for this.

Once we have this inventory of rows, we can then iterate through the columns one by one. For each column, we can perform a single, lightning-fast lookup in our hash map to see if that pattern exists as a row, and if so, how many times.

## Solution Approach

This solution first counts the frequency of every unique row pattern. Then, it constructs each column and looks up how many rows match that column pattern, adding the result to a running total.

```python
import collections
from typing import List

class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:
        n = len(grid)
        pair_count = 0
        
        # Step 1: Create a frequency map of all the row patterns.
        # We convert each row (list) into a tuple so it can be a dictionary key.
        row_counts = collections.Counter(tuple(row) for row in grid)
        
        # Step 2: Iterate through each column.
        for c in range(n):
            # Step 2a: Construct the current column as a tuple.
            current_col = tuple(grid[r][c] for r in range(n))
            
            # Step 2b: Add the number of times this column pattern
            # appeared as a row.
            pair_count += row_counts[current_col]
                
        return pair_count
```

## Detailed Code Analysis

### Step 1: Counting the Row Frequencies

```python
row_counts = collections.Counter(tuple(row) for row in grid)
```

  - This is the powerful pre-computation step.
  - **`tuple(row) for row in grid`**: This is a generator expression. It iterates through each `row` in the `grid` and converts it from a `list` to a `tuple`. We must do this because dictionary keys in Python must be immutable (unchangeable), and lists are mutable, but tuples are not.
  - **`collections.Counter(...)`**: This takes the sequence of row tuples and efficiently creates a hash map (a `Counter` object) where the keys are the unique row patterns (as tuples) and the values are their frequencies.

### Step 2: Iterating Through Columns and Counting Pairs

```python
pair_count = 0
for c in range(n):
    current_col = tuple(grid[r][c] for r in range(n))
    pair_count += row_counts[current_col]
```

  - **`for c in range(n)`**: This loop iterates through the column indices, from `0` to `n-1`.
  - **`current_col = tuple(...)`**: Inside the loop, we build the current column. The expression `(grid[r][c] for r in range(n))` iterates through the rows (`r`) for the fixed column `c`, yielding each element of that column. We then convert this sequence into a tuple.
  - **`pair_count += row_counts[current_col]`**: This is the core lookup. We take the `current_col` tuple and use it as a key to look in our `row_counts` map.
      - If the column pattern exists as a row pattern in the map, `row_counts[current_col]` will return its frequency (e.g., `1`, `2`, etc.). We add this number to our `pair_count`.
      - If the column pattern does **not** exist in the map, `collections.Counter` has a helpful feature where it simply returns `0` instead of raising an error. So, we add `0` to our `pair_count`, which is correct.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `grid = [[3,2,1],[1,7,6],[2,7,7]]` with extreme detail.

1.  **Initialization**:

      * `n = 3`
      * `pair_count = 0`

2.  **Step 1: Create `row_counts`**:

      * Process row 0 `[3,2,1]` -\> convert to tuple `(3,2,1)`.
      * Process row 1 `[1,7,6]` -\> convert to tuple `(1,7,6)`.
      * Process row 2 `[2,7,7]` -\> convert to tuple `(2,7,7)`.
      * After this step, **`row_counts` is `{ (3,2,1): 1, (1,7,6): 1, (2,7,7): 1 }`**.

3.  **Step 2: Loop through columns `c` from 0 to 2**:

| `c` (Column Index) | `current_col` Construction | `current_col` (as tuple) | `row_counts[current_col]`? | `pair_count` (after `+=`)|
| :--- | :--- | :--- | :--- | :--- |
| **Start** | - | - | - | 0 |
| **0** | `(grid[0][0], grid[1][0], grid[2][0])` -\> `(3, 1, 2)`| `(3, 1, 2)` | `0` (not in map) | `0 + 0 = 0` |
| **1** | `(grid[0][1], grid[1][1], grid[2][1])` -\> `(2, 7, 7)`| `(2, 7, 7)` | `1` (found in map) | `0 + 1 = 1` |
| **2** | `(grid[0][2], grid[1][2], grid[2][2])` -\> `(1, 6, 7)`| `(1, 6, 7)` | `0` (not in map) | `1 + 0 = 1` |

4.  **Final Step**: The loop finishes. The function returns the final `pair_count`, which is **1**.

## Performance Analysis

### Time Complexity: O(n²)

  - Where `n` is the side length of the grid.
  - Building the `row_counts` map requires iterating through `n` rows, and for each row, creating a tuple of `n` elements. This takes `O(n * n) = O(n²)`.
  - Iterating through the columns requires `n` iterations. Inside each, we build a column of `n` elements and perform a hash map lookup. Building the column is `O(n)`, and the lookup is `O(n)` on average (because the key itself is of length `n`). The total for this part is `n * O(n) = O(n²)`.
  - The overall time complexity is `O(n²) + O(n²)`, which is `O(n²)`.

### Space Complexity: O(n²)

  - In the worst case, every row in the grid is unique. The `row_counts` hash map would then need to store `n` keys, where each key (a tuple) is of length `n`. This results in a space complexity of `O(n * n) = O(n²)`.