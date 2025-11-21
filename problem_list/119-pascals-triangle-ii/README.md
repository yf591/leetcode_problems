# 119\. Pascal's Triangle II - Solution Explanation

## Problem Overview

Given an integer `rowIndex`, return the specific row of Pascal's triangle corresponding to that index (0-indexed).

**Pascal's Triangle Rules:**

1.  The first and last numbers of every row are `1`.
2.  Any other number is the sum of the two numbers directly above it in the previous row.

**Example (`rowIndex = 3`):**

```
Row 0:      [1]
Row 1:     [1, 1]
Row 2:    [1, 2, 1]
Row 3:   [1, 3, 3, 1]
```

Output: `[1, 3, 3, 1]`

## Key Insights

### 1\. The Relationship Between Rows

To generate Row `N`, you only strictly need Row `N-1`. You don't need Row `N-2` or anything before it. This hints that we don't need to store the entire triangle (which would be $O(N^2)$ space). We only need to keep track of the "current" row.

### 2\. The Problem with Updating In-Place

If we try to update a row from left to right to transform it into the next row, we run into a data overwrite problem.

Let's try to turn Row 2 `[1, 2, 1]` into Row 3 `[1, 3, 3, 1]`.

1.  Expand the array: `[1, 2, 1, 1]`
2.  **Left-to-Right Attempt**:
      * Update `index 1`: We want `old[0] + old[1]`. `1 + 2 = 3`. Array becomes `[1, **3**, 1, 1]`.
      * Update `index 2`: We want `old[1] + old[2]`. But `row[1]` is now **3**, not the original **2**\! The calculation becomes `3 + 1 = 4` (Wrong\! It should be `2 + 1 = 3`).

### 3\. The Backwards Iteration Trick

To solve the overwrite problem without using a second temporary array, we iterate **backwards**.
When calculating `row[j] = row[j] + row[j-1]`, if we start from the right side, `row[j]` and `row[j-1]` still hold their "old" values from the previous level because the loop hasn't reached them yet.

## Solution Approach

This solution uses a single list `row` and evolves it in-place `rowIndex` times.

```python
from typing import List

class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        # Initialize the list with the 0-th row.
        row = [1]
        
        # Perform the transformation 'rowIndex' times.
        for _ in range(rowIndex):
            # 1. Expand the row.
            # We append 1 because every row in Pascal's triangle ends with 1.
            # This increases the length of the array by 1.
            row.append(1)
            
            # 2. Update the intermediate values.
            # We iterate backwards from the second-to-last index down to 1.
            # range(start, stop, step)
            # start: len(row) - 2 (the element before the new 1 we just appended)
            # stop: 0 (exclusive, so we stop at index 1)
            # step: -1 (move backwards)
            for j in range(len(row) - 2, 0, -1):
                row[j] += row[j - 1]
                
        return row
```

## Detailed Code Analysis

### Step 1: Initialization

```python
row = [1]
```

  - We start with the base case, which corresponds to `rowIndex = 0`.

### Step 2: The Expansion Loop

```python
for _ in range(rowIndex):
    row.append(1)
```

  - We loop `rowIndex` times. Each iteration represents moving one level down the triangle.
  - `row.append(1)`: Every new row has one more element than the previous one, and the last element is always `1`. By appending `1`, we set up the correct size and the correct final value.

### Step 3: The Backwards Update Loop

```python
for j in range(len(row) - 2, 0, -1):
    row[j] += row[j - 1]
```

  - **`len(row) - 2`**: We start at the second-to-last element. Why?
      - The last element (index `len(row)-1`) is the `1` we just appended. It doesn't need to change.
  - **`0` (stop)**: We stop before index 0. Why?
      - The first element (index `0`) is always `1`. It doesn't need to change.
  - **`row[j] += row[j-1]`**: The value at the current position becomes the sum of itself (representing the value directly above-right in the visual triangle) and its left neighbor (representing the value directly above-left).

## Step-by-Step Execution Trace

Let's trace `rowIndex = 3`.

**Start**: `row = [1]`

**Iteration 1 (Building Row 1)**:

1.  `append(1)`: `row` becomes `[1, 1]`.
2.  Inner loop `range(0, 0, -1)`: Does not run.
      * Result: `[1, 1]` (Correct)

**Iteration 2 (Building Row 2)**:

1.  `append(1)`: `row` becomes `[1, 1, 1]`.
2.  Inner loop `range(1, 0, -1)` (Index 1 only):
      * `j=1`: `row[1] = row[1] + row[0]` -\> `1 + 1 = 2`.
      * `row` becomes `[1, 2, 1]`.
      * Result: `[1, 2, 1]` (Correct)

**Iteration 3 (Building Row 3)**:

1.  `append(1)`: `row` becomes `[1, 2, 1, 1]`.
2.  Inner loop `range(2, 0, -1)` (Indices 2, 1):
      * **`j=2`**: `row[2] = row[2] + row[1]` -\> `1 + 2 = 3`.
          * `row` becomes `[1, 2, 3, 1]`.
      * **`j=1`**: `row[1] = row[1] + row[0]` -\> `2 + 1 = 3`.
          * `row` becomes `[1, 3, 3, 1]`.
      * Result: `[1, 3, 3, 1]` (Correct)

## Performance Analysis

### Time Complexity: $O(k^2)$

  - Where $k$ is the `rowIndex`.
  - We have an outer loop that runs $k$ times.
  - The inner loop runs roughly $i$ times for the $i$-th iteration.
  - Total operations ≈ $1 + 2 + 3 + ... + k = \frac{k(k+1)}{2}$, which is quadratic.

### Space Complexity: $O(k)$

  - We only use a single list `row` that grows to size $k+1$. This is the minimal space required simply to store the answer. We use no auxiliary data structures (like a matrix).