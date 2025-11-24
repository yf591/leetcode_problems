# 74\. Search a 2D Matrix - Solution Explanation

## Problem Overview

You are given an `m x n` integer matrix with the following two properties:

1.  Each row is sorted in non-decreasing order.
2.  The first integer of each row is greater than the last integer of the previous row.

Given an integer `target`, return `true` if `target` is in the matrix or `false` otherwise. You must write a solution in **O(log(m \* n))** time complexity.

**Example 1:**

```python
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true
```

**Example 2:**

```python
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
```

## Deep Dive: What is Binary Search? 

**Binary Search** is an efficient algorithm for finding an item from a **sorted** list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one.

**The Analogy:**
Imagine looking for a word in a dictionary. You don't read every page from the beginning.

1.  You open the book to the **middle**.
2.  If the word you are looking for comes *alphabetically before* the word on the current page, you ignore the entire second half of the book.
3.  You repeat the process with the first half, opening it to the middle.
4.  You keep cutting the search space in half until you find the word.

**Why is it fast?**
Because we discard half the possibilities in every step, the time complexity is **O(log n)** (logarithmic time). For reference:

  - Searching 1,000,000 items linearly takes up to 1,000,000 steps.
  - Searching 1,000,000 items with Binary Search takes only about **20 steps**.

## Key Insights

### 1\. The "Virtual Flattening" Trick

The problem constraints tell us that the matrix is sorted row by row, and the end of one row flows into the start of the next.

  - Row 0 ends with `7`.
  - Row 1 starts with `10`.
  - Row 1 ends with `20`.
  - Row 2 starts with `23`.

If we were to "unroll" or "flatten" this matrix into a single list, it would look like this:
`[1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]`
This is a perfectly sorted 1D array\!

### 2\. Coordinate Mapping

We don't want to actually convert the matrix to a list (that would take O(m\*n) memory and time). Instead, we can use math to map an index from a "virtual" 1D array back to the 2D matrix coordinates.

If we have an index `mid` ranging from `0` to `(m*n) - 1`:

  - **Row Index**: `row = mid // n` (Integer division by the number of columns).
  - **Column Index**: `col = mid % n` (Modulo by the number of columns).

This allows us to run a standard Binary Search as if we had a 1D array, while accessing the data in the 2D matrix.

## Solution Approach

This solution treats the 2D matrix as a virtual 1D array and performs a standard binary search.

```python
from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix:
            return False
        
        m = len(matrix)     # Number of rows
        n = len(matrix[0])  # Number of columns
        
        # Initialize binary search boundaries for the "virtual" 1D array.
        # Range is from 0 to (total_elements - 1).
        left = 0
        right = (m * n) - 1
        
        while left <= right:
            # Calculate the middle index in the virtual 1D array.
            mid = (left + right) // 2
            
            # Convert the 1D 'mid' index back to 2D matrix coordinates.
            # Row is quotient, Column is remainder.
            row = mid // n
            col = mid % n
            
            # Get the value at the calculated coordinates.
            mid_val = matrix[row][col]
            
            # Standard Binary Search comparison logic.
            if mid_val == target:
                return True
            elif mid_val < target:
                # Value is too small, target is in the right half.
                left = mid + 1
            else:
                # Value is too big, target is in the left half.
                right = mid - 1
                
        return False
```

## Detailed Code Analysis

### Step 1: Initialization

```python
m = len(matrix)
n = len(matrix[0])
left = 0
right = (m * n) - 1
```

  - We get the dimensions of the matrix.
  - `left` is initialized to `0` (the index of the very first element).
  - `right` is initialized to the total number of elements minus 1 (the index of the very last element). This defines our search space.

### Step 2: The Loop and Midpoint

```python
while left <= right:
    mid = (left + right) // 2
```

  - This is the standard binary search loop. It continues as long as the search space is valid (left index is not greater than right index).
  - `mid` calculates the index exactly in the middle of our current search range.

### Step 3: The Coordinate Conversion (The Magic)

```python
row = mid // n
col = mid % n
mid_val = matrix[row][col]
```

  - This is where we translate the 1D concept into 2D reality.
  - If `mid = 5` and we have `4` columns (`n=4`):
      - `row = 5 // 4 = 1` (We are in the second row, index 1).
      - `col = 5 % 4 = 1` (We are in the second column, index 1).
      - So `mid=5` corresponds to `matrix[1][1]`.

### Step 4: Comparison and Adjustment

```python
if mid_val == target:
    return True
elif mid_val < target:
    left = mid + 1
else:
    right = mid - 1
```

  - **Found**: If `mid_val` matches `target`, we return `True` immediately.
  - **Too Small**: If `mid_val < target`, we know the target must be "greater" (further down the list). We discard the left half by moving `left` to `mid + 1`.
  - **Too Big**: If `mid_val > target`, we know the target must be "smaller" (earlier in the list). We discard the right half by moving `right` to `mid - 1`.

## Step-by-Step Execution Trace

Let's trace the algorithm with `matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]` and `target = 3`.
Dimensions: `m = 3`, `n = 4`. Total elements = 12.

### **Initial State:**

  - `left = 0`
  - `right = 11`

-----

### **Iteration 1**

1.  **Calculate Mid**: `mid = (0 + 11) // 2 = 5`.
2.  **Convert Coordinates**:
      - `row = 5 // 4 = 1`
      - `col = 5 % 4 = 1`
3.  **Get Value**: `mid_val = matrix[1][1]`, which is **11**.
4.  **Compare**: `11 > 3` (Too Big).
5.  **Action**: Move `right` to `mid - 1`.
      - `right = 4`.

-----

### **Iteration 2**

1.  **Calculate Mid**: `mid = (0 + 4) // 2 = 2`.
2.  **Convert Coordinates**:
      - `row = 2 // 4 = 0`
      - `col = 2 % 4 = 2`
3.  **Get Value**: `mid_val = matrix[0][2]`, which is **5**.
4.  **Compare**: `5 > 3` (Too Big).
5.  **Action**: Move `right` to `mid - 1`.
      - `right = 1`.

-----

### **Iteration 3**

1.  **Calculate Mid**: `mid = (0 + 1) // 2 = 0`.
2.  **Convert Coordinates**:
      - `row = 0 // 4 = 0`
      - `col = 0 % 4 = 0`
3.  **Get Value**: `mid_val = matrix[0][0]`, which is **1**.
4.  **Compare**: `1 < 3` (Too Small).
5.  **Action**: Move `left` to `mid + 1`.
      - `left = 1`.

-----

### **Iteration 4**

1.  **Calculate Mid**: `mid = (1 + 1) // 2 = 1`.
2.  **Convert Coordinates**:
      - `row = 1 // 4 = 0`
      - `col = 1 % 4 = 1`
3.  **Get Value**: `mid_val = matrix[0][1]`, which is **3**.
4.  **Compare**: `3 == 3` (Match\!).
5.  **Action**: Return **`True`**.

## Performance Analysis

### Time Complexity: O(log(m \* n))

  - We are performing a standard Binary Search on a virtual range of size `m * n`.
  - Binary search cuts the search space in half with each iteration.
  - The number of iterations is proportional to the logarithm of the total number of elements.

### Space Complexity: O(1)

  - We only use a few integer variables (`left`, `right`, `mid`, `row`, `col`) to track our position.
  - We do not create any new data structures that scale with the input size. The "flattening" is purely mathematical and virtual, requiring no extra memory.