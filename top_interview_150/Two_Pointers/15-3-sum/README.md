# 15\. 3Sum - Solution Explanation

## Problem Overview

You are given an array of integers `nums`. The task is to find all **unique triplets** (`[nums[i], nums[j], nums[k]]`) where the three elements sum up to zero (`nums[i] + nums[j] + nums[k] == 0`).

**Key Rules & Constraints:**

  - The three indices `i`, `j`, and `k` must be distinct.
  - The final solution set **must not contain duplicate triplets**. For example, `[-1, 0, 1]` is the same triplet as `[0, 1, -1]`.

**Examples:**

```python
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]

Input: nums = [0,0,0]
Output: [[0,0,0]]
```

## Key Insights

### Reducing the Problem: from 3Sum to 2Sum

A brute-force approach of checking every possible combination of three numbers would be `O(n³)`, which is far too slow.

The key insight is to simplify the problem. If we can fix one of the numbers, say `a`, the problem `a + b + c = 0` becomes a much simpler one: find a pair `b` and `c` such that `b + c = -a`. This is the classic **"2Sum" problem**.

### The Power of Sorting

The "2Sum" subproblem can be solved very efficiently if the array is **sorted**. Sorting the array first allows us to use the **two-pointer technique**. It also makes the second major challenge—handling duplicates—much easier, because all identical numbers will be next to each other.

The overall strategy will be:

1.  **Sort** the entire input array.
2.  **Iterate** through the sorted array with a `for` loop, fixing the first number `nums[i]`.
3.  For each `nums[i]`, use the **two-pointer** technique on the rest of the array to find the other two numbers.

## Solution Approach

This solution implements the "Sort then Two-Pointer" strategy. It includes careful logic to skip over duplicate numbers to ensure the final result set is unique.

```python
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []
        # Step 1: Sort the array.
        nums.sort()
        n = len(nums)

        # Step 2: Main loop to fix the first element 'a' of the triplet.
        for i in range(n - 2):
            # Optimization: Skip duplicate first elements.
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Step 3: Use two pointers for the 'b' and 'c' elements.
            left, right = i + 1, n - 1
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                if current_sum < 0:
                    left += 1
                elif current_sum > 0:
                    right -= 1
                else:  # Found a triplet that sums to 0
                    result.append([nums[i], nums[left], nums[right]])
                    
                    # Move pointers inward and skip duplicates for the other two elements.
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
        return result
```

## Detailed Code Analysis

### Step 1: Sorting

```python
nums.sort()
```

  - This is the most critical pre-processing step. It takes `O(n log n)` time but enables the efficient `O(n²)` overall solution and simplifies duplicate handling.

### Step 2: The Main Loop & Duplicate Skip

```python
for i in range(n - 2):
    if i > 0 and nums[i] == nums[i - 1]:
        continue
```

  - This loop iterates through the array to pick the first element of our triplet, `nums[i]`.
  - The `if` statement is a crucial optimization. If we have already processed `nums[i-1]` as the first element, and `nums[i]` is the same, then any triplets we find starting with `nums[i]` will be duplicates of the ones we found starting with `nums[i-1]`. This check allows us to skip them entirely.

### Step 3: The Two-Pointer Setup

```python
left, right = i + 1, n - 1
while left < right:
    # ...
```

  - For each fixed `nums[i]`, we initialize a `left` pointer to the next element and a `right` pointer to the very last element.
  - The `while` loop will then scan the subarray between these two pointers.

### Step 4: The Core Two-Pointer Logic

```python
current_sum = nums[i] + nums[left] + nums[right]

if current_sum < 0:
    left += 1
elif current_sum > 0:
    right -= 1
else:
    # ... found a solution
```

  - We calculate the sum of the three numbers.
  - If the `sum < 0`, we need a larger sum, so we move the `left` pointer to the right.
  - If the `sum > 0`, we need a smaller sum, so we move the `right` pointer to the left.
  - If the `sum == 0`, we have found a valid triplet.

## Deep Dive: Handling Duplicates After Finding a Solution

