# 198\. House Robber - Solution Explanation

## Problem Overview

You are a robber given a list of houses, `nums`, where `nums[i]` is the amount of money in the `i`-th house. The goal is to find the **maximum total amount of money** you can rob.

**The Main Constraint:**

  - You **cannot** rob two **adjacent** houses. If you do, an alarm will go off.

**Examples:**

```python
Input: nums = [1,2,3,1]
Output: 4
Explanation: The optimal strategy is to rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount = 1 + 3 = 4.

Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9), and rob house 5 (money = 1).
Total amount = 2 + 9 + 1 = 12.
```

## Deep Dive: What is Dynamic Programming (DP)? 🧠

**Dynamic Programming (DP)** is a powerful algorithmic technique for solving complex problems by breaking them down into simpler, **overlapping subproblems**.

Think of it as building a solution from the ground up by solving the easiest, smallest versions of the problem first, and then using those answers to solve slightly larger versions, until you have solved the main problem. It's like building a tower: you build the 1st floor, then use that to build the 2nd, then use the 2nd to build the 3rd.

DP relies on two main properties:

1.  **Overlapping Subproblems**: The problem can be broken down into smaller subproblems that are *reused* multiple times. For example, to find the max profit for 5 houses, you'll need the max profit for 4 houses and 3 houses. To find the max profit for 4 houses, you'll *also* need the max profit for 3 houses. Instead of re-calculating the answer for 3 houses every time, DP says we should **store the answer** the first time we find it (this is called "memoization" or "tabulation").
2.  **Optimal Substructure**: The optimal solution to the main (large) problem can be constructed from the *optimal solutions* to its smaller subproblems.

**How it Applies Here:**
The **maximum profit** you can get from robbing `k` houses is based on the maximum profit you could have gotten from `k-1` houses and `k-2` houses. By finding the optimal solution for the first house, then the first two, then the first three, we can build our way up to the optimal solution for the entire street.

## Key Insights for This Problem

### 1\. The Recurrence Relation (The Core Logic)

This problem has a perfect optimal substructure. Let's think about the choice a robber has at *any* given house `i`:

1.  **Choice 1: Rob this house (`house i`)**

      - You get the money from this house: `nums[i]`.
      - Because you robbed this house, you *cannot* have robbed the previous one (`house i-1`).
      - Therefore, the profit for this choice is: `nums[i] + (the max profit you could have made up to house i-2)`.

2.  **Choice 2: Do NOT rob this house (`house i`)**

      - You get `0` money from this house.
      - Since you didn't rob this house, you are free to have robbed the previous one.
      - Therefore, the profit for this choice is: `the max profit you could have made up to house i-1`.

The best decision is the one that gives the most money. This gives us our **recurrence relation**:

`max_profit_at_house[i] = max( max_profit_at_house[i-1], nums[i] + max_profit_at_house[i-2] )`

### 2\. Space Optimization (From `O(n)` to `O(1)`)

We could create a whole new array `dp` of size `n` to store the max profit at each step.

  - `dp[0] = nums[0]`
  - `dp[1] = max(nums[0], nums[1])`
  - `dp[i] = max(dp[i-1], nums[i] + dp[i-2])`

But notice that to calculate the profit for `dp[i]`, we only need the two values immediately before it: `dp[i-1]` and `dp[i-2]`. We don't need `dp[i-3]` or any other previous value.

This is just like the Fibonacci sequence. We don't need to store the whole array\! We can just use two variables to keep track of the two previous maximums, giving us an incredibly efficient **`O(1)` space complexity**.

## Solution Approach

This solution implements the space-optimized DP strategy. It iterates through the `nums` list once, maintaining two variables:

  - `rob_prev_prev`: Stores the maximum profit from two houses ago (`dp[i-2]`).
  - `rob_prev`: Stores the maximum profit from the previous house (`dp[i-1]`).

At each step, these two variables are used to calculate the new maximum profit, and then they are "shifted" forward for the next iteration.

```python
from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        
        # We use two variables to track the max profit from the
        # previous two steps, effectively dp[i-2] and dp[i-1].
        
        rob_prev_prev = 0  # Represents the max profit from two houses ago (dp[i-2])
        rob_prev = 0       # Represents the max profit from the previous house (dp[i-1])
        
        # Iterate through each house in the list.
        for current_money in nums:
            
            # --- Apply the Recurrence Relation ---
            
            # We must decide what the new max profit is. We have two choices:
            # 1. Skip this house: Profit is 'rob_prev'.
            # 2. Rob this house: Profit is 'current_money + rob_prev_prev'.
            
            # 'temp_max' holds the max profit for the *current* house (dp[i]).
            temp_max = max(current_money + rob_prev_prev, rob_prev)
            
            # --- "Slide" the variables for the next iteration ---
            # The previous profit (rob_prev) now becomes the "two steps ago" profit.
            rob_prev_prev = rob_prev
            # The new max profit we just calculated (temp_max) becomes the "previous" profit.
            rob_prev = temp_max
            
        # After the loop finishes, 'rob_prev' holds the max profit for the
        # entire street (the value for the last house).
        return rob_prev
```

