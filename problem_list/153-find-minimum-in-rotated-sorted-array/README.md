# 153\. Find Minimum in Rotated Sorted Array - Solution Explanation

## Problem Overview

You are given an array of unique integers that was originally sorted in ascending order but has been **rotated** between 1 and `n` times.
Your task is to find the **minimum element** in this array.

**Constraint:** You must write an algorithm that runs in **O(log n)** time.

**What is a Rotation?**
Imagine a sorted array: `[0, 1, 2, 4, 5, 6, 7]`.
If we rotate it 4 times, the first 4 elements move to the back.
Result: `[4, 5, 6, 7, 0, 1, 2]`.

The minimum element is the point where the numbers suddenly drop (from `7` to `0`).

**Example:**

```python
Input: nums = [3, 4, 5, 1, 2]
Output: 1
Explanation: The original array was [1, 2, 3, 4, 5] rotated 3 times.
```

## Deep Dive: What is Binary Search? 🔍

**Binary Search** is an efficient algorithm for finding an item from a sorted list. Instead of checking every element one by one (Linear Search), it repeatedly divides the search interval in half.

**The Analogy (Number Guessing Game):**
I pick a number between 1 and 100. You guess.

1.  You guess **50** (the middle).
2.  I say "My number is **lower**."
3.  You immediately throw away numbers 51-100. You now search 1-49.
4.  You guess **25**.
5.  I say "My number is **higher**."
6.  You throw away 1-25. You search 26-49.

By cutting the possibilities in half every time, you find the answer very quickly.

[Image of binary search tree algorithm]

**Time Complexity:** **O(log n)**.
Even for 1,000,000 items, Binary Search only takes about 20 steps\!

## Key Insights for This Problem

### 1\. Visualizing the "Cliff"

A rotated sorted array isn't random. It consists of **two sorted sections**:

1.  **Left Section**: Values are large (e.g., `[4, 5, 6, 7]`).
2.  **Right Section**: Values are small (e.g., `[0, 1, 2]`).

[Image of rotated sorted array graph showing two slopes]

The minimum element is the **first element of the Right Section**. Our goal is to find the index where the graph "drops".

### 2\. Comparing `mid` vs. `right`

In a standard Binary Search, we compare `nums[mid]` to a `target`. Here, we don't know the target (the minimum value). Instead, we compare `nums[mid]` to `nums[right]` (the end of our current search range).

  * **If `nums[mid] > nums[right]`**:

      * This means `mid` is part of the **Left (High)** section.
      * The "cliff" (minimum) must be to the **right** of `mid`.
      * *Action*: Search the right half.

  * **If `nums[mid] <= nums[right]`**:

      * This means `mid` is part of the **Right (Low)** section (or the array isn't rotated).
      * The minimum is either at `mid` or to the **left** of it.
      * *Action*: Search the left half (keeping `mid` as a candidate).

## Solution Approach

We use a modified Binary Search. We maintain `left` and `right` pointers. We shrink the search space based on the comparison between the middle element and the rightmost element.

```python
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Step 1: Initialize pointers
        left = 0
        right = len(nums) - 1
        
        # Step 2: Binary Search Loop
        # We continue as long as left < right.
        # When left == right, we have found the minimum.
        while left < right:
            # Calculate middle index
            mid = (left + right) // 2
            
            # Step 3: The Decision Logic
            # Compare the middle element with the right boundary
            if nums[mid] > nums[right]:
                # Case A: Mid is in the left (larger) sorted portion.
                # The minimum MUST be to the right of mid.
                # Example: [4, 5, 6, 7, 0, 1, 2], mid=7, right=2
                left = mid + 1
            else:
                # Case B: Mid is in the right (smaller) sorted portion.
                # The minimum is either mid itself or to the left.
                # Example: [7, 0, 1, 2, 4, 5, 6], mid=2, right=6
                # We cannot discard mid, so we set right = mid.
                right = mid
                
        # Step 4: Return the result
        # When the loop ends, left == right, pointing to the minimum.
        return nums[left]
```

## Detailed Code Analysis

### Step 1: Initialization

```python
left = 0
right = len(nums) - 1
```

We set our search range to cover the entire array.

### Step 2: The Loop Condition

```python
while left < right:
```

**Why `<` instead of `<=`?**
In standard Binary Search, we use `<=` because we return immediately if we find the target. Here, we are narrowing down the search space until only **one element remains**. When `left == right`, that single element is our answer, so we stop.

### Step 3: The Logic `nums[mid] > nums[right]`

```python
if nums[mid] > nums[right]:
    left = mid + 1
```

If the middle element is larger than the rightmost element, the sequence is "broken" somewhere between `mid` and `right`. The `mid` element itself cannot be the minimum (because `nums[right]` is smaller than it). So, the minimum must be strictly to the right. We set `left = mid + 1`.

### Step 4: The Logic `else`

```python
else:
    right = mid
```

If `nums[mid] <= nums[right]`, the sequence from `mid` to `right` is sorted (increasing). This means `mid` is the smallest value in the `[mid ... right]` range. However, there could be an even smaller number to the *left* of `mid`.
Therefore, we discard everything to the right of `mid`, but we **keep `mid`** as a candidate. We set `right = mid`.

## Step-by-Step Execution Trace

Let's trace the algorithm with `nums = [3, 4, 5, 1, 2]`.

**Initial State:**
`left = 0`, `right = 4`

-----

### **Iteration 1**

1.  **Calculate Mid**:
    `mid = (0 + 4) // 2 = 2`.
    `nums[mid] = 5`.
2.  **Comparison**:
    Is `nums[mid] > nums[right]`? (`5 > 2`?)
    **YES**.
3.  **Logic**:
    Since 5 is huge and 2 is small, the "drop" must happen to the right of 5.
    `left = mid + 1` =\> `left = 3`.
    (`mid` 5 is discarded).

**New Range**: Indices `[3, 4]` corresponding to `[1, 2]`.

-----

### **Iteration 2**

1.  **Calculate Mid**:
    `mid = (3 + 4) // 2 = 3`.
    `nums[mid] = 1`.
2.  **Comparison**:
    Is `nums[mid] > nums[right]`? (`1 > 2`?)
    **NO**.
3.  **Logic**:
    Since `1 <= 2`, the sequence from `mid` to `right` is sorted. `1` is the smallest in this section. The true minimum is either `1` or to the left.
    `right = mid` =\> `right = 3`.
    (We keep `mid` 1).

**New Range**: Index `[3]` corresponding to `[1]`.

-----

### **Termination**

1.  The condition `left < right` (`3 < 3`) is now **False**.
2.  The loop breaks.
3.  Return `nums[left]`, which is `nums[3] = 1`.

**Correct Output: 1**

## Performance Analysis

### Time Complexity: O(log n)

We divide the search space (the array indices) in half during every iteration of the `while` loop. This is the definition of logarithmic time complexity.

### Space Complexity: O(1)

We only use three variables (`left`, `right`, `mid`) to store indices. We do not use any extra data structures that grow with the input size. The space used is constant.