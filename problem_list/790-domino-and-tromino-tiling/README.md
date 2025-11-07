# 790\. Domino and Tromino Tiling - Solution Explanation

## Problem Overview

You are given a `2 x n` board and two types of tiles: a `2 x 1` domino and an `L-shaped tromino`. You can rotate these tiles. The task is to find the number of different ways you can **completely cover** the board with these tiles.

The answer can be very large, so you must return it **modulo (10⁹ + 7)**.

**Tiles:**

  - **Domino**: Can be placed vertically (`|`, a `2x1` tile) or horizontally (`=`, two `1x2` tiles).
  - **Tromino**: An `L` shape that covers 3 squares. It can be rotated in all 4 orientations.

**Example:**

```python
Input: n = 3
Output: 5
Explanation: The 5 ways to tile a 2x3 board are:
```

## Deep Dive: What is Dynamic Programming (DP)? 🧠

**Dynamic Programming (DP)** is a powerful technique for solving complex problems by breaking them down into simpler, **overlapping subproblems**.

Think of it as building a solution from the ground up, like constructing a tall tower. To build the 10th floor, you first need to have built the 9th floor. To build the 9th, you need the 8th, and so on.

DP relies on two main properties:

1.  **Overlapping Subproblems**: The problem can be broken down into smaller, similar problems that are solved over and over again. For example, to find the number of ways to tile a `2x5` board, you'll need the answer for a `2x4` board and a `2x3` board. To find the answer for a `2x4` board, you'll *also* need the answer for a `2x3` board. This `2x3` problem is an "overlapping subproblem."
2.  **Optimal Substructure**: The optimal solution (or in this case, the total count) for the main problem can be constructed from the solutions of its subproblems.

Instead of re-calculating the answer for the `2x3` board every time, a DP solution **stores the answer** (in a table or array) the first time it's solved. The next time it's needed, we just look up the saved answer. This process is called "memoization" or "tabulation" and is what makes DP so efficient.

For this problem, we will find a formula (a **recurrence relation**) that connects the solution for `n` to the solutions for smaller boards.

## Key Insights

### 1\. The Recurrence Relation (The Hard Part)

This is the most complex part of the problem. If we just try to find `f(n)` (the number of ways to *fully* tile a `2 x n` board), we run into a problem.

  - We can add a `|` (vertical domino) to a full `2 x (n-1)` board. This gives `f(n-1)` ways.
  - We can add an `=` (two horizontal dominos) to a full `2 x (n-2)` board. This gives `f(n-2)` ways.
  - But when we add a tromino, it leaves the board in a *partially complete* state (e.g., with one corner missing).

This tells us our simple DP state `f(n)` is not enough. We also need to track `p(n)`, the number of ways to tile a `2 x n` board with one corner missing.
This leads to a complex system of two equations:

1.  `f(n) = f(n-1) + f(n-2) + 2*p(n-1)`
2.  `p(n) = f(n-2) + p(n-1)`

### 2\. The "Aha\!" Moment: A Simpler Recurrence

While the system above is correct, through algebraic substitution, a much simpler, magical recurrence relation can be found:

**`f(n) = 2 * f(n-1) + f(n-3)`**

This single relation beautifully accounts for all possible tiling combinations, including the complex tromino ones. This is the key insight for an elegant solution.

Let's check this formula with the base cases:

  - `f(0) = 1` (There is 1 way to tile a 2x0 board: do nothing).
  - `f(1) = 1` (1 way: `|`).
  - `f(2) = 2` (2 ways: `||` and `=`).
  - `f(3) = 2 * f(2) + f(0) = 2 * 2 + 1 = 5`. This matches the example\!
  - `f(4) = 2 * f(3) + f(1) = 2 * 5 + 1 = 11`.

This formula is correct, and we can build our solution on it.

### 3\. Space Optimization (From `O(n)` to `O(1)`)

We could use an array `dp = [0] * (n+1)` to store all the values from `f(0)` to `f(n)`. This would work, but it takes `O(n)` space.

If you look at the formula `f(n) = 2 * f(n-1) + f(n-3)`, you'll see that to calculate the value for `n`, we only need the values for `n-1` and `n-3`. We can optimize this by only keeping track of the last three values, which gives us an incredibly efficient **`O(1)` space complexity**.

## Solution Approach

This solution implements the space-optimized, bottom-up DP. It handles the first few base cases and then iterates from 3 up to `n`, using three variables to store the values for `f(i-1)`, `f(i-2)`, and `f(i-3)`.

```python
from typing import List

class Solution:
    def numTilings(self, n: int) -> int:
        
        # Our recurrence relation is: f(n) = 2 * f(n-1) + f(n-3)
        MOD = 10**9 + 7
        
        # Step 1: Handle the base cases that don't fit the loop.
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        # Step 2: Initialize our 3 variables.
        # At the start of the loop (when i=3), we need:
        dp_minus_3 = 1  # This represents f(0) = 1
        dp_minus_2 = 1  # This represents f(1) = 1
        dp_minus_1 = 2  # This represents f(2) = 2
        
        # Step 3: Loop from 3 up to n (inclusive).
        for i in range(3, n + 1):
            
            # Step 3a: Calculate the current DP value using the recurrence relation.
            # We use % MOD at each step to prevent integer overflow.
            dp_current = (2 * dp_minus_1 + dp_minus_3) % MOD
            
            # Step 3b: "Slide" the variables forward for the next iteration.
            # The one that was (i-2) now becomes (i-3).
            dp_minus_3 = dp_minus_2
            # The one that was (i-1) now becomes (i-2).
            dp_minus_2 = dp_minus_1
            # The one we just calculated (i) now becomes (i-1).
            dp_minus_1 = dp_current
            
        # Step 4: After the loop finishes, dp_minus_1 holds f(n).
        return dp_minus_1
```

