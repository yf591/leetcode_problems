# 62\. Unique Paths - Solution Explanation

## Problem Overview

You are given an `m x n` grid. A robot starts at the top-left corner (`(0, 0)`) and wants to move to the bottom-right corner (`(m-1, n-1)`). The robot can **only** move `down` or `right` at any point. The task is to find the total number of unique paths the robot can take.

**Examples:**

```python
Input: m = 3, n = 2
Output: 3
Explanation: There are 3 unique paths:
1. Right -> Down -> Down
2. Down -> Right -> Down
3. Down -> Down -> Right

Input: m = 3, n = 7
Output: 28
```

## Key Insights

### 1\. The Dynamic Programming (DP) Recurrence Relation

This problem can be solved by breaking it down into simpler subproblems. Let's think about how a robot can arrive at any cell `(r, c)`.

  - Since the robot can only move `down` or `right`, to reach `(r, c)`, it *must* have come from either the cell directly above it (`(r-1, c)`) or the cell directly to its left (`(r, c-1)`).
  - Therefore, the total number of unique paths to `(r, c)` is the sum of the paths to `(r-1, c)` and the paths to `(r, c-1)`.
  - This gives us our **recurrence relation**: `paths(r, c) = paths(r-1, c) + paths(r, c-1)`

### 2\. The Base Cases

  - What about the cells in the very first row (`r=0`)? The robot can only reach them by moving `right` from the start. There is only **one** way to reach any cell in the first row.
  - What about the cells in the very first column (`c=0`)? The robot can only reach them by moving `down` from the start. There is only **one** way to reach any cell in the first column.

### 3\. From 2D DP to 1D DP (Space Optimization)

A straightforward DP solution would be to create a 2D grid (`dp[m][n]`) and fill it out using the recurrence relation.

```
  1 1 1 1 ...
  1 2 3 4 ...
  1 3 6 10 ...
  ...
```

However, when we are calculating the values for the *current* row (e.g., row `i`), we only ever need the values from the *previous* row (`i-1`). We don't need to store all `m` rows in memory.

