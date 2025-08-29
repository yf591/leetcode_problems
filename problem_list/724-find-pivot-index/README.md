# 724\. Find Pivot Index - Solution Explanation

## Problem Overview

You are given an array of integers `nums`. The goal is to find a **"pivot index"**.

**Pivot Index Definition:**
A pivot index is an index where the sum of all numbers **strictly to its left** is equal to the sum of all numbers **strictly to its right**.

**Key Rules:**

  - If the pivot is the first element (index 0), the sum of the left side is considered `0`.
  - If the pivot is the last element, the sum of the right side is considered `0`.
  - If multiple pivot indices exist, you must return the **leftmost** one.
  - If no pivot index exists, return `-1`.

**Examples:**

```python
Input: nums = [1,7,3,6,5,6]
Output: 3
Explanation:
At index 3 (value 6):
- Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
- Right sum = nums[4] + nums[5] = 5 + 6 = 11
The sums are equal, so 3 is the pivot index.

Input: nums = [2,1,-1]
Output: 0
Explanation:
At index 0 (value 2):
- Left sum = 0 (no elements to the left)
- Right sum = nums[1] + nums[2] = 1 + (-1) = 0
The sums are equal, so 0 is the pivot index.
```

## Key Insights

### The Inefficient Brute-Force Approach

A naive way to solve this would be to check every single index. For each index, you would loop through all elements to its left to calculate a `left_sum` and loop through all elements to its right for a `right_sum`. This involves nested loops and results in a slow `O(n²)` solution, which is not ideal.

### The Prefix Sum Insight (The Efficient Way)

The key to an efficient `O(n)` solution is to avoid re-calculating the sums over and over. If we know the **total sum** of the entire array, and we keep track of the **sum of elements to the left** as we iterate, we can figure out the sum of the elements to the right with a single, simple calculation.

The formula is:
**`right_sum = total_sum - left_sum - current_number`**

This insight allows us to find the answer in a single pass after an initial sum calculation.

## Solution Approach

This solution first calculates the total sum of the array. Then, it iterates through the array a single time, maintaining a `left_sum` and using the formula to derive the `right_sum`, checking for the pivot condition at each step.

```python
from typing import List

class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        # Step 1: Calculate the total sum of all numbers in the array.
        total_sum = sum(nums)
        
        # Step 2: Initialize the sum of numbers to the left of the current index.
        left_sum = 0
        
        # Step 3: Iterate through the array, checking each index.
        for i, num in enumerate(nums):
            # Step 3a: Calculate the right_sum using our formula.
            right_sum = total_sum - left_sum - num
            
            # Step 3b: Check if the current index is a pivot.
            if left_sum == right_sum:
                return i
            
            # Step 3c: Update the left_sum for the *next* iteration.
            left_sum += num
            
        # Step 4: If the loop finishes, no pivot was found.
        return -1
```

## Detailed Code Analysis

### Step 1: Pre-calculation of Total Sum

```python
total_sum = sum(nums)
```

  - This is our one-time setup step. We get the sum of all numbers in the array. This is an `O(n)` operation. This `total_sum` will be our constant reference for the main loop.

### Step 2: Initialization of Left Sum

```python
left_sum = 0
```

  - We initialize `left_sum` to `0`. This is because before we start our loop at the first element (index `0`), the sum of elements to its left is `0`, as per the problem's definition.

### Step 3: The Main Loop and Pivot Check

```python
for i, num in enumerate(nums):
    right_sum = total_sum - left_sum - num
    if left_sum == right_sum:
        return i
    left_sum += num
```

  - We use `enumerate` to get both the index `i` and the value `num` in each iteration.
  - **`right_sum = total_sum - left_sum - num`**: This is the core calculation. For the current index `i`, we take the grand `total_sum`, subtract everything we've seen so far to the left (`left_sum`), and subtract the current element itself (`num`). What remains must be the sum of everything to the right.
  - **`if left_sum == right_sum:`**: This is the pivot condition check. If it's true, we've found our answer. Since we are iterating from left to right, the first one we find is guaranteed to be the *leftmost* pivot, so we can return `i` immediately.
  - **`left_sum += num`**: This is the crucial update step. *After* checking the current index `i`, we add its number `num` to `left_sum`. This prepares `left_sum` to be correct for the *next* iteration when the loop moves to index `i+1`.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [1, 7, 3, 6, 5, 6]`.

1.  **Pre-calculation**: `total_sum` = `1+7+3+6+5+6` = **28**.
2.  **Initialization**: `left_sum = 0`.
3.  **The Loop**:

| `i` | `num` | `left_sum` (at start) | `right_sum` calculation (`28 - left_sum - num`) | `left_sum == right_sum`? | Action | `left_sum` (at end) |
| :-- | :-- | :--- | :--- | :--- | :--- | :--- |
| **0** | **1** | 0 | `28 - 0 - 1 = 27` | `0 == 27` -\> False | `left_sum += 1` | 1 |
| **1** | **7** | 1 | `28 - 1 - 7 = 20` | `1 == 20` -\> False | `left_sum += 7` | 8 |
| **2** | **3** | 8 | `28 - 8 - 3 = 17` | `8 == 17` -\> False | `left_sum += 3` | 11 |
| **3** | **6** | 11 | `28 - 11 - 6 = 11` | `11 == 11` -\> **True** | **Return `i` (which is 3)** | - |

  - The loop stops and the function returns **3**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We have one pass to calculate `sum(nums)` (`O(n)`) and one `for` loop that iterates `n` times (`O(n)`). The total complexity is `O(n) + O(n)`, which simplifies to `O(n)`.

### Space Complexity: O(1)

  - We only use a few variables (`total_sum`, `left_sum`, `i`, `num`). The space required is constant and does not grow with the size of the input list.

## Key Learning Points

  - **Prefix Sum Technique**: This problem is a prime example of the prefix sum pattern. By keeping a running total (`left_sum`), you can derive related sums (`right_sum`) very efficiently.
  - **Optimization**: This solution shows how to turn a slow, `O(n²)` brute-force idea into a highly efficient `O(n)` linear-time algorithm by avoiding re-computation.
  - **Order of Operations**: The order inside the loop is critical: first check, then update the `left_sum` for the *next* iteration.