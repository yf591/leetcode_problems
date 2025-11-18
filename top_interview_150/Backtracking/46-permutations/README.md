# 46\. Permutations - Solution Explanation

## Problem Overview

You are given an array `nums` of **distinct** integers. The task is to find all possible **permutations** (rearrangements) of these numbers. You can return the answer in any order.

**Key Definitions:**

  - **Permutation**: An arrangement of items where the **order matters**.
  - **Combination**: A selection of items where order **does not matter**.

**Examples:**

```python
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
# [1,2,3] is different from [1,3,2].

Input: nums = [0,1]
Output: [[0,1],[1,0]]
```

]

## Deep Dive: What is Backtracking? 🧠

**Backtracking** is an algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time. It's all about **exploring choices** and then "undoing" them if they don't lead to a solution.

Think of it as navigating a maze or a "decision tree" in search of all possible "treasures" (valid solutions).

1.  **Start**: You are at the entrance.
2.  **Decision Point**: You reach a junction with multiple paths (e.g., "Should I add 1?", "Should I add 2?").
3.  **Choose**: You pick one path to explore (e.g., "I'll **add 1** to my combination").
4.  **Explore**: You move forward down that path. This takes you to the *next* decision point (this is the **recursive call**).
5.  **Hit a Dead End / Found Solution**: You keep exploring until:
      - You find a "treasure" (a valid solution, like our list reaching size `k`). You record it.
      - You hit a "dead end" (an invalid path, e.g., our list is already size `k+1`).
6.  **Unchoose (Backtrack)**: This is the most important step. You **go back** to the previous junction. To do this, you *undo* your choice (e.g., "I'll **remove 1** from my combination").
7.  **Choose Again**: You are now back at the previous junction and can explore the *next* available path (e.g., "This time, I'll **add 2** to my combination").

This "Choose, Explore, Unchoose" pattern is the heart of every backtracking algorithm.

## Key Insights for This Problem

### 1\. This is Not "Combinations"

In the "Combinations" problem (like LC 77), `[1, 2]` was the same as `[2, 1]`. To solve that, we enforced an increasing order (e.g., after picking `1`, we could only pick `2` or `3`).

In this problem, `[1, 2, 3]` and `[1, 3, 2]` are **different** solutions. This means our "choice" at each step is different. At any point in building our permutation, we can choose *any* number from the original list, as long as it hasn't been used in the *current* permutation we're building.

### 2\. The Backtracking "State"

This leads us to the classic **backtracking** approach. To implement this, our recursive function needs to know:

1.  **What path am I currently building?** (e.g., `[1, 2]`)
2.  **What numbers have I already used in this path?** (e.g., `{1, 2}`)

A **`set`** is the perfect tool for tracking the "used" numbers because it gives us an `O(1)` (constant time) lookup to check if a number has been used.

### 3\. The "Choose, Explore, Unchoose" Pattern

Our recursive function will do the following:

  - **Goal**: If our current path's length equals the original array's length, we've built a full permutation. We add it to our list of solutions.
  - **Choices**: We iterate through *every number* in the original `nums` array.
  - **Constraint**: We can only "choose" a number if it's **not** in our `visited` set.
  - **Process**:
    1.  **Choose**: Pick an unused number. Add it to the `current_path` and the `visited_set`.
    2.  **Explore**: Make a recursive call to continue building the *next* level of the path.
    3.  **Unchoose (Backtrack)**: When the recursive call returns (meaning it has finished exploring that entire branch), we *undo* our choice. We remove the number from `current_path` and `visited_set`. This allows the `for` loop to continue to the next number, trying a different path.

## Solution Approach

This solution implements the backtracking algorithm. It uses a recursive helper function `backtrack` that maintains the `current_path` and a `visited_set` to build all possible permutations.

```python
from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        
        # This list will store our final list of all permutation lists.
        results = []
        n = len(nums)
        
        def backtrack(current_path: List[int], visited_set: set):
            
            # --- Base Case: Success ---
            # If the current permutation is the same size as the input,
            # we have a complete and valid permutation.
            if len(current_path) == n:
                # We must append a *copy* of the current path.
                # If we append 'current_path' itself, the 'pop' operations
                # later will empty it.
                results.append(list(current_path))
                return # Stop this path and backtrack.

            # --- Recursive Step: Explore all choices ---
            
            # Iterate through *every* number in the original 'nums' array.
            for num in nums:
                
                # Check our constraint: Have we already used this number
                # in the permutation we are currently building?
                if num not in visited_set:
                    
                    # 1. Choose: Add the number to our path and mark it as visited.
                    current_path.append(num)
                    visited_set.add(num)
                    
                    # 2. Explore: Make a recursive call to build the next
                    #    level of the permutation.
                    backtrack(current_path, visited_set)
                    
                    # 3. Unchoose (Backtrack): This code runs AFTER the recursive
                    #    call above has fully returned (i.e., that entire branch
                    #    has been explored). We undo our choice.
                    visited_set.remove(num)
                    current_path.pop()

        # Start the backtracking process.
        # We start with an empty path and an empty visited set.
        backtrack([], set())
        
        return results
```

## Detailed Code Analysis

### Step 1: Initialization

```python
results = []
n = len(nums)
```

  - `results`: An empty list to store all the complete permutations we find.
  - `n`: Storing the length of `nums` is a small optimization to avoid calling `len()` repeatedly.

