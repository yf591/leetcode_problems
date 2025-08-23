# 80\. Remove Duplicates from Sorted Array II - Solution Explanation

## Problem Overview

Given a **sorted** integer array `nums`, the task is to remove duplicates **in-place** so that each unique element appears **at most twice**. The relative order of the elements must be preserved.

**Key Constraints:**

  - **In-place modification**: You cannot create a new array. You must modify the `nums` array directly.
  - **O(1) Extra Space**: You cannot use auxiliary data structures like hash maps that grow with the input size.
  - **Return Value**: The function should return `k`, the length of the modified array containing the result.

**Examples:**

```python
Input: nums = [1,1,1,2,2,3]
Output: 5, nums = [1,1,2,2,3,_]
# The first five elements are the result. The rest doesn't matter.

Input: nums = [0,0,1,1,1,1,2,3,3]
Output: 7, nums = [0,0,1,1,2,3,3,_,_]
```

## Key Insights

### The Two-Pointer Technique

The constraints (`in-place`, `O(1)` space) and the fact that the array is **sorted** are huge clues. This combination strongly points to a **two-pointer** approach. We can use one pointer to read through the array and another pointer to write the valid elements to the front of the array.

### The Core Question

As we iterate through the array, for each number, we must ask: **"Should I keep this number?"**
The rule is that we can keep a number if it is either the first or second occurrence of that number. Because the array is sorted, we don't need to count all occurrences. We only need to look at the last few elements we've already decided to keep.

The most clever insight is this: a number `num` should be kept if it is **different from the number two positions before the current end of our valid array**. If it's the same, it must be the third duplicate.

## Solution Approach

This solution uses a single "write" pointer, `k`, which tracks the length of the valid portion of the array. We iterate through each number in the input and only copy it to the `k`-th position if it meets our criteria.

```python
from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # 'k' is the "write" pointer. It indicates the next position
        # in the array to place a valid number.
        k = 0
        
        # Iterate through each number 'num' in the input array.
        for num in nums:
            # This condition decides if we should keep the current 'num'.
            # It's true if:
            # 1. We're filling the first two spots of the array (k < 2).
            # OR
            # 2. The current number is greater than the number at k-2.
            if k < 2 or num > nums[k - 2]:
                nums[k] = num
                k += 1
                
        # After the loop, 'k' is the new length of the array.
        return k
```

**Strategy:**

1.  **Initialize Write Pointer**: Start a pointer `k` at `0`. This pointer always points to the next available slot in the valid part of the array.
2.  **Iterate with Read Pointer**: Loop through every `num` in the `nums` array. This `num` is our "read" pointer.
3.  **Apply the Rule**: For each `num`, check if it should be kept. The condition `k < 2 or num > nums[k - 2]` elegantly handles this.
4.  **Write and Increment**: If the number should be kept, place it at `nums[k]` and increment `k`.
5.  **Return**: After the loop, `k` represents the length of the modified, valid array.

## Detailed Code Analysis

### The `if` Condition: The Heart of the Solution

```python
if k < 2 or num > nums[k - 2]:
```

This single line is the most important part of the algorithm. Let's break it down.

  * **`k < 2`**: This part handles the first two elements of the array. The problem allows each number to appear up to twice, so the first two numbers we encounter are *always* valid. We don't need to check anything else for them. This condition ensures they are always copied.

  * **`num > nums[k - 2]`**: This part handles all subsequent elements (when `k` is 2 or more). It's a clever way to check for a third duplicate.

      * `nums[k - 2]` is the last-but-one element in the *valid* part of the array we have built so far.
      * If the current `num` we are considering is the same as `nums[k-1]` and `nums[k-2]`, it means we have a third duplicate (e.g., `[...1, 1, ...]` and the current `num` is also `1`). In this case, `num` would not be greater than `nums[k-2]`, so the condition is false, and we discard `num`.
      * If the current `num` is a new number (e.g., `[...1, 1, ...]` and the current `num` is `2`), then `num` will be greater than `nums[k-2]`, the condition is true, and we keep `num`.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [0,0,1,1,1,1,2,3,3]`.

| `num` (from loop) | `k` (start) | `k < 2`? | `num > nums[k-2]`? | Action | `nums` array state |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | 0 | True | - | `nums[0]=0`, `k=1` | `[0,0,1,1,1,1,2,3,3]` |
| **0** | 1 | True | - | `nums[1]=0`, `k=2` | `[0,0,1,1,1,1,2,3,3]` |
| **1** | 2 | False | `1 > nums[0]` (1\>0) -\> True | `nums[2]=1`, `k=3` | `[0,0,1,1,1,1,2,3,3]` |
| **1** | 3 | False | `1 > nums[1]` (1\>0) -\> True | `nums[3]=1`, `k=4` | `[0,0,1,1,1,1,2,3,3]` |
| **1** | 4 | False | `1 > nums[2]` (1\>1) -\> False | Skip `num` | `[0,0,1,1,1,1,2,3,3]` |
| **1** | 4 | False | `1 > nums[2]` (1\>1) -\> False | Skip `num` | `[0,0,1,1,1,1,2,3,3]` |
| **2** | 4 | False | `2 > nums[2]` (2\>1) -\> True | `nums[4]=2`, `k=5` | `[0,0,1,1,2,1,2,3,3]` |
| **3** | 5 | False | `3 > nums[3]` (3\>1) -\> True | `nums[5]=3`, `k=6` | `[0,0,1,1,2,3,2,3,3]` |
| **3** | 6 | False | `3 > nums[4]` (3\>2) -\> True | `nums[6]=3`, `k=7` | `[0,0,1,1,2,3,3,3,3]` |

  - The loop finishes. The function returns `k`, which is **7**.
  - The final state of the first `k` elements of the array is `[0,0,1,1,2,3,3]`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We iterate through the list exactly once.

### Space Complexity: O(1)

  - We only use a single pointer (`k`) to modify the array in-place. The space required is constant and does not grow with the size of the input list.

## Key Learning Points

  - The two-pointer technique is a powerful pattern for in-place array modifications, especially on sorted arrays.
  - A single, clever condition can often handle multiple cases (like the initial elements vs. subsequent elements) in a clean way.
  - Thinking about the state you need to maintain (`k`) and the condition for advancing that state is key to designing the algorithm.

## Real-World Applications

  - **Data Deduplication**: Cleaning datasets by removing excessive duplicate entries while keeping a limited number for historical or analytical purposes.
  - **Log Processing**: Compacting log files by collapsing repeated, consecutive log messages into a single entry with a count, but maybe keeping the first two for context.
  - **Stream Processing**: Filtering a real-time stream of data to remove redundant signals or events.