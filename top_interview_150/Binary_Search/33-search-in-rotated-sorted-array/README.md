# 33\. Search in Rotated Sorted Array - Solution Explanation

## Problem Overview

You are given an integer array `nums` that was originally sorted in ascending order but has been **rotated** at an unknown pivot index. You are also given an integer `target`. Your task is to find the index of `target` in `nums`. If it doesn't exist, return `-1`.

**Constraint:** You must write an algorithm with **$O(\log n)$** runtime complexity.

**What is a Rotated Array?**
Imagine a sorted array `[0, 1, 2, 4, 5, 6, 7]`.
If we rotate it at index 3 (the value `4`), the part `[4, 5, 6, 7]` moves to the front.
The array becomes: `[4, 5, 6, 7, 0, 1, 2]`.

**Example:**

```python
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

## Deep Dive: What is Binary Search? 

**Binary Search** is an efficient algorithm for finding an item from a **sorted** list. It works by repeatedly dividing the search interval in half.

**The Analogy:**
Imagine a guessing game where you have to guess a number between 1 and 100.

1.  You guess **50** (the middle).
2.  The host says "Too high".
3.  You immediately know the answer is between 1 and 49. You just discarded half the possibilities\!
4.  You guess **25** (the middle of the remaining range).
5.  And so on...

**Why is it fast?**
Because we discard half the possibilities in every step, the time complexity is **$O(\log n)$** (logarithmic time). Even for 1,000,000 elements, it takes only about 20 steps.

## Key Insights for Rotated Arrays

### 1\. The "One Half is Sorted" Rule

Standard Binary Search requires the *entire* array to be sorted. Our array is not. However, it has a special property: **If you cut a rotated sorted array at any point, at least one half will always be sorted.**

Let's look at `[4, 5, 6, 7, 0, 1, 2]`. Midpoint is `7`.

  - **Left side**: `[4, 5, 6]` (Sorted\!)
  - **Right side**: `[0, 1, 2]` (Sorted\!)

Let's look at `[6, 7, 0, 1, 2, 4, 5]`. Midpoint is `1`.

  - **Left side**: `[6, 7, 0]` (Not sorted - this contains the rotation pivot)
  - **Right side**: `[2, 4, 5]` (Sorted\!)

### 2\. The Decision Logic

We can modify Binary Search to leverage this rule:

1.  Find the `mid`.
2.  **Check Left**: Is the left side sorted? (`nums[left] <= nums[mid]`)
      - **Yes**: Is the target inside this sorted range? (`nums[left] <= target < nums[mid]`)
          - If yes, go Left.
          - If no, go Right.
      - **No**: (This implies the Right side *must* be sorted).
          - Is the target inside the sorted right range? (`nums[mid] < target <= nums[right]`)
              - If yes, go Right.
              - If no, go Left.

## Solution Approach

We implement a modified Binary Search that first identifies which half of the array is sorted, and then uses that information to decide whether to search the left or right half.

```python
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            # Case 1: We found the target immediately
            if nums[mid] == target:
                return mid
            
            # Check if the LEFT half is sorted
            if nums[left] <= nums[mid]:
                # We are in the left sorted portion.
                # Check if the target falls within this range.
                if nums[left] <= target < nums[mid]:
                    right = mid - 1  # Target is in the left half
                else:
                    left = mid + 1   # Target must be in the right half
            
            # If the left half isn't sorted, the RIGHT half must be sorted
            else:
                # We are in the right sorted portion.
                # Check if the target falls within this range.
                if nums[mid] < target <= nums[right]:
                    left = mid + 1   # Target is in the right half
                else:
                    right = mid - 1  # Target must be in the left half
                    
        return -1
```

## Detailed Code Analysis

### Step 1: Initialization

```python
left, right = 0, len(nums) - 1
```

  - We set our pointers to the start and end of the array, defining our initial search space.

### Step 2: The Binary Search Loop

```python
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
        return mid
```

  - Standard Binary Search setup. We calculate the middle index. If we are lucky and land directly on the target, we return the index immediately.

### Step 3: Identify the Sorted Half

```python
if nums[left] <= nums[mid]:
```

  - This check determines the "shape" of our current range.
  - If the value at `left` is less than or equal to the value at `mid`, we know the subarray from `left` to `mid` is **contiguous and sorted**. There is no rotation pivot in this section.

### Step 4: Handling a Sorted Left Half

```python
if nums[left] <= target < nums[mid]:
    right = mid - 1
else:
    left = mid + 1
```

  - Since we know the left side is sorted, it's easy to check if `target` belongs there.
  - We simply check if `target` is between `nums[left]` and `nums[mid]`.
  - If it is, we eliminate the right half (`right = mid - 1`).
  - If it isn't, we know the target must be in the right half (either it's larger than `nums[mid]` or smaller than `nums[left]`), so we eliminate the left half (`left = mid + 1`).

### Step 5: Handling a Sorted Right Half

```python
else: # Right side is sorted
    if nums[mid] < target <= nums[right]:
        left = mid + 1
    else:
        right = mid - 1
```

  - If the left side wasn't sorted, the right side (`mid` to `right`) **must** be sorted.
  - We perform the same logic: Check if `target` is within the sorted bounds `(nums[mid], nums[right]]`.
  - If it is, we search there (`left = mid + 1`).
  - If not, we search the other side (`right = mid - 1`).

## Step-by-Step Execution Trace

Let's trace `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`.

### **Iteration 1**

  - `left = 0`, `right = 6`
  - `mid = 3`. `nums[mid] = 7`.
  - **Identify Sorted Side**: `nums[left] (4) <= nums[mid] (7)`? **Yes**. Left side is sorted.
  - **Check Range**: Is `0` in `[4, 7)`? `4 <= 0 < 7`? **No**.
  - **Action**: Go Right. `left = mid + 1 = 4`.

### **Iteration 2**

  - `left = 4`, `right = 6`. (`nums` subset effectively `[0, 1, 2]`)
  - `mid = 5`. `nums[mid] = 1`.
  - **Identify Sorted Side**: `nums[left] (0) <= nums[mid] (1)`? **Yes**. Left side is sorted.
  - **Check Range**: Is `0` in `[0, 1)`? `0 <= 0 < 1`? **Yes**.
  - **Action**: Go Left. `right = mid - 1 = 4`.

### **Iteration 3**

  - `left = 4`, `right = 4`.
  - `mid = 4`. `nums[mid] = 0`.
  - **Found Match**: `nums[mid] == target`.
  - **Return 4**.

## Performance Analysis

### Time Complexity: O(log n)

  - In every iteration of the `while` loop, we cut the search space (`right - left`) in half, regardless of where the rotation pivot is.
  - This satisfies the problem constraint.

### Space Complexity: O(1)

  - We only use a few variables (`left`, `right`, `mid`) to track indices. We do not use recursion or extra data structures. The memory usage is constant.