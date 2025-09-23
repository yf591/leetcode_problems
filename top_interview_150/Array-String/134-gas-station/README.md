# 134\. Gas Station - Solution Explanation

## Problem Overview

You are given a circular route with `n` gas stations. You have two arrays: `gas` and `cost`.

  - `gas[i]` is the amount of fuel you can get at station `i`.
  - `cost[i]` is the amount of fuel it takes to travel from station `i` to station `i+1`.

You start with an empty tank at one of the stations. The goal is to find the starting station's index that allows you to travel around the entire circuit exactly once in a clockwise direction. If a solution exists, it is guaranteed to be unique. If no solution exists, you should return -1.

**Example:**

```python
Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
Output: 3
Explanation: If you start at index 3, you can successfully complete the entire circuit.
- Start at station 3: tank = 4.
- Travel to 4: tank = 4-1+5 = 8.
- Travel to 0: tank = 8-2+1 = 7.
- Travel to 1: tank = 7-3+2 = 6.
- Travel to 2: tank = 6-4+3 = 5.
- Travel back to 3: cost is 5, tank is 5. Possible.
```

## Key Insights

### The `O(n²)` Trap

The most obvious brute-force approach is to try starting at every single station (`i = 0 to n-1`) and, for each start, simulate the entire trip to see if you can make it. This would involve a loop inside another loop, leading to an `O(n²)` time complexity, which is too slow for the given constraints.

### Insight 1: The Global Feasibility Check

Before we even search for a starting point, we can ask a simpler question: "Is a full trip even possible?" A trip is only possible if the total amount of gas available in the entire circuit is at least the total cost of traveling around it.

  - If `sum(gas) < sum(cost)`, it's **impossible** to complete the circuit, no matter where you start. You will always run out of fuel eventually. This gives us a powerful `O(n)` check we can do at the very beginning.

### Insight 2: The Greedy Choice for the Starting Point

If we know a solution is possible (`sum(gas) >= sum(cost)`), how do we find the unique start point in a single pass?

  - Let's try to make the trip starting from index 0 and keep track of our `current_tank`.
  - Suppose we successfully travel from `0` to `i`, but when we try to leave station `i` to go to `i+1`, our `current_tank` goes negative. This means we failed.
  - This failure tells us something crucial:
    1.  Index 0 is not the correct starting point.
    2.  Furthermore, **no station between 0 and `i` can be the starting point either\!** Why? Because if we started at any of those intermediate stations, we would have had even less fuel when we reached station `i`, so we would have failed even earlier.
  - This is the core greedy insight: If a journey starting at `start_index` fails at station `i`, the next possible candidate for a starting station **must be `i + 1`**. We can discard all stations before it.

## Solution Approach

This solution combines these two insights into a single, efficient pass. It first confirms that a solution is possible and then uses a greedy approach to find the unique starting index.

```python
from typing import List

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # Step 1: Check if a solution is possible at all (Insight 1).
        if sum(gas) < sum(cost):
            return -1
        
        # If a solution exists, we can find it in one pass.
        current_tank = 0
        start_index = 0
        
        # Step 2: Iterate through all stations to find the unique start.
        for i in range(len(gas)):
            # Update the tank with the net gain/loss at station i.
            current_tank += gas[i] - cost[i]
            
            # If the tank becomes negative, it means we can't reach this station
            # from our current 'start_index'.
            if current_tank < 0:
                # Based on Insight 2, the new candidate for the start must be
                # the station *after* this failure point.
                start_index = i + 1
                # Reset the tank for this new potential journey segment.
                current_tank = 0
                
        # If the loop completes, and we know a solution exists, 'start_index' must be the answer.
        return start_index
```

## Detailed Code Analysis

### Step 1: The Feasibility Check

```python
if sum(gas) < sum(cost):
    return -1
```

  - This is our first optimization. It calculates the total `gas` and total `cost` in `O(n)` time. If the total cost is more than the total gas, we immediately know the trip is impossible and return `-1`.

### Step 2: Initialization

```python
current_tank = 0
start_index = 0
```

  - `start_index`: This is our candidate for the answer. We optimistically start by assuming we can begin at index `0`.
  - `current_tank`: This tracks the fuel level for the journey *starting from the current `start_index`*.

### Step 3: The Main Loop and Net Calculation

```python
for i in range(len(gas)):
    current_tank += gas[i] - cost[i]
```

  - We iterate through every station `i`.
  - `gas[i] - cost[i]` is the net fuel change at this station. We add this to our `current_tank`.

### Step 4: The Greedy Reset

```python
if current_tank < 0:
    start_index = i + 1
    current_tank = 0
```

  - This is the implementation of our key insight.
  - If `current_tank` goes negative, our journey from the current `start_index` has failed.
  - We know all stations up to and including `i` are invalid starting points, so we set our new candidate `start_index` to `i + 1`.
  - We reset `current_tank` to `0` to begin evaluating the new journey segment starting from this new candidate.

### Step 5: The Final Return

```python
return start_index
```

  - Because we first established that a solution *must exist* (`sum(gas) >= sum(cost)`) and is *unique*, the candidate `start_index` that is left at the end of the single pass is guaranteed to be the correct one.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `gas = [1,2,3,4,5]`, `cost = [3,4,5,1,2]` with extreme detail.

1.  **Feasibility Check**: `sum(gas)` is 15. `sum(cost)` is 15. `15 < 15` is false. A solution exists.
2.  **Initialization**: `current_tank = 0`, `start_index = 0`.
3.  **The Loop**:

| `i` | `gas[i] - cost[i]` | `current_tank` (before `+=`) | `current_tank` (after `+=`) | `current_tank < 0`? | Action on True | `start_index` (at end) |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | `1 - 3 = -2` | 0 | -2 | **True** | `start_index = 1`, `current_tank = 0` | **1** |
| **1** | `2 - 4 = -2` | 0 | -2 | **True** | `start_index = 2`, `current_tank = 0` | **2** |
| **2** | `3 - 5 = -2` | 0 | -2 | **True** | `start_index = 3`, `current_tank = 0` | **3** |
| **3** | `4 - 1 = 3` | 0 | 3 | False | - | 3 |
| **4** | `5 - 2 = 3` | 3 | 6 | False | - | 3 |

4.  **End of Loop**: The `for` loop finishes.
5.  **Return Value**: The function returns the final value of `start_index`, which is **3**.

## Performance Analysis

### Time Complexity: O(n)

  - The algorithm makes a single pass to check the sums (`O(n)`) and another single pass in the main loop (`O(n)`). The total complexity is `O(n) + O(n) = O(n)`.

### Space Complexity: O(1)

  - We only use a few variables (`current_tank`, `start_index`, etc.). The space required is constant and does not grow with the size of the input arrays.