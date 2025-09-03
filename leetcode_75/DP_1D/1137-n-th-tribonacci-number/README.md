# 1137\. N-th Tribonacci Number - Solution Explanation

## Problem Overview

The task is to calculate the **n-th Tribonacci number**, denoted as `Tn`.

**Tribonacci Definition:**
The Tribonacci sequence is a series of numbers where each number is the sum of the **three** preceding ones. It's defined by:

  - `T₀ = 0`
  - `T₁ = 1`
  - `T₂ = 1`
  - And the recursive formula: `Tₙ₊₃ = Tₙ + Tₙ₊₁ + Tₙ₊₂` for `n >= 0`.
    (This is the same as saying `Tₙ = Tₙ₋₁ + Tₙ₋₂ + Tₙ₋₃` for `n >= 3`)

**Example:**

```
Input: n = 4
Output: 4
Explanation:
T₃ = T₀ + T₁ + T₂ = 0 + 1 + 1 = 2
T₄ = T₁ + T₂ + T₃ = 1 + 1 + 2 = 4
```

## Key Insights

### A Variation of Fibonacci

This problem is very similar to the famous Fibonacci sequence, where each number is the sum of the two preceding ones. This "building block" nature, where the current value depends on previous values, is a strong indicator that **Dynamic Programming (DP)** is the right approach.

### The Inefficiency of Recursion

A direct recursive solution `trib(n) = trib(n-1) + trib(n-2) + trib(n-3)` would be extremely slow because it would re-calculate the same values over and over again.

### Bottom-Up Dynamic Programming

The most efficient solution is to build the sequence from the "bottom up." We start with the known base cases (`T₀, T₁, T₂`) and iteratively calculate each subsequent number until we reach `Tₙ`. We only ever need to keep track of the last three numbers in the sequence to calculate the next one, which makes this approach very memory-efficient.

## Solution Approach

This solution implements the bottom-up DP strategy. It handles the base cases first and then uses a loop with three variables that "slide" along the sequence to calculate the final result.

```python
class Solution:
    def tribonacci(self, n: int) -> int:
        # Step 1: Handle the initial base cases.
        if n == 0:
            return 0
        if n == 1 or n == 2:
            return 1
        
        # Step 2: Initialize three variables to hold the first three values, T₀, T₁, and T₂.
        t0, t1, t2 = 0, 1, 1
        
        # Step 3: Loop from 3 up to n to build the sequence.
        for _ in range(3, n + 1):
            # Step 3a: Calculate the next Tribonacci number.
            next_trib = t0 + t1 + t2
            
            # Step 3b: "Slide" the variables forward for the next iteration.
            t0, t1, t2 = t1, t2, next_trib
            
        # Step 4: After the loop, t2 holds the n-th Tribonacci number.
        return t2
```

## Detailed Code Analysis

### Step 1: Handling Base Cases

```python
if n == 0:
    return 0
if n == 1 or n == 2:
    return 1
```

  - The problem defines the first three terms explicitly. By handling these cases at the beginning, we simplify the main loop, which can now assume `n` is at least 3.

### Step 2: Initialization

```python
t0, t1, t2 = 0, 1, 1
```

  - We initialize three variables, `t0`, `t1`, and `t2`, to represent a "sliding window" of the last three numbers in the sequence. We start them with the known values for `T₀`, `T₁`, and `T₂`.

### Step 3: The Loop

```python
for _ in range(3, n + 1):
```

  - This loop will run `n-2` times. It starts at `3` because we already have the values for `n=0, 1, 2`. It goes up to `n + 1` (exclusive) so that the last number we calculate is `Tₙ`.
  - We use `_` as the loop variable because we don't need to know the specific value of `i`; we just need to repeat the action the correct number of times.

### Step 4: The Calculation and "Slide"

```python
next_trib = t0 + t1 + t2
t0, t1, t2 = t1, t2, next_trib
```

  - This is the core of the algorithm.
  - `next_trib = t0 + t1 + t2`: This is a direct implementation of the Tribonacci formula. It calculates the next number in the sequence.
  - `t0, t1, t2 = t1, t2, next_trib`: This is a concise, Pythonic way to "slide" our window of variables one step forward.
      - The old `t1` becomes the new `t0`.
      - The old `t2` becomes the new `t1`.
      - The `next_trib` we just calculated becomes the new `t2`.

## Step-by-Step Execution Trace

Let's trace the algorithm for `n = 4` with extreme detail.

1.  **Check Base Cases**: `n=4` is not 0, 1, or 2. The code proceeds.
2.  **Initialization**: `t0` is set to `0`, `t1` to `1`, and `t2` to `1`.
3.  **Loop**: The loop `for _ in range(3, 5)` will run for the values `3` and `4`.

| Loop Iteration For | `t0` | `t1` | `t2` | `next_trib` Calculation (`t0+t1+t2`) | `(t0, t1, t2)` After Slide |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | 0 | 1 | 1 | - | `(0, 1, 1)` |
| **`_ = 3`** | 0 | 1 | 1 | `0 + 1 + 1 = 2` | `(1, 1, 2)` |
| **`_ = 4`** | 1 | 1 | 2 | `1 + 1 + 2 = 4` | `(1, 2, 4)` |

4.  **End of Loop**: The loop has finished.
5.  **Return Value**: The function returns the final value of `t2`, which is **4**.

## Performance Analysis

### Time Complexity: O(n)

  - The algorithm's runtime is directly proportional to `n` because of the single `for` loop that runs from 3 to `n`.

### Space Complexity: O(1)

  - This is a highly memory-efficient solution. We only use a few variables (`t0`, `t1`, `t2`, `next_trib`) to store our state, regardless of how large `n` is. The space required is constant.

## Why the Iterative "Slide" Matters

The `t0, t1, t2 = t1, t2, next_trib` line is the key to the `O(1)` space complexity. A less optimal solution might store the entire sequence in a list or array:

```python
# Less space-efficient way
dp = [0] * (n + 1)
dp[1] = 1
dp[2] = 1
for i in range(3, n + 1):
    dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
return dp[n]
```

This works, but it uses `O(n)` space to store the `dp` array. Our chosen solution is better because it realizes we only need to remember the **last three** numbers, not the entire history.

## Key Learning Points

  - **Dynamic Programming (DP)**: This problem is a perfect introduction to bottom-up DP, where you solve a problem by building upon the solutions to smaller subproblems.
  - **Space Optimization**: Recognizing that you only need a fixed number of previous states (three, in this case) allows you to optimize a solution from `O(n)` space to `O(1)` space.
  - **Recurrence Relations**: Identifying the recurrence relation (`Tₙ = Tₙ₋₁ + ...`) is the first step in solving many DP problems.