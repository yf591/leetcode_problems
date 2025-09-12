# 334\. Increasing Triplet Subsequence - Solution Explanation

## Problem Overview

You are given an array of integers `nums`. The task is to determine if there exists a **triplet of indices `(i, j, k)`** such that `i < j < k` and the corresponding values are strictly increasing: `nums[i] < nums[j] < nums[k]`.

**Key Definitions:**

  - **Subsequence**: A sequence that can be derived from the array by deleting some or no elements without changing the order of the remaining elements. The elements do not have to be next to each other.
  - **Increasing Triplet**: Three numbers from the array, `a`, `b`, and `c`, such that `a < b < c`, and `a` appears before `b` in the array, and `b` appears before `c`.

**Examples:**

```python
Input: nums = [1,2,3,4,5]
Output: true
Explanation: Any triplet like (1, 2, 3) or (2, 4, 5) works.

Input: nums = [5,4,3,2,1]
Output: false
Explanation: The numbers are always decreasing, so no increasing triplet can be formed.

Input: nums = [2,1,5,0,4,6]
Output: true
Explanation: The triplet for indices (3, 4, 5) is valid because
nums[3] (0) < nums[4] (4) < nums[5] (6).
```

## Key Insights

### The Inefficient Brute-Force Approach

A naive solution would be to use three nested loops to check every possible combination of `(i, j, k)`. This would have a time complexity of `O(n³)`, which is far too slow for the given constraints.

### The Greedy `O(n)` Insight

The key to a fast solution is to realize that we can find the answer in a **single pass**. As we iterate through the array, we don't need to remember every number we've seen. We only need to maintain the best possible candidates for the first two numbers of our triplet.

We can keep track of just two numbers:

1.  **`first`**: The smallest number we have seen so far. This is the best possible candidate for the first number in an increasing triplet because a smaller first number makes it easier to find two larger numbers.
2.  **`second`**: The smallest number we have seen so far that is *greater than* `first`. This is the best possible candidate for the second number.

With these two variables, we can iterate through the array. For any new number we see, we just need to ask:

  - Is it smaller than `first`? (If so, it's an even better `first`).
  - Is it smaller than `second`? (If so, it's a better `second`).
  - Is it larger than both? (If so, we've found our triplet\!).

## Solution Approach

This solution implements the efficient greedy strategy. It iterates through the `nums` list once, maintaining two variables, `first` and `second`, to track the smallest and second-smallest numbers of a potential increasing subsequence.

```python
from typing import List

class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        # 'first' will hold the smallest number of a potential triplet.
        # 'second' will hold the second-smallest number.
        # We initialize them to a value guaranteed to be larger than any element.
        first = float('inf')
        second = float('inf')
        
        # Iterate through each number in the input array.
        for num in nums:
            # Case 1: The current number is the smallest we've seen so far.
            if num <= first:
                first = num
            # Case 2: The number is not the smallest, but it could be our second number.
            elif num <= second:
                second = num
            # Case 3: The number is greater than both 'first' and 'second'.
            else:
                # We have found a triplet: first < second < num
                return True
                
        # If we get through the entire loop, it means no such triplet was found.
        return False
```

## Detailed Code Analysis

### Step 1: Initialization

```python
first = float('inf')
second = float('inf')
```

  - We initialize our two tracking variables, `first` and `second`, to positive infinity.
  - This is a common trick that ensures that the very first number in the `nums` array will be smaller than `first`, and the next distinct number will be smaller than `second`, correctly setting up our initial candidates.

### Step 2: The Loop and the `if/elif/else` Logic

```python
for num in nums:
    if num <= first:
        first = num
    elif num <= second:
        second = num
    else:
        return True
```

  - This is the core of the algorithm, which runs for every `num` in the input list.

  - **`if num <= first:`**

      - This checks if the current `num` is a new, even better candidate for the *first* element of our triplet. A smaller `first` value increases the chances of finding two subsequent numbers that are larger.

  - **`elif num <= second:`**

      - This branch only runs if `num > first`. It checks if `num` can serve as a better *second* element for our triplet. For example, if we have `first = 1` and `second = 5`, and we encounter `num = 3`, we update `second` to `3`. The potential triplet is now `1 < 3 < ?`, which is easier to complete than `1 < 5 < ?`.

  - **`else:`**

      - This branch is our success condition. It only runs if `num > first` and `num > second`.
      - At this point, we have found a number `num` that is strictly greater than `second`. We already know that `second` is strictly greater than `first`. Therefore, we have found a valid triplet `first < second < num` and can immediately return `True`.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [2, 1, 5, 0, 4, 6]` with extreme detail.

1.  **Initialization**: `first = float('inf')`, `second = float('inf')`.

| `num` from `nums` | `first` (at start of loop) | `second` (at start of loop) | Condition Met | Action | `first` (at end of loop) | `second` (at end of loop) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2** | `inf` | `inf` | `if num <= first` (2 \<= inf) | `first = 2` | 2 | `inf` |
| **1** | 2 | `inf` | `if num <= first` (1 \<= 2) | `first = 1` | 1 | `inf` |
| **5** | 1 | `inf` | `elif num <= second` (5 \<= inf) | `second = 5` | 1 | 5 |
| **0** | 1 | 5 | `if num <= first` (0 \<= 1) | `first = 0` | 0 | 5 |
| **4** | 0 | 5 | `elif num <= second` (4 \<= 5) | `second = 4` | 0 | 4 |
| **6** | 0 | 4 | `else` (6 \> 4) | **Return `True`** | - | - |

  - When the loop processes the number `6`, it's not smaller than `first` (0) and not smaller than `second` (4). It falls into the `else` block, which means a triplet has been found. The function immediately returns `True`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. The algorithm iterates through the list exactly once.

### Space Complexity: O(1)

  - We only use two variables (`first` and `second`) to store our state. The space required is constant and does not grow with the size of the input.

## Key Learning Points

  - **Greedy Approach**: This problem demonstrates how a greedy approach can be incredibly effective. By always keeping track of the best possible `first` and `second` candidates, we can efficiently find a solution in a single pass.
  - **State Management**: The solution's elegance comes from realizing that you only need to maintain a very small amount of state (just two numbers) to solve the problem, rather than storing complex subsequence information.
  - This pattern is useful for many subsequence problems where you only need to prove the *existence* of a pattern, not find all occurrences.