### Step 2: The `backtrack` Helper Function

We define a nested function `backtrack` that will do the recursive work.

  - `current_path`: The list representing the permutation being built (e.g., `[1, 3]`).
  - `visited_set`: A set containing the numbers in `current_path` for `O(1)` lookup (e.g., `{1, 3}`).

### Step 3: Base Case (The "Goal")

```python
if len(current_path) == n:
    results.append(list(current_path))
    return
```

  - This is our stopping condition. If our `current_path` has `n` elements, it's a complete permutation.
  - `results.append(list(current_path))`: We add a **copy** of the path to our results. This is critical.
  - `return`: We stop this recursive branch.

### Step 4: The Recursive "Choose, Explore, Unchoose" Loop

```python
for num in nums:
    if num not in visited_set:
        
        # 1. CHOOSE
        current_path.append(num)
        visited_set.add(num)
        
        # 2. EXPLORE
        backtrack(current_path, visited_set)
        
        # 3. UNCHOOSE (Backtrack)
        visited_set.remove(num)
        current_path.pop()
```

  - **`for num in nums:`**: This is the key difference from "Combinations." We *always* loop through the *entire original `nums` array* to see what choices are available.
  - **`if num not in visited_set:`**: This is our constraint check. We only proceed if the number isn't already in the path we are building.
  - **`current_path.append(num)` / `visited_set.add(num)`**: The **"Choose"** step. We commit to this choice.
  - **`backtrack(current_path, visited_set)`**: The **"Explore"** step. We dive deeper, trying to find the *next* number for our permutation.
  - **`visited_set.remove(num)` / `current_path.pop()`**: The **"Unchoose"** step. This code runs *after* the recursive call has returned. It undoes the choice, freeing up `num` so it can be used in a different position in a future path (e.g., `[2, 1, 3]` after `[1, 2, 3]` is finished).

## Step-by-Step Execution Trace

Let's trace `nums = [1, 2]` with extreme detail.

1.  **Initial Call**: `backtrack(current_path=[], visited_set={})`

      - `len` is 0, not 2.
      - `for num in [1, 2]`:
      - **`num = 1`**:
          - `1 not in {}`? True.
          - **Choose**: `current_path = [1]`, `visited_set = {1}`.
          - **Explore**: Call `backtrack(current_path=[1], visited_set={1})`.
              - `len` is 1, not 2.
              - `for num in [1, 2]`:
              - **`num = 1`**:
                  - `1 not in {1}`? False. Skip.
              - **`num = 2`**:
                  - `2 not in {1}`? True.
                  - **Choose**: `current_path = [1, 2]`, `visited_set = {1, 2}`.
                  - **Explore**: Call `backtrack(current_path=[1, 2], visited_set={1, 2})`.
                      - `len` is 2. Base Case Hit\!
                      - `results.append(list([1, 2]))`. `results` is now `[[1, 2]]`.
                      - Returns.
                  - **Unchoose**: `visited_set.remove(2)`, `current_path.pop()`.
                  - `current_path = [1]`, `visited_set = {1}`.
              - Loop finishes. `backtrack([1], {1})` returns.
          - **Unchoose**: `visited_set.remove(1)`, `current_path.pop()`.
          - `current_path = []`, `visited_set = {}`.
      - **`num = 2`**:
          - `2 not in {}`? True.
          - **Choose**: `current_path = [2]`, `visited_set = {2}`.
          - **Explore**: Call `backtrack(current_path=[2], visited_set={2})`.
              - `len` is 1, not 2.
              - `for num in [1, 2]`:
              - **`num = 1`**:
                  - `1 not in {2}`? True.
                  - **Choose**: `current_path = [2, 1]`, `visited_set = {2, 1}`.
                  - **Explore**: Call `backtrack(current_path=[2, 1], visited_set={2, 1})`.
                      - `len` is 2. Base Case Hit\!
                      - `results.append(list([2, 1]))`. `results` is now `[[1, 2], [2, 1]]`.
                      - Returns.
                  - **Unchoose**: `visited_set.remove(1)`, `current_path.pop()`.
                  - `current_path = [2]`, `visited_set = {2}`.
              - **`num = 2`**:
                  - `2 not in {2}`? False. Skip.
              - Loop finishes. `backtrack([2], {2})` returns.
          - **Unchoose**: `visited_set.remove(2)`, `current_path.pop()`.
          - `current_path = []`, `visited_set = {}`.
      - Loop finishes. `backtrack([], {})` returns.

2.  **Final Result**: The function returns `results`: `[[1, 2], [2, 1]]`.

## Performance Analysis

### Time Complexity: O(n \* n\!)

  - `n!` (n-factorial): There are `n!` possible permutations to generate.
  - `* n`: For each of these permutations, we have to create a copy of the list to add to our `results`, which takes `O(n)` time.
  - This is a very high complexity, but it's unavoidable as we must generate every single permutation. This is why the problem constraint is so small (`n <= 6`).

### Space Complexity: O(n)

  - `current_path` will grow to size `n`.
  - `visited_set` will grow to size `n`.
  - The recursion call stack will also go `n` levels deep.
  - The total auxiliary space is therefore `O(n)`. (This does not count the output list, which is `O(n * n!)`).