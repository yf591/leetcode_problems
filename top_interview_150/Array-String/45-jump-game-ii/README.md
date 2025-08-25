# 45\. Jump Game II - Solution Explanation

## Problem Overview

You are given a 0-indexed array of integers `nums`. You start at index 0. Each element `nums[i]` represents the maximum number of steps you can jump forward. The goal is to find the **minimum number of jumps** required to reach the final index of the array.

The problem guarantees that the last index is always reachable.

**Examples:**

```python
Input: nums = [2,3,1,1,4]
Output: 2
Explanation: The minimum number of jumps is 2.
1. Jump from index 0 to index 1 (1 step).
2. Jump from index 1 to the last index (3 steps).

Input: nums = [2,3,0,1,4]
Output: 2
```

## Key Insights

### Shortest Path & Breadth-First Search (BFS)

The phrase **"minimum number of jumps"** is a classic indicator of a **shortest path problem**. The standard algorithm for finding the shortest path in an unweighted graph (where each "jump" or edge has a cost of 1) is **Breadth-First Search (BFS)**.

A standard BFS uses a queue and explores the "graph" (our array) level by level. In this problem, each "level" corresponds to one jump.

### A Greedy BFS

Instead of using an actual queue data structure (which would take `O(n)` space), we can implement a more efficient **greedy BFS** with constant space. The idea is to think in terms of "horizons" or "reach".

1.  **Jump 0**: You are at index 0.
2.  **Jump 1**: From your starting position, find the *farthest you can possibly reach*. This becomes the boundary for your first jump.
3.  **Jump 2**: From *anywhere* within the boundary of your first jump, find the *new farthest you can possibly reach*. This becomes the boundary for your second jump.

By always being greedy and extending our reach to the absolute maximum, we guarantee that we are covering the distance in the fewest possible leaps.

## Solution Approach

This solution implements the greedy BFS strategy in a single pass. It uses three variables to keep track of the state.

```python
from typing import List

class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = 0
        # The end of the range we can reach with the current number of jumps.
        current_reach = 0
        # The farthest we can possibly reach from any position we've explored.
        farthest_reach = 0
        
        # We iterate up to the second to last element.
        # Once we are at a position that can reach the end, we don't need to jump from it.
        for i in range(len(nums) - 1):
            # Update the farthest possible reach from the current position.
            farthest_reach = max(farthest_reach, i + nums[i])
            
            # If our iterator 'i' has reached the boundary of the current jump's range...
            if i == current_reach:
                # ...it's time to take another jump.
                jumps += 1
                # The new jump's boundary is the farthest reach we just calculated.
                current_reach = farthest_reach
                
        return jumps
```

**Strategy:**

1.  **Initialize**: `jumps` starts at 0. `current_reach` and `farthest_reach` also start at 0.
2.  **Iterate**: Loop through the array. The index `i` represents our current position.
3.  **Update `farthest_reach`**: At each position `i`, calculate the potential reach (`i + nums[i]`) and update `farthest_reach` if it's a new maximum.
4.  **Take a Jump**: When our position `i` reaches the boundary of our `current_reach`, it means we cannot go any further without taking another jump. At this point, we increment `jumps` and set our new `current_reach` to the `farthest_reach` we found while exploring the previous "level".

## Detailed Code Analysis

### Variable Initialization

```python
jumps = 0
current_reach = 0
farthest_reach = 0
```

  - `jumps`: The final answer we will return.
  - `current_reach`: The boundary for the current "level" of the BFS. All indices up to this point are reachable with the current `jumps` count.
  - `farthest_reach`: A forward-looking variable that tracks the best possible next boundary.

### The Loop

```python
for i in range(len(nums) - 1):
```

  - We only need to loop up to `len(nums) - 1` because the goal is to *reach* the last index. We don't need to consider jumping *from* the last index.

### The Greedy Choice

```python
farthest_reach = max(farthest_reach, i + nums[i])
```

  - This is the greedy part. As we scan through the indices reachable by our current jump, we constantly update our knowledge of the absolute farthest we can get in the *next* jump.

### The Level Change (Taking a Jump)

```python
if i == current_reach:
    jumps += 1
    current_reach = farthest_reach
```

  - This is the core of the BFS simulation. When `i` equals `current_reach`, it signifies that we have explored all the positions possible with the current number of jumps. We are forced to "expend" a jump to continue.
  - We increment `jumps` and update our `current_reach` to the new `farthest_reach` we've been calculating.

## Step-by-Step Execution Trace

### Example: `nums = [2, 3, 1, 1, 4]`

| `i` | `farthest_reach` (after update) | `i == current_reach`? | Action on True | `jumps` | `current_reach` |
| :-- | :--- | :--- | :--- | :--- | :--- |
| **Start** | 0 | - | - | 0 | 0 |
| **0** | `max(0, 0+2) = 2` | `0==0` -\> **True** | `jumps++`, `current_reach=2` | **1** | **2** |
| **1** | `max(2, 1+3) = 4` | `1==2` -\> False | - | 1 | 2 |
| **2** | `max(4, 2+1) = 4` | `2==2` -\> **True** | `jumps++`, `current_reach=4` | **2** | **4** |
| **3** | `max(4, 3+1) = 4` | `3==4` -\> False | - | 2 | 4 |

  - The loop ends after `i=3`. The function returns the final `jumps` count, which is **2**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in `nums`. We iterate through the list exactly once.

### Space Complexity: O(1)

  - We only use a few variables to store our state. The space required is constant.

## Key Learning Points

  - Recognizing "minimum steps/jumps" problems as a sign to use a Breadth-First Search (BFS) approach.
  - This specific greedy algorithm is a clever, space-efficient way to implement a BFS on an array.
  - The pattern of using `current_reach` and `farthest_reach` is very useful for solving other jump-related array problems.

## Common Pitfalls Avoided

  - Using a slower `O(n^2)` dynamic programming or brute-force solution.
  - Overcomplicating the logic by trying to decide the "best" specific jump from each position, rather than just finding the farthest possible reach from a given range.