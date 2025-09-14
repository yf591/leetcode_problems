# 1004\. Max Consecutive Ones III - Solution Explanation

## Problem Overview

You are given a binary array `nums` (containing only 0s and 1s) and an integer `k`. The task is to find the length of the **longest contiguous subarray** that contains all 1s, with the ability to flip at most `k` zeros into ones.

**The Goal in Simple Terms:**
Find the longest possible "window" or slice of the array that is "valid." A window is considered valid if the number of zeros inside it is less than or equal to `k`.

**Examples:**

```python
Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation:
Consider the subarray [1,1,1,0,0,0]. It has three 0s, which is more than k=2, so it's not valid.
Consider the subarray [1,1,1,0,0,0,1,1,1,1]. This is too long.
The subarray [1,1,1,0,0,0,1,1,1,1,0] has two 0s we can flip. The longest sequence of 1s we can make is `[1,1,1,1,1,1]`, which has length 6.

Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
```

## Key Insights

### The Sliding Window Technique

A brute-force approach of checking every single possible subarray would be far too slow (`O(n²)`). The key to an efficient `O(n)` solution is the **sliding window** technique. This is slightly different from the fixed-size window in the "Max Average Subarray" problem; here, the window's size will grow and shrink.

The core idea is to maintain a "window" (a subarray defined by a `left` and `right` pointer) that is always "valid" or in the process of being made valid.

1.  **Expand**: We continuously expand our window by moving the `right` pointer to the right.
2.  **Maintain Validity**: As we expand, we keep track of how many zeros are in our current window.
3.  **Shrink when Invalid**: If the count of zeros ever exceeds `k`, our window is invalid. To fix it, we must shrink the window from the left by moving the `left` pointer to the right until the window becomes valid again.
4.  **Track Maximum**: After every expansion, we have a potentially new longest valid window. We keep track of the maximum length we've seen so far.

## Solution Approach

This solution implements the variable-size sliding window. It uses a `left` and `right` pointer to define the window and a `zero_count` variable to ensure the window's condition (`zero_count <= k`) is met.

```python
from typing import List

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        max_length = 0
        zero_count = 0
        
        # 'right' pointer expands the window by iterating through the array.
        for right in range(len(nums)):
            # If the new element entering the window is a zero, increment our count.
            if nums[right] == 0:
                zero_count += 1
            
            # If our window is invalid (too many zeros), we must shrink it.
            while zero_count > k:
                # If the element leaving the window from the left is a zero...
                if nums[left] == 0:
                    # ...decrement the zero count.
                    zero_count -= 1
                # Move the left pointer to the right to shrink the window.
                left += 1
            
            # After ensuring the window is valid, update the max_length.
            # The current valid window's length is (right - left + 1).
            max_length = max(max_length, right - left + 1)
            
        return max_length
```

## Detailed Code Analysis

### Step 1: Initialization

```python
left = 0
max_length = 0
zero_count = 0
```

  - `left`: This is the left pointer of our sliding window. It starts at the beginning of the array.
  - `max_length`: This variable will store the final answer. It keeps track of the largest valid window we've found so far.
  - `zero_count`: This is our state variable. It tracks how many zeros are currently inside the window defined by `left` and `right`.

### Step 2: The Expansion Loop

```python
for right in range(len(nums)):
```

  - This `for` loop drives the entire process. The `right` pointer continuously moves from the beginning to the end of the array, expanding the window one element at a time.

### Step 3: Updating State

```python
if nums[right] == 0:
    zero_count += 1
```

  - As a new element `nums[right]` enters the window, we update our state. If it's a zero, we increment `zero_count`.

### Step 4: The Shrinking Loop (Maintaining Validity)

```python
while zero_count > k:
    if nums[left] == 0:
        zero_count -= 1
    left += 1
```

  - This is the critical part that makes the window "slide."
  - The `while` loop runs only if our window is invalid (we have more zeros than allowed by `k`).
  - Inside the loop, we shrink the window from the left. We check if the element at the `left` pointer (`nums[left]`) is a zero. If it is, we decrement `zero_count` as it is now leaving the window.
  - We then increment `left`, effectively making our window smaller.
  - This loop continues until `zero_count` is no longer greater than `k`, at which point our window is valid again.

### Step 5: Calculating the Maximum Length

```python
max_length = max(max_length, right - left + 1)
```

  - This line executes after every single expansion of the `right` pointer.
  - Crucially, it happens *after* the shrinking `while` loop, so we are always calculating the length of a **valid** window.
  - `right - left + 1` is the standard formula for the size of an inclusive window.
  - We compare this current valid window's length with the `max_length` seen so far and keep the larger one.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [1,1,1,0,0,0,1,1,1,1,0]` and `k = 2` with extreme detail.

| `right` | `nums[right]` | `zero_count` (after `if`) | `while` loop runs? | `left` (after `while`)| Window `[left:right]` | `right-left+1` | `max_length` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start**| - | 0 | - | 0 | `[]` | 0 | **0** |
| **0** | 1 | 0 | No | 0 | `[1]` | 1 | **1** |
| **1** | 1 | 0 | No | 0 | `[1,1]` | 2 | **2** |
| **2** | 1 | 0 | No | 0 | `[1,1,1]` | 3 | **3** |
| **3** | 0 | 1 | No | 0 | `[1,1,1,0]` | 4 | **4** |
| **4** | 0 | 2 | No | 0 | `[1,1,1,0,0]` | 5 | **5** |
| **5** | 0 | 3 | `3 > 2` -\> **Yes** | `left`=1, `zero_count`=3 (unchanged)\<br\>`left`=2, `zero_count`=3 (unchanged)\<br\>`left`=3, `zero_count`=3 (unchanged)\<br\>`left`=4, `zero_count`=2 (`nums[3]` was 0) | `[0,0,1,1,1,1,0]`| `5-4+1=2` | 5 |
| **6** | 1 | 2 | No | 4 | `[0,0,1]` | `6-4+1=3` | 5 |
| **7** | 1 | 2 | No | 4 | `[0,0,1,1]` | `7-4+1=4` | 5 |
| **8** | 1 | 2 | No | 4 | `[0,0,1,1,1]` | `8-4+1=5` | 5 |
| **9** | 1 | 2 | No | 4 | `[0,0,1,1,1,1]` | `9-4+1=6` | **6** |
| **10**| 0 | 3 | `3 > 2` -\> **Yes** | `left`=5, `zero_count`=2 (`nums[4]` was 0) | `[0,1,1,1,1,0]` | `10-5+1=6` | 6 |

  - The main loop finishes.
  - The function returns the final `max_length`, which is **6**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the `nums` array. Although there is a nested `while` loop, this is an `O(n)` solution. This is because each pointer, `left` and `right`, only moves forward through the array. Each element is visited at most twice (once by `right` and once by `left`).

### Space Complexity: O(1)

  - We only use a few variables to store our state (`left`, `max_length`, `zero_count`). The space required is constant and does not grow with the size of the input.