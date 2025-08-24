# 55\. Jump Game - Solution Explanation

## Problem Overview

You are given an array of non-negative integers `nums`, where you start at the first index (`index 0`). Each number `nums[i]` represents the maximum number of steps you can jump forward from that position. The goal is to determine if you can reach the very last index of the array.

**Examples:**

```python
Input: nums = [2,3,1,1,4]
Output: true
Explanation: You can jump 1 step from index 0 to 1, then 3 steps from index 1 to the last index.

Input: nums = [3,2,1,0,4]
Output: false
Explanation: From index 0, you can get to 1, 2, or 3. From any of those, you will eventually land on index 3. At index 3, the jump length is 0, making it impossible to move forward and reach the end.
```

## Key Insights

### The Greedy Approach: Maximum Reach

A common mistake is to think you need to decide *which* jump to take at each step (e.g., "Should I jump 1 step or 2 steps from `nums[0]=2`?"). This can lead to complex solutions like backtracking or dynamic programming.

The key insight for a simpler, more efficient solution is to adopt a **greedy** mindset. Instead of worrying about the path, we only need to care about one thing at each position: **"What is the farthest index I can possibly reach from anywhere I've been so far?"**

We can solve this in a single pass. We'll maintain a variable, `max_reach`, that tracks this farthest reachable index. As we iterate through the array, we update this `max_reach`. If at any point our current position is beyond what we could have possibly reached, we know the journey is impossible.

## Solution Approach

This solution iterates through the array once, keeping a single variable `max_reach` to track the furthest index that is reachable.

```python
from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        # 'max_reach' will store the furthest index we can get to.
        max_reach = 0
        n = len(nums)
        
        # We iterate through the array with index 'i'.
        for i, jump_length in enumerate(nums):
            # If the current index 'i' is greater than the furthest we can reach,
            # it means we are stuck and can never get to this point.
            if i > max_reach:
                return False
            
            # Update our maximum reach by considering the jump from the current index.
            # The new reach is the maximum of what we could already reach,
            # and the furthest we can get from our current spot (i + jump_length).
            max_reach = max(max_reach, i + jump_length)
            
            # An optimization: if we can already reach or pass the last index,
            # we know the answer is true and can stop early.
            if max_reach >= n - 1:
                return True
        
        # This line is technically only reachable if the input has one element,
        # but it's good practice. If the loop completes, the end was reachable.
        return True
```

**Strategy:**

1.  **Initialize `max_reach`**: Start with `max_reach = 0`.
2.  **Iterate and Check**: Loop through the array with index `i`. In each step, first check if the current position `i` is reachable (i.e., `i <= max_reach`). If not, return `False`.
3.  **Update Reach**: If the current position is reachable, update `max_reach` to be the maximum of its current value and the furthest jump possible from this new position (`i + nums[i]`).
4.  **Check for Goal**: If `max_reach` ever becomes greater than or equal to the last index (`n-1`), we know we can make it, so we can return `True` early.

## Detailed Code Analysis

### Step 1: Initialization

```python
max_reach = 0
n = len(nums)
```

  - `max_reach` is initialized to 0. Before we look at `nums[0]`, the furthest we can "reach" is the starting line itself.
  - `n` stores the length for easy access.

### Step 2: The Core Loop and Reachability Check

```python
for i, jump_length in enumerate(nums):
    if i > max_reach:
        return False
```

  - This is the most critical check. Before we do anything at index `i`, we must ensure we could have actually gotten here. If our current index `i` is beyond the `max_reach` calculated from all *previous* positions, it's an unreachable island, and the game is lost.

### Step 3: Updating the Maximum Reach

```python
max_reach = max(max_reach, i + jump_length)
```

  - This is the greedy part. We don't care about the path; we only care about potential. We update our `max_reach` to be the best it can be, considering the jump from our current location `i`.

### Step 4: Early Exit Optimization

```python
if max_reach >= n - 1:
    return True
```

  - As soon as our `max_reach` covers the last index, we don't need to check any further. We've proven that the end is reachable.

## Step-by-Step Execution Trace

### Example 1 (Success): `nums = [2, 3, 1, 1, 4]` (`n=5`, `goal_index=4`)

| `i` | `jump_length` | `i > max_reach`? | `max_reach` (before update) | `i + jump_length` | `max_reach` (after update) | `max_reach >= 4`? |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | **2** | `0 > 0` -\> False | 0 | `0 + 2 = 2` | `max(0, 2) = 2` | False |
| **1** | **3** | `1 > 2` -\> False | 2 | `1 + 3 = 4` | `max(2, 4) = 4` | **True** -\> Return `True` |

  - The loop stops at `i=1` because `max_reach` becomes 4, which is equal to the last index.

### Example 2 (Failure): `nums = [3, 2, 1, 0, 4]` (`n=5`, `goal_index=4`)

| `i` | `jump_length` | `i > max_reach`? | `max_reach` (before update) | `i + jump_length` | `max_reach` (after update) | `max_reach >= 4`? |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | **3** | `0 > 0` -\> False | 0 | `0 + 3 = 3` | `max(0, 3) = 3` | False |
| **1** | **2** | `1 > 3` -\> False | 3 | `1 + 2 = 3` | `max(3, 3) = 3` | False |
| **2** | **1** | `2 > 3` -\> False | 3 | `2 + 1 = 3` | `max(3, 3) = 3` | False |
| **3** | **0** | `3 > 3` -\> False | 3 | `3 + 0 = 3` | `max(3, 3) = 3` | False |
| **4** | **4** | `4 > 3` -\> **True** | 3 | - | - | **Return `False`** |

  - The loop stops at `i=4` because the current index is beyond the `max_reach` of 3.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We iterate through the list exactly once.

### Space Complexity: O(1)

  - We only use a few variables (`max_reach`, `n`, `i`, `jump_length`). The space required is constant and does not grow with the size of the input list.

## Key Learning Points

  - Recognizing when a problem can be solved with a greedy approach by focusing on the "best move so far" rather than all possible paths.
  - The "maximum reach" pattern is a powerful technique for solving many array traversal and jump-related problems.
  - An early exit condition (like checking if the goal is already reached) can be a simple but effective optimization.