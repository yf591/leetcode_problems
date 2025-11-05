# 216\. Combination Sum III - Solution Explanation

## Problem Overview

You are given two integers, `k` and `n`. The task is to find all **unique combinations** of `k` numbers that sum up to `n`.

**The Three Constraints:**

1.  You can only use numbers from **1 to 9**.
2.  Each number can be used **at most once** in a single combination.
3.  You must find all unique combinations (e.g., `[1,2,6]` is the same as `[6,2,1]`, so only one should be in the final result).

**Examples:**

```python
Input: k = 3, n = 9
Output: [[1,2,6],[1,3,5],[2,3,4]]
Explanation:
1 + 2 + 6 = 9
1 + 3 + 5 = 9
2 + 3 + 4 = 9

Input: k = 4, n = 1
Output: []
Explanation: The smallest possible sum using 4 unique numbers is 1+2+3+4 = 10, which is > 1.
```

## Deep Dive: What is Backtracking? 🧠

Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time. It's all about **exploring choices**.

Think of it as navigating a maze or a decision tree. You start at the beginning. At each step, you have multiple choices.

1.  **Choose**: You pick one path (or "choice") to explore.
2.  **Explore**: You move forward down that path (this is the recursive call).
3.  **Check for Goal/Dead End**:
      - If you reach a "dead end" (the path is invalid), you stop.
      - If you reach the "exit" (a valid solution), you record it.
4.  **Unchoose (Backtrack)**: This is the most important step. After exploring a path (whether it was a dead end or a solution), you **go back** to the last decision point and *undo* your choice. This allows you to...
5.  **Choose Again**: Pick the *next* available path from that same decision point.

### How it Applies to This Problem:

Let's find `k=3, n=9`. We'll build a combination `path`.

  - **Start**: `path=[]`, `sum=0`. We can choose from `[1-9]`.
  - **Choose `1`**: `path=[1]`, `sum=1`.
      - **Explore**: Now, to avoid duplicates (like `[2,1]`), we only choose numbers *greater than* 1. We can choose from `[2-9]`.
      - **Choose `2`**: `path=[1,2]`, `sum=3`.
          - **Explore**: We can choose from `[3-9]`.
          - **Choose `3`**: `path=[1,2,3]`, `sum=6`.
              - **Explore**: `len(path)` is 3 (which is `k`), but `sum` (6) is not `n` (9). This is a **dead end**.
              - **Unchoose (Backtrack)**: Remove `3`. `path=[1,2]`, `sum=3`.
          - **Choose `4`**: `path=[1,2,4]`, `sum=7`.
              - **Explore**: `len(path)` is 3, `sum` (7) is not 9. Dead end.
              - **Unchoose (Backtrack)**: Remove `4`. `path=[1,2]`, `sum=3`.
          - **Choose `5`**: `path=[1,2,5]`, `sum=8`.
              - **Explore**: `len(path)` is 3, `sum` (8) is not 9. Dead end.
              - **Unchoose (Backtrack)**: Remove `5`. `path=[1,2]`, `sum=3`.
          - **Choose `6`**: `path=[1,2,6]`, `sum=9`.
              - **Explore**: `len(path)` is 3 and `sum` is 9. **This is a solution\!**
              - Record `[1,2,6]`.
              - **Unchoose (Backtrack)**: Remove `6`. `path=[1,2]`, `sum=3`.
          - ...and so on...
      - **Unchoose (Backtrack)**: Remove `2`. `path=[1]`, `sum=1`.
  - **Choose `3`**: `path=[1,3]`, `sum=4`.
      - **Explore**: `backtrack(4, 4, [1,3])`...
  - ...and this continues until all paths are explored.

## Solution Approach

This solution uses a recursive `backtrack` helper function. This function will be responsible for building a potential combination (`current_path`). To prevent duplicate combinations (like `[1,2,4]` and `[4,2,1]`), we enforce an ordering by only allowing our function to pick numbers that are *greater* than the last number it added. We do this by passing a `start_num` parameter.

