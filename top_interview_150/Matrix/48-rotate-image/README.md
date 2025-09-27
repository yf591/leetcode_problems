# 48\. Rotate Image - Solution Explanation

## Problem Overview

You are given an `n x n` 2D matrix which represents an image. The task is to rotate this image by **90 degrees clockwise**.

**Key Constraints:**

  - The rotation must be done **in-place**, which means you have to modify the input matrix directly.
  - You are **not allowed** to allocate a second matrix to perform the rotation. This means the space complexity must be `O(1)`.

**Example:**

  - **Input Matrix:**
    ```
    [ [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9] ]
    ```
  - **Output Matrix (After 90° Clockwise Rotation):**
    ```
    [ [7, 4, 1],
      [8, 5, 2],
      [9, 6, 3] ]
    ```

## Key Insights

### The "In-Place" Challenge

The requirement to perform the rotation in-place with `O(1)` extra space is the main challenge. A simple solution would be to create a new `n x n` matrix and copy the elements from the old matrix to their new, rotated positions. However, this is forbidden by the constraints.

### Decomposing the Rotation

The key insight is that a complex 90-degree clockwise rotation can be broken down into two much simpler, sequential operations:

1.  **Transpose the Matrix**: A transpose operation flips the matrix over its main diagonal (the one from top-left to bottom-right). The element at `(row, col)` swaps with the element at `(col, row)`.
2.  **Reverse Each Row**: After the matrix is transposed, if you reverse each individual row, you achieve the final rotated state.

This two-step process is much easier to implement in-place than a direct four-way swap of corner elements.

## Solution Approach

This solution directly implements the "Transpose and Reverse" strategy. It first modifies the matrix by transposing it, and then it iterates through each row to reverse it.

```python
from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        
        # --- Step 1: Transpose the matrix ---
        # We iterate through the upper triangle of the matrix.
        for i in range(n):
            for j in range(i + 1, n):
                # Swap the element at (i, j) with the element at (j, i).
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
                
        # --- Step 2: Reverse each row ---
        for i in range(n):
            # The list.reverse() method modifies the list in-place.
            matrix[i].reverse()
```

## Detailed Code Analysis

### Step 1: Transposing the Matrix

```python
for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```

  - **The Loops**: This nested loop structure is designed to iterate over the **upper triangle** of the matrix (all elements above the main diagonal).
      - The outer loop `for i in range(n)` iterates through the rows.
      - The inner loop `for j in range(i + 1, n)` iterates through the columns, but critically, it **starts from `i + 1`**.
  - **Why `j` starts at `i + 1`?** This is the key to a correct transpose. It ensures we only swap each pair of elements `(i, j)` and `(j, i)` exactly once. If we looped `for j in range(n)`, we would swap `(0, 1)` with `(1, 0)`, and then later, we would swap `(1, 0)` with `(0, 1)` again, which would undo our work and leave the matrix unchanged\!
  - **The Swap**: `matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]` is a concise, Pythonic way to swap the two values without needing a temporary variable.

### Step 2: Reversing Each Row

```python
for i in range(n):
    matrix[i].reverse()
```

  - After the transpose is complete, we simply loop through each row of the matrix.
  - `matrix[i]` gives us the list representing the `i`-th row.
  - The `.reverse()` method is a built-in Python list method that reverses the elements of the list **in-place**, which perfectly satisfies our `O(1)` space constraint.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `matrix = [[1,2,3],[4,5,6],[7,8,9]]` with extreme detail.

### **Initial Matrix:**

```
[ [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9] ]
```

-----

### **Phase 1: Transpose**

The nested loops will perform the following swaps:

  - `i=0, j=1`: Swap `matrix[0][1]` (2) and `matrix[1][0]` (4).
  - `i=0, j=2`: Swap `matrix[0][2]` (3) and `matrix[2][0]` (7).
  - `i=1, j=2`: Swap `matrix[1][2]` (6) and `matrix[2][1]` (8).

**Matrix after Transpose:**

```
[ [1, 4, 7],
  [2, 5, 8],
  [3, 6, 9] ]
```

-----

### **Phase 2: Reverse Each Row**

The loop will now reverse each of the rows in the transposed matrix.

1.  **Reverse row 0**: `[1, 4, 7]` becomes `[7, 4, 1]`.
2.  **Reverse row 1**: `[2, 5, 8]` becomes `[8, 5, 2]`.
3.  **Reverse row 2**: `[3, 6, 9]` becomes `[9, 6, 3]`.

**Matrix after Reversing Rows (Final Result):**

```
[ [7, 4, 1],
  [8, 5, 2],
  [9, 6, 3] ]
```

The function modifies the matrix in-place and does not return anything. The final state of the matrix is the correct rotated image.

## Performance Analysis

### Time Complexity: O(n²)

  - Where `n` is the side length of the `n x n` matrix.
  - The transpose step involves a nested loop that visits roughly half of the `n * n` elements. This is `O(n²)`.
  - The row reversal step involves iterating through `n` rows and reversing each one. Reversing a row of length `n` takes `O(n)` time. So this step is `n * O(n) = O(n²)`.
  - The total time complexity is `O(n²) + O(n²)`, which is `O(n²)`. This is optimal, as we must touch every element at least once.

### Space Complexity: O(1)

  - All operations (swapping, reversing rows) are done **in-place** on the original matrix. We only use a few variables for loop indices. The extra space required is constant.

## Key Learning Points

  - **Problem Decomposition**: This is a prime example of solving a complex problem by breaking it down into a sequence of simpler, well-known operations (Transpose + Reverse).
  - **In-Place Algorithms**: It showcases powerful techniques for modifying data structures directly in memory to save space.
  - **Matrix Transposition**: Understanding how to correctly iterate over a matrix to perform an in-place transpose is a fundamental skill. The `j = i + 1` trick is the key to avoiding redundant swaps.