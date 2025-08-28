# 283\. Move Zeroes - Solution Explanation

## Problem Overview

Given an array of integers `nums`, the task is to move all the `0`s to the end of the array. This must be done while maintaining the **relative order** of all the non-zero elements.

**Key Constraints:**

  - **In-place modification**: You must modify the original `nums` array directly. You cannot create a new, separate array to build the result.
  - **O(1) Extra Space**: The solution should not use extra memory that scales with the size of the input.

**Examples:**

```python
Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]
# The non-zero elements 1, 3, and 12 maintain their original order.

Input: nums = [0]
Output: [0]
```

## Key Insights

### The Two-Pointer "Snowplow"

The constraints (`in-place`, `O(1)` space) are strong hints that a **two-pointer** approach is the way to go. A brute-force solution with nested loops would be too slow, and creating a new array is forbidden.

The most intuitive way to think about this is the **"snowplow"** analogy:

1.  We need one pointer, let's call it the **`read_ptr`**, that scans through the entire array from beginning to end, inspecting every element.
2.  We need another pointer, the **`write_ptr`**, that marks the boundary of the "cleared road." This is the position where the *next non-zero element* should be placed.
3.  As the `read_ptr` moves forward, if it finds a non-zero element, it "plows" it to the front of the array at the `write_ptr`'s location. The `write_ptr` then advances.
4.  If the `read_ptr` finds a zero, it simply "drives over" it, leaving it behind. The `write_ptr` stays put, waiting for the next non-zero element to fill its spot.

This single-pass approach correctly partitions the array into non-zero elements at the front and zeros at the back, all while preserving the relative order of the non-zero elements.

## Solution Approach

This solution implements the two-pointer "snowplow" technique. It iterates through the array once, swapping non-zero elements to the front.

```python
from typing import List

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # The 'write_ptr' (or wrt_ptr) keeps track of the position where the next
        # non-zero element should be placed.
        write_ptr = 0
        
        # The 'read_ptr' (or rd_ptr) scans through the entire array.
        for read_ptr in range(len(nums)):
            # If the element at the 'read_ptr' is not a zero...
            if nums[read_ptr] != 0:
                # ...swap it with the element at the 'write_ptr' position.
                nums[read_ptr], nums[write_ptr] = nums[write_ptr], nums[read_ptr]
                
                # Advance the 'write_ptr' to the next available slot for a non-zero element.
                write_ptr += 1
```

**Strategy:**

1.  **Initialize Write Pointer**: Start `write_ptr` at index `0`. This pointer marks the end of the non-zero section of the array.
2.  **Iterate with Read Pointer**: Loop through the entire array with `read_ptr` from `0` to the end.
3.  **Find Non-Zero Element**: Inside the loop, check if the element at the current `read_ptr` is non-zero.
4.  **Swap and Advance**: If `nums[read_ptr]` is not zero, swap it with the element at `nums[write_ptr]`, and then increment `write_ptr`.
5.  **Ignore Zeros**: If `nums[read_ptr]` is zero, do nothing. The `read_ptr` will continue forward, but the `write_ptr` will wait, holding its position for the next non-zero element.

## Detailed Code Analysis

### Step 1: Initialization

```python
write_ptr = 0
```

  - We initialize our `write_ptr` at the very beginning of the array. This pointer's job is to always point to the first position that is "dirty" (i.e., it either contains a zero that needs to be moved or it's the spot for the next non-zero element).

### Step 2: The Loop

```python
for read_ptr in range(len(nums)):
```

  - This starts our single scan through the array. `read_ptr` will visit every element from index `0` to `len(nums) - 1`.

### Step 3: The Condition

```python
if nums[read_ptr] != 0:
```

  - This is the core check. We are only interested in doing something when we find a non-zero number.

### Step 4: The Swap and Increment

```python
nums[read_ptr], nums[write_ptr] = nums[write_ptr], nums[read_ptr]
write_ptr += 1
```

  - **The Swap**: `nums[read_ptr], nums[write_ptr] = nums[write_ptr], nums[read_ptr]` is a Pythonic way to swap two elements. This action moves the non-zero element found at `read_ptr` to the `write_ptr` position.
  - **The Increment**: `write_ptr += 1` is crucial. After we've placed a non-zero element at the `write_ptr` position, that spot is now "clean." We advance the `write_ptr` by one so it now points to the next position that needs to be filled with a non-zero number.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [0, 1, 0, 3, 12]`.

| `read_ptr` | `write_ptr` (start) | `nums[read_ptr]` | `nums[read_ptr] != 0`? | Action | `nums` Array State | `write_ptr` (end) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | 0 | `0` | False | Do nothing. | `[0, 1, 0, 3, 12]` | 0 |
| **1** | 0 | `1` | True | Swap `nums[1]` and `nums[0]`. Increment `write_ptr`. | `[1, 0, 0, 3, 12]` | 1 |
| **2** | 1 | `0` | False | Do nothing. | `[1, 0, 0, 3, 12]` | 1 |
| **3** | 1 | `3` | True | Swap `nums[3]` and `nums[1]`. Increment `write_ptr`. | `[1, 3, 0, 0, 12]` | 2 |
| **4** | 2 | `12`| True | Swap `nums[4]` and `nums[2]`. Increment `write_ptr`. | `[1, 3, 12, 0, 0]` | 3 |

  - The loop finishes. The final state of the array is `[1, 3, 12, 0, 0]`, which is the correct answer. The function implicitly modifies `nums` and does not need to return anything.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We iterate through the list exactly once.

### Space Complexity: O(1)

  - The modification is done in-place. We only use two pointers (`read_ptr`, `write_ptr`), so the extra space is constant.

## Key Learning Points

  - The **two-pointer technique** is a fundamental and powerful pattern for in-place array modifications that need to preserve the order of a subset of elements.
  - Separating the roles of "reading" and "writing" into two different pointers can greatly simplify logic that would otherwise be complex.
  - This "snowplow" or "partitioning" idea is applicable to many other problems where you need to group elements with a certain property at the beginning of an array.