```python
from typing import List

class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        
        # This list will store all valid combinations we find.
        results = []

        def backtrack(start_num: int, current_sum: int, current_path: List[int]):
            """
            A recursive helper to find combinations.
            :param start_num: The smallest number we are allowed to add next.
            :param current_sum: The sum of numbers in current_path.
            :param current_path: The list of numbers chosen so far.
            """
            
            # --- Base Case 1: Success ---
            # If we have exactly k numbers and they sum up to n.
            if len(current_path) == k:
                if current_sum == n:
                    # We found a valid solution! Add a *copy* of it.
                    results.append(list(current_path))
                # Stop this path: either we succeeded or len=k but sum!=n (dead end).
                return
            
            # --- Base Case 2: Pruning (Failure/Dead End) ---
            # If we already have too many numbers or the sum is already too big,
            # there's no point in exploring this path further.
            if len(current_path) > k or current_sum > n:
                return

            # --- Recursive Step: Explore all choices ---
            # We can choose any number from 'start_num' up to 9.
            for num in range(start_num, 10):
                # 1. Choose: Add the number to our current path.
                current_path.append(num)
                
                # 2. Explore: Recurse for the next step.
                # The next number must be at least 'num + 1' to avoid duplicates.
                backtrack(num + 1, current_sum + num, current_path)
                
                # 3. Unchoose (Backtrack): Remove the number we just added
                #    so we can try the next number in the loop.
                current_path.pop()

        # Start the backtracking process.
        # We can start with any number from 1.
        backtrack(start_num=1, current_sum=0, current_path=[])
        
        return results
```

## Detailed Code Analysis

### Step 1: Initialization

```python
results = []
```

  - We initialize an empty list, `results`, which will store all the valid combination lists that we find.

### Step 2: The `backtrack` Helper Function

We define a nested function `backtrack` that will contain our core recursive logic. It needs to know:

  - `start_num`: The smallest number it's allowed to pick. This is how we enforce order and prevent duplicate combinations.
  - `current_sum`: The sum of the combination we've built so far.
  - `current_path`: The combination (list of numbers) we've built so far.

### Step 3: Base Case (Success)

```python
if len(current_path) == k:
    if current_sum == n:
        results.append(list(current_path))
    return
```

  - This is our primary stopping condition. We first check if we have picked exactly `k` numbers.
  - If we have, we then check if their sum (`current_sum`) equals our target `n`.
  - If both are true, we've found a solution\! `results.append(list(current_path))` adds a **copy** of the path to our results. We must add a copy, or `current_path` will be emptied by the `pop()` operations later.
  - We `return` to stop this recursive branch.

### Step 4: Base Case (Pruning / Failure)

```python
if len(current_path) > k or current_sum > n:
    return
```

  - This is a critical optimization. If our path is already too long (`> k`) or our sum is already too big (`> n`), there is no possibility that this path will *ever* become a valid solution. We "prune" this branch of the search tree by returning immediately, saving a huge amount of unnecessary computation.

### Step 5: The Recursive "Choose, Explore, Unchoose" Loop

```python
for num in range(start_num, 10):
    # 1. Choose
    current_path.append(num)
    
    # 2. Explore
    backtrack(num + 1, current_sum + num, current_path)
    
    # 3. Unchoose (Backtrack)
    current_path.pop()
```

  - This is the main engine of the algorithm. It tries every possible valid choice.
  - `for num in range(start_num, 10)`: We loop through all numbers we are allowed to pick. We start from `start_num` and go up to 9.
  - **`current_path.append(num)`**: This is the **"Choose"** step. We make a decision and add the number to our path.
  - **`backtrack(num + 1, ...)`**: This is the **"Explore"** step. We make a recursive call to explore all consequences of our choice.
      - `num + 1`: This is how we enforce uniqueness and order. We tell the next call that it can only pick numbers *greater* than the one we just added.
      - `current_sum + num`: We pass the updated sum down.
  - **`current_path.pop()`**: This is the **"Unchoose" (Backtrack)** step. After the recursive call `backtrack(num + 1, ...)` has fully completed (meaning it has explored the entire tree branch starting with `num`), we *undo* our choice by removing `num` from the path. This brings us back to the state we were in before, allowing the `for` loop to continue with the next number (e.g., to try `5` after trying `4`).

## Performance Analysis

### Time Complexity: O(k \* C(9, k))

  - Where `C(9, k)` is "9 choose k," the number of combinations of `k` items from a set of 9.
  - The algorithm will explore all possible valid combinations of `k` numbers from 9.
  - For each valid combination found, we spend `O(k)` time to create a copy of the list to add to our results.

### Space Complexity: O(k)

  - The space complexity is determined by the depth of the recursion call stack.
  - The recursion will go at most `k` levels deep (as we stop when `len(current_path) == k`).
  - Therefore, the space used by the call stack (and the `current_path` list) is proportional to `k`.