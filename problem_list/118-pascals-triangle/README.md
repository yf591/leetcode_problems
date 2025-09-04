# 118\. Pascal's Triangle - Solution Explanation

## Problem Overview

The task is to generate the first `numRows` of **Pascal's Triangle**.

**Pascal's Triangle Definition:**
It's a triangular array of numbers that starts with a `1` at the top. Each subsequent number is the sum of the two numbers directly above it. The edges of the triangle are always `1`.

**Example (`numRows = 5`):**

```
        [1]
       [1,1]
      [1,2,1]
     [1,3,3,1]
    [1,4,6,4,1]
```

The output should be a list of lists, where each inner list represents a row of the triangle.

## Key Insights

### Building Row by Row

The definition of the triangle itself gives us the key insight: **every row can be built using only the information from the row directly above it.** This is a classic "bottom-up" pattern, which is a form of Dynamic Programming. We don't need to know about `row 2` to build `row 4`; we only need `row 3`.

This tells us we can solve the problem with a simple loop. We start with the first row, and in each iteration of the loop, we generate the next row based on the one we just finished.

### The Structure of a Row

Every row in Pascal's Triangle has a predictable structure:

1.  It always starts with a `1`.
2.  Its "middle" elements are the sum of adjacent pairs from the previous row.
3.  It always ends with a `1`.

## Solution Approach

This solution builds the triangle iteratively. It starts with the first row `[[1]]` and then loops `numRows - 1` times. In each iteration, it takes the last row that was added, calculates the next row based on it, and appends the new row to the result.

```python
from typing import List

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        # Handle the edge case where numRows is 0.
        if numRows == 0:
            return []
        
        # Step 1: Start our triangle with the first row, which is always [1].
        triangle = [[1]]
        
        # Step 2: Loop to generate the remaining (numRows - 1) rows.
        # This loop starts from i=1 because we already have row 0.
        for i in range(1, numRows):
            # Step 2a: Get the previous row to build upon.
            prev_row = triangle[-1]
            
            # Step 2b: Every new row starts with a 1.
            new_row = [1]
            
            # Step 2c: Calculate the middle elements by summing adjacent pairs.
            for j in range(len(prev_row) - 1):
                sum_of_pair = prev_row[j] + prev_row[j+1]
                new_row.append(sum_of_pair)
            
            # Step 2d: Every new row also ends with a 1.
            new_row.append(1)
            
            # Step 2e: Add the completed new row to our triangle.
            triangle.append(new_row)
            
        return triangle
```

## Detailed Code Analysis

### Step 1: Initialization

```python
if numRows == 0:
    return []
triangle = [[1]]
```

  - First, we handle the simple edge case. If `numRows` is 0, we just return an empty list.
  - Then, we initialize our `triangle` variable as a list containing one list: `[[1]]`. This represents the first row (row 0) and serves as the foundation for building all subsequent rows.

### Step 2: The Main Loop

```python
for i in range(1, numRows):
```

  - This loop is responsible for creating each new row.
  - It starts from `i = 1` because `i` can represent the row number we are currently building (using 0-based indexing). Since we already have row 0, we start by building row 1.
  - The loop continues until it has built all the rows up to `numRows - 1`.

### Step 3: Inside the Loop - Building a New Row

```python
prev_row = triangle[-1]
```

  - `triangle[-1]` is a Pythonic way to get the last element of a list. In this case, it gives us the most recently added row, which is exactly what we need to build the next one.

<!-- end list -->

```python
new_row = [1]
```

  - We start building our `new_row`. According to the rules of Pascal's Triangle, it must always begin with a `1`.

<!-- end list -->

```python
for j in range(len(prev_row) - 1):
    new_row.append(prev_row[j] + prev_row[j+1])
```

  - This inner loop calculates all the "middle" elements.
  - **Why `len(prev_row) - 1`?** We are summing up *adjacent pairs*. A list of length `L` has `L-1` such pairs. For example, in `[1, 2, 1]` (length 3), the pairs are `(1, 2)` and `(2, 1)`. There are `3 - 1 = 2` pairs. This loop range ensures we don't go out of bounds when accessing `prev_row[j+1]`.

<!-- end list -->

