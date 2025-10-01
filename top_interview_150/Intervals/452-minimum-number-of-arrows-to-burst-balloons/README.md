# 452\. Minimum Number of Arrows to Burst Balloons - Solution Explanation

## Problem Overview

You are given a list of `points`, where each `point` `[xstart, xend]` represents the horizontal diameter of a balloon. The goal is to find the **minimum number of arrows** you need to shoot vertically to burst all the balloons.

**The Rule:**
An arrow shot at a position `x` on the x-axis will burst any balloon whose `xstart` and `xend` range includes `x` (i.e., `xstart <= x <= xend`).

**Example:**

```python
Input: points = [[10,16],[2,8],[1,6],[7,12]]
Output: 2
Explanation:
- An arrow at x=6 can burst balloons [1,6] and [2,8].
- A second arrow at x=11 (or 12) can burst balloons [7,12] and [10,16].
We only need 2 arrows.
```

## Key Insights

### An Interval Problem with a Greedy Solution

This is a classic interval problem. We want to find the minimum number of points that "hit" or "cover" all the given intervals. A brute-force check would be too complicated.

The key insight is to use a **greedy approach**. To make each arrow as effective as possible, we want it to pop the current balloon and have the best chance of popping future balloons.

### The Power of Sorting by End Points

The most crucial step is to **sort the balloons by their end points (`xend`)**.

  - Why? By sorting this way, we always deal with the balloon that "finishes" the earliest.
  - Let's consider the first balloon in this sorted list. We know we *must* shoot an arrow to burst it. Where is the best place to shoot this arrow?
  - The optimal position is at the **very end** of this balloon's range (`xend`). By shooting the arrow as far to the right as possible while still bursting this balloon, we maximize the chance that this same arrow can also burst other balloons that start later but still overlap with this position.

This greedy choice—sort by end point, and place an arrow at that end point—is the foundation of the efficient solution.

## Solution Approach

This solution implements the greedy strategy. It first sorts the balloons by their end coordinates. Then, it iterates through the sorted list, only firing a new arrow when it encounters a balloon that the previous arrow could not have burst.

```python
from typing import List

class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        # Handle the edge case of no balloons.
        if not points:
            return 0
            
        # Step 1: Sort the balloons based on their end points (p[1]).
        points.sort(key=lambda p: p[1])
        
        # Step 2: Initialize for the first arrow.
        # We must shoot at least one arrow to burst the first balloon.
        arrow_count = 1
        # We greedily place this first arrow at the end of the first balloon.
        arrow_pos = points[0][1]
        
        # Step 3: Iterate through all balloons to see if they need a new arrow.
        for start, end in points:
            # If the start of the current balloon is after the last arrow's position...
            if start > arrow_pos:
                # ...then the last arrow cannot burst it. We need a new arrow.
                arrow_count += 1
                # Place this new arrow at the end of the current balloon.
                arrow_pos = end
                
        return arrow_count
```

## Detailed Code Analysis

### Step 1: Sorting

```python
points.sort(key=lambda p: p[1])
```

  - This is the most important part of the algorithm. It sorts the list of balloons in-place.
  - The `key=lambda p: p[1]` tells the sort function to order the balloons based on their second element, which is the `xend` coordinate.

### Step 2: Initialization

```python
arrow_count = 1
arrow_pos = points[0][1]
```

  - After sorting, we know we need at least one arrow. We initialize `arrow_count` to `1`.
  - We make our first greedy choice: we shoot this first arrow at `points[0][1]`, the end point of the balloon that finishes earliest. This `arrow_pos` is the position of our most recently fired arrow.

### Step 3: The Main Loop and Greedy Check

```python
for start, end in points:
    if start > arrow_pos:
        arrow_count += 1
        arrow_pos = end
```

  - We iterate through all the balloons (including the first one again, which is harmless).
  - **`if start > arrow_pos:`**: This is the core greedy check. It asks, "Does the current balloon start to the right of where my last arrow landed?"
      - If **True**: The last arrow cannot possibly burst this balloon. We must fire a new one. We increment `arrow_count` and update `arrow_pos` to the end of this *new* balloon, as this is our new greedy position.
      - If **False**: The `start` of the balloon is at or before `arrow_pos`. Since the list is sorted by `end` points, we also know its `end` must be at or after the previous balloon's end (where `arrow_pos` is). This means the current balloon is definitely burst by our last arrow, so we do nothing and let the loop continue.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `points = [[10,16],[2,8],[1,6],[7,12]]` with extreme detail.

1.  **Initial `points`**: `[[10,16], [2,8], [1,6], [7,12]]`

2.  **After Sorting by `xend`**: `points` becomes `[[1,6], [2,8], [7,12], [10,16]]`

3.  **Initialization**:

      * `arrow_count` = **1**
      * `arrow_pos` = `points[0][1]` = **6**

4.  **The Loop**:

| `balloon` (`[start, end]`) | `arrow_pos` | `start > arrow_pos`? | Action | `arrow_count` (new) | `arrow_pos` (new)|
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[1,6]`** | 6 | `1 > 6` -\> False | Do nothing. | 1 | 6 |
| **`[2,8]`** | 6 | `2 > 6` -\> False | Do nothing. | 1 | 6 |
| **`[7,12]`**| 6 | `7 > 6` -\> **True** | Need a new arrow. | `1 + 1 = 2` | `12` |
| **`[10,16]`**| 12 | `10 > 12`-\> False | Do nothing. | 2 | 12 |

5.  **Final Step**: The loop finishes. The function returns the final `arrow_count`, which is **2**.

## Performance Analysis

### Time Complexity: O(n log n)

  - The time complexity is dominated by the initial sorting step, which takes `O(n log n)` time, where `n` is the number of balloons.
  - The subsequent `for` loop is a single pass over the array, which takes `O(n)` time.
  - The total is `O(n log n) + O(n)`, which simplifies to `O(n log n)`.

### Space Complexity: O(1) or O(n)

  - This depends on the space complexity of the sorting algorithm used by the programming language.
  - If the sort is done in-place, the extra space is `O(1)`. Python's Timsort can use up to `O(n)` space in some cases.

## Key Learning Points

  - **Greedy Algorithms**: This problem is a prime example of a greedy algorithm where making the locally optimal choice (shooting an arrow at the earliest possible end point) leads to the globally optimal solution.
  - **Interval Problems**: Sorting is often the most critical first step in solving interval-based problems. The choice of sorting by *start* or *end* points is a key strategic decision.
  - **The "Earliest Finish Time" Strategy**: The approach of sorting by end times and processing items in that order is a powerful greedy pattern that applies to many other problems, like the "Activity Selection Problem."