This is the most detailed and crucial part of the algorithm, as requested.

```python
else:  # Found a triplet
    result.append([nums[i], nums[left], nums[right]])
    
    # Move pointers inward.
    left += 1
    
    # Skip any duplicates for the 'left' pointer.
    while left < right and nums[left] == nums[left - 1]:
        left += 1
```

  - **`result.append(...)`**: Once we find a valid triplet, we add it to our `result` list.
  - **`left += 1`**: After finding a triplet, we must move our pointers to continue searching for other, different triplets. We start by moving `left` forward.
  - **`while left < right and nums[left] == nums[left - 1]:`**: This is the key duplicate-skipping logic.
      - **Why is this needed?** Imagine the subarray is `[-2, -2, 0, 1, 3, 4, 4]` and our fixed `nums[i]` is `-2`. Our target is `2`. The pointers might find `left` at the second `-2` and `right` at the second `4`, giving `(-2) + 4 = 2`. The triplet is `[-2, -2, 4]`. If we just incremented `left` once, the pointers might then find the pair `(-2, 4)` again, leading to a duplicate result.
      - **How it works**: This `while` loop says, "After moving `left` one step, keep moving it forward as long as it's pointing to the same value as before." This effectively jumps the `left` pointer over all the duplicates of the number we just used in our solution.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [-1, 0, 1, 2, -1, -4]`.

1.  **Sort `nums`**: `[-4, -1, -1, 0, 1, 2]`
2.  **Initialize**: `result = []`

| `i`, `nums[i]` | `left`, `right` | `current_sum` (`nums[i]+nums[l]+nums[r]`) | `sum vs 0`? | Action | `result` state |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0, -4**| 1, 5 | `-4 + (-1) + 2 = -3` | `< 0` | `left++` -\> `left=2` | `[]` |
| | 2, 5 | `-4 + (-1) + 2 = -3` | `< 0` | `left++` -\> `left=3` | `[]` |
| | 3, 5 | `-4 + 0 + 2 = -2` | `< 0` | `left++` -\> `left=4` | `[]` |
| | 4, 5 | `-4 + 1 + 2 = -1` | `< 0` | `left++` -\> `left=5`. `left<right` is false. Loop ends. | `[]` |
| **1, -1**| 2, 5 | `-1 + (-1) + 2 = 0` | `== 0` | **Found `[-1,-1,2]`**. Append it. `left++` to 3. | `[[-1,-1,2]]` |
| | 3, 5 | `-1 + 0 + 2 = 1` | `> 0` | `right--` -\> `right=4` | `[[-1,-1,2]]` |
| | 3, 4 | `-1 + 0 + 1 = 0` | `== 0` | **Found `[-1,0,1]`**. Append it. `left++` to 4. | `[[-1,-1,2], [-1,0,1]]` |
| | 4, 4 | - | - | `left<right` is false. Loop ends. | `[[-1,-1,2], [-1,0,1]]` |
| **2, -1**| - | - | - | Skip `i` because `nums[2]==nums[1]` | `[[-1,-1,2], [-1,0,1]]` |
| **3, 0**| 4, 5 | `0 + 1 + 2 = 3` | `> 0` | `right--` -\> `right=4`. `left<right` is false. Loop ends.| `[[-1,-1,2], [-1,0,1]]` |

  - The main `for` loop finishes.
  - The function returns `[[-1,-1,2], [-1,0,1]]`.

## Performance Analysis

### Time Complexity: O(n²)

  - The initial sort takes `O(n log n)`.
  - The main `for` loop runs `n` times. Inside it, the `while` loop with the two pointers runs in `O(n)` time in the worst case.
  - The total complexity is `O(n log n + n²)`, which simplifies to `O(n²)`.

### Space Complexity: O(1) or O(n)

  - If we ignore the space required for the `result` list, the space complexity is constant (`O(1)`), as we only use a few pointers.
  - The space complexity of the sorting algorithm can vary from `O(log n)` to `O(n)` depending on the implementation.