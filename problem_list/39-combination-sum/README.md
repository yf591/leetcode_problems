# 39\. Combination Sum - Solution Explanation

## Problem Overview

You are given an array of **distinct** integers `candidates` and a target integer `target`. The task is to return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`.

**Key Rules:**

1.  **Unlimited Use**: The same number may be chosen from `candidates` an **unlimited number of times**.
2.  **Unique Combinations**: The order of numbers does not matter. `[2, 2, 3]` is the same combination as `[3, 2, 2]`. You should not return duplicates.

**Example:**

```python
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
- 2 and 3 are candidates, and 2 + 2 + 3 = 7. (2 is used twice).
- 7 is a candidate, and 7 = 7.
```

## Deep Dive: What is Backtracking? 🧠

**Backtracking** is a general algorithm for finding all (or some) solutions to some computational problems, notably constraint satisfaction problems, that incrementally builds candidates to the solutions.

Think of it as exploring a **Decision Tree**.

1.  **Root**: You start with an empty basket (sum = 0).
2.  **Branches**: From your current state, you have several choices (pick number `2`, pick number `3`, etc.).
3.  **Leaves**: You follow a branch until:
      * **Success**: The sum equals `target`. You save this path.
      * **Failure**: The sum exceeds `target`. You stop.
4.  **The "Backtrack"**: When you hit a leaf (success or failure), you go back up the tree to the previous decision point and try a *different* branch.

### The Specific "Twist" for this Problem

Standard backtracking usually moves forward (e.g., picking index `0`, then index `1`, then index `2`).

  * **Standard Combinations**: Once you pick index `i`, you recurse on `i + 1` (can't reuse).
  * **Combination Sum (This Problem)**: Once you pick index `i`, you recurse on **`i`** (can reuse).

However, to prevent duplicate combinations (like `[2, 3]` and `[3, 2]`), we enforce a rule: **We can never look back.** If we are currently considering the number at index `i`, we can pick `i` again, or move to `i + 1`, but we can never pick `i - 1`. This enforces a sorted order (e.g., `2, 2, 3` is valid, but `3, 2, 2` is impossible to generate).

## Solution Approach

This solution uses a recursive backtracking function. It sorts the candidates first to allow for optimization (pruning). It iterates through the candidates, allowing the recursive step to stay at the same index to support unlimited usage.

```python
from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        
        results = []
        
        # Step 1: Sort the candidates.
        # This is not strictly necessary for logic, but it allows for a huge optimization:
        # we can stop the loop early if the sum exceeds the target.
        candidates.sort()
        
        def backtrack(start_index: int, current_sum: int, current_path: List[int]):
            
            # --- Base Case 1: Success ---
            # If the sum equals the target, we found a valid combination.
            if current_sum == target:
                # We append a COPY (list(...)) of the path.
                results.append(list(current_path))
                return
            
            # --- Base Case 2: Failure (Pruning) ---
            # If the sum exceeds the target, this path is a dead end.
            if current_sum > target:
                return

            # --- Recursive Step: Explore Choices ---
            # Iterate starting from 'start_index'. This prevents looking backwards
            # and generating duplicate sets like [2,3] and [3,2].
            for i in range(start_index, len(candidates)):
                num = candidates[i]
                
                # Optimization (Pruning):
                # Since the array is sorted, if the current number makes the sum
                # exceed the target, ALL subsequent numbers will also exceed it.
                # We can break the loop immediately.
                if current_sum + num > target:
                    break
                
                # 1. Choose: Add number to path
                current_path.append(num)
                
                # 2. Explore: Recurse
                # CRITICAL: We pass 'i' as the start_index, NOT 'i + 1'.
                # This tells the next level "You can use this same number again".
                backtrack(i, current_sum + num, current_path)
                
                # 3. Unchoose (Backtrack): Remove number to try next option
                current_path.pop()

        # Start the recursion from the first index (0), sum 0, and empty path.
        backtrack(0, 0, [])
        
        return results
