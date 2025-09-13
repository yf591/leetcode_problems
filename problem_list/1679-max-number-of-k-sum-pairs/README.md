# 1679\. Max Number of K-Sum Pairs - Solution Explanation

## Problem Overview

You are given an array of integers `nums` and a target value `k`. The goal is to find the **maximum number of pairs** you can remove from the array where the two numbers in each pair sum up to `k`. Each number in the array can only be part of one pair.

**Examples:**

```python
Input: nums = [1,2,3,4], k = 5
Output: 2
Explanation:
1. Remove (1, 4). The array is now [2,3].
2. Remove (2, 3). The array is now [].
Total operations = 2.

Input: nums = [3,1,3,4,3], k = 6
Output: 1
Explanation:
1. Remove two of the 3s (3, 3). The array is now [1,4,3].
No other pairs sum to 6.
Total operations = 1.
```

## Key Insights

This is a classic variation of the "Two Sum" problem. For any number `num` we consider, we need to find its "partner" or **complement**, which would be `k - num`. The main challenge is handling duplicates efficiently and ensuring each number is used only once. There are two primary strategies for this.

1.  **The Counting Strategy (Hash Map)**: We can first count the frequency of every number in the array. This gives us an inventory. Then, for each number `num` in our inventory, we can check if its complement (`k - num`) is also available. This is very fast in terms of time complexity.

2.  **The Searching Strategy (Sorting & Two Pointers)**: We can sort the array. Then, we can use two pointers, one at the start (`left`) and one at the end (`right`), and move them inward. By comparing the sum of the numbers at the pointers to `k`, we can efficiently find pairs. This is very efficient in terms of memory.

## Solution Approach (Hash Map / Counter)

This solution is generally faster (`O(n)` time). It uses `collections.Counter` to build a frequency map of all the numbers, then iterates through this map to find and count valid pairs.

```python
import collections
from typing import List

class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        # Step 1: Create a frequency map (inventory) of all numbers.
        counts = collections.Counter(nums)
        operations = 0
        
        # We iterate through a copy of the keys because we will modify the counter.
        for num in list(counts.keys()):
            # If we've already used up this number, skip it.
            if counts[num] == 0:
                continue
                
            complement = k - num
            
            if num == complement:
                # Case 1: The number is its own complement (e.g., 3+3=6).
                # We can form count // 2 pairs.
                pairs = counts[num] // 2
                operations += pairs
                # "Use up" the numbers for this pair.
                counts[num] -= pairs * 2
            
            elif complement in counts and counts[complement] > 0:
                # Case 2: Find pairs of (num, complement).
                # The number of pairs is limited by whichever number is less frequent.
                pairs = min(counts[num], counts[complement])
                operations += pairs
                # "Use up" the numbers for these pairs to prevent re-counting.
                counts[num] -= pairs
                counts[complement] -= pairs
        
        return operations
```

### Detailed Code Analysis (Hash Map)

1.  **`counts = collections.Counter(nums)`**: This efficiently creates a hash map where keys are the numbers in `nums` and values are their frequencies. This is our inventory.
2.  **`for num in list(counts.keys())`**: We loop through each unique number we have. We use `list(...)` to create a static copy of the keys, which is important because we are modifying the `counts` dictionary inside the loop.
3.  **`if num == complement`**: This is the special case where a number is paired with itself. If we have `c` occurrences of this number, we can form `c // 2` pairs.
4.  **`elif complement in counts`**: This is the general case. We check if the partner number exists in our inventory. The number of pairs we can make is the `min()` of their respective counts.
5.  **`counts[num] -= pairs`**: This is a crucial step. After counting a set of pairs, we "remove" those numbers from our inventory by decrementing their counts. This prevents us from using the same number in another pair and also prevents us from double-counting (e.g., counting `(1, 4)` and then later counting `(4, 1)`).

-----

## Alternative Solution (Sorting & Two Pointers)

This solution is more space-efficient and also very elegant.

### How it Works

First, we sort the array. This allows us to use two pointers, one at the small end (`left`) and one at the large end (`right`), and move them inward.

  - If `nums[left] + nums[right]` is **equal to `k`**, we found a pair\! We count it and move both pointers inward.
  - If the sum is **less than `k`**, we need a larger sum. We can achieve this by moving the `left` pointer to the right to get a bigger number.
  - If the sum is **greater than `k`**, we need a smaller sum. We achieve this by moving the `right` pointer to the left to get a smaller number.

### The Code (Two Pointers)

```python
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        # Step 1: Sort the array.
        nums.sort()
        
        # Step 2: Initialize pointers and operation count.
        left, right = 0, len(nums) - 1
        operations = 0
        
        # Step 3: Move pointers inward until they cross.
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == k:
                # Found a pair!
                operations += 1
                left += 1
                right -= 1
            elif current_sum < k:
                # Sum is too small, need a larger number.
                left += 1
            else: # current_sum > k
                # Sum is too big, need a smaller number.
                right -= 1
                
        return operations
```

### Step-by-Step Execution Trace (Two Pointers)

Let's trace the algorithm for `nums = [1, 2, 3, 4]` and `k = 5`.

1.  **Sort**: `nums` is already `[1, 2, 3, 4]`.
2.  **Initialize**: `left = 0`, `right = 3`, `operations = 0`.

| `left` | `right` | `nums[left]` | `nums[right]`| `current_sum` | `sum vs k` | Action | `operations` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | 0 | 3 | 1 | 4 | - | - | - | 0 |
| **1** | 0 | 3 | 1 | 4 | `1+4 = 5` | `== k` | `left++`, `right--` | 1 |
| **2** | 1 | 2 | 2 | 3 | `2+3 = 5` | `== k` | `left++`, `right--` | 2 |
| **End** | 2 | 1 | - | - | - | `left < right` is False | Loop terminates. | 2 |

  - The loop ends. The function returns `operations`, which is **2**.

## Performance Analysis

| Approach | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **Hash Map** | `O(n)` | `O(n)` | Faster time, but uses more memory. |
| **Two Pointers** | `O(n log n)` | `O(1)` or `O(n)` | Slower due to sorting, but very space-efficient. |

## Key Learning Points

  - This problem showcases two of the most common patterns for "pair-finding" problems.
  - **Hash Map**: Best when you need the fastest possible time complexity and can afford the extra memory.
  - **Sorting & Two Pointers**: Best when memory is a concern or when the array is already sorted.
  - Understanding the time vs. space trade-offs between these two patterns is a crucial skill for interviews.