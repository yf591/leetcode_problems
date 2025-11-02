# 435\. Non-overlapping Intervals - Solution Explanation

## Problem Overview

You are given an array of intervals, where each interval `[start, end]` represents a span on the number line. The task is to find the **minimum number of intervals** you need to **remove** so that all the remaining intervals are non-overlapping.

**Key Definitions:**

  - **Overlapping**: Two intervals `[a, b]` and `[c, d]` overlap if `c < b`.
  - **Non-overlapping**: `[1, 2]` and `[2, 3]` are considered non-overlapping (they only "touch" at the boundary).

**Examples:**

```python
Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: [1,3] overlaps with [1,2] and [2,3]. If we remove it, the rest are non-overlapping.

Input: intervals = [[1,2],[1,2],[1,2]]
Output: 2
Explanation: We must remove two of the [1,2] intervals to have a non-overlapping set.
```

## Key Insights

### 1\. Inverting the Problem: The "Aha\!" Moment

The problem asks for the *minimum number of intervals to remove*. This is a tricky way of phrasing a simpler, equivalent problem:

**Find the *maximum number of intervals we can keep* that are non-overlapping.**

If we have 4 total intervals and we find that the maximum number we can keep is 3, then the minimum number we must remove is `4 - 3 = 1`. This "inverted goal" is much easier to solve.

### 2\. The Greedy Strategy: Why Sort by End Time?

To find the maximum number of intervals we can keep, we need a **greedy strategy**. This means making the best *local* choice at each step, hoping it leads to the best *global* solution.

We must sort the intervals first to process them in a logical order. But what's the best way to sort?

  - **Bad Strategy: Sort by Start Time.**

      - Consider `[[1, 100], [2, 5], [6, 10]]`.
      - If we sort by start time, we get `[[1, 100], [2, 5], [6, 10]]`.
      - Our greedy choice would be to keep `[1, 100]` first. But this choice *prevents* us from keeping `[2, 5]` and `[6, 10]`.
      - Final kept count: 1. This is wrong. The best answer is to keep `[2, 5]` and `[6, 10]`, for a count of 2.

  - **Good Strategy: Sort by End Time.**

      - This is the key insight. By always choosing the interval that **finishes earliest**, we free up the timeline as quickly as possible. This maximizes the opportunity for more intervals to be scheduled afterward.
      - Let's use the same example: `[[1, 100], [2, 5], [6, 10]]`.
      - Sorted by end time, we get `[[2, 5], [6, 10], [1, 100]]`.
      - Now, we iterate:
        1.  **Keep `[2, 5]`**. Our last finished time is `5`.
        2.  Check `[6, 10]`. Does it start after `5`? Yes (`6 >= 5`). It doesn't overlap. **Keep `[6, 10]`**. Our last finished time is now `10`.
        3.  Check `[1, 100]`. Does it start after `10`? No (`1 < 10`). It overlaps. **Remove `[1, 100]`**.
      - Final kept count: 2. This is the optimal solution.

## Solution Approach

This solution implements the "Sort by End Time" greedy strategy.

1.  **Sort** the `intervals` list based on each interval's **end time**.
2.  **Initialize** a `intervals_kept` counter to 1 and a `last_end_time` variable to the end time of the *first* interval (which we keep by default).
3.  **Iterate** through the rest of the sorted intervals.
4.  For each interval, check if its `start_time` is greater than or equal to the `last_end_time`.
5.  If it is, it means this interval doesn't overlap with the last one we kept. We "keep" it by incrementing `intervals_kept` and updating `last_end_time` to this interval's end.
6.  If it's not (it overlaps), we "remove" it by simply doing nothing.
7.  Finally, return `total_intervals - intervals_kept`.

<!-- end list -->

```python
from typing import List

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        
        if not intervals:
            return 0

        # Step 1: Sort the intervals by their end time (the 2nd element).
        intervals.sort(key=lambda x: x[1])
        
        # Step 2: Initialize variables.
        # We "keep" the first interval in the sorted list by default.
        intervals_kept = 1
        last_end_time = intervals[0][1]
        
        # Step 3: Iterate from the *second* interval onwards.
        for i in range(1, len(intervals)):
            current_start = intervals[i][0]
            
            # Step 4: Check for non-overlap.
            # If the current interval starts after or at the same time
            # the last kept interval ended, they don't overlap.
            if current_start >= last_end_time:
                # We can keep this interval.
                intervals_kept += 1
                # Update the "last end time" to this interval's end.
                last_end_time = intervals[i][1]
            
            # else: (current_start < last_end_time)
            # This interval overlaps with the 'last_end_time' one.
            # We "remove" it by simply ignoring it and not updating our counters.
            
        # Step 5: The result is the total intervals minus the ones we kept.
        return len(intervals) - intervals_kept
```