## Detailed Code Analysis

### Step 1: Base Cases

```python
MOD = 10**9 + 7
if n == 1:
    return 1
if n == 2:
    return 2
```

  - `MOD = 10**9 + 7`: We define the modulo constant as required by the problem.
  - Our main loop starts at `i = 3` because the recurrence `f(n) = 2*f(n-1) + f(n-3)` depends on `f(0)`.
  - Therefore, we must manually handle `n=1` and `n=2` as special base cases.

### Step 2: Initialization for the Loop

```python
dp_minus_3 = 1  # f(0)
dp_minus_2 = 1  # f(1)
dp_minus_1 = 2  # f(2)
```

  - To prepare for the *first* iteration of our loop (where `i=3`), we need to "seed" our variables with the correct values.
  - When `i=3`:
      - We need `f(i-1)`, which is `f(2)`. So, `dp_minus_1 = 2`.
      - We need `f(i-3)`, which is `f(0)`. So, `dp_minus_3 = 1`.
      - We also store `f(1)` in `dp_minus_2` so it can be "shifted" forward in the next step.

### Step 3: The DP Loop

```python
for i in range(3, n + 1):
    dp_current = (2 * dp_minus_1 + dp_minus_3) % MOD
    dp_minus_3 = dp_minus_2
    dp_minus_2 = dp_minus_1
    dp_minus_1 = dp_current
```

  - **`for i in range(3, n + 1):`**: This loop calculates the answer for all boards from size 3 up to size `n`.
  - **`dp_current = (2 * dp_minus_1 + dp_minus_3) % MOD`**: This is the literal implementation of our recurrence relation: `f(i) = (2 * f(i-1) + f(i-3)) % MOD`.
  - **The "Slide"**:
      - `dp_minus_3 = dp_minus_2`: The old `f(i-2)` becomes the new `f(i-3)`.
      - `dp_minus_2 = dp_minus_1`: The old `f(i-1)` becomes the new `f(i-2)`.
      - `dp_minus_1 = dp_current`: The new `f(i)` becomes the new `f(i-1)` for the *next* loop.
  - This sliding-variable technique brilliantly maintains the only three pieces of information we need, achieving `O(1)` space.

### Step 4: The Final Return

```python
return dp_minus_1
```

  - When the loop finishes, `dp_minus_1` holds the value for `f(n)`, which is our final answer.

## Step-by-Step Execution Trace

Let's trace the algorithm for `n = 4` with extreme detail.

### **Initial State:**

  - `n = 4`. The `n=1` and `n=2` checks fail.
  - `MOD = 1000000007`
  - `dp_minus_3 = 1` (represents `f(0)`)
  - `dp_minus_2 = 1` (represents `f(1)`)
  - `dp_minus_1 = 2` (represents `f(2)`)

### **Loop starts: `i` from 3 to 4**

-----

**Loop 1: `i = 3` (Calculating `f(3)`)**

1.  **Calculate `dp_current`**:
      - `dp_current = (2 * dp_minus_1 + dp_minus_3) % MOD`
      - `dp_current = (2 * 2 + 1) % MOD`
      - `dp_current = 5 % MOD` -\> `dp_current = 5`
2.  **Slide Variables**:
      - `dp_minus_3 = dp_minus_2` -\> `dp_minus_3 = 1`
      - `dp_minus_2 = dp_minus_1` -\> `dp_minus_2 = 2`
      - `dp_minus_1 = dp_current` -\> `dp_minus_1 = 5`
        **State after loop 1**: `dp_minus_3 = 1`, `dp_minus_2 = 2`, `dp_minus_1 = 5` (These now represent `f(1)`, `f(2)`, and `f(3)`)

-----

**Loop 2: `i = 4` (Calculating `f(4)`)**

1.  **Calculate `dp_current`**:
      - `dp_current = (2 * dp_minus_1 + dp_minus_3) % MOD`
      - `dp_current = (2 * 5 + 1) % MOD`
      - `dp_current = 11 % MOD` -\> `dp_current = 11`
2.  **Slide Variables**:
      - `dp_minus_3 = dp_minus_2` -\> `dp_minus_3 = 2`
      - `dp_minus_2 = dp_minus_1` -\> `dp_minus_2 = 5`
      - `dp_minus_1 = dp_current` -\> `dp_minus_1 = 11`
        **State after loop 2**: `dp_minus_3 = 2`, `dp_minus_2 = 5`, `dp_minus_1 = 11` (These now represent `f(2)`, `f(3)`, and `f(4)`)

-----

### **End of Algorithm**

  - The `for` loop finishes (it has completed `i=3` and `i=4`).
  - The function returns the final value of `dp_minus_1`, which is **11**.

## Performance Analysis

### Time Complexity: O(n)

  - The algorithm is dominated by the single `for` loop that runs from 3 to `n`. All operations inside the loop are constant time.

### Space Complexity: O(1)

  - This is the most beautiful part of this solution. We only use a few fixed variables (`dp_minus_1`, `dp_minus_2`, `dp_minus_3`, `dp_current`) to store our state. The memory usage does not grow as `n` grows, so it is constant space.