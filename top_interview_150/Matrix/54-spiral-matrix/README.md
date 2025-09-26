# 54\. Spiral Matrix - Solution Explanation

## Problem Overview

You are given an `m x n` matrix (a 2D grid of numbers). The task is to return all the elements of the matrix in **spiral order**.

**Spiral Order Definition:**
The traversal starts at the top-left corner (`matrix[0][0]`), moves right to the end of the first row, then down the last column, then left across the last row, then up the first column, and continues this pattern, spiraling inwards.

**Examples:**

```python
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]

Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

## Key Insights

### Simulating the Path with Boundaries

A complex mathematical formula to calculate the position of each element would be very difficult to figure out. A much more direct and intuitive approach is to **simulate** the spiral path.

The key insight is that we can think of the spiral as a series of **layers**. We first traverse the outermost layer of the matrix, then the next layer inside that, and so on, until we reach the center.

To manage this, we can use **four pointers** to define the boundaries of the current rectangular layer we are traversing:

  - `top`: The index of the top row of the current layer.
  - `bottom`: The index of the bottom row.
  - `left`: The index of the leftmost column.
  - `right`: The index of the rightmost column.

After we traverse each side of a layer, we simply "shrink" the corresponding boundary inward to define the next, smaller layer.

## Solution Approach

This solution implements the layer-by-layer traversal using the four boundary pointers. A `while` loop continues as long as there is a valid layer to process, and inside the loop, four `for` loops handle the four directions of movement.

```python
from typing import List

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix:
            return []
        
        result = []
        rows, cols = len(matrix), len(matrix[0])
        
        # Initialize the four boundaries
        top, bottom = 0, rows - 1
        left, right = 0, cols - 1
        
        # Loop as long as the boundaries define a valid area
        while left <= right and top <= bottom:
            
            # --- Traverse the top row (left to right) ---
            for i in range(left, right + 1):
                result.append(matrix[top][i])
            top += 1
            
            # --- Traverse the right column (top to bottom) ---
            for i in range(top, bottom + 1):
                result.append(matrix[i][right])
            right -= 1
            
            # Check if there's still a valid row to traverse (for non-square matrices)
            if top <= bottom:
                # --- Traverse the bottom row (right to left) ---
                for i in range(right, left - 1, -1):
                    result.append(matrix[bottom][i])
                bottom -= 1
            
            # Check if there's still a valid column to traverse
            if left <= right:
                # --- Traverse the left column (bottom to top) ---
                for i in range(bottom, top - 1, -1):
                    result.append(matrix[i][left])
                left += 1
                
        return result
```

## Detailed Code Analysis

### Step 1: Initialization

```python
result = []
rows, cols = len(matrix), len(matrix[0])
top, bottom = 0, rows - 1
left, right = 0, cols - 1
```

  - We initialize an empty `result` list to store our output.
  - We set up our four boundary pointers to encompass the entire matrix.

### Step 2: The Main Loop

```python
while left <= right and top <= bottom:
```

  - This loop is the engine of the algorithm. It continues as long as our boundaries define a valid, non-empty rectangle. The moment `left` crosses `right` or `top` crosses `bottom`, it means we have visited every element.

### Step 3: Traversing a Layer (Inside the `while` loop)

The process is a sequence of four movements for each layer.

**Movement 1: Go Right**

```python
for i in range(left, right + 1):
    result.append(matrix[top][i])
top += 1
```

  - We iterate from the `left` column to the `right` column along the current `top` row, appending each element.
  - After we've finished the row, we increment `top` to "shrink" the boundary, as this row is now fully processed.

**Movement 2: Go Down**

```python
for i in range(top, bottom + 1):
    result.append(matrix[i][right])
right -= 1
```

  - Next, we iterate from the new `top` row down to the `bottom` row along the `right` column.
  - After finishing, we decrement `right` to shrink the right boundary inward.

**Movement 3: Go Left**

```python
if top <= bottom:
    for i in range(right, left - 1, -1):
        result.append(matrix[bottom][i])
    bottom -= 1
```

  - We iterate from the new `right` column back to the `left` column (in reverse) along the `bottom` row.
  - The `if top <= bottom:` check is crucial. For matrices that are just a single column or after a few spirals, the `top` pointer might have already crossed the `bottom` pointer. This check prevents us from re-processing a row.

**Movement 4: Go Up**

```python
if left <= right:
    for i in range(bottom, top - 1, -1):
        result.append(matrix[i][left])
    left += 1
```

  - Finally, we iterate from the new `bottom` row up to the `top` row (in reverse) along the `left` column.
  - The `if left <= right:` check is similar to the one above, preventing re-processing of a single column.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `matrix = [[1,2,3],[4,5,6],[7,8,9]]` with extreme detail.

### **Initial State:**

  - `result = []`
  - `top = 0`, `bottom = 2`, `left = 0`, `right = 2`

-----

### **Pass 1 (Outer Layer)**

1.  **Go Right**: `for i` from `0` to `2`. Appends `matrix[0][0]`, `matrix[0][1]`, `matrix[0][2]`.
      - `result` is now `[1, 2, 3]`.
      - Shrink boundary: `top` becomes `1`.
2.  **Go Down**: `for i` from `1` to `2`. Appends `matrix[1][2]`, `matrix[2][2]`.
      - `result` is now `[1, 2, 3, 6, 9]`.
      - Shrink boundary: `right` becomes `1`.
3.  **Go Left**: `if 1 <= 2` is true. `for i` from `1` down to `0`. Appends `matrix[2][1]`, `matrix[2][0]`.
      - `result` is now `[1, 2, 3, 6, 9, 8, 7]`.
      - Shrink boundary: `bottom` becomes `1`.
4.  **Go Up**: `if 0 <= 1` is true. `for i` from `1` down to `1`. Appends `matrix[1][0]`.
      - `result` is now `[1, 2, 3, 6, 9, 8, 7, 4]`.
      - Shrink boundary: `left` becomes `1`.

**State after Pass 1:**

  - `result = [1, 2, 3, 6, 9, 8, 7, 4]`
  - `top = 1`, `bottom = 1`, `left = 1`, `right = 1`

-----

### **Pass 2 (Inner Layer)**

  - The `while` condition `1 <= 1 AND 1 <= 1` is true.

<!-- end list -->

1.  **Go Right**: `for i` from `1` to `1`. Appends `matrix[1][1]`.
      - `result` is now `[1, 2, 3, 6, 9, 8, 7, 4, 5]`.
      - Shrink boundary: `top` becomes `2`.
2.  **Go Down**: `for i` from `2` to `1`. The loop range is empty, so nothing happens.
      - Shrink boundary: `right` becomes `0`.
3.  **Go Left**: The check `if top <= bottom` (`2 <= 1`) is now **False**. This step is skipped.
4.  **Go Up**: The check `if left <= right` (`1 <= 0`) is now **False**. This step is skipped.

**State after Pass 2:**

  - `result = [1, 2, 3, 6, 9, 8, 7, 4, 5]`
  - `top = 2`, `bottom = 1`, `left = 1`, `right = 0`

-----

### **End of Algorithm**

  - The `while` condition `1 <= 0 AND 2 <= 1` is now **False**. The loop terminates.
  - The function returns the final `result`: **`[1, 2, 3, 6, 9, 8, 7, 4, 5]`**.

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` is the number of rows and `n` is the number of columns. The algorithm visits every element in the matrix exactly once.

### Space Complexity: O(1)

  - If we do not count the output `result` array, the algorithm uses only a few pointer variables. The space required is constant.