```python
new_row.append(1)
```

  - After calculating the middle elements, we add the final `1` to the end of the `new_row`.

<!-- end list -->

```python
triangle.append(new_row)
```

  - The `new_row` is now complete. We append it to our main `triangle` list.

## Step-by-Step Execution Trace

Let's trace the algorithm for `numRows = 5` with extreme detail.

1.  **Initialization**: `triangle` starts as `[[1]]`. The `for` loop will run for `i = 1, 2, 3, 4`.

-----

### **`i = 1` (Building the 2nd row)**

  - `prev_row` = `triangle[-1]` -\> `[1]`
  - `new_row` starts as `[1]`
  - The inner loop is `for j in range(len([1]) - 1)`, which is `range(0)`. The loop does not run.
  - `new_row.append(1)`. `new_row` is now `[1, 1]`.
  - `triangle.append([1, 1])`.
  - **`triangle` state**: `[[1], [1, 1]]`

-----

### **`i = 2` (Building the 3rd row)**

  - `prev_row` = `triangle[-1]` -\> `[1, 1]`
  - `new_row` starts as `[1]`
  - The inner loop is `for j in range(len([1,1]) - 1)`, which is `range(1)`. It runs once for `j = 0`.
      - `j = 0`: `new_row.append(prev_row[0] + prev_row[1])` -\> `new_row.append(1 + 1)`. `new_row` is now `[1, 2]`.
  - `new_row.append(1)`. `new_row` is now `[1, 2, 1]`.
  - `triangle.append([1, 2, 1])`.
  - **`triangle` state**: `[[1], [1, 1], [1, 2, 1]]`

-----

### **`i = 3` (Building the 4th row)**

  - `prev_row` = `triangle[-1]` -\> `[1, 2, 1]`
  - `new_row` starts as `[1]`
  - The inner loop is `for j in range(len([1,2,1]) - 1)`, which is `range(2)`. It runs for `j = 0, 1`.
      - `j = 0`: `new_row.append(prev_row[0] + prev_row[1])` -\> `new_row.append(1 + 2)`. `new_row` is `[1, 3]`.
      - `j = 1`: `new_row.append(prev_row[1] + prev_row[2])` -\> `new_row.append(2 + 1)`. `new_row` is `[1, 3, 3]`.
  - `new_row.append(1)`. `new_row` is now `[1, 3, 3, 1]`.
  - `triangle.append([1, 3, 3, 1])`.
  - **`triangle` state**: `[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]`

-----

### **`i = 4` (Building the 5th row)**

  - `prev_row` = `triangle[-1]` -\> `[1, 3, 3, 1]`
  - `new_row` starts as `[1]`
  - The inner loop is `for j in range(len([1,3,3,1]) - 1)`, which is `range(3)`. It runs for `j = 0, 1, 2`.
      - `j = 0`: `new_row.append(1 + 3)`. `new_row` is `[1, 4]`.
      - `j = 1`: `new_row.append(3 + 3)`. `new_row` is `[1, 4, 6]`.
      - `j = 2`: `new_row.append(3 + 1)`. `new_row` is `[1, 4, 6, 4]`.
  - `new_row.append(1)`. `new_row` is now `[1, 4, 6, 4, 1]`.
  - `triangle.append([1, 4, 6, 4, 1])`.
  - **`triangle` final state**: `[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]`

-----

The main loop finishes. The function returns the final `triangle`.

## Performance Analysis

### Time Complexity: O(numRows²)

  - The total number of elements in Pascal's triangle with `N` rows is `1 + 2 + 3 + ... + N`, which is approximately `N²/2`. Since we generate every number once, the time complexity is quadratic with respect to `numRows`.

### Space Complexity: O(numRows²)

  - We need to store the entire triangle in memory. The space required is proportional to the total number of elements, which is also `O(numRows²)`.

## Key Learning Points

  - **Iterative Construction**: This problem is a prime example of building a complex structure iteratively, where each step depends on the result of the previous step.
  - **Dynamic Programming**: This is a form of bottom-up dynamic programming. The solution for row `i` is computed from the solution for row `i-1`.
  - **Looping over Pairs**: The pattern `for j in range(len(list) - 1)` is a standard way to iterate over adjacent pairs of elements in a list.