```

## Detailed Code Analysis

### Step 1: Sorting

```python
candidates.sort()
```

  - Sorting helps us "prune" the decision tree. If we are trying to reach 7 and we have `[2, 3, 6, 7]`, and `current_sum` is 6:
      - Try 2: `6+2=8` (Too big).
      - Because the list is sorted, we know 3, 6, and 7 will *also* be too big. We don't even need to check them.

### Step 2: The `backtrack` Function

```python
def backtrack(start_index: int, current_sum: int, current_path: List[int]):
```

  - `start_index`: The index in `candidates` we are allowed to start picking from. This ensures we only pick numbers from left to right (e.g., `2, 2, 3`), never right to left (`3, 2`), preventing duplicates.

### Step 3: The Recursion

```python
backtrack(i, current_sum + num, current_path)
```

  - **This is the most important line.**
  - In standard combination problems (items unique), we would pass `i + 1`.
  - Here, we pass `i`. This effectively says: "I just picked `candidates[i]`. For the next step, you are allowed to pick `candidates[i]` again if you want."
  - The loop `range(start_index, ...)` handles the progression. If the recursion decides *not* to use `i` again, it returns, the loop increments to `i+1`, and we move to the next number.

## Step-by-Step Execution Trace

Let's trace `candidates = [2, 3, 5]`, `target = 5`.

1.  **`backtrack(0, 0, [])`** (Can use 2, 3, 5)
      - **Loop `i=0` (Val 2)**:
          - Choose 2. `path=[2]`, `sum=2`.
          - **Recurse `backtrack(0, 2, [2])`** (Can use 2, 3, 5)
              - **Loop `i=0` (Val 2)**:
                  - Choose 2. `path=[2, 2]`, `sum=4`.
                  - **Recurse `backtrack(0, 4, [2, 2])`**
                      - **Loop `i=0` (Val 2)**: `4+2=6 > 5`. Break (Pruning).
                      - **Loop `i=1` (Val 3)**: `4+3=7 > 5`. Break.
                  - Backtrack: `path=[2]`.
              - **Loop `i=1` (Val 3)**:
                  - Choose 3. `path=[2, 3]`, `sum=5`.
                  - **Recurse `backtrack(1, 5, [2, 3])`**
                      - **Base Case**: `sum == 5`. **Add `[2, 3]` to results**. Return.
                  - Backtrack: `path=[2]`.
              - **Loop `i=2` (Val 5)**: `2+5=7 > 5`. Break.
          - Backtrack: `path=[]`.
      - **Loop `i=1` (Val 3)**:
          - Choose 3. `path=[3]`, `sum=3`.
          - **Recurse `backtrack(1, 3, [3])`** (Can use 3, 5)
              - **Loop `i=1` (Val 3)**: `3+3=6 > 5`. Break.
              - **Loop `i=2` (Val 5)**: `3+5=8 > 5`. Break.
          - Backtrack: `path=[]`.
      - **Loop `i=2` (Val 5)**:
          - Choose 5. `path=[5]`, `sum=5`.
          - **Recurse `backtrack(2, 5, [5])`**
              - **Base Case**: `sum == 5`. **Add `[5]` to results**. Return.
          - Backtrack: `path=[]`.

**Final Result**: `[[2, 3], [5]]`

## Performance Analysis

### Time Complexity: $O(N^{\frac{T}{M}})$

  - $N$: Number of candidates.
  - $T$: Target value.
  - $M$: Minimum value in candidates.
  - **Explanation**: The maximum depth of the recursion tree is $T/M$ (e.g., reaching target 10 with only 1s has depth 10). At each step, we branch roughly $N$ times. This is loosely exponential. However, in practice, the sorting and pruning (`current_sum > target`) make it much faster.

### Space Complexity: $O(\frac{T}{M})$

  - This is the space required for the recursion stack. In the worst case (using the smallest number repeatedly), the stack goes $T/M$ levels deep. `current_path` also takes this amount of space.