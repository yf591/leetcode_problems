# 746\. Min Cost Climbing Stairs - Solution Explanation

## Problem Overview

You are given a staircase represented by an array `cost`, where `cost[i]` is the price you must pay to step on stair `i`. Once you pay the cost, you can climb either **one** or **two** steps. The goal is to find the **minimum total cost** to reach the "top of the floor," which is considered one step beyond the last stair.

**Key Rules:**

  - You can start your climb from either index `0` or index `1`.
  - The cost is paid when you *step on* a stair.

**Examples:**

```python
Input: cost = [10,15,20]
Output: 15
Explanation: The cheapest way is to start at index 1, pay 15, and climb two steps to reach the top.

Input: cost = [1,100,1,1,1,100,1,1,100,1]
Output: 6
Explanation: The cheapest path involves stepping on indices 0, 2, 4, 6, 7, and 9. The total cost is 1+1+1+1+1+1 = 6.
```

## Key Insights

### A Classic Dynamic Programming Problem

The phrase **"minimum cost"** combined with making a sequence of choices (jump 1 or 2 steps) is a strong signal that this is a **Dynamic Programming (DP)** problem. DP is an approach where you solve a complex problem by breaking it down into simpler, overlapping subproblems.

### The Recurrence Relation

The key insight is to define the minimum cost to reach any step `i` based on the costs to reach the steps before it.

  - To arrive at step `i`, you must have come from either step `i-1` (by taking a 1-step jump) or step `i-2` (by taking a 2-step jump).
  - To minimize the cost to reach step `i`, you should have jumped from whichever of the previous two steps was cheaper to reach.
  - This gives us the formula:
    `min_cost_to_reach[i] = cost[i] + min(min_cost_to_reach[i-1], min_cost_to_reach[i-2])`

### Space Optimization: In-Place Modification

Instead of creating a new `dp` array to store these minimum costs, we can be more efficient. Once we calculate the minimum cost to reach step `i`, the *original* `cost[i]` is no longer needed for future calculations. This allows us to overwrite the `cost` array and use it as our DP table, achieving `O(1)` extra space.

## Solution Approach

This solution modifies the `cost` array in-place. Each element `cost[i]` is updated to represent the minimum total cost to reach that step. The final answer is then the minimum of the costs to reach the last two steps, from which you can take the final leap to the top.

```python
from typing import List

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        
        # Iterate from the third step (index 2) to the end of the array.
        for i in range(2, n):
            # Update the cost of reaching the current step. It's the step's own cost
            # plus the minimum of the costs to reach the previous two steps.
            cost[i] += min(cost[i - 1], cost[i - 2])
            
        # The final cost to reach the top is the minimum of the costs
        # to reach the last step or the second-to-last step.
        return min(cost[n - 1], cost[n - 2])
```

## Detailed Code Analysis

### Step 1: The Loop

```python
for i in range(2, n):
```

  - We start the loop at index `2`. Why?
      - The cost to reach step `0` is simply `cost[0]`.
      - The cost to reach step `1` is simply `cost[1]`.
      - This is because the problem states we can start at either index `0` or `1`, so there's no prior cost. The first calculation we need to do is for step `2`, which depends on the costs of steps 0 and 1.

### Step 2: The Dynamic Programming Update

```python
cost[i] += min(cost[i - 1], cost[i - 2])
```

  - This is the heart of the algorithm, where we update the array.
  - **`min(cost[i - 1], cost[i - 2])`**: This part makes the greedy choice. It looks at the two previous steps and finds the minimum total cost to reach either of them.
  - **`cost[i] += ...`**: We add this minimum cost to the cost of the current step (`cost[i]`). The value at `cost[i]` is now transformed: it no longer represents the cost of just this single step, but the **minimum total cost to arrive at this step from the start**.

### Step 3: The Final Result

```python
return min(cost[n - 1], cost[n - 2])
```

  - The "top of the floor" is a destination one step past the end of the array.
  - To get there, you can make a final jump from either the last step (`n-1`) or the second-to-last step (`n-2`).
  - By this point in the code, `cost[n-1]` and `cost[n-2]` hold the total minimum costs to reach those respective steps.
  - Therefore, the cheapest way to reach the top is simply the minimum of these two final costs.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]`.

1.  **Initial State**: `n = 10`. The loop will run for `i` from `2` up to `9`.
2.  **The Loop**:

| `i` | `cost[i-1]` | `cost[i-2]` | `min(...)` | `cost[i]` (original) | `cost[i]` (new value) | `cost` Array State (up to `i`) |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start**| - | - | - | - | - | `[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]` |
| **2** | 100 | 1 | 1 | 1 | `1 + 1 = 2` | `[1, 100, 2, ...]` |
| **3** | 2 | 100 | 2 | 1 | `1 + 2 = 3` | `[1, 100, 2, 3, ...]` |
| **4** | 3 | 2 | 2 | 1 | `1 + 2 = 3` | `[1, 100, 2, 3, 3, ...]` |
| **5** | 3 | 3 | 3 | 100 | `100 + 3 = 103`| `[..., 2, 3, 3, 103, ...]` |
| **6** | 103 | 3 | 3 | 1 | `1 + 3 = 4` | `[..., 3, 3, 103, 4, ...]` |
| **7** | 4 | 103 | 4 | 1 | `1 + 4 = 5` | `[..., 3, 103, 4, 5, ...]` |
| **8** | 5 | 4 | 4 | 100 | `100 + 4 = 104`| `[..., 103, 4, 5, 104, ...]` |
| **9** | 104 | 5 | 5 | 1 | `1 + 5 = 6` | `[..., 4, 5, 104, 6]` |

3.  **Final Step**:
      * The loop finishes. The final `cost` array is `[1, 100, 2, 3, 3, 103, 4, 5, 104, 6]`.
      * The code returns `min(cost[n - 1], cost[n - 2])`.
      * `min(cost[9], cost[8])` -\> `min(6, 104)`.
      * The final answer is **6**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of steps in `cost`. We iterate through the list exactly once.

### Space Complexity: O(1)

  - The solution brilliantly modifies the input array in-place. It does not use any extra data structures that scale with the size of the input, so the extra space is constant.

## Key Learning Points

  - **Dynamic Programming (DP)**: This is a perfect example of a DP problem where the solution to a larger problem (`min_cost_to_reach[i]`) is built from the solutions to smaller subproblems (`min_cost_to_reach[i-1]` and `min_cost_to_reach[i-2]`).
  - **Space Optimization**: The in-place modification is a common and powerful technique in DP to reduce space complexity from `O(n)` (for a separate `dp` array) to `O(1)`.
  - **Bottom-Up Approach**: Building the solution from the known base cases (`cost[0]`, `cost[1]`) up to the final answer is a clear and efficient way to structure a DP solution.