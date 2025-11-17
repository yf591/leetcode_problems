# 77\. Combinations - Solution Explanation

## Problem Overview

You are given two integers, `n` and `k`. The task is to find all possible **combinations** of `k` numbers chosen from the range `[1, n]`.

**Key Definitions & Rules:**

  - **Combination**: A selection of items where the order **does not matter**. This is the key constraint. The combination `[1, 2]` is considered the *same* as `[2, 1]`.
  - **Output**: A list of lists, where each inner list is a unique combination.

**Examples:**

```python
Input: n = 4, k = 2
Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]

Input: n = 1, k = 1
Output: [[1]]
```

## Deep Dive: What is Backtracking? 🧠

**Backtracking** is an algorithmic technique for solving problems recursively by trying to build a solution step-by-step. It's all about **exploring choices** and then "undoing" them if they don't lead to a solution.

Think of it as navigating a maze or a "decision tree" in search of all possible "treasures" (valid solutions).

1.  **Start**: You are at the entrance.
2.  **Decision Point**: You reach a junction with multiple paths (e.g., "Should I add 1?", "Should I add 2?").
3.  **Choose**: You pick one path to explore (e.g., "I'll **add 1** to my combination").
4.  **Explore**: You move forward down that path. This takes you to the *next* decision point (this is the **recursive call**).
5.  **Hit a Dead End / Found Solution**: You keep exploring until:
      - You find a "treasure" (a valid solution, like our list reaching size `k`). You record it.
      - You hit a "dead end" (an invalid path, e.g., our list is already size `k+1`).
6.  **Unchoose (Backtrack)**: This is the most important step. You **go back** to the previous junction. To do this, you *undo* the choice you made (e.g., "I'll **remove 1** from my combination").
7.  **Choose Again**: You are now back at the previous junction and can explore the *next* available path (e.g., "This time, I'll **add 2** to my combination").

This "Choose, Explore, Unchoose" pattern is the heart of every backtracking algorithm.

## Key Insights for This Problem

### 1\. The "Duplicate Combination" Problem

The problem states that `[1, 2]` and `[2, 1]` are the same. If we just explore all possibilities, we'll generate many duplicates. How do we prevent this?

### 2\. The "Enforced Order" Solution

The key insight is to **enforce an order** on the combinations we build. We can decide that all our combinations *must* be in **increasing order**.

  - If we generate `[1, 2]`, we will never even *try* to generate `[2, 1]`.
  - If we pick `3`, the next number we are allowed to pick must be `4` or greater.

How do we enforce this? We pass a `start_num` parameter in our recursive function. This tells the function, "You are only allowed to choose numbers starting from this one."

  - `backtrack(1, [])` -\> can choose `1, 2, 3, 4`
  - It chooses `1`. It then calls `backtrack(2, [1])`.
  - `backtrack(2, [1])` -\> can *only* choose `2, 3, 4`. It can't choose `1` again.
  - It chooses `2`. `[1, 2]` is a solution.
  - It backtracks, then chooses `3`. `[1, 3]` is a solution.

## Solution Approach

This solution implements the backtracking algorithm. It uses a recursive helper function `backtrack` that builds a `current_path` (a potential combination). The `start_num` parameter is used to enforce the increasing order, which cleverly avoids duplicate combinations.

```python
from typing import List

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        
        # This list will store our final list of all valid combinations.
        results = []

        def backtrack(start_num: int, current_path: List[int]):
            """
            A recursive helper to find combinations.
            :param start_num: The number to start our loop from (to avoid duplicates).
            :param current_path: The list of numbers chosen so far.
            """
            
            # --- Base Case: Success ---
            # If our current combination has reached the target size k...
            if len(current_path) == k:
                # ...we have found a valid solution.
                # We must append a *copy* of the current path.
                results.append(list(current_path))
                # Stop exploring this path and backtrack.
                return

            # --- Recursive Step: Explore all valid choices ---
            
            # We iterate from our 'start_num' up to 'n' (inclusive).
            for num in range(start_num, n + 1):
                
                # 1. Choose: Add the current number to our path.
                current_path.append(num)
                
                # 2. Explore: Recursively call the function for the next
                #    number. The next starting number will be 'num + 1'.
                backtrack(num + 1, current_path)
                
                # 3. Unchoose (Backtrack): Remove the number we just added.
                #    This is the "backtracking" step. It allows the 'for' loop
                #    to continue with the next number.
                current_path.pop()

        # Kick off the entire backtracking process.
        # We can start with any number from 1, and our initial path is empty.
        backtrack(1, [])
        
        return results
```

## Detailed Code Analysis

### Step 1: Initialization

```python
results = []
```

  - We create an empty list, `results`, which will store all the valid combination lists that we find.

### Step 2: The `backtrack` Helper Function

We define a nested function `backtrack` that will contain our core recursive logic. It needs to know:

  - `start_num`: The smallest number it's allowed to pick in its `for` loop. This is the key to enforcing order and preventing duplicate combinations.
  - `current_path`: The list representing the single combination we are currently building.

### Step 3: Base Case (The "Goal")

```python
if len(current_path) == k:
    results.append(list(current_path))
    return
```

  - This is our stopping condition. We check if the `current_path` has reached the desired length `k`.
  - If it has, we've found a valid solution.
  - **`results.append(list(current_path))`**: This is a **critical** line. We append a **copy** of `current_path`. If we just appended `current_path` itself, all subsequent `pop()` operations would empty it, and our `results` list would end up full of empty lists.
  - `return`: We stop this branch of the recursion. There's no need to add more numbers if we're already at size `k`.

