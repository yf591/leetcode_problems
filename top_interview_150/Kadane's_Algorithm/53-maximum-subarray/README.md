# 53\. Maximum Subarray - Solution Explanation

## Problem Overview

You are given an integer array `nums`. The task is to find the **contiguous subarray** (containing at least one number) which has the largest sum and return that sum.

**Examples:**

```python
Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Explanation: The subarray [4, -1, 2, 1] has the largest sum = 6.

Input: nums = [1]
Output: 1

Input: nums = [5, 4, -1, 7, 8]
Output: 23
```

## Deep Dive: What is Kadane's Algorithm? 🧠

**Kadane's Algorithm** is a dynamic programming approach used to solve the maximum subarray problem in **linear time** ($O(n)$).

### The Intuition: "Drop the Baggage" 🎒

Imagine you are walking along the array, picking up numbers and adding them to your bag (your `current_sum`). You want your bag to be as heavy as possible.

1.  **Positive Numbers Help**: If you have a positive sum in your bag (say, `5`) and you pick up a `3`, your total becomes `8`. Great\! You keep going.
2.  **Negative Numbers Hurt**: If you pick up a `-10`, your total drops. But you might still keep going because a huge positive number might be coming up next that makes up for it.
3.  **The "Reset" Point**: However, if the sum in your bag ever drops **below zero** (e.g., `-5`), this sum has become a liability.
      * If the next number is `10`, adding your "baggage" of `-5` results in `5`.
      * If you dropped the bag and started fresh at `10`, you would have `10`.
      * **Conclusion**: Whenever your running sum becomes negative, it is mathematically better to throw it away and start a new subarray at the current element.

### The Logic

At every index `i`, we ask a specific question to calculate `current_sum`:

> "Which is greater: the number at `i` alone, OR the number at `i` plus the previous sum?"

  * If `nums[i] > current_sum + nums[i]`, it means `current_sum` was negative. We **restart** the subarray at `nums[i]`.
  * If `nums[i] < current_sum + nums[i]`, it means `current_sum` was positive. We **extend** the subarray to include `nums[i]`.

## Solution Approach

This solution implements Kadane's Algorithm. It iterates through the array exactly once, maintaining a `current_sum` (local maximum) and a `max_sum` (global maximum).

```python
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # Initialize variables using the first element.
        # It is crucial NOT to initialize with 0, because the array might 
        # contain only negative numbers (e.g., [-5, -2]).
        max_sum = nums[0]
        current_sum = nums[0]
        
        # Iterate through the array starting from the second element.
        for i in range(1, len(nums)):
            
            # --- The Core of Kadane's Algorithm ---
            # We calculate the maximum sum ending at the current position 'i'.
            # We have two choices:
            # 1. Start a new subarray at nums[i] (if previous sum was negative).
            # 2. Extend the existing subarray (add nums[i] to current_sum).
            current_sum = max(nums[i], current_sum + nums[i])
            
            # Update the global maximum if the local maximum is higher.
            max_sum = max(max_sum, current_sum)
            
        return max_sum
```

## Detailed Code Analysis

### Step 1: Initialization

```python
max_sum = nums[0]
current_sum = nums[0]
```

  - We define two variables.
  - `max_sum`: Stores the highest sum found anywhere in the array so far.
  - `current_sum`: Stores the highest sum of a subarray **ending at the current index**.
  - We initialize them to `nums[0]` to handle edge cases where the array contains only negative numbers (e.g., `[-2, -1]`). If we initialized `max_sum` to `0`, the answer would be `0` (incorrect) instead of `-1`.

### Step 2: The Loop

```python
for i in range(1, len(nums)):
```

  - We start the loop from index `1` because index `0` has already been accounted for in the initialization.

### Step 3: The Decision (Local Maximum)

```python
current_sum = max(nums[i], current_sum + nums[i])
```

  - This line determines the fate of the subarray.
  - `current_sum + nums[i]`: This represents **extending** the previous subarray.
  - `nums[i]`: This represents **starting a new** subarray at the current position.
  - If the previous `current_sum` was negative, adding it to `nums[i]` would make the result smaller than `nums[i]` alone. So `max()` naturally picks `nums[i]`, effectively "resetting" the subarray.

### Step 4: Updating the Global Maximum

```python
max_sum = max(max_sum, current_sum)
```

  - We compare our newly calculated `current_sum` against the all-time best `max_sum`. If the current streak is better, we update the record.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`.

**Initial State:**

  - `max_sum = -2`
  - `current_sum = -2`

| Index | Value `nums[i]` | Previous `current_sum` | Calculation `max(val, prev + val)` | Decision | New `current_sum` | `max_sum` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **1** | -2 | `max(1, -2 + 1)` | **Restart** | 1 | **1** |
| **2** | **-3** | 1 | `max(-3, 1 - 3)` | Extend | -2 | 1 |
| **3** | **4** | -2 | `max(4, -2 + 4)` | **Restart** | 4 | **4** |
| **4** | **-1** | 4 | `max(-1, 4 - 1)` | Extend | 3 | 4 |
| **5** | **2** | 3 | `max(2, 3 + 2)` | Extend | 5 | **5** |
| **6** | **1** | 5 | `max(1, 5 + 1)` | Extend | 6 | **6** |
| **7** | **-5** | 6 | `max(-5, 6 - 5)` | Extend | 1 | 6 |
| **8** | **4** | 1 | `max(4, 1 + 4)` | Extend | 5 | 6 |

**Final Result:** `6` (which corresponds to the subarray `[4, -1, 2, 1]`).

## Performance Analysis

### Time Complexity: O(N)

  - We traverse the array exactly once with a single `for` loop.
  - Inside the loop, we perform constant time operations (addition, comparison, assignment).
  - Therefore, the time complexity is linear, or `O(N)`.

### Space Complexity: O(1)

  - We only use two variables (`max_sum` and `current_sum`) to store the state.
  - Regardless of how large the input array is, the memory usage remains constant.
  - Therefore, the space complexity is `O(1)`.