## Deep Dive: `lambda` Functions

You asked for a detailed explanation of the `lambda` function.
`lambda x: x[1]`

  * **What is it?**
    A `lambda` function is a small, **anonymous** (unnamed) function. It's a convenience for when you need a simple, one-line function and don't want to define it formally using the `def` keyword.

  * **Syntax Breakdown:**
    `lambda arguments : expression`

      - `lambda`: The keyword that tells Python you are creating an anonymous function.
      - `arguments`: The input parameter(s) for the function. In our case, `x`.
      - `:`: The separator.
      - `expression`: The single expression that is evaluated and returned. In our case, `x[1]`.

  * **How it's Used in `sort()`:**
    The `sort()` method can accept a `key` argument. This `key` is a function that `sort()` will call on *every item* in the list before it makes comparisons. The `sort()` method then uses the *returned value* of this function to perform the sort.

    Let's trace: `intervals.sort(key=lambda x: x[1])`

    1.  `sort()` picks an interval, e.g., `[1, 3]`. It passes this as the argument `x` to the lambda function.
    2.  `lambda [1, 3]: [1, 3][1]` runs. It returns the element at index 1, which is `3`.
    3.  `sort()` picks another interval, e.g., `[2, 6]`. It calls `lambda [2, 6]: [2, 6][1]`. It returns `6`.
    4.  `sort()` now compares the returned values `3` and `6`. Since `3 < 6`, it knows that `[1, 3]` should come before `[2, 6]` in the sorted list.

In short: `key=lambda x: x[1]` is a short and elegant way of saying, "Sort this list of lists based on the value of the **second element** of each inner list."

## Step-by-Step Execution Trace

Let's trace the algorithm with `intervals = [[1,2],[2,3],[3,4],[1,3]]` with extreme detail.

### **Initial State:**

  - `intervals` = `[[1,2], [2,3], [3,4], [1,3]]`

### **Step 1: Sort by End Time**

  - Sorting `[[1,2], [2,3], [3,4], [1,3]]` by their second element (`[2, 3, 4, 3]`).
  - `intervals` becomes `[[1,2], [2,3], [1,3], [3,4]]`
    *(Note: `[2,3]` and `[1,3]` both end at 3. Their relative order is not guaranteed by the sort, but it doesn't matter for the algorithm's correctness. Let's assume this order.)*

### **Step 2: Initialization**

  - `intervals_kept = 1` (We are keeping `[1,2]`).
  - `last_end_time = intervals[0][1]` -\> `last_end_time = 2`.

### **Step 3: The Loop**

  - The loop runs from `i = 1` to `3`.

| `i` | `current_interval` | `current_start` | `last_end_time` | `current_start >= last_end_time`? | Action | `intervals_kept` |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `[2,3]` | 2 | 2 | `2 >= 2` -\> **True** | Keep. `last_end_time` becomes 3. | 2 |
| **2** | `[1,3]` | 1 | 3 | `1 >= 3` -\> **False**| Overlaps. "Remove". Do nothing. | 2 |
| **3** | `[3,4]` | 3 | 3 | `3 >= 3` -\> **True** | Keep. `last_end_time` becomes 4. | 3 |

### **Step 4: End of Loop**

  - The `for` loop finishes.
  - `intervals_kept` is **3**.

### **Step 5: Final Calculation**

  - `return len(intervals) - intervals_kept`
  - `return 4 - 3` -\> **1**
  - The function returns `1`, which is the correct answer.

## Performance Analysis

### Time Complexity: O(n log n)

  - The most expensive operation in this algorithm is the **sorting step**, which takes `O(n log n)` time, where `n` is the number of intervals.
  - The subsequent `for` loop is a single pass, which only takes `O(n)` time.
  - The total time complexity is dominated by the sort, so it is `O(n log n)`.

### Space Complexity: O(log n) or O(n)

  - The space complexity depends on the implementation of the sorting algorithm.
  - Python's Timsort (used by `list.sort()`) can require `O(n)` space in the worst case, but it is often `O(log n)` on average for many inputs. We are not creating any new data structures that scale with `n`, aside from what the sort needs.