# 162\. Find Peak Element - Solution Explanation

## Problem Overview

You are given a 0-indexed array of integers `nums`. The goal is to find and return the index of any **"peak element"**.

**Peak Element Definition:**
A peak element is an element that is **strictly greater than its immediate neighbors**.

**Key Rules & Constraints:**

  - The array can contain multiple peaks. Returning the index of *any* of them is a valid solution.
  - **`O(log n)` Time:** You *must* write an algorithm that runs in logarithmic time. This is the most important constraint and a massive hint.
  - **Imaginary Boundaries:** You must imagine that `nums[-1]` and `nums[n]` (the elements just outside the array) are both **-∞** (negative infinity). This is a crucial rule that guarantees a peak always exists. For example, in `[1, 2, 3]`, the `3` is a peak because it's greater than `2` (its left neighbor) and greater than `-∞` (its imaginary right neighbor).

**Examples:**

```python
Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak (3 > 2 and 3 > 1). Its index is 2.

Input: nums = [1,2,1,3,5,6,4]
Output: 5  # or 1
Explanation: 6 is a peak at index 5. 2 is also a peak at index 1. Both are valid answers.
```

## Deep Dive: What is Binary Search? 🧠

**Binary Search** is an extremely fast search algorithm. Its time complexity is `O(log n)`, which is exactly what the problem demands.

**Classic Use (The Dictionary Analogy):**
Normally, you use Binary Search on a **sorted array** to find a specific value. Think of looking for a word ("kangaroo") in a 1000-page dictionary:

1.  You don't start at page 1. You open to the middle (page 500).
2.  You see the words start with 'M'. You know 'K' comes *before* 'M'.
3.  You have just **eliminated half the book** (pages 500-1000) in one step.
4.  You repeat the process on the first half (pages 1-499), opening to its middle (page 250), and so on.

By repeatedly halving the search space, you find the word in a tiny number of steps, much faster than reading every page.

**Adapting Binary Search (For This Problem):**
This problem is different. The array is **not sorted**, and we are **not looking for a specific value**.
So, how can we use binary search?

We can use binary search on any search space that has a specific "property" that allows us to discard half of it. In our case, the "property" is the **slope** of the array. The `O(log n)` constraint is telling us to find a way to discard half of the array at every step.

## Key Insights for This Problem

### 1\. The `O(log n)` Constraint is Everything

This tells us we *must* use a Binary Search approach. Our task is to figure out the logic *inside* the binary search.

### 2\. The "-∞" Boundaries Guarantee a Peak

The fact that `nums[-1] = -∞` and `nums[n] = -∞` is the key. Imagine the array as a mountain range.

  - You start at `-∞` (sea level).
  - The first number, `nums[0]`, is guaranteed to be higher than `-∞`. So, the path is *going up* at the start.
  - The last number, `nums[n-1]`, is guaranteed to be higher than `nums[n]` (`-∞`). So, the path is *going down* at the end.
  - Since you start by going up and end by going down, you **must** have crossed at least one peak somewhere in the middle.

### 3\. The "Slope" Logic

Our binary search will work by checking the "slope" at the middle element.
Let's pick an element at `mid`. We only need to compare it to **one** neighbor to make our decision. Let's use `mid + 1`.

  - **Case 1: `nums[mid] < nums[mid + 1]`**

      - This means we are on an **"uphill" slope** (e.g., `...4, 5...`).
      - We know a peak *must* exist to our right. Why? Because we are currently going up, but we know the very end of the array is `-∞` (down). To go from an upward slope back down to `-∞`, we *must* cross a peak.
      - Therefore, we can safely **discard the entire left half**, including `mid`. Our new search space is `[mid + 1, ... right]`.

  - **Case 2: `nums[mid] > nums[mid + 1]`**

      - This means we are on a **"downhill" slope** (e.g., `...5, 4...`).
      - We know a peak *must* exist to our left (or `mid` itself could be the peak). Why? Because we know the very beginning of the array is `-∞` (down). To go from `-∞` up to `nums[mid]` (which is higher than its right neighbor), we *must* have crossed a peak.
      - Therefore, we can safely **discard the entire right half**. Our new search space is `[left, ... mid]`.

This logic guarantees that at every step, we discard the half of the array that is *not* guaranteed to hold a peak, while keeping the half that *is*.

## Solution Approach

This solution implements the efficient Binary Search described above. It uses two pointers, `left` and `right`, to define the search space. It repeatedly checks the element at `mid` and its right neighbor `mid + 1` to decide which half of the search space to discard.