This is the key insight for optimization: we can use a single 1D array (let's call it `dp_row`) of size `n` to store the path counts for the *previous* row. We can then calculate the values for the *new* row in-place.

## Solution Approach

This solution implements the space-optimized dynamic programming approach. It uses a single 1D array, `row`, of size `n`. This array is first initialized to represent the base case (the top row). Then, it iterates `m-1` times, with each iteration transforming the `row` array from its state in row `i-1` to its state in row `i`.

```python
from typing import List

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        
        # We can use a 1D DP array (representing a row) of size n.
        # Initialize it with all 1s. This represents our base case,
        # the top row (row 0), where there is 1 way to reach any cell.
        row = [1] * n
        
        # We have 'm' rows. We already have the values for the first row (row 0).
        # So, we loop 'm - 1' more times to calculate the remaining rows.
        for i in range(m - 1):
            
            # For each new row, we update the values in our 'row' array.
            # We iterate from the second element (index 1) to the end.
            for j in range(1, n):
                # The formula is:
                # new_value[j] = value_above[j] + value_left[j]
                
                # In our 1D array:
                # value_above[j] is the value currently in 'row[j]' (from the previous row).
                # value_left[j] is the value in 'row[j-1]' (which we just updated).
                row[j] = row[j] + row[j-1]
                
        # After all rows are computed, the final answer is the value
        # in the last cell (bottom-right corner).
        return row[n-1]
```

## Detailed Code Analysis

### Step 1: Initialization

```python
row = [1] * n
```

  - We create a list called `row` with `n` elements, all set to `1`.
  - This list represents the **base case** of our DP problem. It's the top row of the grid (row 0). There is exactly one path to get to any cell in the first row: by moving right from the start.
  - `row = [1, 1, 1, ..., 1]`

### Step 2: The Outer Loop (Row Iteration)

```python
for i in range(m - 1):
```

  - This loop iterates through the remaining rows that need to be calculated.
  - If `m=3`, we have 3 rows. We've already initialized for row 0. So, this loop needs to run 2 more times (for row 1 and row 2). `range(m-1)` (which is `range(2)`) gives us `i=0` and `i=1`.

### Step 3: The Inner Loop (Column Iteration)

```python
for j in range(1, n):
```

  - This loop calculates the values for the new row, from left to right.
  - Why do we start at `j = 1`? Because the first cell of every row (the cell at `j=0`) is part of the first column. The number of paths to any cell in the first column is always 1 (by only moving down). Our `row[0]` already holds the value `1` and will never change, so we can skip it.

### Step 4: The Magic DP Calculation

```python
row[j] = row[j] + row[j-1]
```

  - This is the most beautiful part of the solution and the implementation of our recurrence relation: `paths(r, c) = paths(r-1, c) + paths(r, c-1)`.
  - Let's analyze this line in the middle of an iteration:
      - `row[j]` (on the right side): This is the value that was in the `row` array *before* we started this inner loop. It represents the number of paths to the cell **directly above** our current cell, i.e., `paths(r-1, c)`.
      - `row[j-1]` (on the right side): This is the value that we *just calculated* in the previous step of the inner loop. It represents the number of paths to the cell **immediately to the left** of our current cell, i.e., `paths(r, c-1)`.
  - We sum them and store the new value back into `row[j]`, overwriting the old value from the previous row.

## Step-by-Step Execution Trace

Let's trace the algorithm with `m = 3` and `n = 4` with extreme detail.

### **Initial State:**

  - `m = 3`, `n = 4`
  - `row = [1, 1, 1, 1]` (This represents the state of **Row 0**)

-----

### **Outer Loop 1 (for `i = 0`): Calculating values for Row 1**

  - The outer loop starts (for `m-1` = 2 times).
  - The inner loop starts: `for j in range(1, 4)` (j will be 1, 2, 3).
  - **Inner Loop (j=1):**
      - `row[1] = row[1] + row[0]`
      - `row[1] = 1 + 1` -\> `row[1] = 2`
      - `row` is now `[1, 2, 1, 1]`
  - **Inner Loop (j=2):**
      - `row[2] = row[2] + row[1]`
      - `row[2] = 1 + 2` -\> `row[2] = 3`
      - `row` is now `[1, 2, 3, 1]`
  - **Inner Loop (j=3):**
      - `row[3] = row[3] + row[2]`
      - `row[3] = 1 + 3` -\> `row[3] = 4`
      - `row` is now `[1, 2, 3, 4]`

**End of Outer Loop 1**: `row` now holds the path counts for **Row 1**.

-----

### **Outer Loop 2 (for `i = 1`): Calculating values for Row 2**

  - The outer loop runs for the second and final time.
  - The inner loop starts: `for j in range(1, 4)`.
  - **Inner Loop (j=1):**
      - `row[1] = row[1] + row[0]`
      - `row[1] = 2 + 1` -\> `row[1] = 3`
      - `row` is now `[1, 3, 3, 4]`
  - **Inner Loop (j=2):**
      - `row[2] = row[2] + row[1]`
      - `row[2] = 3 + 3` -\> `row[2] = 6`
      - `row` is now `[1, 3, 6, 4]`
  - **Inner Loop (j=3):**
      - `row[3] = row[3] + row[2]`
      - `row[3] = 4 + 6` -\> `row[3] = 10`
      - `row` is now `[1, 3, 6, 10]`

**End of Outer Loop 2**: `row` now holds the path counts for **Row 2**.

-----

### **End of Algorithm**

  - The outer `for` loop finishes.
  - The function returns `row[n-1]`, which is `row[3]`.
  - The final answer is **10**.

## Performance Analysis

### Time Complexity: O(m \* n)

  - The algorithm has a nested loop structure.
  - The outer loop runs `m-1` times.
  - The inner loop runs `n-1` times.
  - The total number of calculations is proportional to `(m-1) * (n-1)`, which simplifies to `O(m * n)`.

### Space Complexity: O(n)

  - This is the key optimization. We only store a single array (`row`) of size `n`. The space required is proportional to `n`, not `m * n`.