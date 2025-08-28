# 643\. Maximum Average Subarray I - Solution Explanation

## Problem Overview

You are given an array of integers `nums` and a number `k`. The goal is to find the **maximum average value** among all possible **contiguous subarrays** that have a length of exactly `k`.

**Key Definitions:**

  - **Contiguous Subarray**: A slice of the array where the elements are next to each other (e.g., in `[1,2,3,4]`, `[2,3]` is a contiguous subarray, but `[1,3]` is not).
  - **Average**: The sum of the elements in the subarray divided by its length, `k`.

**Examples:**

```python
Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: The subarray [12, -5, -6, 50] has the maximum sum of 51.
The average is 51 / 4 = 12.75.
```

## Key Insights

### Maximizing the Sum

The problem asks for the maximum *average*. Since the length of the subarray, `k`, is always the same for every calculation, the fraction `sum / k` is maximized when the `sum` is maximized. This simplifies the problem: we just need to find the subarray of length `k` with the greatest possible **sum**.

### The Sliding Window Technique

A naive or brute-force approach would be to calculate the sum of every possible subarray of length `k`. This would be very slow because you would be re-calculating sums over and over.

The key insight for an efficient solution is the **sliding window** technique.

1.  Start by calculating the sum of the very first window of `k` elements.
2.  Then, instead of moving to the next position and recalculating a whole new sum, just "slide" the window one position to the right.
3.  To update the sum for this new window, you only need to **add the new element** that just entered the window and **subtract the old element** that just left. This is an extremely fast, constant-time `O(1)` update.

## Solution Approach

This solution implements the sliding window technique. It computes the sum of the initial window and then slides it across the rest of the array, efficiently updating the sum at each step and keeping track of the maximum sum found.

```python
from typing import List

class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        # Step 1: Calculate the sum of the initial window of size 'k'.
        current_sum = sum(nums[:k])
        # This is the maximum sum we've seen so far.
        max_sum = current_sum
        
        # Step 2: Slide the window from the k-th element to the end of the array.
        for i in range(k, len(nums)):
            # Step 2a: Update the sum efficiently for the new window.
            current_sum += nums[i] - nums[i - k]
            
            # Step 2b: Update our maximum sum if the current window's sum is greater.
            max_sum = max(max_sum, current_sum)
            
        # Step 3: The maximum average is the maximum sum divided by k.
        return max_sum / k
```

## Detailed Code Analysis

### Step 1: Initialization

```python
current_sum = sum(nums[:k])
max_sum = current_sum
```

  - We begin by calculating the sum of the very first subarray of length `k`. `nums[:k]` creates a slice of the first `k` elements.
  - We initialize both `current_sum` (the sum of the window we are currently looking at) and `max_sum` (the best sum we've found so far) to this initial value.

### Step 2: The Sliding Loop

```python
for i in range(k, len(nums)):
```

  - This loop handles the "sliding" of the window.
  - It starts at index `k`, which is the first element *outside* our initial window. In each iteration, `nums[i]` will be the new element entering the window from the right.

### Step 3: The O(1) Window Update

```python
current_sum += nums[i] - nums[i - k]
```

  - This is the heart of the sliding window algorithm. It updates the sum in a single, efficient step.
  - **`+ nums[i]`**: We add the new element that is just entering the window.
  - **`- nums[i - k]`**: We subtract the element that is now falling off the left side of the window. For example, when `i` is `k`, `i-k` is `0`, so we subtract the very first element.

### Step 4: Tracking the Maximum

```python
max_sum = max(max_sum, current_sum)
```

  - After each slide, our `current_sum` represents the sum of the new subarray. We compare it with the `max_sum` we've recorded so far and update `max_sum` if the current one is better.

### Step 5: Final Calculation

```python
return max_sum / k
```

  - After the loop has finished, `max_sum` holds the largest sum found among all subarrays of length `k`. We divide this by `k` to get the final maximum average.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [1, 12, -5, -6, 50, 3]` and `k = 4`.

1.  **Initialization**:

      * The first window is `[1, 12, -5, -6]`.
      * `current_sum` = `1 + 12 - 5 - 6` = **2**.
      * `max_sum` is initialized to **2**.
      * The loop will run for `i` from `4` to `5`.

2.  **The Loop**:

| `i` | Window `nums[i-k+1:i+1]` | `nums[i]` (Entering) | `nums[i-k]` (Leaving) | `current_sum` (before) | `current_sum` (after update) | `max_sum` (after update) |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | `[1, 12, -5, -6]` | - | - | 2 | 2 | **2** |
| **4** | `[12, -5, -6, 50]` | 50 | 1 | 2 | `2 + 50 - 1 = 51` | `max(2, 51) = 51` |
| **5** | `[-5, -6, 50, 3]` | 3 | 12 | 51 | `51 + 3 - 12 = 42` | `max(51, 42) = 51` |

3.  **Final Step**:
      * The loop finishes.
      * `return max_sum / k` -\> `51 / 4`
      * The final output is **`12.75`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We calculate the initial sum in `O(k)` and then loop `n-k` times with constant `O(1)` work inside. The total time complexity is `O(k + (n-k))`, which simplifies to `O(n)`.

### Space Complexity: O(1)

  - We only use a few variables (`current_sum`, `max_sum`, `i`). The space required is constant and does not grow with the size of the input.

## Key Learning Points

  - **Sliding Window**: This is a fundamental technique for problems involving contiguous subarrays. It is extremely efficient for avoiding recalculations.
  - **Problem Simplification**: Recognizing that maximizing the average (with a fixed `k`) is the same as maximizing the sum is a key first step.
  - **O(1) Updates**: The `current_sum += new_element - old_element` pattern is the core of the fixed-size sliding window algorithm.