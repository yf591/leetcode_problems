# 34\. Find First and Last Position of Element in Sorted Array - Solution Explanation

## Problem Overview

You are given an array of integers `nums` sorted in non-decreasing order (ascending). You are also given a `target` value.

Your task is to find the **starting** and **ending** position of that `target` value.
If the target is not found in the array, return `[-1, -1]`.

**Key Constraint:** You must write an algorithm with **$O(\log n)$** runtime complexity.

**Example:**

```python
Input: nums = [5, 7, 7, 8, 8, 10], target = 8
Output: [3, 4]
# The value 8 appears at index 3 and index 4.
```

## Deep Dive: What is Binary Search? 🔍

**Binary Search** is an efficient algorithm for finding an item from a **sorted** list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one.

**The Analogy:**
Imagine looking for a word in a dictionary. You don't read every page from the beginning.

1.  You open the book to the **middle**.
2.  If the word you are looking for comes *alphabetically before* the word on the current page, you ignore the entire second half of the book.
3.  You repeat the process with the first half, opening it to the middle.
4.  You keep cutting the search space in half until you find the word.

**Why is it fast?**
Because we discard half the possibilities in every step, the time complexity is **$O(\log n)$** (logarithmic time). For reference:

  - Searching 1,000,000 items linearly takes up to 1,000,000 steps.
  - Searching 1,000,000 items with Binary Search takes only about **20 steps**.

## Key Insights for This Problem

### 1\. The Limitation of Standard Binary Search

A standard Binary Search stops the moment it finds the target.

  - If we search for `8` in `[5, 7, 7, 8, 8, 10]`, standard Binary Search might hit the `8` at index **4** and return `4`.
  - However, we need the **first** (index 3) and the **last** (index 4). Standard Binary Search doesn't distinguish between duplicates.

### 2\. Modifying the "Found" Condition

To solve this, we need to change what happens when `nums[mid] == target`. Instead of returning immediately, we must **keep searching**:

  - **To find the First Position:** Even if we find the target, we treat it as "possibly not the first one." We assume there might be another 8 to the **left**, so we continue searching in the left half.
  - **To find the Last Position:** If we find the target, we assume there might be another 8 to the **right**, so we continue searching in the right half.

## Solution Approach

We create a helper function `findBound(isFirst)` that performs a modified binary search.

1.  If `isFirst` is true, it searches for the left-most occurrence.
2.  If `isFirst` is false, it searches for the right-most occurrence.

We run this function twice to get our answer.

```python
from typing import List

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        
        # Helper function to find the specific boundary
        def findBound(isFirst: bool) -> int:
            left, right = 0, len(nums) - 1
            bound_idx = -1
            
            while left <= right:
                mid = (left + right) // 2
                
                if nums[mid] == target:
                    # Record the index we found
                    bound_idx = mid
                    
                    # CRITICAL STEP: Do not return yet!
                    if isFirst:
                        # If finding the FIRST occurrence, narrow scope to the LEFT.
                        # We discard the right side (including mid) to see if 
                        # there is an 8 earlier.
                        right = mid - 1
                    else:
                        # If finding the LAST occurrence, narrow scope to the RIGHT.
                        # We discard the left side (including mid) to see if 
                        # there is an 8 later.
                        left = mid + 1
                        
                elif nums[mid] < target:
                    # Value too small, go right
                    left = mid + 1
                else:
                    # Value too big, go left
                    right = mid - 1
                    
            return bound_idx

        # 1. Find Start
        start = findBound(True)
        
        # Optimization: If start is -1, the target isn't there. No need to search for end.
        if start == -1:
            return [-1, -1]
            
        # 2. Find End
        end = findBound(False)
        
        return [start, end]
```

## Detailed Code Analysis

### The `findBound` Helper Function

**1. Initialization:**

```python
left, right = 0, len(nums) - 1
bound_idx = -1
```

  - Standard binary search setup. `bound_idx` stores the *best* index we've found so far matching the target. We start with `-1` (not found).

**2. The Loop:**

```python
while left <= right:
    mid = (left + right) // 2
```

  - Standard loop. It calculates the middle index.

**3. The "Found" Logic (The Magic):**

```python
if nums[mid] == target:
    bound_idx = mid  # Save this position
    
    if isFirst:
        right = mid - 1 
    else:
        left = mid + 1
```

  - When `nums[mid] == target`, we don't stop. We record `mid` in `bound_idx`.
  - **Finding First:** We set `right = mid - 1`. This forces the search to continue in the indices *smaller* than `mid`. If there is an earlier `8`, we will find it. If not, `bound_idx` (the current `mid`) remains the answer.
  - **Finding Last:** We set `left = mid + 1`. This forces the search to continue in the indices *larger* than `mid`. If there is a later `8`, we will find it.

**4. Standard Navigation:**

```python
elif nums[mid] < target:
    left = mid + 1
else:
    right = mid - 1
```

  - If the value at `mid` is not the target, we behave exactly like a normal binary search to get closer to the target.

## Step-by-Step Execution Trace

Let's trace the input: `nums = [5, 7, 7, 8, 8, 10]`, `target = 8`.

### **Pass 1: Finding the START (`findBound(True)`)**

| Iteration | `left` | `right` | `mid` | `nums[mid]` | Comparison | Action | `bound_idx` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | 0 | 5 | - | - | - | - | -1 |
| **1** | 0 | 5 | **2** | 7 | `7 < 8` | `left = mid + 1` | -1 |
| **2** | 3 | 5 | **4** | 8 | `8 == 8` | Found\! Save index. **Go Left**. `right = mid - 1` | **4** |
| **3** | 3 | 3 | **3** | 8 | `8 == 8` | Found\! Save index. **Go Left**. `right = mid - 1` | **3** |
| **End** | 3 | 2 | - | - | `left > right` | Loop Ends | **3** |

  * **Result for Start:** 3

### **Pass 2: Finding the END (`findBound(False)`)**

| Iteration | `left` | `right` | `mid` | `nums[mid]` | Comparison | Action | `bound_idx` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | 0 | 5 | - | - | - | - | -1 |
| **1** | 0 | 5 | **2** | 7 | `7 < 8` | `left = mid + 1` | -1 |
| **2** | 3 | 5 | **4** | 8 | `8 == 8` | Found\! Save index. **Go Right**. `left = mid + 1` | **4** |
| **3** | 5 | 5 | **5** | 10 | `10 > 8` | Too big. `right = mid - 1` | 4 |
| **End** | 5 | 4 | - | - | `left > right` | Loop Ends | **4** |

  * **Result for End:** 4

### **Final Output**

The function combines the results: `[3, 4]`.

## Performance Analysis

### Time Complexity: O(log n)

  - We perform Binary Search twice.
  - Binary Search takes $O(\log n)$ time.
  - Total time = $O(\log n) + O(\log n) = O(\log n)$.
  - This meets the problem's requirements perfectly.

### Space Complexity: O(1)

  - We are using an iterative approach (loops instead of recursion).
  - We only need a few variables (`left`, `right`, `mid`, `bound_idx`) to keep track of our position.
  - The memory usage does not grow with the size of the input array.