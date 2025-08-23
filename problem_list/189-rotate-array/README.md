# 189\. Rotate Array - Solution Explanation

## Problem Overview

Given an array of integers `nums`, the task is to rotate its elements to the right by `k` steps. The modification must be done **in-place**, meaning you should alter the original array without creating a new one.

**Rotation Definition:**
A single right rotation moves the last element to the first position and shifts all other elements one spot to the right. This is repeated `k` times.

**Examples:**

```python
Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
After 1 step: [7,1,2,3,4,5,6]
After 2 steps: [6,7,1,2,3,4,5]
After 3 steps: [5,6,7,1,2,3,4]

Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
```

## Key Insights

### In-Place Modification

The core challenge is modifying the array with `O(1)` extra space. This rules out simple solutions that involve creating a new, separate array to store the result.

### The Reversal Algorithm

The most clever and space-efficient way to solve this is with a three-step reversal algorithm. It's a non-intuitive trick that correctly reorders the elements in-place.

1.  Reverse the entire array.
2.  Reverse the first `k` elements.
3.  Reverse the remaining `n-k` elements.

### Handling Large `k`

A crucial preliminary step is to handle cases where `k` is larger than the array's length. Rotating an array of length `n` by `n` steps brings it back to its original state. Therefore, the effective number of rotations is the remainder of `k` divided by `n`. This is calculated with the modulo operator: `k = k % n`.

## Solution Approach (In-Place Reversal)

This is the optimal solution that runs in `O(n)` time and `O(1)` space.

```python
from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        # Handle cases where k is larger than the array length
        k %= n

        def reverse(start: int, end: int):
            """Helper function to reverse a portion of the nums array in-place."""
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        # Step 1: Reverse the entire array.
        reverse(0, n - 1)

        # Step 2: Reverse the first k elements.
        reverse(0, k - 1)

        # Step 3: Reverse the remaining n-k elements.
        reverse(k, n - 1)
```

**Strategy:**

1.  **Normalize `k`**: Calculate `k = k % n` to get the effective number of rotations.
2.  **Reverse All**: Reverse the entire `nums` array.
3.  **Reverse First Part**: Reverse the sub-array from the beginning up to index `k-1`.
4.  **Reverse Second Part**: Reverse the sub-array from index `k` to the end.

## Detailed Code Analysis

### Step 1: Normalizing `k`

```python
n = len(nums)
k %= n
```

  - This step prevents unnecessary work. If you need to rotate an array of size 7 by `k=10` steps, it's the same as rotating it by `10 % 7 = 3` steps.

### Step 2: The `reverse` Helper Function

```python
def reverse(start: int, end: int):
    while start < end:
        nums[start], nums[end] = nums[end], nums[start]
        start += 1
        end -= 1
```

  - This is a standard in-place reversal algorithm. It uses two pointers, `start` and `end`, that move toward the center of the sub-array, swapping elements as they go.

### Step 3: The Three Reversals

```python
reverse(0, n - 1)
reverse(0, k - 1)
reverse(k, n - 1)
```

  - These three calls execute the core logic of the algorithm. Each call modifies the `nums` array in-place, building towards the final rotated state.

## Step-by-Step Execution Trace

Let's visually trace the algorithm with `nums = [1,2,3,4,5,6,7]` and `k = 3`.

| Step | Action | Array State |
| :--- | :--- | :--- |
| **Initial** | | `[1, 2, 3, 4, 5, 6, 7]` |
| **1** | Reverse the whole array. | `[7, 6, 5, 4, 3, 2, 1]` |
| **2** | Reverse the first `k=3` elements. | `[5, 6, 7, 4, 3, 2, 1]` |
| **3** | Reverse the remaining `n-k=4` elements. | `[5, 6, 7, 1, 2, 3, 4]` |

  - The final state is the correctly rotated array.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We pass through the array a constant number of times (once for the first reversal, and once more in total for the two partial reversals). This is a linear time operation.

### Space Complexity: O(1)

  - The reversals are done in-place. No auxiliary data structures that scale with the input size are used. This is a constant space solution.

## Alternative Solution (Using Slicing)

This solution is much simpler to write in Python but does not meet the `O(1)` space constraint.

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        
        # This one line does the rotation.
        nums[:] = nums[-k:] + nums[:-k]
```

  - **Explanation**:
      - `nums[-k:]` creates a new list containing the last `k` elements.
      - `nums[:-k]` creates a new list containing the first `n-k` elements.
      - These two lists are concatenated, and `nums[:]` overwrites the original `nums` list with the content of this new, rotated list.
  - **Pros & Cons**:
      - ✅ Very simple, readable, and Pythonic.
      - ❌ Uses `O(n)` extra space because the slicing and concatenation operations create temporary copies of the array. In an interview, you would likely be asked for the `O(1)` space solution.