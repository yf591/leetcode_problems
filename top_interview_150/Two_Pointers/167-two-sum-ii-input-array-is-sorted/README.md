# 167\. Two Sum II - Input Array Is Sorted - Solution Explanation

## Problem Overview

You are given a **1-indexed** array of integers `numbers` that is already **sorted** in non-decreasing order. The task is to find two numbers in this array that add up to a specific `target` number.

**Key Rules & Constraints:**

  - The input array is **sorted**. This is a major hint.
  - The output must be a list of the two **1-indexed** positions (e.g., `[index1, index2]`).
  - There is guaranteed to be **exactly one solution**.
  - You must solve it using **constant extra space**, meaning you cannot create new data structures like hash maps whose size depends on the input.

**Example:**

```python
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation:
- The number at index 1 is 2. (Note: 1-indexed)
- The number at index 2 is 7.
- 2 + 7 = 9.
- We return the 1-indexed positions: [1, 2].
```

## Key Insights

### Why a Hash Map Won't Work

For the original "Two Sum" problem (with an unsorted array), a hash map is the best solution. However, this problem adds a crucial constraint: **you must use only constant extra space**. A hash map would require `O(n)` space to store the numbers, which violates this rule.

### The Power of a Sorted Array

The most important piece of information is that the array is **sorted**. This allows us to be much smarter about how we search for the pair. We don't have to check every possible combination.

The key insight is to use a **two-pointer technique**.

1.  Start with one pointer (`left`) at the smallest element (the beginning of the array) and another pointer (`right`) at the largest element (the end of the array).
2.  Calculate the sum of the two numbers these pointers are pointing to.
3.  Based on this sum, you can make an intelligent decision:
      - If the sum is **too small**, you need a larger sum. Since the array is sorted, the only way to get a larger number is to move the `left` pointer to the right.
      - If the sum is **too big**, you need a smaller sum. The only way to get a smaller number is to move the `right` pointer to the left.
4.  By repeatedly moving the pointers inward, you are guaranteed to find the one and only solution in a single pass.

## Solution Approach

This solution is a direct implementation of the two-pointer strategy. It efficiently hones in on the solution by shrinking the search space from both ends of the sorted array.

```python
from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        # 1. Initialize pointers at the start and end of the array.
        left, right = 0, len(numbers) - 1

        # 2. Loop until the pointers meet or cross.
        while left < right:
            # 3. Calculate the sum of the values at the two pointers.
            current_sum = numbers[left] + numbers[right]

            # 4. Compare the sum to the target and make a decision.
            if current_sum == target:
                # Found the solution! Return the 1-indexed positions.
                return [left + 1, right + 1]
            elif current_sum < target:
                # The sum is too small, so we need a larger number.
                # Move the left pointer one step to the right.
                left += 1
            else:  # current_sum > target
                # The sum is too big, so we need a smaller number.
                # Move the right pointer one step to the left.
                right -= 1
```

## Detailed Code Analysis

### Step 1: Pointer Initialization

```python
left, right = 0, len(numbers) - 1
```

  - We create two pointers. `left` starts at index `0` (the smallest element). `right` starts at the last index of the array (the largest element). This establishes our initial search window, which covers the entire array.

### Step 2: The Loop Condition

```python
while left < right:
```

  - This loop will continue as long as our pointers have not crossed. `left < right` ensures we are always looking at a valid pair of two distinct elements. The moment they meet or cross, the loop terminates. (Since the problem guarantees a solution, we will always find it before this happens).

### Step 3: The Sum and Comparison

```python
current_sum = numbers[left] + numbers[right]

if current_sum == target:
    # ...
elif current_sum < target:
    # ...
else:
    # ...
```

  - This is the core of the algorithm.
  - **`if current_sum == target:`**: If we find the exact sum, we have won. We return `[left + 1, right + 1]`. We add `1` to each index because the problem asks for **1-indexed** results, while Python arrays are **0-indexed**.
  - **`elif current_sum < target:`**: If our sum is too small, we need to increase it. Since the array is sorted, the only way to guarantee a potentially larger sum is to move the `left` pointer to the right (`left += 1`), as `numbers[left + 1]` will be greater than or equal to `numbers[left]`.
  - **`else:`**: If our sum is too large, we need to decrease it. The only way to guarantee a potentially smaller sum is to move the `right` pointer to the left (`right -= 1`), as `numbers[right - 1]` will be less than or equal to `numbers[right]`.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `numbers = [2, 7, 11, 15]` and `target = 9` with extreme detail.

1.  **Initialization**: `left = 0`, `right = 3`.

| Iteration | `left` | `right` | `numbers[left]` | `numbers[right]` | `current_sum` | `sum vs. target` (`9`) | Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | 0 | 3 | 2 | 15 | - | - | - |
| **1** | 0 | 3 | 2 | 15 | `2 + 15 = 17` | `17 > 9` (Too large) | `right -= 1`. `right` becomes 2. |
| **2** | 0 | 2 | 2 | 11 | `2 + 11 = 13` | `13 > 9` (Too large) | `right -= 1`. `right` becomes 1. |
| **3** | 0 | 1 | 2 | 7 | `2 + 7 = 9` | `9 == 9` (Match\!) | **Return `[left+1, right+1]`** |

  - The function returns **`[1, 2]`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `numbers`. In the worst-case scenario, the `left` and `right` pointers will each traverse the entire array once, meeting in the middle. The total number of steps is proportional to `n`.

### Space Complexity: O(1)

  - The solution uses only a few variables to store the pointers and the sum. The amount of extra memory used is constant and does not grow with the size of the input array. This perfectly satisfies the problem's constraint.

## Key Learning Points

  - **Two-Pointer Technique**: This is a fundamental and powerful pattern for solving problems on **sorted arrays**.
  - **Problem Constraints are Hints**: The combination of a "sorted array" and "O(1) space" is a massive clue to use the two-pointer approach instead of a hash map.
  - **Shrinking the Search Space**: The logic of moving pointers inward is a form of "divide and conquer" where you intelligently eliminate parts of the array where the solution cannot possibly be.