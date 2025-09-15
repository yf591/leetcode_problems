# 1493\. Longest Subarray of 1's After Deleting One Element - Solution Explanation

## Problem Overview

You are given a binary array `nums` (containing only 0s and 1s). The task is to delete **exactly one element** from it to produce the longest possible contiguous subarray containing only `1`'s. You must return the length of this longest subarray.

**Key Definitions:**

  - You **must** delete one element.
  - The final result is the length of a subarray containing only `1`'s.

**Examples:**

```python
Input: nums = [1,1,0,1]
Output: 3
Explanation: By deleting the 0 at index 2, the array becomes [1,1,1]. The longest subarray of 1's has length 3.

Input: nums = [0,1,1,1,0,1,1,0,1]
Output: 5
Explanation: By deleting the 0 at index 4, the two groups of 1's [1,1,1] and [1,1] merge to form [1,1,1,1,1], which has length 5.

Input: nums = [1,1,1]
Output: 2
Explanation: Since you must delete one element, the best you can do is delete one of the 1's, resulting in a subarray of length 2.
```

## Key Insights

### Rephrasing the Problem

This is the most critical insight. The problem "find the longest subarray of 1's after deleting one element" is a clever disguise for a simpler problem:

**"Find the longest contiguous subarray that contains at most one zero."**

Why are they the same?

  - If you find a window like `[1, 1, 0, 1, 1, 1]`, its length is 6. It contains one zero. If you delete that zero, you get a subarray of 1's with length `6 - 1 = 5`.
  - If you find a window with no zeros, like `[1, 1, 1]`, its length is 3. The problem states you *must* delete one element, so you would delete one of the 1s, resulting in a subarray of length `3 - 1 = 2`.

This rephrasing allows us to use the **variable-size sliding window** technique, which is perfect for finding the longest subarray that satisfies a certain condition.

## Solution Approach

This solution implements the variable-size sliding window. We expand a window from the right and shrink it from the left whenever it becomes "invalid" (contains more than one zero). We keep track of the largest valid window found.

```python
from typing import List

class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        left = 0
        zero_count = 0
        max_window_len = 0
        
        # 'right' pointer expands the window by iterating through the array.
        for right in range(len(nums)):
            # If the new element entering the window is a zero, increment our count.
            if nums[right] == 0:
                zero_count += 1
            
            # If our window is invalid (it has more than one zero)...
            while zero_count > 1:
                # ...we must shrink it from the left.
                # If the element leaving the window is a zero...
                if nums[left] == 0:
                    # ...decrement the zero count.
                    zero_count -= 1
                # Move the left pointer to the right to shrink the window.
                left += 1
            
            # Update the max_window_len with the size of the current valid window.
            max_window_len = max(max_window_len, right - left + 1)
            
        # The result is the longest window with at most one zero, minus the one
        # element that needs to be deleted.
        return max_window_len - 1
```

## Detailed Code Analysis

### Step 1: Initialization

```python
left = 0
zero_count = 0
max_window_len = 0
```

  - `left`: This is the left pointer of our sliding window, starting at the beginning.
  - `zero_count`: This is our crucial state variable. It tracks how many zeros are currently inside the window defined by `left` and `right`.
  - `max_window_len`: This variable will store the length of the largest valid window (with at most one zero) we find.

### Step 2: The Expansion Loop

```python
for right in range(len(nums)):
```

  - This `for` loop drives the process. The `right` pointer continuously moves from `0` to the end of the array, expanding our window by one element in each iteration.

### Step 3: Updating State

```python
if nums[right] == 0:
    zero_count += 1
```

  - As the new element `nums[right]` enters the window, we check if it's a zero. If it is, we increment our `zero_count`.

### Step 4: The Shrinking Loop (Maintaining a Valid Window)

```python
while zero_count > 1:
    if nums[left] == 0:
        zero_count -= 1
    left += 1
```

  - This is the core of the variable-size window logic.
  - The `while` loop runs only if our window is **invalid** (i.e., it contains more than one zero).
  - Inside the loop, we shrink the window from the left. We check if the element leaving the window (`nums[left]`) is a zero. If so, we decrement `zero_count`.
  - We then increment `left`, effectively making the window one element smaller. This loop continues until `zero_count` is back down to 1, making our window valid again.

### Step 5: Calculating the Maximum Length

```python
max_window_len = max(max_window_len, right - left + 1)
```

  - This line executes at the end of every `for` loop iteration.
  - Crucially, it runs *after* the shrinking `while` loop, so the window `[left...right]` is **guaranteed to be valid** (containing at most one zero) when this line is executed.
  - `right - left + 1` is the current valid window's length. We compare it with our recorded `max_window_len` and keep the larger one.

### Step 6: The Final Return

```python
return max_window_len - 1
```

  - After the `for` loop finishes, `max_window_len` holds the length of the longest subarray with at most one zero.
  - The problem requires us to delete one element, so the final length of the subarray of pure 1's is `max_window_len - 1`. This correctly handles both cases: if the window contained one zero, we delete it; if it contained all ones, we must delete one of the ones.

## Step-by-Step Execution Trace

### Example: `nums = [0, 1, 1, 1, 0, 1, 1, 0, 1]`

| `right` | `nums[right]` | `zero_count` (after `if`) | `while` loop runs? (`zero_count`\>1)| `left` (after `while`)| Window's length (`right-left+1`)| `max_window_len` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start**| - | 0 | - | 0 | 0 | **0** |
| **0** | 0 | 1 | No | 0 | `0-0+1=1` | **1** |
| **1** | 1 | 1 | No | 0 | `1-0+1=2` | **2** |
| **2** | 1 | 1 | No | 0 | `2-0+1=3` | **3** |
| **3** | 1 | 1 | No | 0 | `3-0+1=4` | **4** |
| **4** | 0 | 2 | Yes | `left`=1, `zero_count`=1 | `4-1+1=4` | 4 |
| **5** | 1 | 1 | No | 1 | `5-1+1=5` | **5** |
| **6** | 1 | 1 | No | 1 | `6-1+1=6` | **6** |
| **7** | 0 | 2 | Yes | `left` moves from 1 to 5, `zero_count` becomes 1 | `7-5+1=3` | 6 |
| **8** | 1 | 1 | No | 5 | `8-5+1=4` | 6 |

  - The main loop finishes.
  - The final `max_window_len` is **6**.
  - The function returns `max_window_len - 1` -\> `6 - 1` = **5**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of `nums`. Although there is a nested `while` loop, each pointer (`left` and `right`) only moves forward through the array. Each element is visited at most twice, resulting in a linear time complexity.

### Space Complexity: O(1)

  - We only use a few variables to store our state (`left`, `zero_count`, `max_window_len`). The space required is constant.