### Step 4: The Recursive "Choose, Explore, Unchoose" Loop

```python
for num in range(start_num, n + 1):
    
    # 1. CHOOSE
    current_path.append(num)
    
    # 2. EXPLORE
    backtrack(num + 1, current_path)
    
    # 3. UNCHOOSE (Backtrack)
    current_path.pop()
```

  - This is the main engine of the algorithm. It tries every possible valid choice.
  - **`for num in range(start_num, n + 1):`**: We loop through all numbers we are allowed to pick. We start from `start_num` (which we got from the previous call) and go up to `n` (which is `n + 1` in a `range` function).
  - **`current_path.append(num)`**: This is the **"Choose"** step. We make a decision and add the number to our path.
  - **`backtrack(num + 1, current_path)`**: This is the **"Explore"** step. We make a recursive call to explore all consequences of our choice. We pass `num + 1` as the *new* `start_num` to ensure the next number chosen is strictly greater than the one we just added.
  - **`current_path.pop()`**: This is the **"Unchoose"** or "Backtrack" step. This line only runs *after* the recursive call `backtrack(num + 1, ...)` has fully completed (i.e., it has explored the entire tree branch starting with `num` and has returned). We undo our choice by removing `num` from the path. This brings us back to the state we were in before, allowing the `for` loop to continue with its next number.

## Step-by-Step Execution Trace

Let's trace `n = 4, k = 2` with extreme detail.

1.  **Initial Call**: `backtrack(start_num=1, current_path=[])`

      - `len` is 0, not `k`.
      - `for` loop runs `num` in `range(1, 5)` -\> `[1, 2, 3, 4]`.
      - **`num = 1`**:
          - **Choose**: `current_path.append(1)`. `path` is `[1]`.
          - **Explore**: Call `backtrack(start_num=2, current_path=[1])`.
              - `len` is 1, not `k`.
              - `for` loop runs `num` in `range(2, 5)` -\> `[2, 3, 4]`.
              - **`num = 2`**:
                  - **Choose**: `current_path.append(2)`. `path` is `[1, 2]`.
                  - **Explore**: Call `backtrack(start_num=3, current_path=[1, 2])`.
                      - `len` is 2, which is `k`. Base case hit\!
                      - `results.append(list([1, 2]))`. `results` is `[[1, 2]]`.
                      - Returns.
                  - **Unchoose**: `current_path.pop()`. `path` is `[1]`.
              - **`num = 3`**:
                  - **Choose**: `current_path.append(3)`. `path` is `[1, 3]`.
                  - **Explore**: Call `backtrack(start_num=4, current_path=[1, 3])`.
                      - `len` is 2, which is `k`. Base case hit\!
                      - `results.append(list([1, 3]))`. `results` is `[[1, 2], [1, 3]]`.
                      - Returns.
                  - **Unchoose**: `current_path.pop()`. `path` is `[1]`.
              - **`num = 4`**:
                  - **Choose**: `current_path.append(4)`. `path` is `[1, 4]`.
                  - **Explore**: Call `backtrack(start_num=5, current_path=[1, 4])`.
                      - `len` is 2, which is `k`. Base case hit\!
                      - `results.append(list([1, 4]))`. `results` is `[[1, 2], [1, 3], [1, 4]]`.
                      - Returns.
                  - **Unchoose**: `current_path.pop()`. `path` is `[1]`.
              - Loop finishes. `backtrack(2, [1])` returns.
          - **Unchoose**: `current_path.pop()`. `path` is `[]`.
      - **`num = 2`**:
          - **Choose**: `current_path.append(2)`. `path` is `[2]`.
          - **Explore**: Call `backtrack(start_num=3, current_path=[2])`.
              - ... (This will find `[2, 3]` and `[2, 4]`) ...
          - **Unchoose**: `current_path.pop()`. `path` is `[]`.
      - **`num = 3`**:
          - **Choose**: `current_path.append(3)`. `path` is `[3]`.
          - **Explore**: Call `backtrack(start_num=4, current_path=[3])`.
              - ... (This will find `[3, 4]`) ...
          - **Unchoose**: `current_path.pop()`. `path` is `[]`.
      - **`num = 4`**:
          - **Choose**: `current_path.append(4)`. `path` is `[4]`.
          - **Explore**: Call `backtrack(start_num=5, current_path=[4])`.
              - `len` is 1, not `k`.
              - `for` loop runs `num` in `range(5, 5)`. Loop is empty.
              - `backtrack(5, [4])` returns.
          - **Unchoose**: `current_path.pop()`. `path` is `[]`.
      - Loop finishes. `backtrack(1, [])` returns.

2.  **Final Result**: The function returns `results`: `[[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]`.

## Performance Analysis

### Time Complexity: O(k \* C(n, k))

  - Where `C(n, k)` is "n choose k", which is the number of combinations.
  - The algorithm's main job is to find all `C(n, k)` valid combinations.
  - For each combination it finds, it spends `O(k)` time to create a *copy* of the list to append to the `results`.
  - Thus, the total time is proportional to the number of combinations multiplied by the time to copy each one.

### Space Complexity: O(k)

  - The space is dominated by the recursion call stack and the `current_path` list.
  - The recursion will go at most `k` levels deep (as we stop when the path length reaches `k`).
  - `current_path` also stores at most `k` elements.
  - (This analysis does not count the space required for the `results` output list, which would be `O(k * C(n, k))`).