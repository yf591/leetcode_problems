# 73\. Set Matrix Zeroes - Solution Explanation

## Problem Overview

You are given an `m x n` matrix of integers. The task is to modify the matrix such that if any cell `(row, col)` has a value of `0`, its entire row and its entire column are set to `0`.

**Key Constraints:**

  - The modification must be done **in-place**, meaning you must alter the original `matrix` directly.
  - The most efficient solution should use **constant (`O(1)`) extra space**.

**Example:**

  - **Input Matrix:**
    ```
    [ [1, 1, 1],
      [1, 0, 1],
      [1, 1, 1] ]
    ```
  - **Explanation**: A zero exists at `(1, 1)`. Therefore, row 1 and column 1 must be zeroed out.
  - **Output Matrix:**
    ```
    [ [1, 0, 1],
      [0, 0, 0],
      [1, 0, 1] ]
    ```

## Key Insights

### The "Chain Reaction" Trap

The most significant challenge is the "in-place" requirement. A naive approach would be to iterate through the matrix, and as soon as you find a `0`, you immediately set its row and column to zeros.

  - **The Problem**: Doing this will create *new* zeros. When your iteration later encounters one of these newly created zeros, it will incorrectly trigger another round of zeroing out, corrupting the result.

### A Better Approach: `O(m + n)` Space

To avoid the chain reaction, we can use a two-pass approach with extra memory.

1.  **Pass 1 (Marking)**: Create two separate sets, `rows_to_zero` and `cols_to_zero`. Iterate through the entire matrix. If you find a zero at `(r, c)`, add `r` to `rows_to_zero` and `c` to `cols_to_zero`.
2.  **Pass 2 (Setting)**: Iterate through the matrix again. For each cell `(r, c)`, if `r` is in `rows_to_zero` or `c` is in `cols_to_zero`, set `matrix[r][c] = 0`.

<!-- end list -->

  - This works perfectly but uses `O(m + n)` extra space for the sets, which doesn't meet the follow-up constraint.

### The Optimal Insight: Using the Matrix as Memory (`O(1)` Space)

The key to a constant space solution is to realize that we don't need separate sets. We can use a part of the matrix **itself** as our memory to "mark" which rows and columns need to be zeroed. The most convenient place to do this is the **first row and first column**.

**The Caveat**: What if the first row or first column *originally* contained a zero? Using them as markers would overwrite this information. To solve this, we must use two extra boolean flags, `first_row_has_zero` and `first_col_has_zero`, to store their initial state before we start the marking process.

## Solution Approach

This solution uses the first row and column as markers to achieve `O(1)` space complexity. The process is broken down into four distinct steps.

```python
from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        rows, cols = len(matrix), len(matrix[0])
        first_row_has_zero = False
        first_col_has_zero = False

        # Step 1: Check if the first row and first column have any zeros.
        for r in range(rows):
            if matrix[r][0] == 0:
                first_col_has_zero = True
                break
        for c in range(cols):
            if matrix[0][c] == 0:
                first_row_has_zero = True
                break

        # Step 2: Use the first row/col as markers for the rest of the matrix.
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][c] == 0:
                    matrix[r][0] = 0
                    matrix[0][c] = 0

        # Step 3: Zero out cells based on the markers in the first row/col.
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0

        # Step 4: Zero out the first row and/or column if they needed it.
        if first_row_has_zero:
            for c in range(cols):
                matrix[0][c] = 0
        
        if first_col_has_zero:
            for r in range(rows):
                matrix[r][0] = 0
```

## Detailed Code Analysis

### Step 1: Check the First Row and Column

```python
first_row_has_zero = False
first_col_has_zero = False
# ... loops to check matrix[r][0] and matrix[0][c] ...
```

  - This is our "backup" step. We are about to use the first row and column as a scratchpad. Before we do, we must check if they themselves need to be zeroed out at the end. We store this information in two boolean flags.

### Step 2: Mark the First Row/Column

```python
for r in range(1, rows):
    for c in range(1, cols):
        if matrix[r][c] == 0:
            matrix[r][0] = 0
            matrix[0][c] = 0
```

  - This is the "marking" pass. We iterate through the *rest* of the matrix (everything except the first row and column).
  - If we find a zero at `matrix[r][c]`, we don't touch that cell. Instead, we place a zero at the top of its column (`matrix[0][c] = 0`) and at the start of its row (`matrix[r][0] = 0`). These act as signals.

### Step 3: Set Zeros Based on Marks

```python
for r in range(1, rows):
    for c in range(1, cols):
        if matrix[r][0] == 0 or matrix[0][c] == 0:
            matrix[r][c] = 0
```

  - This is the "setting" pass. Again, we iterate through the rest of the matrix.
  - For each cell `matrix[r][c]`, we look at its markers. If the marker at the start of its row (`matrix[r][0]`) is zero, OR the marker at the top of its column (`matrix[0][c]`) is zero, then we know this cell must be set to `0`.

