# 56\. Merge Intervals - Solution Explanation

## Problem Overview

You are given a collection of intervals, where each interval is represented as a pair of integers `[start, end]`. The task is to merge all **overlapping** intervals and return a new list of non-overlapping intervals that cover all the original intervals.

**Overlap Definition:**
Two intervals `[start1, end1]` and `[start2, end2]` are considered overlapping if they touch or intersect. For example, `[1,3]` and `[2,6]` overlap. `[1,4]` and `[4,5]` are also considered overlapping.

**Examples:**

```python
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, they are merged into [1,6].

Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: The intervals touch at 4, so they are merged.
```

## Key Insights

### The Power of Sorting

The main challenge is that the input intervals can be in any order, making it difficult to know which ones to compare. The most crucial insight is that if we **sort the intervals based on their start times**, the problem becomes dramatically simpler.

Once sorted, we can just iterate through the list in a single pass. Any interval that can be merged with the current one will always appear right after it in the sorted list.

### Greedy Merging

With a sorted list of intervals, we can use a **greedy** approach.

1.  We start with the first interval and add it to our result list.
2.  Then, we look at the next interval and compare it to the *last* interval we added to our result.
3.  If they overlap, we merge them by updating the end time of the last interval in our result.
4.  If they don't overlap, the new interval is the start of a new, non-overlapping block, so we just add it to our result list.

We repeat this process until we've gone through all the intervals.

## Solution Approach

This solution first sorts the intervals by their start time. Then, it iterates through the sorted list, building a new list of merged intervals.

```python
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Handle the edge case of an empty list.
        if not intervals:
            return []
        
        # Step 1: Sort the intervals based on their start time.
        intervals.sort(key=lambda x: x[0])
        
        # Step 2: Initialize the 'merged' list with the first interval.
        merged = [intervals[0]]
        
        # Step 3: Iterate through the rest of the intervals.
        for current_interval in intervals[1:]:
            # Get the last interval that was added to our result.
            last_merged_interval = merged[-1]
            
            # Step 4: Check for overlap and merge if necessary.
            if current_interval[0] <= last_merged_interval[1]:
                # There is an overlap, so merge.
                last_merged_interval[1] = max(last_merged_interval[1], current_interval[1])
            else:
                # No overlap, so add the current interval as a new one.
                merged.append(current_interval)
                
        return merged
```

## Deep Dive: Lambda Functions

You asked for more detail on `lambda`. It's a powerful feature for creating small, one-time-use functions.

  * **What is a Lambda Function?**
    A `lambda` function is a small, **anonymous** (unnamed) function. You define it on the fly, right where you need it, without using the standard `def` keyword.

  * **Syntax**: `lambda arguments: expression`

      - `lambda`: The keyword that declares an anonymous function.
      - `arguments`: The input(s) to the function (e.g., `x`).
      - `expression`: A single expression that is evaluated and returned.

  * **How it's Used Here (`key=lambda x: x[0]`)**:

      - The `.sort()` method can take a `key` argument, which specifies *how* to sort the items. This `key` must be a function.
      - Our list `intervals` contains other lists, like `[1, 3]` and `[2, 6]`. We want to sort based on the first number (`1`, `2`, etc.).
      - `lambda x: x[0]` is a short function that says: "Given an input `x` (which will be one of our intervals like `[1, 3]`), return the element at index `0` of that input (`x[0]`)."
      - So, `intervals.sort(key=lambda x: x[0])` tells Python to sort the list of intervals by comparing their first elements.

## Detailed Code Analysis

### Step 1: Sorting

```python
intervals.sort(key=lambda x: x[0])
```

  - This is the most important step. We sort the list of lists in-place.
  - The `key=lambda x: x[0]` tells the sort function to look only at the first element (`start_time`) of each interval when comparing them.

### Step 2: Initialization

```python
merged = [intervals[0]]
```

  - We create our `merged` result list. Instead of starting empty, we prime it with the very first interval from our now-sorted list. This gives us a `last_merged_interval` to compare against when our loop starts.

### Step 3: The Loop

```python
for current_interval in intervals[1:]:
```

  - We loop through the `intervals`, but we can skip the first one (`intervals[0]`) because we've already added it to `merged`. `intervals[1:]` is a slice that contains all elements from the second one to the end.

### Step 4: The Overlap Logic

```python
last_merged_interval = merged[-1]
if current_interval[0] <= last_merged_interval[1]:
    # ... merge ...
else:
    # ... append new ...
```

  - `last_merged_interval = merged[-1]`: In each iteration, we get a reference to the last interval in our `merged` list.
  - **`if current_interval[0] <= last_merged_interval[1]:`**: This is the core overlap check. It asks, "Does the current interval start before or at the same time the last merged interval ends?" If yes, they overlap.
  - **The Merge**: `last_merged_interval[1] = max(last_merged_interval[1], current_interval[1])`. If there is an overlap, we don't need to change the start time. We only need to update the end time of our `last_merged_interval` to be the "farthest" end time between the two overlapping intervals.
  - **No Overlap**: `else: merged.append(current_interval)`. If they don't overlap, the `current_interval` starts a new, separate block. We simply append it to our `merged` list, and it will become the `last_merged_interval` for the next iteration.

## Step-by-Step Execution Trace

Let's trace the algorithm with `intervals = [[1,3],[8,10],[2,6],[15,18]]` with extreme detail.

1.  **Initial `intervals`**: `[[1,3], [8,10], [2,6], [15,18]]`
2.  **After Sorting**: `intervals` becomes `[[1,3], [2,6], [8,10], [15,18]]`
3.  **Initialization**: `merged` is initialized with the first interval: `[[1,3]]`.
4.  **The Loop Starts**: `for` loop will process `[2,6]`, `[8,10]`, and `[15,18]`.

| `current_interval` | `last_merged_interval` (`merged[-1]`) | Overlap Check (`current[0] <= last[1]`) | Action | `merged` state |
| :--- | :--- | :--- | :--- | :--- |
| **`[2,6]`** | `[1,3]` | `2 <= 3` -\> **True** | Merge: `last[1] = max(3, 6) = 6` | `[[1,6]]` |
| **`[8,10]`**| `[1,6]` | `8 <= 6` -\> **False**| No Overlap: `merged.append([8,10])` | `[[1,6], [8,10]]`|
| **`[15,18]`**| `[8,10]`| `15 <= 10` -\> **False**| No Overlap: `merged.append([15,18])`| `[[1,6], [8,10], [15,18]]` |

5.  **End of Loop**: The loop finishes.
6.  **Return**: The function returns the final `merged` list: `[[1,6], [8,10], [15,18]]`.

## Performance Analysis

### Time Complexity: O(n log n)

  - The time complexity is dominated by the initial sorting step, which takes `O(n log n)` time, where `n` is the number of intervals.
  - The subsequent loop to merge the intervals is a single pass, which takes `O(n)` time.
  - The total is `O(n log n) + O(n)`, which simplifies to `O(n log n)`.

### Space Complexity: O(n)

  - The space required for the `merged` output list can be up to `O(n)` in the worst case (if no intervals are merged).
  - Additionally, the sorting algorithm used in Python (Timsort) can require `O(n)` space in some cases.