## Detailed Code Analysis

### Step 1: Initialization

```python
rob_prev_prev = 0
rob_prev = 0
```

  - We initialize both variables to `0`. `rob_prev_prev` is the profit from two steps back, and `rob_prev` is from one step back. Before the loop starts (at an imaginary "house -1"), the max profit is 0.

### Step 2: The Loop

```python
for current_money in nums:
```

  - We iterate through each number in `nums` one by one. `current_money` is `nums[i]`.

### Step 3: The DP Calculation

```python
temp_max = max(current_money + rob_prev_prev, rob_prev)
```

  - This is the most important line. It's a direct translation of our recurrence relation: `dp[i] = max(nums[i] + dp[i-2], dp[i-1])`.
      - `current_money + rob_prev_prev` is the profit from **robbing this house**.
      - `rob_prev` is the profit from **skipping this house**.
  - We store the result in a temporary variable `temp_max` so we don't overwrite `rob_prev` before we use it in the next step.

### Step 4: The "Slide"

```python
rob_prev_prev = rob_prev
rob_prev = temp_max
```

  - This is the "shift" that prepares our variables for the *next* iteration of the loop.
  - The value that *was* the previous max (`rob_prev`) now becomes the "two ago" max (`rob_prev_prev`).
  - The value we *just* calculated (`temp_max`) now becomes the "previous" max (`rob_prev`).
  - This way, when the loop runs for the next house, `rob_prev` and `rob_prev_prev` hold the correct values from its two predecessors.

### Step 5: The Final Return

```python
return rob_prev
```

  - When the loop finishes, `rob_prev` will be holding the value of the last `temp_max` that was calculated. This represents the maximum profit possible after considering all houses in the list.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `nums = [2, 7, 9, 3, 1]` with extreme detail.

### **Initial State:**

  - `rob_prev_prev = 0`
  - `rob_prev = 0`

-----

### **Loop 1: `current_money = 2`**

1.  **Calculate `temp_max`**:
      - `rob_this_house = 2 + rob_prev_prev` -\> `2 + 0 = 2`
      - `skip_this_house = rob_prev` -\> `0`
      - `temp_max = max(2, 0) = 2`
2.  **Slide Variables**:
      - `rob_prev_prev = rob_prev` -\> `rob_prev_prev = 0`
      - `rob_prev = temp_max` -\> `rob_prev = 2`

**State after loop 1:** `rob_prev_prev = 0`, `rob_prev = 2`

-----

### **Loop 2: `current_money = 7`**

1.  **Calculate `temp_max`**:
      - `rob_this_house = 7 + rob_prev_prev` -\> `7 + 0 = 7`
      - `skip_this_house = rob_prev` -\> `2`
      - `temp_max = max(7, 2) = 7`
2.  **Slide Variables**:
      - `rob_prev_prev = rob_prev` -\> `rob_prev_prev = 2`
      - `rob_prev = temp_max` -\> `rob_prev = 7`

**State after loop 2:** `rob_prev_prev = 2`, `rob_prev = 7`

-----

### **Loop 3: `current_money = 9`**

1.  **Calculate `temp_max`**:
      - `rob_this_house = 9 + rob_prev_prev` -\> `9 + 2 = 11`
      - `skip_this_house = rob_prev` -\> `7`
      - `temp_max = max(11, 7) = 11`
2.  **Slide Variables**:
      - `rob_prev_prev = rob_prev` -\> `rob_prev_prev = 7`
      - `rob_prev = temp_max` -\> `rob_prev = 11`

**State after loop 3:** `rob_prev_prev = 7`, `rob_prev = 11`

-----

### **Loop 4: `current_money = 3`**

1.  **Calculate `temp_max`**:
      - `rob_this_house = 3 + rob_prev_prev` -\> `3 + 7 = 10`
      - `skip_this_house = rob_prev` -\> `11`
      - `temp_max = max(10, 11) = 11`
2.  **Slide Variables**:
      - `rob_prev_prev = rob_prev` -\> `rob_prev_prev = 11`
      - `rob_prev = temp_max` -\> `rob_prev = 11`

**State after loop 4:** `rob_prev_prev = 11`, `rob_prev = 11`

-----

### **Loop 5: `current_money = 1`**

1.  **Calculate `temp_max`**:
      - `rob_this_house = 1 + rob_prev_prev` -\> `1 + 11 = 12`
      - `skip_this_house = rob_prev` -\> `11`
      - `temp_max = max(12, 11) = 12`
2.  **Slide Variables**:
      - `rob_prev_prev = rob_prev` -\> `rob_prev_prev = 11`
      - `rob_prev = temp_max` -\> `rob_prev = 12`

**State after loop 5:** `rob_prev_prev = 11`, `rob_prev = 12`

-----

### **End of Algorithm**

  - The `for` loop finishes.
  - The function returns the final `rob_prev`, which is **12**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of houses. We iterate through the list exactly once.

### Space Complexity: O(1)

  - This is the beauty of this solution. We only use a few constant-space variables (`rob_prev_prev`, `rob_prev`, `temp_max`). The space required does not grow with the size of the input list.