### Step 4: Final Cleanup

```python
if first_row_has_zero:
    # ... zero out first row ...
if first_col_has_zero:
    # ... zero out first column ...
```

  - This is the final step where we use our backup flags. After the main matrix has been modified, we now zero out the first row and/or column if they were flagged in Step 1. This is done last to ensure their marker values are used by Step 3 before being erased.

## Step-by-Step Execution Trace

Let's trace the algorithm with `matrix = [[1,1,1],[1,0,1],[1,1,1]]` with extreme detail.

### **Initial State:**

  - `matrix` = `[[1,1,1],[1,0,1],[1,1,1]]`
  - `first_row_has_zero = False`
  - `first_col_has_zero = False`

-----

### **Step 1: Check First Row/Col**

  - Loop through first column `[1, 1, 1]`. No zeros found. `first_col_has_zero` remains `False`.
  - Loop through first row `[1, 1, 1]`. No zeros found. `first_row_has_zero` remains `False`.

-----

### **Step 2: Marking Pass**

  - Loop starts from `r=1, c=1`.
  - `r=1, c=1`: `matrix[1][1]` is `0`.
      - Set marker `matrix[1][0] = 0`.
      - Set marker `matrix[0][1] = 0`.
  - **Matrix state after marking:** (markers are bold)
    ```
    [ [1, **0**, 1],
      [**0**, 0, 1],
      [1, 1, 1] ]
    ```

-----

### **Step 3: Setting Pass**

  - Loop starts from `r=1, c=1`.

  - `r=1, c=1`: Check markers `matrix[1][0]` (is 0) or `matrix[0][1]` (is 0). Condition is true. Set `matrix[1][1] = 0`.

  - `r=1, c=2`: Check markers `matrix[1][0]` (is 0) or `matrix[0][2]` (is 1). Condition is true. Set `matrix[1][2] = 0`.

  - `r=2, c=1`: Check markers `matrix[2][0]` (is 1) or `matrix[0][1]` (is 0). Condition is true. Set `matrix[2][1] = 0`.

  - `r=2, c=2`: Check markers `matrix[2][0]` (is 1) or `matrix[0][2]` (is 1). Condition is false. `matrix[2][2]` remains `1`.

  - **Matrix state after setting:**

    ```
    [ [1, 0, 1],
      [0, 0, 0],
      [1, 0, 1] ]
    ```

    Wait, there's a mistake in the trace. Let's re-verify the logic. Ah, `matrix[2][2]` should be `1` in the input, but in the output it is `1`. Why? The marker for column 2 is `matrix[0][2]`. The marker for row 2 is `matrix[2][0]`. Let's re-trace the example `[[0,1,2,0],[3,4,5,2],[1,3,1,5]]` as it's more illustrative. My apologies, the previous trace was based on the simple example which made it hard to see the final step. The logic of the code is sound, the trace was flawed. Let's re-do the trace with the first example from the prompt. `matrix = [[1,1,1],[1,0,1],[1,1,1]]`.

  - **Initial State**: `[[1,1,1],[1,0,1],[1,1,1]]`

  - **Step 1**: `first_row_has_zero` = false, `first_col_has_zero` = false.

  - **Step 2 (Marking)**: `r=1, c=1` is 0. So, set `matrix[1][0] = 0` and `matrix[0][1] = 0`.

      - Matrix becomes: `[[1, **0**, 1], [**0**, 0, 1], [1, 1, 1]]`

  - **Step 3 (Setting)**:

      - `r=1, c=1`: `matrix[1][0]` is 0, so `matrix[1][1]` becomes 0.
      - `r=1, c=2`: `matrix[1][0]` is 0, so `matrix[1][2]` becomes 0.
      - `r=2, c=1`: `matrix[0][1]` is 0, so `matrix[2][1]` becomes 0.
      - `r=2, c=2`: `matrix[2][0]` is 1 and `matrix[0][2]` is 1. No change.
      - Matrix becomes: `[[1, 0, 1], [0, 0, 0], [1, 0, 1]]`

  - **Step 4 (Cleanup)**: `first_row_has_zero` and `first_col_has_zero` are both false. Nothing to do.

  - **Final Result**: `[[1,0,1],[0,0,0],[1,0,1]]`, which is correct.

## Performance Analysis

### Time Complexity: O(m \* n)

  - The algorithm iterates through the matrix a constant number of times (once to check the first row/col, once to mark, once to set, and once to clean up). The total time is proportional to the number of cells in the matrix.

### Space Complexity: O(1)

  - This is the main advantage of this approach. We only use two boolean flags. The space required is constant and does not depend on the size of the matrix.