```python
from typing import List

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        
        # Initialize the search space boundaries.
        left = 0
        # The right boundary is the last valid index.
        right = len(nums) - 1
        
        # We loop as long as the search space has more than one element.
        # The loop will terminate when left == right.
        while left < right:
            # Calculate the middle index.
            # Using integer division // is standard.
            mid = (left + right) // 2
            
            # --- This is the core logic ---
            
            # Case 1: We are on an "uphill" slope.
            # The peak must be to the right.
            if nums[mid] < nums[mid + 1]:
                # Discard the left half, including 'mid' itself,
                # because we know 'mid' is not a peak.
                left = mid + 1
            
            # Case 2: We are on a "downhill" slope.
            # The peak is either at 'mid' or to its left.
            else: # nums[mid] > nums[mid + 1]
                # Discard the right half. We keep 'mid' as a
                # potential peak.
                right = mid
                
        # When the loop terminates, 'left' and 'right' will have converged
        # on the same index, which is guaranteed to be a peak.
        return left
```

## Detailed Code Analysis

### Step 1: Initialization

```python
left = 0
right = len(nums) - 1
```

  - `left`: Pointer to the start of our search space, `index 0`.
  - `right`: Pointer to the end of our search space, `index n-1`.

### Step 2: The Loop Condition

```python
while left < right:
```

  - This is a standard binary search loop condition. It means "keep searching as long as our search space has at least two elements."
  - When `left` becomes equal to `right`, the search space has shrunk to a single element, which must be our answer. The loop terminates.

### Step 3: The Midpoint and Comparison

```python
mid = (left + right) // 2
if nums[mid] < nums[mid + 1]:
    ...
else:
    ...
```

  - We calculate `mid`.
  - We compare the value at `mid` to the value of its right neighbor `mid + 1`. This is our "slope" check.

### Step 4: Shrinking the Search Space

```python
if nums[mid] < nums[mid + 1]:
    left = mid + 1
```

  - If we're on an uphill slope, we know `nums[mid]` is *not* a peak (since its right neighbor is greater).
  - We also know a peak is *guaranteed* to be somewhere in the range `[mid + 1, ... right]`.
  - So, we update our `left` pointer to `mid + 1`, effectively discarding the entire left half.

<!-- end list -->

```python
else:
    right = mid
```

  - If we're on a downhill slope (`nums[mid] > nums[mid + 1]`), we know that `mid` *might* be a peak, or a peak is to its left.
  - We know a peak is *guaranteed* to be somewhere in the range `[left, ... mid]`.
  - So, we update our `right` pointer to `mid`. We **do not** set it to `mid - 1`, because `mid` itself is a valid candidate for the peak.

### Step 5: The Return

```python
return left
```

  - The loop stops when `left == right`. At this point, both pointers have converged on a single index. This index is guaranteed to be a peak element based on our logic. We can return `left` (or `right`, as they are the same).

## Step-by-Step Execution Trace

Let's trace `nums = [1, 2, 1, 3, 5, 6, 4]`.

### **Initial State:**

  - `left = 0`
  - `right = 6`

-----

### **Loop 1:**

  - `mid = (0 + 6) // 2 = 3`. `nums[mid]` is `nums[3] = 3`.
  - `mid + 1 = 4`. `nums[mid + 1]` is `nums[4] = 5`.
  - Check: `nums[mid] < nums[mid + 1]`? -\> `3 < 5`? **True**.
  - We are on an uphill slope. Peak must be to the right.
  - `left = mid + 1` -\> `left = 4`.
  - **New Range**: `left = 4`, `right = 6`.

-----

### **Loop 2:**

  - `mid = (4 + 6) // 2 = 5`. `nums[mid]` is `nums[5] = 6`.
  - `mid + 1 = 6`. `nums[mid + 1]` is `nums[6] = 4`.
  - Check: `nums[mid] < nums[mid + 1]`? -\> `6 < 4`? **False**.
  - We are on a downhill slope. Peak is at `mid` or to its left.
  - `right = mid` -\> `right = 5`.
  - **New Range**: `left = 4`, `right = 5`.

-----

### **Loop 3:**

  - `mid = (4 + 5) // 2 = 4`. `nums[mid]` is `nums[4] = 5`.
  - `mid + 1 = 5`. `nums[mid + 1]` is `nums[5] = 6`.
  - Check: `nums[mid] < nums[mid + 1]`? -\> `5 < 6`? **True**.
  - We are on an uphill slope. Peak must be to the right.
  - `left = mid + 1` -\> `left = 5`.
  - **New Range**: `left = 5`, `right = 5`.

-----

### **End of Algorithm**

  - The `while left < right` condition (`5 < 5`) is now **False**. The loop terminates.
  - The function returns `left`, which is **5**.
  - The element at index 5 is `6`, which is a valid peak.

## Performance Analysis

### Time Complexity: O(log n)

  - This is the entire point of the algorithm. At each step, we are dividing our search space in half. The number of times you can halve a list of size `n` is `log n`.

### Space Complexity: O(1)

  - We only use a few variables (`left`, `right`, `mid`). The space required is constant and does not grow with the size of the input array.